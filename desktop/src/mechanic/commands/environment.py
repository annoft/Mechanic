"""
Environment commands for WoW addon development.
Handles addon creation, junction syncing, and library management.
"""

from afd import CommandResult, success, error
from afd.core.metadata import create_source, create_warning, WarningSeverity
from pathlib import Path
from pydantic import BaseModel, Field
from typing import Any, Dict, List, Optional
import subprocess
import shutil

# Use centralized config
from ..config import get_config, find_addon_path
from ..runtime_installation import (
    MECHANIC_RUNTIME_ADDONS,
    format_runtime_issues,
    inspect_mechanic_runtime,
    mechanic_runtime_is_complete,
)


# ═══════════════════════════════════════════════════════════════════════════════
# COMMAND REGISTRATION
# ═══════════════════════════════════════════════════════════════════════════════


def register_commands(server):
    """Register all environment commands with the AFD server."""

    # ═══════════════════════════════════════════════════════════════════════════
    # addon.create - Create new addon from template
    # ═══════════════════════════════════════════════════════════════════════════

    class AddonCreateInput(BaseModel):
        name: str = Field(..., description="Name for the new addon")
        template: Optional[str] = Field(
            None, description="Template to use (defaults to _TemplateAddon)"
        )
        author: Optional[str] = Field(None, description="Author name for metadata")

    class AddonCreateResult(BaseModel):
        name: str
        path: str
        files_created: int = 0
        next_steps: List[str] = []

    @server.command(
        name="addon.create",
        description="Create a new WoW addon from a template",
        input_schema=AddonCreateInput,
        output_schema=AddonCreateResult,
    )
    async def create_addon(
        input: AddonCreateInput, context: Any = None
    ) -> CommandResult[AddonCreateResult]:
        config = get_config()
        dev_path = config.dev_path

        if not dev_path or not dev_path.exists():
            return error(
                code="DEV_PATH_NOT_FOUND",
                message="Development path not found or not configured",
                suggestion="Set MECHANIC_DEV_PATH environment variable or create ~/.mechanic/config.json",
            )

        # Check if addon already exists
        addon_path = dev_path / input.name
        if addon_path.exists():
            return error(
                code="ADDON_EXISTS",
                message=f"Addon '{input.name}' already exists at {addon_path}",
                suggestion="Choose a different name or delete the existing folder",
            )

        # Find template
        template_path = Path(input.template) if input.template else config.template_path
        if not template_path or not template_path.exists():
            return error(
                code="TEMPLATE_NOT_FOUND",
                message=f"Template not found: {template_path}",
                suggestion="Ensure _TemplateAddon exists in your dev path or specify a valid template path",
            )

        # Copy template
        try:
            shutil.copytree(template_path, addon_path)
        except Exception as e:
            return error(
                code="COPY_FAILED",
                message=f"Failed to copy template: {e}",
                suggestion="Check permissions and disk space",
            )

        # Rename nested folder and files, update content
        files_created = 0
        template_name = "TemplateAddon"  # Hardcoded based on known structure

        # 1. Rename the nested addon folder if it exists
        nested_addon_path = addon_path / template_name
        if nested_addon_path.exists() and nested_addon_path.is_dir():
            new_nested_path = addon_path / input.name
            nested_addon_path.rename(new_nested_path)

        # 2. Process all files
        # We walk top-down so we can rename directories as we go?
        # Actually rglob is fine, but we must be careful about renaming parents while iterating.
        # Safest to do content updates first, then renames.

        all_files = list(addon_path.rglob("*"))

        # Content updates
        for file_path in all_files:
            if file_path.is_file():
                files_created += 1
                if file_path.suffix in [
                    ".lua",
                    ".toc",
                    ".md",
                    ".xml",
                    ".json",
                    ".yaml",
                ]:
                    try:
                        content = file_path.read_text(encoding="utf-8")
                        if template_name in content or "Your Name" in content:
                            content = content.replace(template_name, input.name)
                            if input.author:
                                content = content.replace(
                                    "## Author: Your Name", f"## Author: {input.author}"
                                )
                                content = content.replace("Your Name", input.author)
                            file_path.write_text(content, encoding="utf-8")
                    except Exception:
                        pass

        # Filename/Directory Renames (Deepest first to avoid breaking paths)
        # Re-list to get current paths
        # We need to rename files named "TemplateAddon.*" to "NewName.*"

        for file_path in sorted(
            addon_path.rglob("*"), key=lambda p: len(p.parts), reverse=True
        ):
            if template_name in file_path.name:
                new_name = file_path.name.replace(template_name, input.name)
                new_path = file_path.parent / new_name
                try:
                    file_path.rename(new_path)
                except Exception:
                    pass

        src = create_source(
            type="folder",
            id=f"addon-{input.name}",
            title=input.name,
            location=str(addon_path),
        )

        return success(
            data=AddonCreateResult(
                name=input.name,
                path=str(addon_path),
                files_created=files_created,
                next_steps=[
                    f'Run: mech call addon.sync \'{{"addon": "{input.name}"}}\'',
                    f'Run: mech call addon.validate \'{{"addon": "{input.name}"}}\'',
                    f"Edit {input.name}/Core.lua to add your addon logic",
                ],
            ),
            reasoning=f"Created addon repo '{input.name}' with nested '{input.name}' folder",
            sources=[src],
            confidence=1.0,
        )

    # ═══════════════════════════════════════════════════════════════════════════
    # addon.sync - Create junction links to WoW clients
    # ═══════════════════════════════════════════════════════════════════════════

    class AddonSyncInput(BaseModel):
        addon: str = Field(..., description="Name of the addon to sync")
        flavors: Optional[List[str]] = Field(
            None, description="WoW flavors to sync to (defaults to all)"
        )

    class SyncLink(BaseModel):
        addon: str
        flavor: str
        target: str
        status: str

    class AddonSyncResult(BaseModel):
        addon: str
        addons: List[str] = []
        links: List[SyncLink] = []
        success_count: int = 0
        error_count: int = 0
        diagnostics: List[str] = []
        mechanic_runtime_healthy: Optional[bool] = None

    def _resolve_sync_sources(addons: List[str]) -> tuple[Dict[str, Path], List[str]]:
        sources = {}
        diagnostics = []

        for addon_name in addons:
            source_path = find_addon_path(addon_name)
            if not source_path:
                diagnostics.append(f"{addon_name}: source addon not found")
                continue

            toc_path = source_path / f"{addon_name}.toc"
            if not toc_path.exists():
                diagnostics.append(
                    f"{addon_name}: source exists at {source_path} but {addon_name}.toc is missing"
                )
                continue

            sources[addon_name] = source_path

        return sources, diagnostics

    def _sync_one_addon_to_flavor(
        addon_name: str, source_path: Path, wow_base: Path, flavor: str
    ) -> tuple[SyncLink, bool, Optional[str]]:
        addons_path = wow_base / flavor / "Interface" / "AddOns" / addon_name

        if addons_path.exists():
            toc_path = addons_path / f"{addon_name}.toc"
            if toc_path.exists():
                return (
                    SyncLink(
                        addon=addon_name,
                        flavor=flavor,
                        target=str(addons_path),
                        status="exists",
                    ),
                    True,
                    None,
                )

            diagnostic = (
                f"{flavor}: {addon_name} exists at {addons_path} but "
                f"{addon_name}.toc is missing; existing folder was not replaced"
            )
            return (
                SyncLink(
                    addon=addon_name,
                    flavor=flavor,
                    target=str(addons_path),
                    status="exists_missing_toc",
                ),
                False,
                diagnostic,
            )

        try:
            addons_path.parent.mkdir(parents=True, exist_ok=True)

            if subprocess.sys.platform == "win32":
                result = subprocess.run(
                    [
                        "cmd",
                        "/c",
                        "mklink",
                        "/J",
                        str(addons_path),
                        str(source_path),
                    ],
                    capture_output=True,
                    text=True,
                    timeout=10,
                )
                if result.returncode == 0:
                    return (
                        SyncLink(
                            addon=addon_name,
                            flavor=flavor,
                            target=str(addons_path),
                            status="created",
                        ),
                        True,
                        None,
                    )

                detail = (
                    result.stderr.strip()
                    or result.stdout.strip()
                    or "mklink failed"
                )
                return (
                    SyncLink(
                        addon=addon_name,
                        flavor=flavor,
                        target=str(addons_path),
                        status=f"failed: {detail}",
                    ),
                    False,
                    f"{flavor}: failed to sync {addon_name}: {detail}",
                )

            addons_path.symlink_to(source_path)
            return (
                SyncLink(
                    addon=addon_name,
                    flavor=flavor,
                    target=str(addons_path),
                    status="created",
                ),
                True,
                None,
            )
        except Exception as e:
            return (
                SyncLink(
                    addon=addon_name,
                    flavor=flavor,
                    target=str(addons_path),
                    status=f"error: {e}",
                ),
                False,
                f"{flavor}: failed to sync {addon_name}: {e}",
            )

    @server.command(
        name="addon.sync",
        description="Create junction links from development addon to WoW client folders. For !Mechanic or Mechanic, syncs both runtime addons.",
        input_schema=AddonSyncInput,
        output_schema=AddonSyncResult,
    )
    async def sync_addon(
        input: AddonSyncInput, context: Any = None
    ) -> CommandResult[AddonSyncResult]:
        config = get_config()
        wow_base = config.wow_root

        if not wow_base or not wow_base.exists():
            return error(
                code="WOW_NOT_FOUND",
                message="WoW installation not found",
                suggestion="Set MECHANIC_WOW_ROOT environment variable or create ~/.mechanic/config.json",
            )

        runtime_sync = input.addon in MECHANIC_RUNTIME_ADDONS
        addons_to_sync = (
            list(MECHANIC_RUNTIME_ADDONS) if runtime_sync else [input.addon]
        )

        source_paths, source_diagnostics = _resolve_sync_sources(addons_to_sync)
        if not source_paths:
            return error(
                code="ADDON_NOT_FOUND",
                message=f"Addon '{input.addon}' not found or missing required .toc",
                suggestion="Check the addon name or run this from a Mechanic checkout that contains both !Mechanic and Mechanic.",
                details={"diagnostics": source_diagnostics},
            )

        flavors = input.flavors or config.flavors
        links = []
        success_count = 0
        error_count = len(source_diagnostics)
        diagnostics = list(source_diagnostics)

        for addon_name, source_path in source_paths.items():
            for flavor in flavors:
                flavor_path = wow_base / flavor
                if runtime_sync and not flavor_path.exists():
                    target_path = (
                        flavor_path / "Interface" / "AddOns" / addon_name
                    )
                    links.append(
                        SyncLink(
                            addon=addon_name,
                            flavor=flavor,
                            target=str(target_path),
                            status="client_missing",
                        )
                    )
                    if input.flavors is not None:
                        diagnostics.append(
                            f"{flavor}: WoW client folder missing at {flavor_path}; skipped {addon_name}"
                        )
                        error_count += 1
                    continue

                link, link_ok, diagnostic = _sync_one_addon_to_flavor(
                    addon_name, source_path, wow_base, flavor
                )
                links.append(link)
                if link_ok:
                    success_count += 1
                else:
                    error_count += 1
                    if diagnostic:
                        diagnostics.append(diagnostic)

        mechanic_runtime_healthy = None
        if runtime_sync:
            runtime_status = inspect_mechanic_runtime(wow_base, flavors)
            mechanic_runtime_healthy = mechanic_runtime_is_complete(runtime_status)
            if not mechanic_runtime_healthy:
                for issue in format_runtime_issues(runtime_status):
                    if issue not in diagnostics:
                        diagnostics.append(issue)

        sources = [
            create_source(
                type="junction",
                id=f"sync-{addon_name}",
                title=f"Junction Links for {addon_name}",
                location=str(source_path),
            )
            for addon_name, source_path in source_paths.items()
        ]

        warnings = []
        if diagnostics:
            warnings.append(
                create_warning(
                    "MECHANIC_RUNTIME_INCOMPLETE"
                    if runtime_sync
                    else "ADDON_SYNC_INCOMPLETE",
                    "; ".join(diagnostics[:3]),
                    WarningSeverity.CAUTION,
                    details={"diagnostics": diagnostics},
                )
            )

        if runtime_sync:
            reasoning = (
                f"Synced Mechanic runtime addons {', '.join(addons_to_sync)}: "
                f"{success_count} links healthy/created, {error_count} issues. "
                "After resolving issues, run /reload in-game."
            )
        else:
            reasoning = (
                f"Synced {input.addon} to {success_count} clients "
                f"({error_count} issues)"
            )

        return success(
            data=AddonSyncResult(
                addon=input.addon,
                addons=addons_to_sync,
                links=links,
                success_count=success_count,
                error_count=error_count,
                diagnostics=diagnostics,
                mechanic_runtime_healthy=mechanic_runtime_healthy,
            ),
            reasoning=reasoning,
            sources=sources,
            warnings=warnings or None,
            confidence=1.0,
        )

    # ═══════════════════════════════════════════════════════════════════════════
    # libs.check - Check library sync status
    # ═══════════════════════════════════════════════════════════════════════════

    class LibsCheckInput(BaseModel):
        addon: str = Field(..., description="Name of the addon to check")

    class LibStatus(BaseModel):
        name: str
        configured_version: Optional[str] = None
        installed_version: Optional[str] = None
        status: str = "ok"  # ok, missing, incomplete, extra, outdated
        path: Optional[str] = None

    class LibsCheckResult(BaseModel):
        addon: str
        has_config: bool = False
        config_mode: Optional[str] = None
        libraries: List[LibStatus] = []
        issues: List[str] = []

    def _load_libs_config(libs_path: Path) -> Optional[Dict]:
        """Load libs.json from a Libs folder."""
        import json

        config_file = libs_path / "libs.json"
        if config_file.exists():
            try:
                return json.loads(config_file.read_text(encoding="utf-8"))
            except Exception:
                return None
        return None

    def _extract_lib_version(lib_path: Path) -> Optional[str]:
        """Extract version from library files."""
        import re

        for file in lib_path.glob("*.lua"):
            try:
                content = file.read_text(encoding="utf-8", errors="replace")[:1000]
                # Look for MINOR pattern (common in Ace3/libs)
                match = re.search(r"MINOR\s*=\s*(\d+)", content)
                if match:
                    return f"r{match.group(1)}"
            except Exception:
                pass
        return None

    LOADABLE_LIBRARY_SUFFIXES = (".lua", ".xml", ".toc")

    def _inspect_library_install(
        lib_path: Path, lib_name: str
    ) -> tuple[bool, Optional[str], Optional[str]]:
        """Check whether a library directory has a root-level loadable file."""
        if not lib_path.exists():
            return False, "directory is missing", None
        if not lib_path.is_dir():
            return False, "path is not a directory", None

        try:
            root_entries = list(lib_path.iterdir())
        except OSError as exc:
            return False, f"cannot inspect directory: {exc}", None

        if any(
            entry.is_file() and entry.suffix.lower() in LOADABLE_LIBRARY_SUFFIXES
            for entry in root_entries
        ):
            return True, None, _extract_lib_version(lib_path)

        expected_text = "root-level .lua, .xml, or .toc file"
        if not root_entries:
            return False, f"empty directory; expected {expected_text}", None
        return (
            False,
            f"missing loadable file; expected {expected_text}",
            _extract_lib_version(lib_path),
        )

    @server.command(
        name="libs.check",
        description="Check addon library status against libs.json config",
        input_schema=LibsCheckInput,
        output_schema=LibsCheckResult,
    )
    async def check_libs(
        input: LibsCheckInput, context: Any = None
    ) -> CommandResult[LibsCheckResult]:
        addon_path = find_addon_path(input.addon)
        if not addon_path:
            return error(
                code="ADDON_NOT_FOUND",
                message=f"Addon '{input.addon}' not found",
                suggestion="Check the addon name",
            )

        libs_path = addon_path / "Libs"
        if not libs_path.exists():
            return success(
                data=LibsCheckResult(addon=input.addon, issues=["No Libs folder"]),
                reasoning="No Libs folder found in addon",
                confidence=1.0,
            )

        # Load libs.json config
        libs_config = _load_libs_config(libs_path)
        has_config = libs_config is not None
        config_mode = libs_config.get("mode", "include") if libs_config else None
        configured_libs = libs_config.get("libraries", {}) if libs_config else {}

        # Scan installed libraries
        installed_libs = {}
        for item in libs_path.iterdir():
            if item.is_dir() and item.name != "__pycache__":
                complete, incomplete_reason, installed_version = (
                    _inspect_library_install(item, item.name)
                )
                installed_libs[item.name] = {
                    "complete": complete,
                    "incomplete_reason": incomplete_reason,
                    "installed_version": installed_version,
                }

        libraries = []
        issues = []

        if has_config and config_mode == "include":
            # Check for missing configured libs
            for lib_name, configured_version in configured_libs.items():
                configured_version_label = _get_lib_version_config(configured_version)
                if lib_name in installed_libs:
                    lib_info = installed_libs[lib_name]
                    if lib_info["complete"]:
                        libraries.append(
                            LibStatus(
                                name=lib_name,
                                configured_version=configured_version_label,
                                installed_version=lib_info["installed_version"],
                                status="ok",
                                path=str(libs_path / lib_name),
                            )
                        )
                        continue

                    libraries.append(
                        LibStatus(
                            name=lib_name,
                            configured_version=configured_version_label,
                            installed_version=lib_info["installed_version"],
                            status="incomplete",
                            path=str(libs_path / lib_name),
                        )
                    )
                    issues.append(
                        f"Incomplete: {lib_name} ({lib_info['incomplete_reason']})"
                    )
                else:
                    libraries.append(
                        LibStatus(
                            name=lib_name,
                            configured_version=configured_version_label,
                            status="missing",
                        )
                    )
                    issues.append(f"Missing: {lib_name}")

            # Check for extra libs not in config
            for lib_name, lib_info in installed_libs.items():
                if lib_name not in configured_libs and lib_name != "libs.json":
                    libraries.append(
                        LibStatus(
                            name=lib_name,
                            installed_version=lib_info["installed_version"],
                            status="extra",
                            path=str(libs_path / lib_name),
                        )
                    )
                    issues.append(f"Extra (not in config): {lib_name}")
        else:
            # No config - just report what's installed
            for lib_name, lib_info in installed_libs.items():
                libraries.append(
                    LibStatus(
                        name=lib_name,
                        installed_version=lib_info["installed_version"],
                        status="ok" if lib_info["complete"] else "incomplete",
                        path=str(libs_path / lib_name),
                    )
                )
            if not has_config:
                issues.append("No libs.json - run 'libs.init' to create one")

        src = create_source(
            type="folder",
            id=f"libs-{input.addon}",
            title="Libs",
            location=str(libs_path),
        )

        return success(
            data=LibsCheckResult(
                addon=input.addon,
                has_config=has_config,
                config_mode=config_mode,
                libraries=sorted(libraries, key=lambda x: x.name),
                issues=issues,
            ),
            reasoning=f"Found {len(libraries)} libraries, {len(issues)} issues",
            sources=[src],
            confidence=1.0,
        )

    # ═══════════════════════════════════════════════════════════════════════════
    # libs.init - Initialize libs.json from existing Libs folder
    # ═══════════════════════════════════════════════════════════════════════════

    class LibsInitInput(BaseModel):
        addon: str = Field(..., description="Name of the addon")
        mode: str = Field(
            "include",
            description="Config mode: 'include' (whitelist) or 'exclude' (blocklist)",
        )
        overwrite: bool = Field(False, description="Overwrite existing libs.json")

    class LibsInitResult(BaseModel):
        addon: str
        config_path: str
        libraries_count: int
        libraries: Dict[str, str]

    @server.command(
        name="libs.init",
        description="Creates a libs.json config file from currently installed libraries. ⚠️ Will NOT overwrite existing config unless overwrite=true is set.",
        input_schema=LibsInitInput,
        output_schema=LibsInitResult,
    )
    async def init_libs(
        input: LibsInitInput, context: Any = None
    ) -> CommandResult[LibsInitResult]:
        import json

        addon_path = find_addon_path(input.addon)
        if not addon_path:
            return error(
                code="ADDON_NOT_FOUND",
                message=f"Addon '{input.addon}' not found",
                suggestion="Check the addon name",
            )

        libs_path = addon_path / "Libs"
        if not libs_path.exists():
            return error(
                code="NO_LIBS",
                message=f"No Libs folder found in {input.addon}",
                suggestion="Create a Libs folder first",
            )

        config_file = libs_path / "libs.json"
        if config_file.exists() and not input.overwrite:
            return error(
                code="CONFIG_EXISTS",
                message="libs.json already exists",
                suggestion="Use overwrite=true to replace it",
            )

        # Scan existing libraries
        libraries = {}
        for item in libs_path.iterdir():
            if item.is_dir() and item.name not in ["__pycache__"]:
                # Default to "latest", could be enhanced to detect pinning needs
                libraries[item.name] = "latest"

        # Build config
        config = {
            "$schema": "https://mechanic.dev/schemas/libs.json",
            "description": f"Library configuration for {input.addon}",
            "mode": input.mode,
            "libraries": dict(sorted(libraries.items())),
        }

        # Write config
        config_file.write_text(json.dumps(config, indent=2), encoding="utf-8")

        src = create_source(
            type="file",
            id=f"libs-config-{input.addon}",
            title="libs.json",
            location=str(config_file),
        )

        return success(
            data=LibsInitResult(
                addon=input.addon,
                config_path=str(config_file),
                libraries_count=len(libraries),
                libraries=libraries,
            ),
            reasoning=f"Generated libs.json with {len(libraries)} libraries",
            sources=[src],
            confidence=1.0,
        )

    # ═══════════════════════════════════════════════════════════════════════════
    # libs.sync - Sync libraries based on libs.json config
    # ═══════════════════════════════════════════════════════════════════════════

    class LibsSyncInput(BaseModel):
        addon: str = Field(..., description="Name of the addon to sync")
        source: Optional[str] = Field(
            None, description="Source library path (defaults to ADDON_DEV Libs)"
        )
        dry_run: bool = Field(False, description="Preview changes without applying")
        force: bool = Field(
            False, description="Force update existing libraries (replaces them)"
        )
        remove_extra: bool = Field(False, description="Remove libraries not in config")

    class SyncAction(BaseModel):
        library: str
        action: str  # copy, update, skip, remove, error
        source: Optional[str] = None
        target: Optional[str] = None
        reason: str

    class LibsSyncResult(BaseModel):
        addon: str
        dry_run: bool
        actions: List[SyncAction] = []
        copied: int = 0
        updated: int = 0
        skipped: int = 0
        removed: int = 0
        errors: int = 0

    def _find_library_source(
        lib_name: str,
        lib_config,
        default_source: Optional[Path],
        dev_path: Optional[Path],
        exclude_path: Optional[Path] = None,
    ) -> Optional[Path]:
        """Find the source path for a library.

        Checks in order:
        1. Per-library 'source' in libs.json config
        2. Default source path (from command input or auto-detected)
        3. Standalone repo in dev_path (e.g., _dev_/FenUI)
        """
        excluded = exclude_path.resolve() if exclude_path else None

        def is_usable_source(path: Path) -> bool:
            if excluded and path.resolve() == excluded:
                return False
            return _inspect_library_install(path, lib_name)[0]

        # 1. Check per-library source config
        if isinstance(lib_config, dict) and lib_config.get("source"):
            custom_source = Path(lib_config["source"])
            # Handle relative paths (relative to dev_path)
            if not custom_source.is_absolute() and dev_path:
                custom_source = dev_path / custom_source
            if is_usable_source(custom_source):
                return custom_source
            return None

        # 2. Check default source path
        if default_source:
            source_path = default_source / lib_name
            if is_usable_source(source_path):
                return source_path

        # 3. Check for standalone repo in dev_path (e.g., FenUI as its own folder)
        if dev_path and (dev_path / lib_name).exists():
            standalone = dev_path / lib_name
            if is_usable_source(standalone):
                return standalone

        return None

    def _get_lib_version_config(lib_config) -> str:
        """Extract version from library config (handles both string and dict formats)."""
        if isinstance(lib_config, dict):
            return lib_config.get("version", "latest")
        return lib_config  # Simple string format

    # Folders to exclude when copying libraries
    IGNORE_PATTERNS = {
        ".git",
        ".coverage",
        "__pycache__",
        ".github",
        "Tests",
        ".deprecation-report.md",
        "PLANS",
    }

    def _copy_library(src: Path, dst: Path) -> None:
        """Copy a library, excluding development-only folders."""

        def ignore_patterns(directory, files):
            return [f for f in files if f in IGNORE_PATTERNS]

        shutil.copytree(src, dst, ignore=ignore_patterns)

    def _remove_tree_robust(path: Path) -> None:
        """Remove a directory tree, handling .git permission issues on Windows."""
        import stat

        def on_rm_error(func, path, exc_info):
            # Handle read-only files (common in .git)
            os.chmod(path, stat.S_IWRITE)
            func(path)

        import os

        shutil.rmtree(path, onerror=on_rm_error)

    @server.command(
        name="libs.sync",
        description="Sync addon libraries based on libs.json config",
        input_schema=LibsSyncInput,
        output_schema=LibsSyncResult,
    )
    async def sync_libs(
        input: LibsSyncInput, context: Any = None
    ) -> CommandResult[LibsSyncResult]:
        config = get_config()

        addon_path = find_addon_path(input.addon)
        if not addon_path:
            return error(
                code="ADDON_NOT_FOUND",
                message=f"Addon '{input.addon}' not found",
                suggestion="Check the addon name",
            )

        libs_path = addon_path / "Libs"
        if not libs_path.exists():
            return error(
                code="NO_LIBS",
                message=f"No Libs folder in {input.addon}",
                suggestion="Create Libs folder and libs.json first",
            )

        # Load libs.json
        libs_config = _load_libs_config(libs_path)
        if not libs_config:
            return error(
                code="NO_CONFIG",
                message="No libs.json found",
                suggestion="Run 'libs.init' to create one",
            )

        mode = libs_config.get("mode", "include")
        configured_libs = libs_config.get("libraries", {})
        notes = libs_config.get("notes", {})

        # Find default source library path
        default_source = Path(input.source) if input.source else None
        if not default_source:
            # Try common locations (Libs is the canonical location)
            if config.dev_path:
                possible_sources = [
                    config.dev_path / "Libs",  # Canonical location
                    config.dev_path / "MechanicLocal" / "Libs",  # Legacy
                    config.dev_path / "_SharedLibs",  # Alternative
                ]
                for p in possible_sources:
                    if p.exists():
                        default_source = p
                        break

        actions = []
        copied = updated = skipped = removed = errors = 0

        # Get currently installed
        installed = {item.name for item in libs_path.iterdir() if item.is_dir()}

        if mode == "include":
            # Process configured libraries
            for lib_name, lib_config in configured_libs.items():
                target_path = libs_path / lib_name
                version = _get_lib_version_config(lib_config)

                # Find source for this library
                src_lib = _find_library_source(
                    lib_name,
                    lib_config,
                    default_source,
                    config.dev_path,
                    exclude_path=target_path,
                )

                # Handle "local" libs - sync from shared Libs folder
                if version == "local":
                    if not src_lib:
                        actions.append(
                            SyncAction(
                                library=lib_name,
                                action="skip",
                                reason=notes.get(
                                    lib_name, "Local library not found in shared Libs"
                                ),
                            )
                        )
                        skipped += 1
                        continue
                    # Continue with normal sync logic below (src_lib is set)

                # Check if already installed
                if target_path.exists():
                    target_complete, incomplete_reason, _installed_version = (
                        _inspect_library_install(target_path, lib_name)
                    )
                    should_update = input.force or not target_complete

                    if should_update and src_lib:
                        reason_prefix = (
                            "Force updated"
                            if input.force and target_complete
                            else "Repaired incomplete install"
                        )
                        dry_run_prefix = (
                            "Would force update"
                            if input.force and target_complete
                            else "Would repair incomplete install"
                        )
                        if not input.dry_run:
                            try:
                                _remove_tree_robust(target_path)
                                _copy_library(src_lib, target_path)
                                actions.append(
                                    SyncAction(
                                        library=lib_name,
                                        action="update",
                                        source=str(src_lib),
                                        target=str(target_path),
                                        reason=f"{reason_prefix} from {src_lib.name}",
                                    )
                                )
                                updated += 1
                            except Exception as e:
                                actions.append(
                                    SyncAction(
                                        library=lib_name, action="error", reason=str(e)
                                    )
                                )
                                errors += 1
                        else:
                            actions.append(
                                SyncAction(
                                    library=lib_name,
                                    action="update",
                                    source=str(src_lib),
                                    target=str(target_path),
                                    reason=f"{dry_run_prefix} from {src_lib.name}",
                                )
                            )
                            updated += 1
                    elif should_update:
                        if input.force and target_complete:
                            reason = "force=true requested but source not found"
                        else:
                            reason = (
                                "Existing library is incomplete "
                                f"({incomplete_reason}); source not found"
                            )
                        actions.append(
                            SyncAction(
                                library=lib_name,
                                action="error",
                                target=str(target_path),
                                reason=reason,
                            )
                        )
                        errors += 1
                    else:
                        actions.append(
                            SyncAction(
                                library=lib_name,
                                action="skip",
                                target=str(target_path),
                                reason="Already installed (use force=true to update)",
                            )
                        )
                        skipped += 1
                    continue

                # Copy new library
                if src_lib:
                    if not input.dry_run:
                        try:
                            _copy_library(src_lib, target_path)
                            actions.append(
                                SyncAction(
                                    library=lib_name,
                                    action="copy",
                                    source=str(src_lib),
                                    target=str(target_path),
                                    reason=f"Copied from {src_lib.name}",
                                )
                            )
                            copied += 1
                        except Exception as e:
                            actions.append(
                                SyncAction(
                                    library=lib_name, action="error", reason=str(e)
                                )
                            )
                            errors += 1
                    else:
                        actions.append(
                            SyncAction(
                                library=lib_name,
                                action="copy",
                                source=str(src_lib),
                                target=str(target_path),
                                reason=f"Would copy from {src_lib.name}",
                            )
                        )
                        copied += 1
                else:
                    actions.append(
                        SyncAction(
                            library=lib_name, action="error", reason="Source not found"
                        )
                    )
                    errors += 1

            # Handle extra libraries (not in config)
            if input.remove_extra:
                for lib_name in installed:
                    if lib_name not in configured_libs and lib_name != "libs.json":
                        target_path = libs_path / lib_name
                        if not input.dry_run:
                            try:
                                shutil.rmtree(target_path)
                                actions.append(
                                    SyncAction(
                                        library=lib_name,
                                        action="remove",
                                        target=str(target_path),
                                        reason="Not in libs.json config",
                                    )
                                )
                                removed += 1
                            except Exception as e:
                                actions.append(
                                    SyncAction(
                                        library=lib_name, action="error", reason=str(e)
                                    )
                                )
                                errors += 1
                        else:
                            actions.append(
                                SyncAction(
                                    library=lib_name,
                                    action="remove",
                                    target=str(target_path),
                                    reason="Would remove (not in config)",
                                )
                            )
                            removed += 1

        src = create_source(
            type="folder",
            id=f"libs-sync-{input.addon}",
            title="Library Sync",
            location=str(libs_path),
        )

        return success(
            data=LibsSyncResult(
                addon=input.addon,
                dry_run=input.dry_run,
                actions=actions,
                copied=copied,
                updated=updated,
                skipped=skipped,
                removed=removed,
                errors=errors,
            ),
            reasoning=f"{'Preview: ' if input.dry_run else ''}{copied} copied, {updated} updated, {skipped} skipped, {removed} removed, {errors} errors",
            sources=[src],
            confidence=1.0,
        )

    # ═══════════════════════════════════════════════════════════════════════════
    # env.status - Environment status for dashboard
    # ═══════════════════════════════════════════════════════════════════════════

    class FlavorInfo(BaseModel):
        name: str
        path: str
        exists: bool

    class RuntimeAddonInfo(BaseModel):
        addon: str
        path: str
        present: bool
        toc_path: str
        toc_present: bool
        healthy: bool
        status: str

    class RuntimeFlavorInfo(BaseModel):
        flavor: str
        path: str
        exists: bool
        addons_path: str
        addons_path_exists: bool
        addons: List[RuntimeAddonInfo]
        healthy: bool
        status: str

    class EnvStatusInput(BaseModel):
        """Empty input for env.status"""

        pass

    class EnvStatusResult(BaseModel):
        wow_root: Optional[str]
        dev_path: Optional[str]
        data_dir: str
        flavors: List[FlavorInfo]
        mechanic_runtime: List[RuntimeFlavorInfo]
        mechanic_runtime_healthy: bool
        mechanic_runtime_issues: List[str]

    @server.command(
        name="env.status",
        description="Get Mechanic environment configuration and runtime installation status",
        input_schema=EnvStatusInput,
        output_schema=EnvStatusResult,
    )
    async def env_status(
        input: EnvStatusInput, context: Any = None
    ) -> CommandResult[EnvStatusResult]:
        config = get_config()

        # Gather flavor information
        flavors = []
        for flavor in config.flavors:
            flavor_path = config.wow_root / flavor if config.wow_root else None
            flavors.append(
                FlavorInfo(
                    name=flavor,
                    path=str(flavor_path) if flavor_path else "",
                    exists=flavor_path.exists() if flavor_path else False,
                )
            )

        runtime_status = inspect_mechanic_runtime(config.wow_root, config.flavors)
        runtime_healthy = mechanic_runtime_is_complete(runtime_status)
        runtime_issues = format_runtime_issues(runtime_status)
        runtime_info = [
            RuntimeFlavorInfo(**status.to_dict()) for status in runtime_status
        ]

        warnings = None
        if not runtime_healthy:
            warnings = [
                create_warning(
                    "MECHANIC_RUNTIME_INCOMPLETE",
                    "; ".join(runtime_issues[:3]),
                    WarningSeverity.CAUTION,
                    details={"issues": runtime_issues},
                )
            ]

        return success(
            data=EnvStatusResult(
                wow_root=str(config.wow_root) if config.wow_root else None,
                dev_path=str(config.dev_path) if config.dev_path else None,
                data_dir=str(config.data_dir),
                flavors=flavors,
                mechanic_runtime=runtime_info,
                mechanic_runtime_healthy=runtime_healthy,
                mechanic_runtime_issues=runtime_issues,
            ),
            reasoning=f"Environment configured with {len([f for f in flavors if f.exists])} active WoW clients; Mechanic runtime {'complete' if runtime_healthy else 'incomplete'}",
            warnings=warnings,
            confidence=1.0,
        )

    # ═══════════════════════════════════════════════════════════════════════════
    # system.pick_file - Open native file picker dialog
    # ═══════════════════════════════════════════════════════════════════════════

    class PickFileInput(BaseModel):
        title: str = Field("Select File", description="Title of the dialog window")
        filter: str = Field(
            "All Files (*.*)|*.*",
            description="File filter (e.g., 'Text Files (*.txt)|*.txt')",
        )

    class PickFileResult(BaseModel):
        path: str
        filename: str
        directory: str

    @server.command(
        name="system.pick_file",
        description="Open a native file picker dialog to select a file",
        input_schema=PickFileInput,
        output_schema=PickFileResult,
    )
    async def pick_file(
        input: PickFileInput, context: Any = None
    ) -> CommandResult[PickFileResult]:
        # PowerShell script to open file dialog
        ps_script = f"""
        Add-Type -AssemblyName System.Windows.Forms
        $FileBrowser = New-Object System.Windows.Forms.OpenFileDialog
        $FileBrowser.Title = '{input.title}'
        $FileBrowser.Filter = '{input.filter}'
        $FileBrowser.InitialDirectory = [System.Environment]::GetFolderPath('MyDocuments')
        
        if ($FileBrowser.ShowDialog() -eq [System.Windows.Forms.DialogResult]::OK) {{
            Write-Output $FileBrowser.FileName
        }}
        """

        try:
            result = subprocess.run(
                ["powershell", "-Command", ps_script],
                capture_output=True,
                text=True,
                timeout=60,  # Give user time to pick
            )

            file_path = result.stdout.strip()

            if not file_path or not Path(file_path).exists():
                return error(
                    code="NO_SELECTION",
                    message="No file selected or file does not exist",
                    suggestion="Try again and select a valid file",
                )

            path_obj = Path(file_path)

            src = create_source(
                type="file",
                id="file-picker",
                title="User Selection",
                location=str(path_obj),
            )

            return success(
                data=PickFileResult(
                    path=str(path_obj),
                    filename=path_obj.name,
                    directory=str(path_obj.parent),
                ),
                reasoning=f"User selected: {path_obj.name}",
                sources=[src],
                confidence=1.0,
            )

        except subprocess.TimeoutExpired:
            return error(code="TIMEOUT", message="File picker timed out")
        except Exception as e:
            return error(code="ERROR", message=f"File picker failed: {e}")
