-- Generated APIDefinitions for namespace: C_HousingInspectMode
local _, ns = ...
local APIDefs = ns.APIDefinitions

APIDefs["C_HousingInspectMode.EnterInspectMode"] = {
    key = "C_HousingInspectMode.EnterInspectMode",
    name = "EnterInspectMode",
    category = "general",
    subcategory = "c_housinginspectmode",
    func = _G["C_HousingInspectMode"] and _G["C_HousingInspectMode"]["EnterInspectMode"],
    funcPath = "C_HousingInspectMode.EnterInspectMode",
    params = {  },
    returns = {  },
    midnightImpact = "NORMAL",
}

APIDefs["C_HousingInspectMode.ExitInspectMode"] = {
    key = "C_HousingInspectMode.ExitInspectMode",
    name = "ExitInspectMode",
    category = "general",
    subcategory = "c_housinginspectmode",
    func = _G["C_HousingInspectMode"] and _G["C_HousingInspectMode"]["ExitInspectMode"],
    funcPath = "C_HousingInspectMode.ExitInspectMode",
    params = {  },
    returns = {  },
    midnightImpact = "NORMAL",
}

APIDefs["C_HousingInspectMode.GetHoveredDecorGUID"] = {
    key = "C_HousingInspectMode.GetHoveredDecorGUID",
    name = "GetHoveredDecorGUID",
    category = "general",
    subcategory = "c_housinginspectmode",
    func = _G["C_HousingInspectMode"] and _G["C_HousingInspectMode"]["GetHoveredDecorGUID"],
    funcPath = "C_HousingInspectMode.GetHoveredDecorGUID",
    params = {  },
    returns = { { name = "decorGUID", type = "WOWGUID", canBeSecret = false } },
    midnightImpact = "NORMAL",
}

APIDefs["C_HousingInspectMode.IsHoveringDecor"] = {
    key = "C_HousingInspectMode.IsHoveringDecor",
    name = "IsHoveringDecor",
    category = "general",
    subcategory = "c_housinginspectmode",
    func = _G["C_HousingInspectMode"] and _G["C_HousingInspectMode"]["IsHoveringDecor"],
    funcPath = "C_HousingInspectMode.IsHoveringDecor",
    params = {  },
    returns = { { name = "isHoveringDecor", type = "bool", canBeSecret = false } },
    midnightImpact = "NORMAL",
}

APIDefs["C_HousingInspectMode.IsInInspectMode"] = {
    key = "C_HousingInspectMode.IsInInspectMode",
    name = "IsInInspectMode",
    category = "general",
    subcategory = "c_housinginspectmode",
    func = _G["C_HousingInspectMode"] and _G["C_HousingInspectMode"]["IsInInspectMode"],
    funcPath = "C_HousingInspectMode.IsInInspectMode",
    params = {  },
    returns = { { name = "isInInspectMode", type = "bool", canBeSecret = false } },
    midnightImpact = "NORMAL",
}
