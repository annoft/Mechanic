"""
Command Unit Tests for Mechanic Desktop.

Tests verify all 39 commands follow structured patterns:
- Success/error result structure
- Proper reasoning and sources
- Schema validation
"""

import pytest
import asyncio
import tempfile
import os
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
from mechanic.commands.core import get_server
from afd.testing.assertions import assert_success, assert_error, assert_has_reasoning, assert_has_sources


# ═══════════════════════════════════════════════════════════════════════════════
# SavedVariables Commands (sv.*)
# ═══════════════════════════════════════════════════════════════════════════════

@pytest.mark.asyncio
async def test_sv_discover():
    """Test sv.discover finds WoW installations."""
    server = get_server()
    result = await server.execute("sv.discover", {})

    if result.success:
        data = assert_success(result)
        assert hasattr(data, 'paths')
        assert isinstance(data.paths, list)
        assert_has_sources(result)
    else:
        # Valid error if no WoW found
        assert_error(result, "NOT_FOUND")


@pytest.mark.asyncio
async def test_sv_parse_missing_file():
    """Test sv.parse handles missing file gracefully."""
    server = get_server()
    result = await server.execute("sv.parse", {"file_path": "non_existent_file.lua"})

    assert_error(result, "FILE_NOT_FOUND")
    assert "not found" in result.error.message.lower()


@pytest.mark.asyncio
async def test_sv_parse_valid_file():
    """Test sv.parse with a valid Lua file."""
    server = get_server()

    # Create a temporary valid SavedVariables file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.lua', delete=False) as f:
        f.write('TestDB = { version = 1, data = "test" }')
        temp_path = f.name

    try:
        result = await server.execute("sv.parse", {"file_path": temp_path})
        data = assert_success(result)
        # sv.parse returns SavedVariables with addons attribute
        assert hasattr(data, 'addons')
    finally:
        os.unlink(temp_path)


# ═══════════════════════════════════════════════════════════════════════════════
# Addon Commands (addon.*)
# ═══════════════════════════════════════════════════════════════════════════════

@pytest.mark.asyncio
async def test_addon_output():
    """Test addon.output returns structured markdown output."""
    server = get_server()
    result = await server.execute("addon.output", {})

    data = assert_success(result)

    # Verify schema
    assert hasattr(data, 'output')
    assert hasattr(data, 'error_count')
    assert hasattr(data, 'test_count')
    assert hasattr(data, 'console_count')

    # Verify compliance
    assert_has_reasoning(result)
    assert_has_sources(result)

    # Verify markdown structure
    assert "## Addon Output" in data.output
    assert "### Errors" in data.output
    assert "### Tests" in data.output
    assert "### Console" in data.output


@pytest.mark.asyncio
async def test_addon_output_agent_mode():
    """Test addon.output with agent_mode compression."""
    server = get_server()
    result = await server.execute("addon.output", {"agent_mode": True})

    data = assert_success(result)
    assert hasattr(data, 'output')
    # Agent mode should still produce valid output
    assert "## Addon Output" in data.output


@pytest.mark.asyncio
async def test_addon_output_reports_missing_hub_data_when_runtime_healthy(tmp_path):
    """Runtime is installed, but MechanicDB.addonData is absent/empty."""
    server = get_server()
    mechanic_sv = tmp_path / "!Mechanic.lua"
    mechanic_sv.write_text("MechanicDB = {}", encoding="utf-8")

    config = SimpleNamespace(wow_root=tmp_path, flavors=["_retail_"])
    parsed_sv = {
        "MechanicDB": {
            "profiles": {
                "Default": {
                    "addonData": {},
                    "consoleBuffer": {},
                    "loadedLibraries": {},
                    "testResults": {},
                }
            }
        }
    }

    with (
        patch("mechanic.server.storage.get_latest_metrics", return_value=None),
        patch("mechanic.config.get_config", return_value=config),
        patch("mechanic.config.discover_saved_variables", return_value=[tmp_path]),
        patch("mechanic.parsers.parse_savedvariables", return_value=parsed_sv),
        patch("mechanic.commands.output.inspect_mechanic_runtime", return_value=[]),
        patch(
            "mechanic.commands.output.mechanic_runtime_is_complete",
            return_value=True,
        ),
        patch("mechanic.commands.output.format_runtime_issues", return_value=[]),
    ):
        result = await server.execute("addon.output", {})

    data = assert_success(result)
    warnings = result.warnings or []

    assert "Mechanic Hub Diagnostic" in data.output
    assert "hub has not registered addon data" in data.output
    assert "hub has not registered addon data" in result.reasoning
    assert any(w.code == "MECHANIC_HUB_DATA_MISSING" for w in warnings)


@pytest.mark.asyncio
async def test_addon_validate_missing_addon():
    """Test addon.validate handles missing addon gracefully."""
    server = get_server()
    result = await server.execute("addon.validate", {"addon": "NonExistentAddon12345"})

    # Should error with NOT_FOUND or similar
    assert not result.success
    assert result.error is not None


@pytest.mark.asyncio
async def test_addon_lint_missing_addon():
    """Test addon.lint handles missing addon gracefully."""
    server = get_server()
    result = await server.execute("addon.lint", {"addon": "NonExistentAddon12345"})

    assert not result.success
    assert result.error is not None


@pytest.mark.asyncio
async def test_addon_format_missing_addon():
    """Test addon.format handles missing addon gracefully."""
    server = get_server()
    result = await server.execute("addon.format", {"addon": "NonExistentAddon12345", "check": True})

    assert not result.success
    assert result.error is not None


@pytest.mark.asyncio
async def test_addon_test_missing_addon():
    """Test addon.test handles missing addon gracefully."""
    server = get_server()
    result = await server.execute("addon.test", {"addon": "NonExistentAddon12345"})

    assert not result.success
    assert result.error is not None


@pytest.mark.asyncio
async def test_addon_deprecations_missing_addon():
    """Test addon.deprecations handles missing addon gracefully."""
    server = get_server()
    result = await server.execute("addon.deprecations", {"addon": "NonExistentAddon12345"})

    assert not result.success
    assert result.error is not None


@pytest.mark.asyncio
async def test_addon_create_missing_name():
    """Test addon.create requires addon name."""
    server = get_server()
    result = await server.execute("addon.create", {})

    # Should fail validation or require name parameter
    assert not result.success


@pytest.mark.asyncio
async def test_addon_sync_missing_addon():
    """Test addon.sync handles missing addon gracefully."""
    server = get_server()
    result = await server.execute("addon.sync", {"addon": "NonExistentAddon12345"})

    assert not result.success
    assert result.error is not None


# ═══════════════════════════════════════════════════════════════════════════════
# Library Commands (libs.*)
# ═══════════════════════════════════════════════════════════════════════════════

@pytest.mark.asyncio
async def test_libs_check_missing_addon():
    """Test libs.check handles missing addon gracefully."""
    server = get_server()
    result = await server.execute("libs.check", {"addon": "NonExistentAddon12345"})

    assert not result.success
    assert result.error is not None


@pytest.mark.asyncio
async def test_libs_init_missing_addon():
    """Test libs.init handles missing addon gracefully."""
    server = get_server()
    result = await server.execute("libs.init", {"addon": "NonExistentAddon12345"})

    assert not result.success
    assert result.error is not None


@pytest.mark.asyncio
async def test_libs_sync_missing_addon():
    """Test libs.sync handles missing addon gracefully."""
    server = get_server()
    result = await server.execute("libs.sync", {"addon": "NonExistentAddon12345"})

    assert not result.success
    assert result.error is not None


@pytest.mark.parametrize("manifest_name", ["lib.xml", "widget.xml"])
@pytest.mark.asyncio
async def test_libs_check_accepts_root_level_loadable_manifest(tmp_path, manifest_name):
    """Root-level loadable files do not need to match the library folder name."""
    addon_path = tmp_path / "TestAddon"
    libs_path = addon_path / "Libs"
    lib_path = libs_path / "ManifestLib-1.0"
    lib_path.mkdir(parents=True)
    (addon_path / "TestAddon.toc").write_text("## Interface: 120005\n", encoding="utf-8")
    (libs_path / "libs.json").write_text(
        '{"mode":"include","libraries":{"ManifestLib-1.0":"latest"}}',
        encoding="utf-8",
    )
    (lib_path / manifest_name).write_text("<Ui></Ui>\n", encoding="utf-8")

    server = get_server()
    with patch("mechanic.commands.environment.find_addon_path", return_value=addon_path):
        result = await server.execute("libs.check", {"addon": "TestAddon"})

    data = assert_success(result)
    lib_status = next(lib for lib in data.libraries if lib.name == "ManifestLib-1.0")
    assert lib_status.status == "ok"
    assert data.issues == []


@pytest.mark.asyncio
async def test_libs_check_reports_empty_configured_library(tmp_path):
    """Configured library folders without loadable files are incomplete."""
    addon_path = tmp_path / "TestAddon"
    libs_path = addon_path / "Libs"
    (libs_path / "EmptyLib-1.0").mkdir(parents=True)
    (addon_path / "TestAddon.toc").write_text("## Interface: 120005\n", encoding="utf-8")
    (libs_path / "libs.json").write_text(
        '{"mode":"include","libraries":{"EmptyLib-1.0":"latest"}}',
        encoding="utf-8",
    )

    server = get_server()
    with patch("mechanic.commands.environment.find_addon_path", return_value=addon_path):
        result = await server.execute("libs.check", {"addon": "TestAddon"})

    data = assert_success(result)
    lib_status = next(lib for lib in data.libraries if lib.name == "EmptyLib-1.0")
    assert lib_status.status == "incomplete"
    assert any("Incomplete: EmptyLib-1.0" in issue for issue in data.issues)


@pytest.mark.asyncio
async def test_libs_check_reports_non_loadable_only_configured_library(tmp_path):
    """Configured library folders with only docs are incomplete."""
    addon_path = tmp_path / "TestAddon"
    libs_path = addon_path / "Libs"
    lib_path = libs_path / "DocsOnlyLib-1.0"
    lib_path.mkdir(parents=True)
    (addon_path / "TestAddon.toc").write_text("## Interface: 120005\n", encoding="utf-8")
    (libs_path / "libs.json").write_text(
        '{"mode":"include","libraries":{"DocsOnlyLib-1.0":"latest"}}',
        encoding="utf-8",
    )
    (lib_path / "README.md").write_text("# Docs only\n", encoding="utf-8")

    server = get_server()
    with patch("mechanic.commands.environment.find_addon_path", return_value=addon_path):
        result = await server.execute("libs.check", {"addon": "TestAddon"})

    data = assert_success(result)
    lib_status = next(lib for lib in data.libraries if lib.name == "DocsOnlyLib-1.0")
    assert lib_status.status == "incomplete"
    assert any("Incomplete: DocsOnlyLib-1.0" in issue for issue in data.issues)


@pytest.mark.asyncio
async def test_libs_sync_repairs_incomplete_existing_library(tmp_path):
    """Existing incomplete target directories are updated from a valid source."""
    addon_path = tmp_path / "TestAddon"
    libs_path = addon_path / "Libs"
    target_path = libs_path / "RepairLib-1.0"
    source_root = tmp_path / "SharedLibs"
    source_path = source_root / "RepairLib-1.0"
    target_path.mkdir(parents=True)
    source_path.mkdir(parents=True)
    (addon_path / "TestAddon.toc").write_text("## Interface: 120005\n", encoding="utf-8")
    (libs_path / "libs.json").write_text(
        '{"mode":"include","libraries":{"RepairLib-1.0":"latest"}}',
        encoding="utf-8",
    )
    (source_path / "RepairLib-1.0.lua").write_text(
        "local MAJOR, MINOR = 'RepairLib-1.0', 1\n", encoding="utf-8"
    )
    config = SimpleNamespace(dev_path=tmp_path, data_dir=tmp_path)

    server = get_server()
    with patch("mechanic.commands.environment.find_addon_path", return_value=addon_path), patch(
        "mechanic.commands.environment.get_config", return_value=config
    ):
        result = await server.execute(
            "libs.sync",
            {"addon": "TestAddon", "source": str(source_root)},
        )

    data = assert_success(result)
    action = next(action for action in data.actions if action.library == "RepairLib-1.0")
    assert action.action == "update"
    assert data.updated == 1
    assert (target_path / "RepairLib-1.0.lua").exists()


@pytest.mark.asyncio
async def test_libs_sync_errors_when_incomplete_library_has_no_source(tmp_path):
    """Incomplete target directories without a source are not silently skipped."""
    addon_path = tmp_path / "TestAddon"
    libs_path = addon_path / "Libs"
    (libs_path / "MissingSource-1.0").mkdir(parents=True)
    (addon_path / "TestAddon.toc").write_text("## Interface: 120005\n", encoding="utf-8")
    (libs_path / "libs.json").write_text(
        '{"mode":"include","libraries":{"MissingSource-1.0":"latest"}}',
        encoding="utf-8",
    )
    config = SimpleNamespace(dev_path=tmp_path, data_dir=tmp_path)

    server = get_server()
    with patch("mechanic.commands.environment.find_addon_path", return_value=addon_path), patch(
        "mechanic.commands.environment.get_config", return_value=config
    ):
        result = await server.execute("libs.sync", {"addon": "TestAddon"})

    data = assert_success(result)
    action = next(
        action for action in data.actions if action.library == "MissingSource-1.0"
    )
    assert action.action == "error"
    assert data.errors == 1
    assert "incomplete" in action.reason


@pytest.mark.asyncio
async def test_libs_sync_invalid_library_source_does_not_use_sibling_addon(tmp_path):
    """Invalid per-library source config is not masked by sibling addon Libs."""
    addon_path = tmp_path / "TestAddon"
    libs_path = addon_path / "Libs"
    target_path = libs_path / "FallbackLib-1.0"
    sibling_source = tmp_path / "SourceAddon" / "SourceAddon" / "Libs" / "FallbackLib-1.0"
    libs_path.mkdir(parents=True)
    sibling_source.mkdir(parents=True)
    (addon_path / "TestAddon.toc").write_text("## Interface: 120005\n", encoding="utf-8")
    (libs_path / "libs.json").write_text(
        (
            '{"mode":"include","libraries":'
            '{"FallbackLib-1.0":{"version":"latest","source":"MissingLibs/FallbackLib-1.0"}}}'
        ),
        encoding="utf-8",
    )
    (sibling_source / "FallbackLib-1.0.lua").write_text("new\n", encoding="utf-8")
    config = SimpleNamespace(dev_path=tmp_path, data_dir=tmp_path)

    server = get_server()
    with patch("mechanic.commands.environment.find_addon_path", return_value=addon_path), patch(
        "mechanic.commands.environment.get_config", return_value=config
    ):
        result = await server.execute("libs.sync", {"addon": "TestAddon"})

    data = assert_success(result)
    action = next(action for action in data.actions if action.library == "FallbackLib-1.0")
    assert action.action == "error"
    assert action.source is None
    assert data.errors == 1
    assert not target_path.exists()


@pytest.mark.asyncio
async def test_libs_sync_force_uses_external_source_not_target(tmp_path):
    """Force sync excludes the installed target when finding a source."""
    addon_path = tmp_path / "TestAddon"
    libs_path = addon_path / "Libs"
    target_path = libs_path / "ForceLib-1.0"
    source_path = tmp_path / "ForceLib-1.0"
    target_path.mkdir(parents=True)
    source_path.mkdir(parents=True)
    (addon_path / "TestAddon.toc").write_text("## Interface: 120005\n", encoding="utf-8")
    (libs_path / "libs.json").write_text(
        '{"mode":"include","libraries":{"ForceLib-1.0":"latest"}}',
        encoding="utf-8",
    )
    (target_path / "ForceLib-1.0.lua").write_text("old\n", encoding="utf-8")
    (source_path / "ForceLib-1.0.lua").write_text("new\n", encoding="utf-8")
    config = SimpleNamespace(dev_path=tmp_path, data_dir=tmp_path)

    server = get_server()
    with patch("mechanic.commands.environment.find_addon_path", return_value=addon_path), patch(
        "mechanic.commands.environment.get_config", return_value=config
    ):
        result = await server.execute(
            "libs.sync",
            {"addon": "TestAddon", "force": True},
        )

    data = assert_success(result)
    action = next(action for action in data.actions if action.library == "ForceLib-1.0")
    assert action.action == "update"
    assert action.source == str(source_path)
    assert (target_path / "ForceLib-1.0.lua").read_text(encoding="utf-8") == "new\n"


@pytest.mark.asyncio
async def test_libs_sync_dry_run_does_not_write_debug_file(tmp_path):
    """Dry-run sync does not write troubleshooting files into data_dir."""
    addon_path = tmp_path / "TestAddon"
    libs_path = addon_path / "Libs"
    source_root = tmp_path / "SharedLibs"
    source_path = source_root / "DryRunLib-1.0"
    data_dir = tmp_path / "data"
    libs_path.mkdir(parents=True)
    source_path.mkdir(parents=True)
    data_dir.mkdir()
    (addon_path / "TestAddon.toc").write_text("## Interface: 120005\n", encoding="utf-8")
    (libs_path / "libs.json").write_text(
        '{"mode":"include","libraries":{"DryRunLib-1.0":"latest"}}',
        encoding="utf-8",
    )
    (source_path / "DryRunLib-1.0.lua").write_text("new\n", encoding="utf-8")
    config = SimpleNamespace(dev_path=tmp_path, data_dir=data_dir)

    server = get_server()
    with patch("mechanic.commands.environment.find_addon_path", return_value=addon_path), patch(
        "mechanic.commands.environment.get_config", return_value=config
    ):
        result = await server.execute(
            "libs.sync",
            {"addon": "TestAddon", "source": str(source_root), "dry_run": True},
        )

    data = assert_success(result)
    action = next(action for action in data.actions if action.library == "DryRunLib-1.0")
    assert action.action == "copy"
    assert data.copied == 1
    assert not (libs_path / "DryRunLib-1.0").exists()
    assert not (data_dir / "libs_sync_debug.json").exists()


# ═══════════════════════════════════════════════════════════════════════════════
# API Reference Commands (api.*)
# ═══════════════════════════════════════════════════════════════════════════════

@pytest.mark.asyncio
async def test_api_search():
    """Test api.search finds WoW APIs."""
    server = get_server()
    result = await server.execute("api.search", {"query": "UnitHealth"})

    data = assert_success(result)
    assert hasattr(data, 'results') or hasattr(data, 'apis') or hasattr(data, 'matches')
    assert_has_reasoning(result)


@pytest.mark.asyncio
async def test_api_search_no_results():
    """Test api.search handles no matches gracefully."""
    server = get_server()
    result = await server.execute("api.search", {"query": "xyznonexistent12345"})

    # Should succeed with empty results, not error
    data = assert_success(result)


@pytest.mark.asyncio
async def test_api_info():
    """Test api.info returns API details."""
    server = get_server()
    result = await server.execute("api.info", {"api": "UnitHealth"})

    if result.success:
        data = assert_success(result)
        assert_has_reasoning(result)
    else:
        # API might not be in database
        assert result.error is not None


@pytest.mark.asyncio
async def test_api_list():
    """Test api.list returns API namespaces."""
    server = get_server()
    result = await server.execute("api.list", {})

    data = assert_success(result)
    assert_has_reasoning(result)


@pytest.mark.asyncio
async def test_api_list_by_namespace():
    """Test api.list filters by namespace."""
    server = get_server()
    result = await server.execute("api.list", {"namespace": "C_Spell"})

    if result.success:
        data = assert_success(result)
        assert_has_reasoning(result)


@pytest.mark.asyncio
async def test_api_queue(tmp_path):
    """Test api.queue accepts API test requests."""
    server = get_server()
    with patch("mechanic.commands.api.find_addon_path", return_value=tmp_path):
        result = await server.execute("api.queue", {"apis": ["UnitHealth", "UnitName"]})

    if result.success:
        data = assert_success(result)
        assert_has_reasoning(result)


@pytest.mark.asyncio
async def test_api_stats():
    """Test api.stats returns API statistics."""
    server = get_server()
    result = await server.execute("api.stats", {})

    data = assert_success(result)
    assert_has_reasoning(result)


# ═══════════════════════════════════════════════════════════════════════════════
# Lua Eval Commands (lua.*)
# ═══════════════════════════════════════════════════════════════════════════════

@pytest.mark.asyncio
async def test_lua_queue(tmp_path):
    """Test lua.queue accepts Lua code for evaluation."""
    server = get_server()
    # lua.queue expects a list of code strings
    with patch("mechanic.commands.lua.find_addon_path", return_value=tmp_path):
        result = await server.execute("lua.queue", {
            "code": ["return 1 + 1"]
        })

    data = assert_success(result)
    assert_has_reasoning(result)


@pytest.mark.asyncio
async def test_lua_results():
    """Test lua.results returns evaluation results."""
    server = get_server()
    result = await server.execute("lua.results", {})

    data = assert_success(result)
    assert_has_reasoning(result)


# ═══════════════════════════════════════════════════════════════════════════════
# Sandbox Commands (sandbox.*)
# ═══════════════════════════════════════════════════════════════════════════════

@pytest.mark.asyncio
async def test_sandbox_status():
    """Test sandbox.status returns sandbox state."""
    server = get_server()
    result = await server.execute("sandbox.status", {})

    data = assert_success(result)
    assert_has_reasoning(result)


@pytest.mark.asyncio
async def test_sandbox_generate():
    """Test sandbox.generate creates test stubs."""
    server = get_server()
    result = await server.execute("sandbox.generate", {"addon": "NonExistentAddon"})

    # May fail for missing addon, but should return valid response
    assert result.success is True or result.error is not None


@pytest.mark.asyncio
async def test_sandbox_exec():
    """Test sandbox.exec runs sandbox tests."""
    server = get_server()
    result = await server.execute("sandbox.exec", {"addon": "NonExistentAddon"})

    # May fail for missing addon
    assert result.success is True or result.error is not None


@pytest.mark.asyncio
async def test_sandbox_test():
    """Test sandbox.test validates sandbox setup."""
    server = get_server()
    # sandbox.test requires addon parameter
    result = await server.execute("sandbox.test", {"addon": "!Mechanic"})

    if result.success:
        data = assert_success(result)
        assert_has_reasoning(result)
    else:
        # May fail if addon not found or no tests
        assert result.error is not None


# ═══════════════════════════════════════════════════════════════════════════════
# Locale Commands (locale.*)
# ═══════════════════════════════════════════════════════════════════════════════

@pytest.mark.asyncio
async def test_locale_validate_missing_addon():
    """Test locale.validate handles missing addon gracefully."""
    server = get_server()
    result = await server.execute("locale.validate", {"addon": "NonExistentAddon12345"})

    assert not result.success
    assert result.error is not None


@pytest.mark.asyncio
async def test_locale_extract_missing_addon():
    """Test locale.extract handles missing addon gracefully."""
    server = get_server()
    result = await server.execute("locale.extract", {"addon": "NonExistentAddon12345"})

    assert not result.success
    assert result.error is not None


# ═══════════════════════════════════════════════════════════════════════════════
# Atlas Commands (atlas.*)
# ═══════════════════════════════════════════════════════════════════════════════

@pytest.mark.asyncio
async def test_atlas_search():
    """Test atlas.search finds UI atlas icons."""
    server = get_server()
    result = await server.execute("atlas.search", {"query": "button"})

    # May fail if atlas index doesn't exist (expected in test env)
    if result.success:
        data = assert_success(result)
        assert_has_reasoning(result)
    else:
        assert_error(result, "INDEX_NOT_FOUND")


# ═══════════════════════════════════════════════════════════════════════════════
# Release Pipeline Commands (version.*, changelog.*, git.*, release.*)
# ═══════════════════════════════════════════════════════════════════════════════

@pytest.mark.asyncio
async def test_version_bump_missing_addon():
    """Test version.bump handles missing addon gracefully."""
    server = get_server()
    result = await server.execute("version.bump", {
        "addon": "NonExistentAddon12345",
        "version": "1.0.0"
    })

    assert not result.success
    assert result.error is not None


@pytest.mark.asyncio
async def test_changelog_add_missing_addon():
    """Test changelog.add handles missing addon gracefully."""
    server = get_server()
    result = await server.execute("changelog.add", {
        "addon": "NonExistentAddon12345",
        "version": "1.0.0",
        "changes": ["Test change"]
    })

    assert not result.success
    assert result.error is not None


@pytest.mark.asyncio
async def test_git_commit_missing_addon():
    """Test git.commit handles missing addon gracefully."""
    server = get_server()
    result = await server.execute("git.commit", {
        "addon": "NonExistentAddon12345",
        "message": "Test commit"
    })

    assert not result.success
    assert result.error is not None


@pytest.mark.asyncio
async def test_git_tag_missing_addon():
    """Test git.tag handles missing addon gracefully."""
    server = get_server()
    result = await server.execute("git.tag", {
        "addon": "NonExistentAddon12345",
        "version": "1.0.0"
    })

    assert not result.success
    assert result.error is not None


@pytest.mark.asyncio
async def test_release_all_missing_addon():
    """Test release.all handles missing addon gracefully."""
    server = get_server()
    result = await server.execute("release.all", {
        "addon": "NonExistentAddon12345",
        "version": "1.0.0",
        "message": "Test release"
    })

    assert not result.success
    assert result.error is not None


# ═══════════════════════════════════════════════════════════════════════════════
# Documentation Commands (docs.*)
# ═══════════════════════════════════════════════════════════════════════════════

@pytest.mark.asyncio
async def test_docs_generate():
    """Test docs.generate creates documentation."""
    server = get_server()
    result = await server.execute("docs.generate", {"format": "markdown"})

    data = assert_success(result)
    assert_has_reasoning(result)


@pytest.mark.asyncio
async def test_docs_generate_json():
    """Test docs.generate with JSON format."""
    server = get_server()
    result = await server.execute("docs.generate", {"format": "json"})

    data = assert_success(result)


@pytest.mark.asyncio
async def test_docs_generate_uses_shell_safe_payload_examples(tmp_path):
    """Generated docs distinguish Bash and PowerShell payload forms."""
    server = get_server()
    output_path = tmp_path / "cli-reference.md"

    result = await server.execute(
        "docs.generate",
        {"format": "markdown", "output_path": str(output_path)},
    )

    assert_success(result)
    text = output_path.read_text(encoding="utf-8")
    from mechanic.commands.atlas import DEFAULT_WOW_UI_SOURCE

    private_fallback = str(DEFAULT_WOW_UI_SOURCE).replace("\\", "/")

    assert "```powershell" in text
    assert 'mech call <command> \'{\\"param\\": \\"value\\"}\'' in text
    assert "mech call <command> '@payload.json'" in text
    assert "Payload (`payload.json`):" in text
    assert '"code": [' in text
    assert '"labels": [' in text
    assert "mech call lua.queue '@payload.json'" in text
    assert "second `/reload` or game exit/logout writes results to SavedVariables on disk" in text
    assert "mech call atlas.scan '{}'" in text
    assert "C:/path/to/wow-ui-source" in text
    assert private_fallback not in text
    assert 'mech call atlas.search \'{"query": "<query>"}\'' in text
    assert 'mech call lua.queue \'{"code": "<code>"}\'' not in text


# ═══════════════════════════════════════════════════════════════════════════════
# Environment Commands (env.*, tools.*, system.*)
# ═══════════════════════════════════════════════════════════════════════════════

@pytest.mark.asyncio
async def test_env_status():
    """Test env.status returns environment configuration."""
    server = get_server()
    result = await server.execute("env.status", {})

    data = assert_success(result)
    assert_has_reasoning(result)


@pytest.mark.asyncio
async def test_tools_status():
    """Test tools.status returns installed tools info."""
    server = get_server()
    result = await server.execute("tools.status", {})

    data = assert_success(result)
    assert_has_reasoning(result)


@pytest.mark.asyncio
async def test_system_pick_file():
    """Test system.pick_file command exists (may not work headless)."""
    server = get_server()
    # This command opens a file picker, so it may fail in headless mode
    # Just verify the command is registered
    commands = server.list_commands()
    command_names = [c.name for c in commands]
    assert "system.pick_file" in command_names


# ═══════════════════════════════════════════════════════════════════════════════
# Dashboard Commands (dashboard.*)
# ═══════════════════════════════════════════════════════════════════════════════

@pytest.mark.asyncio
async def test_dashboard_metrics():
    """Test dashboard.metrics returns reload and test history."""
    server = get_server()
    result = await server.execute("dashboard.metrics", {})

    data = assert_success(result)
    assert_has_reasoning(result)


# ═══════════════════════════════════════════════════════════════════════════════
# Server Commands (server.*)
# ═══════════════════════════════════════════════════════════════════════════════

@pytest.mark.asyncio
async def test_server_shutdown():
    """Test server.shutdown returns proper response.

    Note: This actually triggers shutdown after 500ms delay,
    so we only verify the immediate response.
    """
    server = get_server()
    result = await server.execute("server.shutdown", {})

    data = assert_success(result)
    assert data.status == "shutting_down"


# ═══════════════════════════════════════════════════════════════════════════════
# Command Registration Tests
# ═══════════════════════════════════════════════════════════════════════════════

# ═══════════════════════════════════════════════════════════════════════════════
# Research Commands (research.*)
# ═══════════════════════════════════════════════════════════════════════════════

@pytest.mark.asyncio
async def test_research_query_missing_api_key():
    """Test research.query handles missing API key gracefully."""
    server = get_server()
    # Temporarily clear the API key if set
    original_key = os.environ.pop("GEMINI_API_KEY", None)
    try:
        result = await server.execute("research.query", {"query": "test query"})
        assert_error(result, "API_KEY_MISSING")
        assert "GEMINI_API_KEY" in result.error.message
    finally:
        if original_key:
            os.environ["GEMINI_API_KEY"] = original_key


# ═══════════════════════════════════════════════════════════════════════════════
# Asset Commands (assets.*)
# ═══════════════════════════════════════════════════════════════════════════════

@pytest.mark.asyncio
async def test_assets_list():
    """Test assets.list returns asset info."""
    server = get_server()
    result = await server.execute("assets.list", {"addon": "!Mechanic"})

    # May succeed with empty results or fail if addon not found
    if result.success:
        data = assert_success(result)
        assert hasattr(data, 'source_count')
        assert hasattr(data, 'target_count')


@pytest.mark.asyncio
async def test_assets_sync_missing_addon():
    """Test assets.sync handles missing addon gracefully."""
    server = get_server()
    result = await server.execute("assets.sync", {"addon": "NonExistentAddon12345"})

    assert not result.success
    assert result.error is not None


# ═══════════════════════════════════════════════════════════════════════════════
# Performance Commands (perf.*)
# ═══════════════════════════════════════════════════════════════════════════════

@pytest.mark.asyncio
async def test_perf_list():
    """Test perf.list returns list of addons with baselines."""
    server = get_server()
    result = await server.execute("perf.list", {})

    data = assert_success(result)
    assert hasattr(data, 'addons')
    assert hasattr(data, 'count')
    assert isinstance(data.addons, list)


@pytest.mark.asyncio
async def test_perf_baseline():
    """Test perf.baseline records a measurement."""
    server = get_server()
    result = await server.execute("perf.baseline", {
        "addon": "TestAddon",
        "version": "1.0.0",
        "memory_kb": 100.5,
        "cpu_ms": 1.5
    })

    data = assert_success(result)
    assert data.addon == "TestAddon"
    assert data.version == "1.0.0"
    assert data.memory_kb == 100.5


@pytest.mark.asyncio
async def test_perf_compare_no_baseline():
    """Test perf.compare handles missing baseline gracefully."""
    server = get_server()
    result = await server.execute("perf.compare", {
        "addon": "NonExistentAddon12345",
        "memory_kb": 100.0,
        "cpu_ms": 1.0
    })

    # Should succeed with "no baseline" message
    data = assert_success(result)
    assert not data.has_regression


@pytest.mark.asyncio
async def test_perf_report_no_history():
    """Test perf.report handles missing history gracefully."""
    server = get_server()
    result = await server.execute("perf.report", {"addon": "NonExistentAddon12345"})

    data = assert_success(result)
    assert len(data.history) == 0


# ═══════════════════════════════════════════════════════════════════════════════
# API Definition Commands (api.populate, api.generate, api.refresh)
# ═══════════════════════════════════════════════════════════════════════════════

@pytest.mark.asyncio
async def test_api_generate_missing_database():
    """Test api.generate handles missing database gracefully."""
    server = get_server()
    result = await server.execute("api.generate", {"database_path": "/nonexistent/path.json"})

    assert_error(result, "DATABASE_NOT_FOUND")


@pytest.mark.asyncio
async def test_api_populate_missing_source():
    """Test api.populate handles missing source path gracefully."""
    server = get_server()
    result = await server.execute("api.populate", {"source_path": "/nonexistent/wow-ui-source"})

    assert_error(result, "SOURCE_NOT_FOUND")


# ═══════════════════════════════════════════════════════════════════════════════
# Atlas Commands (atlas.scan, atlas.search)
# ═══════════════════════════════════════════════════════════════════════════════

@pytest.mark.asyncio
async def test_atlas_scan_missing_source():
    """Test atlas.scan handles missing source path gracefully."""
    server = get_server()
    result = await server.execute("atlas.scan", {"source_path": "/nonexistent/wow-ui-source"})

    assert_error(result, "SOURCE_NOT_FOUND")


@pytest.mark.asyncio
async def test_atlas_scan_without_source_reports_discovery_hint():
    """atlas.scan {} returns an actionable error when no source can be found."""
    server = get_server()

    with patch("mechanic.commands.atlas._get_wow_ui_source_candidates", return_value=[]):
        result = await server.execute("atlas.scan", {})

    err = assert_error(result, "SOURCE_NOT_DISCOVERED")
    assert err.code != "COMMAND_EXECUTION_ERROR"
    assert "mech call atlas.scan" in err.suggestion
    assert "source_path" in err.suggestion
    assert "MECHANIC_WOW_UI_SOURCE" in err.suggestion
    assert "C:/path/to/wow-ui-source" in err.suggestion
    from mechanic.commands.atlas import DEFAULT_WOW_UI_SOURCE

    assert str(DEFAULT_WOW_UI_SOURCE).replace("\\", "/") not in err.suggestion


@pytest.mark.asyncio
async def test_atlas_scan_without_source_uses_discovered_candidate(tmp_path):
    """atlas.scan {} can use an auto-discovered valid wow-ui-source tree."""
    source_root = tmp_path / "wow-ui-source"
    blizzard_path = source_root / "Interface" / "AddOns" / "Blizzard_ActionBar"
    blizzard_path.mkdir(parents=True)
    (blizzard_path / "Test.lua").write_text(
        'frame:SetAtlas("UI-Discovered-Atlas")',
        encoding="utf-8",
    )
    config = SimpleNamespace(data_dir=tmp_path, dev_path=None, wow_ui_source=None)

    server = get_server()
    with (
        patch(
            "mechanic.commands.atlas._get_wow_ui_source_candidates",
            return_value=[source_root],
        ),
        patch("mechanic.commands.atlas.get_config", return_value=config),
    ):
        result = await server.execute("atlas.scan", {})

    data = assert_success(result)
    assert data.atlas_count == 1
    assert Path(data.output_file).exists()


@pytest.mark.asyncio
async def test_atlas_scan_accepts_root_and_interface_addons_path(tmp_path):
    """Explicit wow-ui-source root and Interface/AddOns paths remain valid."""
    addons_path = tmp_path / "Interface" / "AddOns"
    blizzard_path = addons_path / "Blizzard_ActionBar"
    blizzard_path.mkdir(parents=True)
    (blizzard_path / "Test.xml").write_text(
        '<Texture atlas="UI-Test-Atlas" />',
        encoding="utf-8",
    )
    output_path = tmp_path / "atlas_index.json"

    server = get_server()
    root_result = await server.execute(
        "atlas.scan",
        {"source_path": str(tmp_path), "output_path": str(tmp_path / "root_index.json")},
    )
    root_data = assert_success(root_result)
    assert root_data.atlas_count == 1

    result = await server.execute(
        "atlas.scan",
        {"source_path": str(addons_path), "output_path": str(output_path)},
    )

    data = assert_success(result)
    assert data.atlas_count == 1
    assert output_path.exists()


@pytest.mark.asyncio
async def test_atlas_search_no_index():
    """Test atlas.search handles missing index gracefully."""
    server = get_server()
    with patch("mechanic.commands.atlas._find_atlas_index", return_value=None):
        result = await server.execute("atlas.search", {"query": "sword"})

    err = assert_error(result, "INDEX_NOT_FOUND")
    assert "mech call atlas.scan" in err.suggestion
    assert "source_path" in err.suggestion
    assert "C:/path/to/wow-ui-source" in err.suggestion
    from mechanic.commands.atlas import DEFAULT_WOW_UI_SOURCE

    assert str(DEFAULT_WOW_UI_SOURCE).replace("\\", "/") not in err.suggestion


def test_mcp_atlas_examples_match_current_schema():
    """MCP examples use current atlas field names."""
    from mechanic.mcp_server import TOOL_EXAMPLES

    assert TOOL_EXAMPLES["atlas.scan"] == "{}"
    assert '"query"' in TOOL_EXAMPLES["atlas.search"]
    assert '"pattern"' not in TOOL_EXAMPLES["atlas.search"]


def test_all_commands_registered():
    """Test all 50 expected commands are registered."""
    server = get_server()
    commands = server.list_commands()
    command_names = [c.name for c in commands]

    expected_commands = [
        # sv.*
        "sv.parse", "sv.discover",
        # addon.*
        "addon.output", "addon.validate", "addon.lint", "addon.format",
        "addon.test", "addon.deprecations", "addon.create", "addon.sync",
        # libs.*
        "libs.check", "libs.init", "libs.sync",
        # api.*
        "api.search", "api.info", "api.list", "api.queue", "api.stats",
        "api.populate", "api.generate", "api.refresh",
        # lua.*
        "lua.queue", "lua.results",
        # sandbox.*
        "sandbox.generate", "sandbox.status", "sandbox.exec", "sandbox.test",
        # locale.*
        "locale.validate", "locale.extract",
        # atlas.*
        "atlas.scan", "atlas.search",
        # release pipeline (git.commit, git.tag, release.all removed - subprocess hangs in MCP)
        "version.bump", "changelog.add",
        # docs.*
        "docs.generate",
        # environment
        "env.status", "tools.status", "system.pick_file",
        # dashboard
        "dashboard.metrics",
        # server
        "server.shutdown",
        # research.*
        "research.query",
        # assets.*
        "assets.sync", "assets.list",
        # perf.*
        "perf.baseline", "perf.compare", "perf.list", "perf.report",
    ]

    for cmd in expected_commands:
        assert cmd in command_names, f"Missing command: {cmd}"


def test_commands_have_descriptions():
    """Test all commands have descriptions (required for MCP)."""
    server = get_server()
    commands = server.list_commands()

    for cmd in commands:
        assert cmd.description, f"Command {cmd.name} missing description"
        assert len(cmd.description) > 10, f"Command {cmd.name} description too short"
