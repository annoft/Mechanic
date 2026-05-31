# FenUI Dependency Removal Plan

**Status**: Deferred / Not Started
**Target Version**: Unscheduled
**Priority**: Medium

---

## Overview

Mechanic currently embeds FenUI as its primary in-game UI framework. FenUI is
loaded through `Mechanic/embeds.xml`, declared as a local library in
`Mechanic/Libs/libs.json`, and used directly throughout the main frame and most
UI tabs.

This plan records a future migration path for removing Mechanic's hard
dependency on FenUI. It is not a request to start the migration now.

---

## Current Dependency Shape

Mechanic depends on FenUI in these areas:

- **Packaging and sync tooling**: `Mechanic/embeds.xml` includes
  `Libs/FenUI/FenUI.xml`; `libs.json` declares FenUI as a local library; the
  library sync command can discover a standalone `FenUI` repo under the
  configured development path.
- **Main shell**: `UI/MainFrame.lua` uses FenUI for the main panel, tab group,
  status row, image buttons, checkbox, and color tokens.
- **Shared layouts**: `UI/Shared/SplitNavLayout.lua` wraps
  `FenUI:CreateSplitLayout`, indirectly affecting Console, Errors, Performance,
  and Tools.
- **Tab widgets**: API, Console, Errors, Tests, Inspect, Performance, and Tools
  use FenUI toolbars, inputs, dropdowns, edit boxes, trees, image buttons,
  checkboxes, and buttons.
- **Style tokens**: several modules call `FenUI:GetColorRGB`, `FenUI:GetColor`,
  and `FenUI:GetFont` directly.
- **Utilities**: `Utils.lua` partially delegates environment, color, menu, and
  widget helpers to `FenUI.Utils`.
- **Diagnostics**: Core library health checks treat `_G.FenUI` as a required
  loaded dependency.

The embedded copy in `Mechanic/Libs/FenUI` is not a clean mirror of the current
standalone `FenUI` repository. Mechanic's copy includes `Widgets/VirtualList.lua`
and local changes, while the standalone repository contains files not embedded
by Mechanic. Blindly syncing from the standalone repository can remove Mechanic
specific behavior.

---

## Non-Goals

- Do not rewrite the UI in one large pass.
- Do not replace visual design and interaction behavior unless needed to remove
  the dependency.
- Do not remove FenUI before all direct call sites are behind a Mechanic-owned
  abstraction.
- Do not treat `F:/Projects/FenUI` as a safe source of truth for Mechanic until
  a compatibility contract exists.

---

## Migration Strategy

### Phase 0: Guard the Current State

- [ ] Add a documented FenUI compatibility contract listing every FenUI API
      Mechanic currently requires.
- [ ] Add a check to `libs.check` or a dedicated diagnostic command that verifies
      those APIs exist in the embedded FenUI copy.
- [ ] Mark the embedded FenUI copy as a Mechanic-specific vendored fork until a
      replacement is complete.
- [ ] Prevent or warn against `libs.sync --force` replacing Mechanic's FenUI with
      a standalone repo copy that lacks Mechanic-only files such as
      `Widgets/VirtualList.lua`.

### Phase 1: Introduce a Mechanic-Owned UI Facade

- [ ] Add a small `Mechanic.UI` / `ns.UIKit` module that exposes the UI services
      Mechanic needs: colors, fonts, panel, tab group, status row, toolbar,
      split layout, input, dropdown, multiline edit box, tree, virtual list,
      image button, checkbox, and button.
- [ ] Initially implement the facade as a thin delegation layer over FenUI.
- [ ] Replace direct `FenUI:*` calls in Mechanic code with the facade, one module
      at a time.
- [ ] Keep the first phase behavior-preserving; no visual redesign.

### Phase 2: Replace Low-Risk Primitives

- [ ] Move color, font, spacing, and icon conventions into Mechanic-owned tokens.
- [ ] Replace basic buttons, image buttons, checkboxes, inputs, and dropdowns
      with native Mechanic widgets behind the facade.
- [ ] Replace `Utils.lua` dependencies on `FenUI.Utils` with Mechanic-owned
      helpers.
- [ ] Verify each tab after every slice.

### Phase 3: Replace Layout and Shell Widgets

- [ ] Replace toolbar and status row implementations.
- [ ] Replace split navigation layout.
- [ ] Replace main panel behavior: movable, resizable, closable, safe content
      area, size persistence, and frame strata.
- [ ] Replace tab group behavior and active-tab persistence.

### Phase 4: Replace Complex Widgets

- [ ] Replace multiline edit box behavior used by Console, Errors, API results,
      Tests, export dialogs, and help dialogs.
- [ ] Replace tree behavior used by Tests.
- [ ] Replace virtual list behavior used by the API tab.
- [ ] Keep API tab search, filtering, selection, and row rendering behavior
      stable.

### Phase 5: Remove FenUI

- [ ] Remove `Libs/FenUI/FenUI.xml` from `Mechanic/embeds.xml`.
- [ ] Remove `FenUI` from `Mechanic/Libs/libs.json`.
- [ ] Remove `Mechanic/Libs/FenUI` after no direct or indirect references remain.
- [ ] Remove FenUI-specific diagnostics and `/fenui` side effects from Mechanic's
      runtime surface.
- [ ] Update docs and release notes to describe the new internal UI layer.

---

## Verification Gates

Every phase must pass:

- [ ] `rg "FenUI" Mechanic --glob "!Libs/FenUI/**"` shows only expected legacy
      references for the current phase.
- [ ] `mech call addon.validate '{"addon":"Mechanic"}'`
- [ ] `mech call addon.lint '{"addon":"Mechanic"}'`
- [ ] `mech call libs.check '{"addon":"Mechanic"}'`
- [ ] In-game `/reload` with no BugGrabber errors.
- [ ] Open every Mechanic tab: Inspect, Console, Errors, Tests, Performance,
      Tools, and API.
- [ ] Exercise API tab search, impact filter, namespace filter, safe-only toggle,
      API selection, parameter inputs, examples, run, copy, and notes.
- [ ] Exercise Inspect pick/watch/property editor flows.
- [ ] Exercise Console copy/filter behavior and Errors session navigation.

Final removal must additionally pass:

- [ ] No direct `FenUI` references outside archived docs or changelog history.
- [ ] No `Libs/FenUI` directory in the packaged addon.
- [ ] No dependency on a standalone FenUI addon or global `_G.FenUI`.
- [ ] `addon.output` reports no Mechanic runtime errors after user-confirmed
      `/reload`.

---

## Risks

- **Large visual regression surface**: FenUI owns both layout and styling, so a
  direct replacement can shift many screens at once.
- **Hidden behavior coupling**: widgets include sizing, scroll, hover, selected
  state, text sanitization, and menu behavior that callers may rely on
  implicitly.
- **API tab fragility**: API uses Mechanic-specific `CreateVirtualList`, which is
  not present in the current standalone FenUI repository.
- **Sync hazard**: local library sync can discover `F:/Projects/FenUI`; a forced
  sync can overwrite Mechanic's vendored fork.
- **Global namespace conflicts**: embedded FenUI uses the global `FenUI`
  namespace rather than LibStub-style version negotiation.

---

## Recommended First Slice

Start with Phase 0 only:

1. Add a FenUI compatibility contract for the current embedded copy.
2. Add a lightweight automated check for required FenUI functions.
3. Add a warning to library sync when the source FenUI copy does not provide all
   required Mechanic APIs.

This reduces immediate breakage risk without starting the full UI migration.
