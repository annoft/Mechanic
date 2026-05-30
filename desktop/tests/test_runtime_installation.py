from mechanic.runtime_installation import (
    format_runtime_issues,
    inspect_mechanic_runtime,
    mechanic_runtime_is_complete,
)


def test_inspect_mechanic_runtime_reports_missing_hub(tmp_path):
    wow_root = tmp_path / "World of Warcraft"
    addons = wow_root / "_retail_" / "Interface" / "AddOns"
    bootstrap = addons / "!Mechanic"
    bootstrap.mkdir(parents=True)
    (bootstrap / "!Mechanic.toc").write_text("## Interface: 120005", encoding="utf-8")

    statuses = inspect_mechanic_runtime(wow_root, ["_retail_"])

    assert mechanic_runtime_is_complete(statuses) is False
    retail = statuses[0]
    assert retail.status == "runtime_incomplete"
    assert retail.addons[0].addon == "!Mechanic"
    assert retail.addons[0].healthy is True
    assert retail.addons[1].addon == "Mechanic"
    assert retail.addons[1].status == "missing"

    issues = format_runtime_issues(statuses)
    assert any("Mechanic missing" in issue for issue in issues)


def test_inspect_mechanic_runtime_treats_missing_toc_as_unhealthy(tmp_path):
    wow_root = tmp_path / "World of Warcraft"
    addons = wow_root / "_retail_" / "Interface" / "AddOns"

    for addon in ("!Mechanic", "Mechanic"):
        (addons / addon).mkdir(parents=True)

    statuses = inspect_mechanic_runtime(wow_root, ["_retail_"])

    assert mechanic_runtime_is_complete(statuses) is False
    assert [addon.status for addon in statuses[0].addons] == [
        "missing_toc",
        "missing_toc",
    ]

    issues = format_runtime_issues(statuses)
    assert any("!Mechanic.toc is missing" in issue for issue in issues)
    assert any("Mechanic.toc is missing" in issue for issue in issues)


def test_inspect_mechanic_runtime_complete_for_active_flavor(tmp_path):
    wow_root = tmp_path / "World of Warcraft"
    addons = wow_root / "_retail_" / "Interface" / "AddOns"

    for addon in ("!Mechanic", "Mechanic"):
        addon_path = addons / addon
        addon_path.mkdir(parents=True)
        (addon_path / f"{addon}.toc").write_text(
            "## Interface: 120005", encoding="utf-8"
        )

    statuses = inspect_mechanic_runtime(wow_root, ["_retail_", "_ptr_"])

    assert statuses[0].status == "healthy"
    assert statuses[1].status == "client_missing"
    assert mechanic_runtime_is_complete(statuses) is True
    assert format_runtime_issues(statuses) == []
