-- Generated APIDefinitions for namespace: C_NamePlate
local _, ns = ...
local APIDefs = ns.APIDefinitions

APIDefs["C_NamePlate.GetNamePlateForUnit"] = {
    key = "C_NamePlate.GetNamePlateForUnit",
    name = "GetNamePlateForUnit",
    category = "combat_midnight",
    subcategory = "c_nameplate",
    func = _G["C_NamePlate"] and _G["C_NamePlate"]["GetNamePlateForUnit"],
    funcPath = "C_NamePlate.GetNamePlateForUnit",
    params = { { name = "unitToken", type = "UnitTokenNamePlate", default = nil }, { name = "includeForbidden", type = "bool", default = false } },
    returns = { { name = "nameplate", type = "NamePlateFrame", canBeSecret = false } },
    midnightImpact = "RESTRICTED",
    protected = true,
    midnightNote = "Secret behavior: SecretArguments=AllowedWhenUntainted",
}

APIDefs["C_NamePlate.GetNamePlateSize"] = {
    key = "C_NamePlate.GetNamePlateSize",
    name = "GetNamePlateSize",
    category = "general",
    subcategory = "c_nameplate",
    func = _G["C_NamePlate"] and _G["C_NamePlate"]["GetNamePlateSize"],
    funcPath = "C_NamePlate.GetNamePlateSize",
    params = {  },
    returns = { { name = "width", type = "uiUnit", canBeSecret = false }, { name = "height", type = "uiUnit", canBeSecret = false } },
    midnightImpact = "NORMAL",
}

APIDefs["C_NamePlate.GetNamePlates"] = {
    key = "C_NamePlate.GetNamePlates",
    name = "GetNamePlates",
    category = "general",
    subcategory = "c_nameplate",
    func = _G["C_NamePlate"] and _G["C_NamePlate"]["GetNamePlates"],
    funcPath = "C_NamePlate.GetNamePlates",
    params = {  },
    returns = { { name = "nameplates", type = "table", canBeSecret = false } },
    midnightImpact = "NORMAL",
}

APIDefs["C_NamePlate.SetNamePlateSize"] = {
    key = "C_NamePlate.SetNamePlateSize",
    name = "SetNamePlateSize",
    category = "combat_midnight",
    subcategory = "c_nameplate",
    func = _G["C_NamePlate"] and _G["C_NamePlate"]["SetNamePlateSize"],
    funcPath = "C_NamePlate.SetNamePlateSize",
    params = { { name = "width", type = "uiUnit", default = nil }, { name = "height", type = "uiUnit", default = nil } },
    returns = {  },
    midnightImpact = "RESTRICTED",
    protected = true,
    midnightNote = "Secret behavior: SecretArguments=AllowedWhenUntainted",
}
