# CLI Reference

> Auto-generated from `mechanic-desktop` v0.1.0 on 2026-06-01

This document lists all available Mechanic CLI commands with their inputs and outputs.

## Quick Reference

| Command | Description |
|---------|-------------|
| `dashboard.metrics` | Get the latest reload and test metrics from the local histor... |
| `server.shutdown` | Gracefully shut down the Mechanic Desktop server |
| `sv.discover` | Automatically discover SavedVariables paths for all WoW flav... |
| `sv.parse` | Parse a WoW SavedVariables file and extract !Mechanic data |
| `addon.complexity` | Detect code complexity issues in a WoW addon (nesting, long ... |
| `addon.create` | Create a new WoW addon from a template |
| `addon.deadcode` | Detect dead code in a WoW addon (unused functions, orphaned ... |
| `addon.deprecations` | Scan a WoW addon for deprecated API calls (100+ APIs, 11.0-1... |
| `addon.format` | Run StyLua formatter on a WoW addon |
| `addon.lint` | Run Luacheck linter on a WoW addon |
| `addon.output` | Get all addon output (errors, tests, console) for agent cons... |
| `addon.security` | Detect security issues in a WoW addon (combat lockdown, secr... |
| `addon.sync` | Create junction links from development addon to WoW client f... |
| `addon.test` | Run Busted unit tests on a WoW addon |
| `addon.validate` | Validate a WoW addon's .toc file for common issues |
| `changelog.add` | Add an entry to the addon's CHANGELOG.md |
| `version.bump` | Update the version in a WoW addon's .toc file |
| `atlas.scan` | Scan wow-ui-source for atlas icons and generate searchable i... |
| `atlas.search` | Search Blizzard UI atlas icons by name pattern (supports wil... |
| `locale.extract` | Extract potential localizable strings from addon code |
| `locale.validate` | Validate locale coverage against the enUS baseline |
| `libs.check` | Check addon library status against libs.json config |
| `libs.init` | Creates a libs.json config file from currently installed lib... |
| `libs.sync` | Sync addon libraries based on libs.json config |
| `tools.status` | Check the status of development tools (luacheck, stylua, etc... |
| `docs.generate` | Generate CLI reference documentation from registered command... |
| `docs.stale` | Detect stale or broken documentation in a WoW addon |
| `api.download` | Download FrameXML from Townlong Yak and optionally refresh A... |
| `api.generate` | Generate APIDefs Lua files from api_database.json for Mechan... |
| `api.info` | Get detailed information about a specific WoW API |
| `api.list` | List APIs by namespace or category |
| `api.populate` | Parse Blizzard API documentation and generate api_database.j... |
| `api.queue` | Queue API tests for in-game execution. After running this, /... |
| `api.refresh` | Full refresh: parse Blizzard docs and regenerate all APIDefs... |
| `api.search` | Search WoW APIs by name pattern. Works offline (reads static... |
| `api.stats` | Get statistics about available WoW APIs |
| `assets.list` | List asset files in an addon's assets_source and assets fold... |
| `assets.sync` | Sync addon assets: convert PNG to TGA and copy other files f... |
| `env.status` | Get Mechanic environment configuration and runtime installat... |
| `fencore-catalog` | Get full catalog of FenCore logic domains and functions |
| `fencore-info` | Get detailed info about a specific FenCore function |
| `fencore-search` | Search FenCore functions by name or description |
| `lua.queue` | Queue Lua snippets. First /reload executes them; second /rel... |
| `lua.results` | Read Lua eval results already persisted to SavedVariables |
| `perf.baseline` | Record a performance baseline measurement for an addon |
| `perf.compare` | Compare current performance against baseline and detect regr... |
| `perf.list` | List all addons with performance baselines |
| `perf.report` | Generate a performance report showing history and trends |
| `research.query` | Search the web for addon development information using Gemin... |
| `sandbox.exec` | Execute Lua code in sandbox environment with WoW API stubs |
| `sandbox.generate` | Generate WoW API stubs from APIDefs database for sandbox tes... |
| `sandbox.status` | Get status of generated WoW API stubs |
| `sandbox.test` | Run Busted tests for an addon's Core layer with WoW API stub... |
| `system.pick_file` | Open a native file picker dialog to select a file |

---

## Core Commands

### `dashboard.metrics`

Get the latest reload and test metrics from the local history

**Parameters:** None

**Example:**

```bash
mech call dashboard.metrics
```

---

### `server.shutdown`

Gracefully shut down the Mechanic Desktop server

**Parameters:** None

**Example:**

```bash
mech call server.shutdown
```

---

### `sv.discover`

Automatically discover SavedVariables paths for all WoW flavors

**Parameters:** None

**Example:**

```bash
mech call sv.discover
```

---

### `sv.parse`

Parse a WoW SavedVariables file and extract !Mechanic data

**Parameters:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `file_path` | `string` | Yes | Absolute path to the !Mechanic.lua file |

**Example:**

Bash/Zsh:

```bash
mech call sv.parse '{"file_path": "<file_path>"}'
```

PowerShell:

```powershell
mech call sv.parse '{\"file_path\": \"<file_path>\"}'
```

---

## Development Commands

### `addon.complexity`

Detect code complexity issues in a WoW addon (nesting, long functions, magic numbers)

**Parameters:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `addon` | `string` | Yes | Name of the addon to analyze |
| `path` | `string` | No (default: `None`) | Override path to addon folder |
| `categories` | `string` | No (default: `None`) | Specific categories to check (default: all) |
| `max_nesting` | `number` | No (default: `5`) | Maximum allowed nesting depth |
| `max_function_lines` | `number` | No (default: `100`) | Maximum lines per function |
| `max_file_lines` | `number` | No (default: `500`) | Maximum lines per file |

**Example:**

Bash/Zsh:

```bash
mech call addon.complexity '{"addon": "<addon>"}'
```

PowerShell:

```powershell
mech call addon.complexity '{\"addon\": \"<addon>\"}'
```

---

### `addon.create`

Create a new WoW addon from a template

**Parameters:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | `string` | Yes | Name for the new addon |
| `template` | `string` | No (default: `None`) | Template to use (defaults to _TemplateAddon) |
| `author` | `string` | No (default: `None`) | Author name for metadata |

**Example:**

Bash/Zsh:

```bash
mech call addon.create '{"name": "<name>"}'
```

PowerShell:

```powershell
mech call addon.create '{\"name\": \"<name>\"}'
```

---

### `addon.deadcode`

Detect dead code in a WoW addon (unused functions, orphaned files, etc.)

**Parameters:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `addon` | `string` | Yes | Name of the addon to analyze |
| `path` | `string` | No (default: `None`) | Override path to addon folder |
| `categories` | `string` | No (default: `None`) | Specific categories to check (default: all) |
| `include_suspicious` | `boolean` | No (default: `True`) | Include lower-confidence findings |

**Example:**

Bash/Zsh:

```bash
mech call addon.deadcode '{"addon": "<addon>"}'
```

PowerShell:

```powershell
mech call addon.deadcode '{\"addon\": \"<addon>\"}'
```

---

### `addon.deprecations`

Scan a WoW addon for deprecated API calls (100+ APIs, 11.0-12.0)

**Parameters:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `addon` | `string` | Yes | Name of the addon to scan |
| `path` | `string` | No (default: `None`) | Override path to addon folder |
| `fix` | `boolean` | No (default: `False`) | Attempt to auto-fix deprecated calls |
| `category` | `string` | No (default: `None`) | Filter by category (e.g., spells, items, containers) |
| `min_severity` | `string` | No (default: `'warning'`) | Minimum severity: info, warning, or error |

**Example:**

Bash/Zsh:

```bash
mech call addon.deprecations '{"addon": "<addon>"}'
```

PowerShell:

```powershell
mech call addon.deprecations '{\"addon\": \"<addon>\"}'
```

---

### `addon.format`

Run StyLua formatter on a WoW addon

**Parameters:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `addon` | `string` | Yes | Name of the addon to format |
| `path` | `string` | No (default: `None`) | Override path to addon folder |
| `check` | `boolean` | No (default: `False`) | Only check formatting, don't modify files |

**Example:**

Bash/Zsh:

```bash
mech call addon.format '{"addon": "<addon>"}'
```

PowerShell:

```powershell
mech call addon.format '{\"addon\": \"<addon>\"}'
```

---

### `addon.lint`

Run Luacheck linter on a WoW addon

**Parameters:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `addon` | `string` | Yes | Name of the addon to lint |
| `path` | `string` | No (default: `None`) | Override path to addon folder |
| `fix` | `boolean` | No (default: `False`) | Not applicable for Luacheck (read-only) |

**Example:**

Bash/Zsh:

```bash
mech call addon.lint '{"addon": "<addon>"}'
```

PowerShell:

```powershell
mech call addon.lint '{\"addon\": \"<addon>\"}'
```

---

### `addon.output`

Get all addon output (errors, tests, console) for agent consumption. Use agent_mode=true for compressed output.

**Parameters:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `agent_mode` | `boolean` | No (default: `False`) | Enable smart compression for AI agents |

**Example:**

```bash
mech call addon.output
```

---

### `addon.security`

Detect security issues in a WoW addon (combat lockdown, secret values, taint)

**Parameters:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `addon` | `string` | Yes | Name of the addon to analyze |
| `path` | `string` | No (default: `None`) | Override path to addon folder |
| `categories` | `string` | No (default: `None`) | Specific categories to check (default: all) |
| `include_suspicious` | `boolean` | No (default: `True`) | Include lower-confidence findings |

**Example:**

Bash/Zsh:

```bash
mech call addon.security '{"addon": "<addon>"}'
```

PowerShell:

```powershell
mech call addon.security '{\"addon\": \"<addon>\"}'
```

---

### `addon.sync`

Create junction links from development addon to WoW client folders. For !Mechanic or Mechanic, syncs both runtime addons.

**Parameters:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `addon` | `string` | Yes | Name of the addon to sync |
| `flavors` | `string` | No (default: `None`) | WoW flavors to sync to (defaults to all) |

**Example:**

Bash/Zsh:

```bash
mech call addon.sync '{"addon": "<addon>"}'
```

PowerShell:

```powershell
mech call addon.sync '{\"addon\": \"<addon>\"}'
```

---

### `addon.test`

Run Busted unit tests on a WoW addon

**Parameters:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `addon` | `string` | Yes | Name of the addon to test |
| `path` | `string` | No (default: `None`) | Override path to addon folder |
| `coverage` | `boolean` | No (default: `False`) | Generate code coverage report |

**Example:**

Bash/Zsh:

```bash
mech call addon.test '{"addon": "<addon>"}'
```

PowerShell:

```powershell
mech call addon.test '{\"addon\": \"<addon>\"}'
```

---

### `addon.validate`

Validate a WoW addon's .toc file for common issues

**Parameters:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `addon` | `string` | Yes | Name of the addon to operate on |
| `path` | `string` | No (default: `None`) | Override path to addon folder |

**Example:**

Bash/Zsh:

```bash
mech call addon.validate '{"addon": "<addon>"}'
```

PowerShell:

```powershell
mech call addon.validate '{\"addon\": \"<addon>\"}'
```

---

## Release Commands

### `changelog.add`

Add an entry to the addon's CHANGELOG.md

**Parameters:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `addon` | `string` | Yes | Name of the addon |
| `version` | `string` | Yes | Version for the changelog entry |
| `message` | `string` | Yes | Change description |
| `category` | `string` | No (default: `'Changed'`) | Category: Added, Changed, Fixed, Removed |
| `path` | `string` | No (default: `None`) | Override path to addon folder |

**Example:**

Bash/Zsh:

```bash
mech call changelog.add '{"addon": "<addon>", "version": "<version>", "message": "<message>"}'
```

PowerShell:

```powershell
mech call changelog.add '{\"addon\": \"<addon>\", \"version\": \"<version>\", \"message\": \"<message>\"}'
```

---

### `version.bump`

Update the version in a WoW addon's .toc file

**Parameters:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `addon` | `string` | Yes | Name of the addon |
| `version` | `string` | Yes | New version string (e.g., '1.2.0') |
| `path` | `string` | No (default: `None`) | Override path to addon folder |

**Example:**

Bash/Zsh:

```bash
mech call version.bump '{"addon": "<addon>", "version": "<version>"}'
```

PowerShell:

```powershell
mech call version.bump '{\"addon\": \"<addon>\", \"version\": \"<version>\"}'
```

---

## Localization Commands

### `atlas.scan`

Scan wow-ui-source for atlas icons and generate searchable index

**Parameters:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `source_path` | `string` | No (default: `None`) | Optional path to wow-ui-source repository root or Interface/AddOns. If omitted, Mechanic tries MECHANIC_WOW_UI_SOURCE, config wow_ui_source, and common local source paths. |
| `output_path` | `string` | No (default: `None`) | Output path for atlas_index.json (defaults to data_dir) |

**Example:**

Auto-discover:

```bash
mech call atlas.scan '{}'
```

Explicit source path:

```bash
mech call atlas.scan '{"source_path": "C:/path/to/wow-ui-source"}'
```

PowerShell:

```powershell
mech call atlas.scan '{}'
mech call atlas.scan '{\"source_path\": \"C:/path/to/wow-ui-source\"}'
```

---

### `atlas.search`

Search Blizzard UI atlas icons by name pattern (supports wildcards)

**Parameters:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `query` | `string` | Yes | Search query for atlas icons (supports * wildcards) |
| `limit` | `number` | No (default: `20`) | Maximum results to return |
| `include_files` | `boolean` | No (default: `False`) | Include source file paths in results |

**Example:**

Bash/Zsh:

```bash
mech call atlas.search '{"query": "<query>"}'
```

PowerShell:

```powershell
mech call atlas.search '{\"query\": \"<query>\"}'
```

---

### `locale.extract`

Extract potential localizable strings from addon code

**Parameters:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `addon` | `string` | Yes | Name of the addon |
| `path` | `string` | No (default: `None`) | Override path to addon folder |

**Example:**

Bash/Zsh:

```bash
mech call locale.extract '{"addon": "<addon>"}'
```

PowerShell:

```powershell
mech call locale.extract '{\"addon\": \"<addon>\"}'
```

---

### `locale.validate`

Validate locale coverage against the enUS baseline

**Parameters:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `addon` | `string` | Yes | Name of the addon to validate |
| `path` | `string` | No (default: `None`) | Override path to addon folder |

**Example:**

Bash/Zsh:

```bash
mech call locale.validate '{"addon": "<addon>"}'
```

PowerShell:

```powershell
mech call locale.validate '{\"addon\": \"<addon>\"}'
```

---

## Environment Commands

### `libs.check`

Check addon library status against libs.json config

**Parameters:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `addon` | `string` | Yes | Name of the addon to check |

**Example:**

Bash/Zsh:

```bash
mech call libs.check '{"addon": "<addon>"}'
```

PowerShell:

```powershell
mech call libs.check '{\"addon\": \"<addon>\"}'
```

---

### `libs.init`

Creates a libs.json config file from currently installed libraries. ⚠️ Will NOT overwrite existing config unless overwrite=true is set.

**Parameters:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `addon` | `string` | Yes | Name of the addon |
| `mode` | `string` | No (default: `'include'`) | Config mode: 'include' (whitelist) or 'exclude' (blocklist) |
| `overwrite` | `boolean` | No (default: `False`) | Overwrite existing libs.json |

**Example:**

Bash/Zsh:

```bash
mech call libs.init '{"addon": "<addon>"}'
```

PowerShell:

```powershell
mech call libs.init '{\"addon\": \"<addon>\"}'
```

---

### `libs.sync`

Sync addon libraries based on libs.json config

**Parameters:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `addon` | `string` | Yes | Name of the addon to sync |
| `source` | `string` | No (default: `None`) | Source library path (defaults to ADDON_DEV Libs) |
| `dry_run` | `boolean` | No (default: `False`) | Preview changes without applying |
| `force` | `boolean` | No (default: `False`) | Force update existing libraries (replaces them) |
| `remove_extra` | `boolean` | No (default: `False`) | Remove libraries not in config |

**Example:**

Bash/Zsh:

```bash
mech call libs.sync '{"addon": "<addon>"}'
```

PowerShell:

```powershell
mech call libs.sync '{\"addon\": \"<addon>\"}'
```

---

## Tools Commands

### `tools.status`

Check the status of development tools (luacheck, stylua, etc.)

**Parameters:** None

**Example:**

```bash
mech call tools.status
```

---

## Documentation Commands

### `docs.generate`

Generate CLI reference documentation from registered commands

**Parameters:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `output_path` | `string` | No (default: `None`) | Output file path. Defaults to docs/cli-reference.md |
| `format` | `string` | No (default: `'markdown'`) | Output format: 'markdown' or 'json' |

**Example:**

```bash
mech call docs.generate
```

---

### `docs.stale`

Detect stale or broken documentation in a WoW addon

**Parameters:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `addon` | `string` | Yes | Name of the addon to analyze |
| `path` | `string` | No (default: `None`) | Override path to addon folder |
| `include_suspicious` | `boolean` | No (default: `True`) | Include lower-confidence findings |
| `commits_threshold` | `number` | No (default: `10`) | Flag docs not updated in this many commits |

**Example:**

Bash/Zsh:

```bash
mech call docs.stale '{"addon": "<addon>"}'
```

PowerShell:

```powershell
mech call docs.stale '{\"addon\": \"<addon>\"}'
```

---

## Other Commands

### `api.download`

Download FrameXML from Townlong Yak and optionally refresh API definitions

**Parameters:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `build_id` | `string` | No (default: `None`) | Specific build ID to download (e.g., '64889'). If not provided, fetches latest. |
| `output_path` | `string` | No (default: `None`) | Where to extract the download. Defaults to _dev_/framexml/{version} |
| `refresh` | `boolean` | No (default: `True`) | Run api.refresh after download |

**Example:**

```bash
mech call api.download
```

---

### `api.generate`

Generate APIDefs Lua files from api_database.json for Mechanic

**Parameters:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `database_path` | `string` | No (default: `None`) | Path to api_database.json (defaults to data_dir) |
| `output_path` | `string` | No (default: `None`) | Output path for APIDefs (defaults to Mechanic/UI/APIDefs) |

**Example:**

```bash
mech call api.generate
```

---

### `api.info`

Get detailed information about a specific WoW API

**Parameters:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `api_name` | `string` | Yes | Full API name (e.g., C_Spell.GetSpellInfo) |

**Example:**

Bash/Zsh:

```bash
mech call api.info '{"api_name": "<api_name>"}'
```

PowerShell:

```powershell
mech call api.info '{\"api_name\": \"<api_name>\"}'
```

---

### `api.list`

List APIs by namespace or category

**Parameters:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `namespace` | `string` | No (default: `None`) | Namespace to list (e.g., C_Spell) |
| `category` | `string` | No (default: `None`) | Category to list |
| `limit` | `number` | No (default: `50`) | Max results |

**Example:**

```bash
mech call api.list
```

---

### `api.populate`

Parse Blizzard API documentation and generate api_database.json

**Parameters:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `source_path` | `string` | Yes | Path to wow-ui-source repository root |
| `output_path` | `string` | No (default: `None`) | Output path for api_database.json (defaults to data_dir) |

**Example:**

Bash/Zsh:

```bash
mech call api.populate '{"source_path": "<source_path>"}'
```

PowerShell:

```powershell
mech call api.populate '{\"source_path\": \"<source_path>\"}'
```

---

### `api.queue`

Queue API tests for in-game execution. After running this, /reload in WoW to execute tests.

**Parameters:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `apis` | `array` | Yes | List of API names to queue for testing |
| `params` | `string` | No (default: `None`) | Optional parameters per API: {'C_Spell.GetSpellInfo': {'spellID': 8690}} |

**Example:**

Bash/Zsh:

```bash
mech call api.queue '{"apis": ["<apis>"]}'
```

PowerShell:

```powershell
mech call api.queue '{\"apis\": [\"<apis>\"]}'
```

---

### `api.refresh`

Full refresh: parse Blizzard docs and regenerate all APIDefs in one step

**Parameters:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `source_path` | `string` | Yes | Path to wow-ui-source repository root or Townlong Yak extract |

**Example:**

Bash/Zsh:

```bash
mech call api.refresh '{"source_path": "<source_path>"}'
```

PowerShell:

```powershell
mech call api.refresh '{\"source_path\": \"<source_path>\"}'
```

---

### `api.search`

Search WoW APIs by name pattern. Works offline (reads static definitions).

**Parameters:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `query` | `string` | Yes | Search pattern (supports * wildcards) |
| `category` | `string` | No (default: `None`) | Filter by category |
| `namespace` | `string` | No (default: `None`) | Filter by namespace |
| `limit` | `number` | No (default: `20`) | Max results to return |

**Example:**

Bash/Zsh:

```bash
mech call api.search '{"query": "<query>"}'
```

PowerShell:

```powershell
mech call api.search '{\"query\": \"<query>\"}'
```

---

### `api.stats`

Get statistics about available WoW APIs

**Parameters:** None

**Example:**

```bash
mech call api.stats
```

---

### `assets.list`

List asset files in an addon's assets_source and assets folders

**Parameters:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `addon` | `string` | Yes | Name of the addon |

**Example:**

Bash/Zsh:

```bash
mech call assets.list '{"addon": "<addon>"}'
```

PowerShell:

```powershell
mech call assets.list '{\"addon\": \"<addon>\"}'
```

---

### `assets.sync`

Sync addon assets: convert PNG to TGA and copy other files from assets_source to assets

**Parameters:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `addon` | `string` | Yes | Name of the addon to sync assets for |
| `verbose` | `boolean` | No (default: `False`) | Show detailed output |

**Example:**

Bash/Zsh:

```bash
mech call assets.sync '{"addon": "<addon>"}'
```

PowerShell:

```powershell
mech call assets.sync '{\"addon\": \"<addon>\"}'
```

---

### `env.status`

Get Mechanic environment configuration and runtime installation status

**Parameters:** None

**Example:**

```bash
mech call env.status
```

---

### `fencore-catalog`

Get full catalog of FenCore logic domains and functions

**Parameters:** None

**Example:**

```bash
mech call fencore-catalog
```

---

### `fencore-info`

Get detailed info about a specific FenCore function

**Parameters:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `domain` | `string` | Yes | Domain name (e.g., 'Math') |
| `function` | `string` | Yes | Function name (e.g., 'Clamp') |

**Example:**

Bash/Zsh:

```bash
mech call fencore-info '{"domain": "<domain>", "function": "<function>"}'
```

PowerShell:

```powershell
mech call fencore-info '{\"domain\": \"<domain>\", \"function\": \"<function>\"}'
```

---

### `fencore-search`

Search FenCore functions by name or description

**Parameters:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `query` | `string` | Yes | Search query (partial match on name or description) |
| `limit` | `number` | No (default: `20`) | Maximum results to return |

**Example:**

Bash/Zsh:

```bash
mech call fencore-search '{"query": "<query>"}'
```

PowerShell:

```powershell
mech call fencore-search '{\"query\": \"<query>\"}'
```

---

### `lua.queue`

Queue Lua snippets. First /reload executes them; second /reload or game exit persists results to SavedVariables for lua.results.

**Parameters:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `code` | `array` | Yes | List of Lua code snippets to execute. Each snippet should return a value. |
| `labels` | `array` | No (default: `None`) | Optional labels for each snippet (for easier identification in results) |

**Example:**

Payload (`payload.json`):

```json
{
  "code": [
    "<code>"
  ],
  "labels": [
    "<label>"
  ]
}
```

```bash
mech call lua.queue @payload.json
```

```powershell
mech call lua.queue '@payload.json'
```

Then in WoW: first `/reload` executes the queue; a second `/reload` or game exit/logout writes results to SavedVariables on disk for `mech call lua.results`.

---

### `lua.results`

Read Lua eval results already persisted to SavedVariables

**Parameters:** None

**Example:**

```bash
mech call lua.results
```

---

### `perf.baseline`

Record a performance baseline measurement for an addon

**Parameters:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `addon` | `string` | Yes | Name of the addon |
| `version` | `string` | Yes | Version being measured |
| `memory_kb` | `number` | Yes | Memory usage in KB |
| `cpu_ms` | `number` | Yes | CPU time in milliseconds |

**Example:**

Bash/Zsh:

```bash
mech call perf.baseline '{"addon": "<addon>", "version": "<version>", "memory_kb": "<memory_kb>", "cpu_ms": "<cpu_ms>"}'
```

PowerShell:

```powershell
mech call perf.baseline '{\"addon\": \"<addon>\", \"version\": \"<version>\", \"memory_kb\": \"<memory_kb>\", \"cpu_ms\": \"<cpu_ms>\"}'
```

---

### `perf.compare`

Compare current performance against baseline and detect regressions

**Parameters:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `addon` | `string` | Yes | Name of the addon |
| `memory_kb` | `number` | Yes | Current memory usage in KB |
| `cpu_ms` | `number` | Yes | Current CPU time in milliseconds |
| `memory_threshold` | `number` | No (default: `1.5`) | Memory increase factor that triggers warning |
| `cpu_threshold` | `number` | No (default: `2.0`) | CPU increase factor that triggers warning |

**Example:**

Bash/Zsh:

```bash
mech call perf.compare '{"addon": "<addon>", "memory_kb": "<memory_kb>", "cpu_ms": "<cpu_ms>"}'
```

PowerShell:

```powershell
mech call perf.compare '{\"addon\": \"<addon>\", \"memory_kb\": \"<memory_kb>\", \"cpu_ms\": \"<cpu_ms>\"}'
```

---

### `perf.list`

List all addons with performance baselines

**Parameters:** None

**Example:**

```bash
mech call perf.list
```

---

### `perf.report`

Generate a performance report showing history and trends

**Parameters:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `addon` | `string` | Yes | Name of the addon |
| `limit` | `number` | No (default: `10`) | Number of recent measurements to show |

**Example:**

Bash/Zsh:

```bash
mech call perf.report '{"addon": "<addon>"}'
```

PowerShell:

```powershell
mech call perf.report '{\"addon\": \"<addon>\"}'
```

---

### `research.query`

Search the web for addon development information using Gemini with Google Search grounding

**Parameters:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `query` | `string` | Yes | Search query or question |
| `mode` | `string` | No (default: `'fast'`) | Search mode: 'fast' (Gemini Flash, ~15-30s) or 'thinking' (Gemini Pro, ~30-90s) |
| `json_output` | `boolean` | No (default: `False`) | Request structured JSON response |

**Example:**

Bash/Zsh:

```bash
mech call research.query '{"query": "<query>"}'
```

PowerShell:

```powershell
mech call research.query '{\"query\": \"<query>\"}'
```

---

### `sandbox.exec`

Execute Lua code in sandbox environment with WoW API stubs

**Parameters:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `code` | `string` | Yes | Lua code to execute |
| `addon` | `string` | No (default: `None`) | Name of addon to load before execution (looks in _dev_ folder) |
| `load_stubs` | `boolean` | No (default: `True`) | Whether to load WoW API stubs |

**Example:**

Bash/Zsh:

```bash
mech call sandbox.exec '{"code": "<code>"}'
```

PowerShell:

```powershell
mech call sandbox.exec '{\"code\": \"<code>\"}'
```

---

### `sandbox.generate`

Generate WoW API stubs from APIDefs database for sandbox testing

**Parameters:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `namespace` | `string` | No (default: `None`) | Specific namespace to generate (e.g., 'C_Spell'). If not provided, generates all. |
| `force` | `boolean` | No (default: `False`) | Regenerate even if stubs exist |

**Example:**

```bash
mech call sandbox.generate
```

---

### `sandbox.status`

Get status of generated WoW API stubs

**Parameters:** None

**Example:**

```bash
mech call sandbox.status
```

---

### `sandbox.test`

Run Busted tests for an addon's Core layer with WoW API stubs

**Parameters:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `addon` | `string` | Yes | Name of addon to test (looks in _dev_ folder) |
| `filter` | `string` | No (default: `None`) | Filter pattern for test names |

**Example:**

Bash/Zsh:

```bash
mech call sandbox.test '{"addon": "<addon>"}'
```

PowerShell:

```powershell
mech call sandbox.test '{\"addon\": \"<addon>\"}'
```

---

### `system.pick_file`

Open a native file picker dialog to select a file

**Parameters:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `title` | `string` | No (default: `'Select File'`) | Title of the dialog window |
| `filter` | `string` | No (default: `'All Files (*.*)|*.*'`) | File filter (e.g., 'Text Files (*.txt)|*.txt') |

**Example:**

```bash
mech call system.pick_file
```

---

## Usage Notes

### Global Flags

| Flag | Description |
|------|-------------|
| `--json` | Output raw JSON (for parsing) |
| `--quiet` | Suppress non-essential output |
| `--agent` | Smart compression for AI agents |

### Calling Commands

```bash
# Bash/Zsh: inline JSON
mech call <command> '{"param": "value"}'

# Bash/Zsh: file input
mech call <command> @payload.json
```

```powershell
# PowerShell: inline JSON
mech call <command> '{\"param\": \"value\"}'

# PowerShell: quote @file args to avoid splatting
mech call <command> '@payload.json'
```

```bash
# File payloads are recommended for array inputs such as lua.queue
mech call lua.queue @payload.json
# First /reload executes; second /reload or game exit/logout writes results to SavedVariables on disk for lua.results

# Shorthand for common commands
mech addon.output  # Direct command shortcut
```

---

<p align="center">
  <em>Generated by <code>mech call docs.generate</code></em>
</p>