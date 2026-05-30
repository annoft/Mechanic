"""
Tool setup module for downloading and installing development tools.
Supports Windows (direct download) and macOS (Homebrew/LuaRocks instructions).
"""

import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path
from typing import Optional, Dict, Any, List, Tuple
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError


# Paths
BIN_DIR = Path(__file__).parent.parent.parent / "bin"
CHECKSUMS_FILE = BIN_DIR / "checksums.json"
BUSTED_RECOMMENDED_VERSION = "2.2.0-1"


def get_platform() -> str:
    """Get current platform: 'windows' or 'darwin'."""
    if sys.platform == "win32":
        return "windows"
    elif sys.platform == "darwin":
        return "darwin"
    else:
        return "linux"  # Unsupported but handle gracefully


def load_checksums() -> Dict[str, Any]:
    """Load the checksums manifest file."""
    if CHECKSUMS_FILE.exists():
        return json.loads(CHECKSUMS_FILE.read_text(encoding="utf-8"))
    return {}


def verify_checksum(file_path: Path, expected_hash: str) -> bool:
    """Verify SHA256 checksum of a file."""
    if expected_hash == "skip" or expected_hash == "placeholder":
        return True

    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha256.update(chunk)
    return sha256.hexdigest().lower() == expected_hash.lower()


def verify_checksum_bytes(content: bytes, expected_hash: str) -> bool:
    """Verify SHA256 checksum of in-memory content."""
    if expected_hash == "skip" or expected_hash == "placeholder":
        return True

    return hashlib.sha256(content).hexdigest().lower() == expected_hash.lower()


def download_file(url: str, timeout: int = 60) -> bytes:
    """Download a file from URL and return its contents."""
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Mechanic/1.0"}
    request = Request(url, headers=headers)
    with urlopen(request, timeout=timeout) as response:
        return response.read()


def extract_from_zip(zip_content: bytes, archive_path: str) -> bytes:
    """Extract a specific file from a zip archive."""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".zip") as tmp:
        tmp.write(zip_content)
        tmp_path = Path(tmp.name)

    try:
        with zipfile.ZipFile(tmp_path, "r") as zf:
            # Try exact path first
            if archive_path in zf.namelist():
                return zf.read(archive_path)

            # Try finding the file by name (in case it's nested)
            for member in zf.namelist():
                if member.endswith(archive_path) or member.endswith("/" + archive_path):
                    return zf.read(member)

            raise FileNotFoundError(
                f"'{archive_path}' not found in archive. Contents: {zf.namelist()}"
            )
    finally:
        tmp_path.unlink()


def find_tool(name: str) -> Optional[Path]:
    """
    Find a tool, checking Mechanic bin/ first, then system PATH.

    Args:
        name: Tool name without extension (e.g., 'luacheck')

    Returns:
        Path to the tool if found, None otherwise.
    """
    # Platform-specific executable extensions
    extensions = [".exe", ".bat", ".cmd", ""] if sys.platform == "win32" else [""]

    # 1. Check Mechanic bin/
    for ext in extensions:
        tool_path = BIN_DIR / f"{name}{ext}"
        if tool_path.exists():
            return tool_path

    # Lua 5.1 Windows distributions often install lua5.1.exe rather than
    # lua.exe. Treat it as the Lua tool so users do not need to create shims.
    if name == "lua" and sys.platform == "win32":
        lua_candidates = [BIN_DIR / "lua5.1.exe", Path("C:/Lua/lua5.1.exe")]
        localappdata = os.environ.get("LOCALAPPDATA")
        if localappdata:
            lua_candidates.insert(1, Path(localappdata) / "LuaRocks51" / "lua5.1.exe")
        for tool_path in lua_candidates:
            if tool_path.exists():
                return tool_path

        result = shutil.which("lua5.1")
        if result:
            return Path(result)

    # 2. Check system PATH
    result = shutil.which(name)
    if result:
        return Path(result)

    return None


def get_tool_version(tool_path: Path, name: str) -> Optional[str]:
    """Try to get the version of an installed tool."""
    ok, version, _message = probe_tool(tool_path, name)
    return version if ok else None


def probe_tool(tool_path: Path, name: str) -> Tuple[bool, Optional[str], Optional[str]]:
    """Run a tool's version command and report whether it actually works."""

    version_flags = {
        "luacheck": ["--version"],
        "stylua": ["--version"],
        "lua": ["-v"],
    }

    flags = version_flags.get(name, ["--version"])

    try:
        result = subprocess.run(
            [str(tool_path)] + flags, capture_output=True, text=True, timeout=5
        )
        output = result.stdout or result.stderr
        first_line = output.strip().split("\n")[0] if output else None

        if result.returncode != 0:
            message = first_line or f"Exited with code {result.returncode}"
            return False, first_line, message

        if not first_line:
            return False, None, "No version output"

        return True, first_line, None
    except Exception as e:
        return False, None, str(e)

    return False, None, "Unknown tool error"


def download_tool_windows(
    name: str, info: Dict[str, Any], force: bool = False
) -> Tuple[bool, str]:
    """
    Download and install a tool on Windows.

    Returns:
        Tuple of (success, message)
    """
    platform_info = info.get("windows", {})
    if not platform_info:
        return False, f"No Windows configuration for {name}"

    filename = platform_info["filename"]
    target = BIN_DIR / filename

    # Skip if already installed and valid
    if target.exists() and not force:
        if verify_checksum(target, platform_info.get("sha256", "skip")):
            return True, f"Already installed: {filename}"

    if not force:
        existing_tool = find_tool(name)
        if existing_tool and existing_tool != target:
            ok, version, _message = probe_tool(existing_tool, name)
            if ok:
                return True, f"Already installed: {existing_tool} v{version}"

    url = platform_info.get("url")
    archive_path = platform_info.get("archive_path")

    if not url:
        tool_path = find_tool(name)
        message = platform_info.get("message") or f"Manual installation required for {name}"
        if tool_path:
            ok, version, error_message = probe_tool(tool_path, name)
            if ok:
                return True, f"Already installed: {tool_path.name} v{version}"
            return False, f"{message}. Existing {tool_path.name} failed: {error_message}"
        return False, message

    try:
        content = download_file(url)

        writes: List[Tuple[Path, bytes]] = []

        # Handle archives whenever archive_path is present. Some providers
        # redirect from non-.zip URLs, so URL suffix is not reliable.
        if archive_path:
            archive_content = content
            primary_content = extract_from_zip(archive_content, archive_path)
            writes.append((target, primary_content))

            for extra_file in platform_info.get("extra_files", []):
                extra_content = extract_from_zip(archive_content, extra_file)
                writes.append((BIN_DIR / Path(extra_file).name, extra_content))
        else:
            writes.append((target, content))

        # Verify checksum before touching the existing installation.
        expected_hash = platform_info.get("sha256", "skip")
        if not verify_checksum_bytes(writes[0][1], expected_hash):
            return False, f"Checksum mismatch for {filename}"

        # Write only after the primary file is known-good.
        BIN_DIR.mkdir(parents=True, exist_ok=True)
        for write_path, write_content in writes:
            write_path.write_bytes(write_content)

        return True, f"Installed: {filename} v{info.get('version', '?')}"

    except HTTPError as e:
        return False, f"Download failed ({e.code}): {url}"
    except URLError as e:
        return False, f"Network error: {e.reason}"
    except zipfile.BadZipFile:
        return False, f"Downloaded archive was not a valid ZIP: {url}"
    except Exception as e:
        return False, f"Error: {str(e)}"


def get_macos_instructions(name: str, info: Dict[str, Any]) -> str:
    """Get macOS installation instructions for a tool."""
    platform_info = info.get("darwin", {})
    if not platform_info:
        return f"No macOS configuration for {name}"

    if "install_cmd" in platform_info:
        return f"Run: {platform_info['install_cmd']}"
    elif "url" in platform_info:
        return f"Download from: {platform_info['url']}"
    else:
        return "See documentation for installation"


def setup_tools(force: bool = False, verify_only: bool = False) -> List[Dict[str, Any]]:
    """
    Download and install all required tools.

    Args:
        force: Re-download even if tools exist
        verify_only: Only check if tools are installed, don't download

    Returns:
        List of tool status dictionaries
    """
    checksums = load_checksums()
    if not checksums:
        return [
            {"name": "error", "installed": False, "message": "checksums.json not found"}
        ]

    platform = get_platform()
    tools = checksums.get("tools", {})
    results = []

    for name, info in tools.items():
        required = info.get("required", True)

        if verify_only:
            # Check that the tool exists and can run its version command.
            tool_path = find_tool(name)
            if tool_path:
                ok, version, message = probe_tool(tool_path, name)
                results.append(
                    {
                        "name": name,
                        "installed": ok,
                        "path": str(tool_path),
                        "version": version or info.get("version"),
                        "required": required,
                        "message": None if ok else f"Found but failed to run: {message}",
                    }
                )
            else:
                results.append(
                    {
                        "name": name,
                        "installed": False,
                        "path": None,
                        "version": None,
                        "required": required,
                        "message": "Not found",
                    }
                )
        else:
            # Download/install
            if platform == "windows":
                success, message = download_tool_windows(name, info, force)
                tool_path = find_tool(name)
                results.append(
                    {
                        "name": name,
                        "installed": success,
                        "path": str(tool_path) if tool_path else None,
                        "version": info.get("version"),
                        "required": required,
                        "message": message,
                    }
                )
            elif platform == "darwin":
                # macOS: Check if installed, otherwise provide instructions
                tool_path = find_tool(name)
                if tool_path:
                    results.append(
                        {
                            "name": name,
                            "installed": True,
                            "path": str(tool_path),
                            "version": get_tool_version(tool_path, name)
                            or info.get("version"),
                            "required": required,
                        }
                    )
                else:
                    instructions = get_macos_instructions(name, info)
                    results.append(
                        {
                            "name": name,
                            "installed": False,
                            "path": None,
                            "version": None,
                            "required": required,
                            "message": instructions,
                        }
                    )
            else:
                results.append(
                    {
                        "name": name,
                        "installed": False,
                        "path": None,
                        "version": None,
                        "required": required,
                        "message": "Platform not supported",
                    }
                )

    return results


def get_setup_summary(results: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Generate a summary of setup results."""
    installed = [r for r in results if r.get("installed")]
    missing = [r for r in results if not r.get("installed")]
    required_missing = [r for r in missing if r.get("required")]

    return {
        "success": len(required_missing) == 0,
        "installed_count": len(installed),
        "missing_count": len(missing),
        "required_missing": len(required_missing),
        "platform": get_platform(),
        "tools": results,
    }


# ═══════════════════════════════════════════════════════════════════════════════
# LUAROCKS / BUSTED SETUP
# ═══════════════════════════════════════════════════════════════════════════════


def _version_key(path: Path) -> Tuple[int, ...]:
    """Sort LuaRocks versions naturally enough for busted 2.x folders."""
    return tuple(int(part) for part in re.findall(r"\d+", path.name))


def find_luarocks_paths() -> Optional[Dict[str, Any]]:
    """
    Find LuaRocks installation and return relevant paths.

    Returns dict with:
        - luarocks_home: LuaRocks user directory
        - share_path: Lua modules path
        - lib_path: Native libraries path
        - busted_bin: Path to busted script
    """
    home = Path.home()
    candidates: List[Path] = []

    def add_candidate(value: Optional[str | Path]) -> None:
        if not value:
            return
        path = Path(value).expanduser()
        if path not in candidates:
            candidates.append(path)

    add_candidate(os.environ.get("LUAROCKS_HOME"))
    add_candidate(os.environ.get("MECHANIC_LUAROCKS_TREE"))

    appdata = os.environ.get("APPDATA")
    localappdata = os.environ.get("LOCALAPPDATA")
    add_candidate(Path(appdata) / "luarocks" if appdata else None)
    add_candidate(home / "AppData" / "Roaming" / "luarocks")
    add_candidate(Path(localappdata) / "LuaRocks51" if localappdata else None)
    add_candidate(Path(localappdata) / "LuaRocks51" / "systree" if localappdata else None)
    add_candidate("C:/Program Files/luarocks")
    add_candidate("C:/Program Files (x86)/luarocks")

    for luarocks_home in candidates:
        if not luarocks_home.exists():
            continue

        share_path = luarocks_home / "share" / "lua" / "5.1"
        lib_path = luarocks_home / "lib" / "lua" / "5.1"

        # Find busted in rocks directory
        rocks_dir = luarocks_home / "lib" / "luarocks" / "rocks-5.1" / "busted"
        if rocks_dir.exists():
            # Get highest version
            versions = list(rocks_dir.iterdir())
            if versions:
                latest = sorted(versions, key=_version_key)[-1]
                for busted_bin in (
                    latest / "bin" / "busted",
                    latest / "bin" / "busted.bat",
                    latest / "bin" / "busted.lua",
                ):
                    if busted_bin.exists():
                        return {
                            "luarocks_home": luarocks_home,
                            "share_path": share_path,
                            "lib_path": lib_path,
                            "busted_bin": busted_bin,
                            "busted_version": latest.name,
                        }

    return None


def generate_busted_bat(output_path: Optional[Path] = None) -> Tuple[bool, str]:
    """
    Generate busted.bat with correct paths for this user's LuaRocks install.

    Args:
        output_path: Where to write busted.bat (default: BIN_DIR/busted.bat)

    Returns:
        Tuple of (success, message)
    """
    if get_platform() != "windows":
        return False, "busted.bat generation is Windows-only"

    # Find LuaRocks
    paths = find_luarocks_paths()
    if not paths:
        return False, "LuaRocks not found. Install busted via: luarocks install busted"

    # Find Lua in our bin/
    lua_path = find_tool("lua")
    if not lua_path:
        return False, "lua.exe not found in bin/. Run 'mech setup' first."

    # Build the bat file content
    share_path = paths["share_path"]
    lib_path = paths["lib_path"]
    busted_bin = paths["busted_bin"]
    busted_version = paths.get("busted_version", BUSTED_RECOMMENDED_VERSION)

    # Escape backslashes for Lua string
    share_lua = str(share_path).replace("\\", "\\\\")
    lib_lua = str(lib_path).replace("\\", "\\\\")
    busted_lua = str(busted_bin).replace("\\", "\\\\")

    bat_content = f'''@echo off
setlocal
"{lua_path}" -e "package.path=\\"{share_lua}\\\\?.lua;{share_lua}\\\\?\\\\init.lua;\\"..package.path;package.cpath=\\"{lib_lua}\\\\?.dll;\\"..package.cpath;local k,l=pcall(require,'luarocks.loader') if k and l.add_context then pcall(l.add_context,'busted','{busted_version}') end" "{busted_lua}" %*
exit /b %ERRORLEVEL%
'''

    # Write file
    target = output_path or (BIN_DIR / "busted.bat")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(bat_content, encoding="utf-8")

    return True, f"Generated {target}"


def setup_busted() -> Tuple[bool, str]:
    """
    Setup busted test runner by generating busted.bat.

    This should be called after luarocks install busted.
    """
    return generate_busted_bat()
