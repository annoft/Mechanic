"""Inspection helpers for the in-game Mechanic runtime installation."""

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable, Optional


MECHANIC_RUNTIME_ADDONS = ("!Mechanic", "Mechanic")


@dataclass(frozen=True)
class RuntimeAddonStatus:
    addon: str
    path: str
    present: bool
    toc_path: str
    toc_present: bool
    healthy: bool
    status: str

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True)
class RuntimeFlavorStatus:
    flavor: str
    path: str
    exists: bool
    addons_path: str
    addons_path_exists: bool
    addons: list[RuntimeAddonStatus]
    healthy: bool
    status: str

    def to_dict(self) -> dict:
        data = asdict(self)
        data["addons"] = [addon.to_dict() for addon in self.addons]
        return data


def inspect_mechanic_runtime(
    wow_root: Optional[Path], flavors: Iterable[str]
) -> list[RuntimeFlavorStatus]:
    """Inspect !Mechanic and Mechanic under each configured WoW flavor."""
    statuses = []

    for flavor in flavors:
        flavor_path = wow_root / flavor if wow_root else None
        flavor_exists = flavor_path.exists() if flavor_path else False
        addons_path = (
            flavor_path / "Interface" / "AddOns" if flavor_path else None
        )
        addons_path_exists = addons_path.exists() if addons_path else False

        addon_statuses = []
        for addon in MECHANIC_RUNTIME_ADDONS:
            addon_path = addons_path / addon if addons_path else None
            toc_path = addon_path / f"{addon}.toc" if addon_path else None
            present = addon_path.exists() if addon_path else False
            toc_present = toc_path.exists() if toc_path else False
            healthy = present and toc_present

            if healthy:
                status = "healthy"
            elif present:
                status = "missing_toc"
            else:
                status = "missing"

            addon_statuses.append(
                RuntimeAddonStatus(
                    addon=addon,
                    path=str(addon_path) if addon_path else "",
                    present=present,
                    toc_path=str(toc_path) if toc_path else "",
                    toc_present=toc_present,
                    healthy=healthy,
                    status=status,
                )
            )

        if not flavor_exists:
            flavor_status = "client_missing"
            healthy = False
        elif not addons_path_exists:
            flavor_status = "addons_folder_missing"
            healthy = False
        elif all(addon.healthy for addon in addon_statuses):
            flavor_status = "healthy"
            healthy = True
        else:
            flavor_status = "runtime_incomplete"
            healthy = False

        statuses.append(
            RuntimeFlavorStatus(
                flavor=flavor,
                path=str(flavor_path) if flavor_path else "",
                exists=flavor_exists,
                addons_path=str(addons_path) if addons_path else "",
                addons_path_exists=addons_path_exists,
                addons=addon_statuses,
                healthy=healthy,
                status=flavor_status,
            )
        )

    return statuses


def mechanic_runtime_is_complete(statuses: Iterable[RuntimeFlavorStatus]) -> bool:
    """Return True when every active WoW flavor has both runtime addons healthy."""
    active_statuses = [status for status in statuses if status.exists]
    return bool(active_statuses) and all(status.healthy for status in active_statuses)


def format_runtime_issues(statuses: Iterable[RuntimeFlavorStatus]) -> list[str]:
    """Create concise actionable issue strings for active flavor problems."""
    issues = []
    active_statuses = [status for status in statuses if status.exists]

    if not active_statuses:
        return ["No active WoW client folders were found under the configured wow_root."]

    for status in active_statuses:
        if not status.addons_path_exists:
            issues.append(
                f"{status.flavor}: AddOns folder missing at {status.addons_path}"
            )
            continue

        for addon in status.addons:
            if addon.healthy:
                continue
            if addon.present:
                issues.append(
                    f"{status.flavor}: {addon.addon} exists but {addon.addon}.toc is missing at {addon.toc_path}"
                )
            else:
                issues.append(
                    f"{status.flavor}: {addon.addon} missing at {addon.path}"
                )

    return issues
