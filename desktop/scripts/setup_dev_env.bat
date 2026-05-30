@echo off
setlocal EnableExtensions

echo ==========================================
echo   Mechanic Developer Environment Setup
echo ==========================================
echo.
echo This script prepares the Windows Lua/Busted toolchain used by
echo "mech call addon.test" and "mech setup-busted".
echo.

REM 1. Find an x86 Visual Studio C++ toolchain.
echo [1/4] Finding Visual Studio Build Tools x86 environment...
set "VCVARS="
set "VSWHERE=%ProgramFiles(x86)%\Microsoft Visual Studio\Installer\vswhere.exe"

if exist "%VSWHERE%" (
    for /f "usebackq tokens=*" %%i in (`"%VSWHERE%" -latest -products * -requires Microsoft.VisualStudio.Component.VC.Tools.x86.x64 -find VC\Auxiliary\Build\vcvars32.bat`) do (
        if not defined VCVARS set "VCVARS=%%i"
    )
)

if not defined VCVARS (
    for %%P in (
        "C:\Program Files (x86)\Microsoft Visual Studio\18\BuildTools"
        "C:\Program Files (x86)\Microsoft Visual Studio\18\Community"
        "C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools"
        "C:\Program Files (x86)\Microsoft Visual Studio\2022\Community"
        "C:\Program Files (x86)\Microsoft Visual Studio\2019\BuildTools"
        "C:\Program Files (x86)\Microsoft Visual Studio\2019\Community"
    ) do (
        if not defined VCVARS if exist "%%~P\VC\Auxiliary\Build\vcvars32.bat" set "VCVARS=%%~P\VC\Auxiliary\Build\vcvars32.bat"
    )
)

if not defined VCVARS (
    echo [ERROR] Could not find vcvars32.bat.
    echo Install "Visual Studio Build Tools" with "Desktop development with C++".
    echo The x86 toolchain is required because the recommended LuaRocks bundle
    echo installs a 32-bit Lua 5.1 runtime.
    exit /b 1
)

echo Found: %VCVARS%
call "%VCVARS%" >NUL
echo Environment initialized.

REM 2. Verify LuaRocks.
echo.
echo [2/4] Checking LuaRocks...
where luarocks >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] 'luarocks' was not found in PATH.
    echo.
    echo Recommended install from a Visual Studio x86 command prompt:
    echo   cd C:\luarocks-3.13.0-win32
    echo   install.bat /P "%%LOCALAPPDATA%%\LuaRocks51" /SELFCONTAINED /L /NOADMIN /NOREG /Q /MSVC
    echo   set PATH=%%LOCALAPPDATA%%\LuaRocks51;%%PATH%%
    exit /b 1
)

luarocks --version

REM 3. Configure LuaRocks for MSVC and a predictable user rock tree.
echo.
echo [3/4] Configuring LuaRocks...
set "ROCKTREE=%APPDATA%\luarocks"

luarocks --lua-version=5.1 config variables.CC cl
luarocks --lua-version=5.1 config variables.LD link
luarocks --lua-version=5.1 config variables.MAKE nmake

REM 4. Install Busted and native dependencies.
echo.
echo [4/4] Installing Busted 2.2.0-1 into %ROCKTREE%...
luarocks --lua-version=5.1 --tree "%ROCKTREE%" install busted 2.2.0-1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Failed to install Busted.
    echo Ensure the Visual Studio x86 environment was initialized and try again.
    exit /b 1
)

echo.
echo ==========================================
echo   SUCCESS
echo.
echo Next steps:
echo   set LUAROCKS_HOME=%ROCKTREE%
echo   mech setup-busted
echo   .\bin\busted.bat --version
echo ==========================================
