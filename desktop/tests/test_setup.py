"""
Setup tests for Mechanic Desktop.

These cover Windows tool installation edge cases without touching the real
desktop/bin folder or downloading from the network.
"""

import hashlib
import io
import zipfile

from mechanic import setup


def _zip_bytes(entries):
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as zf:
        for name, content in entries.items():
            zf.writestr(name, content)
    return buffer.getvalue()


def test_download_tool_windows_extracts_archive_without_zip_url(monkeypatch, tmp_path):
    """Archive extraction should depend on archive_path, not URL suffix."""
    archive = _zip_bytes(
        {
            "nested/tool.exe": b"primary-binary",
            "nested/tool.dll": b"extra-binary",
        }
    )
    expected_hash = hashlib.sha256(b"primary-binary").hexdigest()

    monkeypatch.setattr(setup, "BIN_DIR", tmp_path)
    monkeypatch.setattr(setup, "download_file", lambda _url: archive)

    success, message = setup.download_tool_windows(
        "tool",
        {
            "version": "1.0",
            "windows": {
                "url": "https://example.invalid/tool/download",
                "filename": "tool.exe",
                "archive_path": "tool.exe",
                "extra_files": ["tool.dll"],
                "sha256": expected_hash,
            },
        },
    )

    assert success, message
    assert (tmp_path / "tool.exe").read_bytes() == b"primary-binary"
    assert (tmp_path / "tool.dll").read_bytes() == b"extra-binary"


def test_download_tool_windows_manual_tool_does_not_download(monkeypatch):
    """Manual tools such as busted should not try to download a null URL."""
    monkeypatch.setattr(setup, "find_tool", lambda _name: None)

    success, message = setup.download_tool_windows(
        "busted",
        {
            "windows": {
                "url": None,
                "filename": "busted.bat",
                "message": "Manual install required: luarocks install busted",
            }
        },
    )

    assert not success
    assert "Manual install required" in message


def test_setup_verify_requires_tools_to_execute(monkeypatch, tmp_path):
    """A stale busted.bat should not be reported installed just because it exists."""
    fake_tool = tmp_path / "busted.bat"
    fake_tool.write_text("@echo off\nexit /b 1\n", encoding="utf-8")

    monkeypatch.setattr(setup, "get_platform", lambda: "windows")
    monkeypatch.setattr(setup, "load_checksums", lambda: {
        "tools": {
            "busted": {
                "required": False,
                "windows": {"filename": "busted.bat", "url": None},
            }
        }
    })
    monkeypatch.setattr(setup, "find_tool", lambda _name: fake_tool)
    monkeypatch.setattr(setup, "probe_tool", lambda _path, _name: (False, None, "bad path"))

    results = setup.setup_tools(verify_only=True)

    assert results[0]["name"] == "busted"
    assert results[0]["installed"] is False
    assert "bad path" in results[0]["message"]


def test_find_tool_accepts_lua51_executable(monkeypatch, tmp_path):
    """Windows Lua 5.1 installs often expose lua5.1.exe instead of lua.exe."""
    lua51 = tmp_path / "lua5.1.exe"
    lua51.write_text("", encoding="utf-8")

    monkeypatch.setattr(setup.sys, "platform", "win32")
    monkeypatch.setattr(setup, "BIN_DIR", tmp_path)

    assert setup.find_tool("lua") == lua51


def test_generate_busted_bat_uses_discovered_version(monkeypatch, tmp_path):
    """The generated wrapper should not hard-code a user path or busted version."""
    lua_path = tmp_path / "lua.exe"
    lua_path.write_text("", encoding="utf-8")
    output_path = tmp_path / "busted.bat"

    monkeypatch.setattr(setup, "get_platform", lambda: "windows")
    monkeypatch.setattr(setup, "find_tool", lambda _name: lua_path)
    monkeypatch.setattr(setup, "find_luarocks_paths", lambda: {
        "luarocks_home": tmp_path / "rocks",
        "share_path": tmp_path / "rocks" / "share" / "lua" / "5.1",
        "lib_path": tmp_path / "rocks" / "lib" / "lua" / "5.1",
        "busted_bin": tmp_path / "rocks" / "lib" / "luarocks" / "rocks-5.1" / "busted" / "2.3.0-1" / "bin" / "busted",
        "busted_version": "2.3.0-1",
    })

    success, message = setup.generate_busted_bat(output_path)

    assert success, message
    content = output_path.read_text(encoding="utf-8")
    assert "2.3.0-1" in content
    assert "C:\\Program Files\\luarocks" not in content
