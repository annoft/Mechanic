-- Generated APIDefinitions for namespace: C_TableUtil
local _, ns = ...
local APIDefs = ns.APIDefinitions

APIDefs["C_TableUtil.FindIndexedMismatch"] = {
    key = "C_TableUtil.FindIndexedMismatch",
    name = "FindIndexedMismatch",
    category = "combat_midnight",
    subcategory = "c_tableutil",
    func = _G["C_TableUtil"] and _G["C_TableUtil"]["FindIndexedMismatch"],
    funcPath = "C_TableUtil.FindIndexedMismatch",
    params = { { name = "t1", type = "LuaValueReference", default = nil }, { name = "t2", type = "LuaValueReference", default = nil } },
    returns = { { name = "index", type = "number", canBeSecret = false } },
    midnightImpact = "RESTRICTED",
    protected = true,
    midnightNote = "Secret behavior: SecretArguments=AllowedWhenUntainted",
}

APIDefs["C_TableUtil.count"] = {
    key = "C_TableUtil.count",
    name = "count",
    category = "combat_midnight",
    subcategory = "c_tableutil",
    func = _G["C_TableUtil"] and _G["C_TableUtil"]["count"],
    funcPath = "C_TableUtil.count",
    params = { { name = "table", type = "LuaValueReference", default = nil } },
    returns = { { name = "numTableNodes", type = "number", canBeSecret = false }, { name = "numArrayNodes", type = "number", canBeSecret = false }, { name = "maxArrayIndex", type = "number", canBeSecret = false } },
    midnightImpact = "RESTRICTED",
    protected = true,
    midnightNote = "Secret behavior: SecretArguments=AllowedWhenUntainted",
}

APIDefs["C_TableUtil.create"] = {
    key = "C_TableUtil.create",
    name = "create",
    category = "combat_midnight",
    subcategory = "c_tableutil",
    func = _G["C_TableUtil"] and _G["C_TableUtil"]["create"],
    funcPath = "C_TableUtil.create",
    params = { { name = "arraySizeHint", type = "number", default = nil }, { name = "nodeSizeHint", type = "number", default = 0 } },
    returns = { { name = "table", type = "LuaValueReference", canBeSecret = false } },
    midnightImpact = "RESTRICTED",
    protected = true,
    midnightNote = "Secret behavior: SecretArguments=AllowedWhenUntainted",
}

APIDefs["C_TableUtil.freeze"] = {
    key = "C_TableUtil.freeze",
    name = "freeze",
    category = "combat_midnight",
    subcategory = "c_tableutil",
    func = _G["C_TableUtil"] and _G["C_TableUtil"]["freeze"],
    funcPath = "C_TableUtil.freeze",
    params = { { name = "table", type = "LuaValueReference", default = nil } },
    returns = {  },
    midnightImpact = "RESTRICTED",
    protected = true,
    midnightNote = "Secret behavior: SecretArguments=AllowedWhenUntainted",
}

APIDefs["C_TableUtil.isfrozen"] = {
    key = "C_TableUtil.isfrozen",
    name = "isfrozen",
    category = "combat_midnight",
    subcategory = "c_tableutil",
    func = _G["C_TableUtil"] and _G["C_TableUtil"]["isfrozen"],
    funcPath = "C_TableUtil.isfrozen",
    params = { { name = "table", type = "LuaValueReference", default = nil } },
    returns = { { name = "frozen", type = "bool", canBeSecret = false } },
    midnightImpact = "RESTRICTED",
    protected = true,
    midnightNote = "Secret behavior: SecretArguments=AllowedWhenUntainted",
}
