-- Generated APIDefinitions for namespace: C_CurveUtil
local _, ns = ...
local APIDefs = ns.APIDefinitions

APIDefs["C_CurveUtil.CreateColorCurve"] = {
    key = "C_CurveUtil.CreateColorCurve",
    name = "CreateColorCurve",
    category = "general",
    subcategory = "c_curveutil",
    func = _G["C_CurveUtil"] and _G["C_CurveUtil"]["CreateColorCurve"],
    funcPath = "C_CurveUtil.CreateColorCurve",
    params = {  },
    returns = { { name = "curve", type = "LuaColorCurveObject", canBeSecret = false } },
    midnightImpact = "NORMAL",
}

APIDefs["C_CurveUtil.CreateCurve"] = {
    key = "C_CurveUtil.CreateCurve",
    name = "CreateCurve",
    category = "general",
    subcategory = "c_curveutil",
    func = _G["C_CurveUtil"] and _G["C_CurveUtil"]["CreateCurve"],
    funcPath = "C_CurveUtil.CreateCurve",
    params = {  },
    returns = { { name = "curve", type = "LuaCurveObject", canBeSecret = false } },
    midnightImpact = "NORMAL",
}

APIDefs["C_CurveUtil.EvaluateColorFromBoolean"] = {
    key = "C_CurveUtil.EvaluateColorFromBoolean",
    name = "EvaluateColorFromBoolean",
    category = "combat_midnight",
    subcategory = "c_curveutil",
    func = _G["C_CurveUtil"] and _G["C_CurveUtil"]["EvaluateColorFromBoolean"],
    funcPath = "C_CurveUtil.EvaluateColorFromBoolean",
    params = { { name = "boolean", type = "bool", default = nil }, { name = "valueIfTrue", type = "colorRGBA", default = nil }, { name = "valueIfFalse", type = "colorRGBA", default = nil } },
    returns = { { name = "value", type = "colorRGBA", canBeSecret = false } },
    midnightImpact = "RESTRICTED",
    protected = true,
    midnightNote = "Secret behavior: SecretArguments=AllowedWhenTainted",
}

APIDefs["C_CurveUtil.EvaluateColorValueFromBoolean"] = {
    key = "C_CurveUtil.EvaluateColorValueFromBoolean",
    name = "EvaluateColorValueFromBoolean",
    category = "combat_midnight",
    subcategory = "c_curveutil",
    func = _G["C_CurveUtil"] and _G["C_CurveUtil"]["EvaluateColorValueFromBoolean"],
    funcPath = "C_CurveUtil.EvaluateColorValueFromBoolean",
    params = { { name = "boolean", type = "bool", default = nil }, { name = "valueIfTrue", type = "SingleColorValue", default = nil }, { name = "valueIfFalse", type = "SingleColorValue", default = nil } },
    returns = { { name = "value", type = "SingleColorValue", canBeSecret = false } },
    midnightImpact = "RESTRICTED",
    protected = true,
    midnightNote = "Secret behavior: SecretArguments=AllowedWhenTainted",
}

APIDefs["C_CurveUtil.EvaluateGameCurve"] = {
    key = "C_CurveUtil.EvaluateGameCurve",
    name = "EvaluateGameCurve",
    category = "combat_midnight",
    subcategory = "c_curveutil",
    func = _G["C_CurveUtil"] and _G["C_CurveUtil"]["EvaluateGameCurve"],
    funcPath = "C_CurveUtil.EvaluateGameCurve",
    params = { { name = "curveID", type = "number", default = nil }, { name = "x", type = "number", default = nil } },
    returns = { { name = "y", type = "number", canBeSecret = false } },
    midnightImpact = "RESTRICTED",
    protected = true,
    midnightNote = "Secret behavior: SecretArguments=AllowedWhenUntainted",
}
