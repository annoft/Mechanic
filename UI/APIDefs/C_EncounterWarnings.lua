-- Generated APIDefinitions for namespace: C_EncounterWarnings
local _, ns = ...
local APIDefs = ns.APIDefinitions

APIDefs["C_EncounterWarnings.GetColorForSeverity"] = {
    key = "C_EncounterWarnings.GetColorForSeverity",
    name = "GetColorForSeverity",
    category = "combat_midnight",
    subcategory = "c_encounterwarnings",
    func = _G["C_EncounterWarnings"] and _G["C_EncounterWarnings"]["GetColorForSeverity"],
    funcPath = "C_EncounterWarnings.GetColorForSeverity",
    params = { { name = "severity", type = "EncounterEventSeverity", default = nil } },
    returns = { { name = "color", type = "colorRGB", canBeSecret = false } },
    midnightImpact = "RESTRICTED",
    protected = true,
    midnightNote = "Secret behavior: SecretArguments=AllowedWhenUntainted",
}

APIDefs["C_EncounterWarnings.GetEditModeWarningInfo"] = {
    key = "C_EncounterWarnings.GetEditModeWarningInfo",
    name = "GetEditModeWarningInfo",
    category = "combat_midnight",
    subcategory = "c_encounterwarnings",
    func = _G["C_EncounterWarnings"] and _G["C_EncounterWarnings"]["GetEditModeWarningInfo"],
    funcPath = "C_EncounterWarnings.GetEditModeWarningInfo",
    params = { { name = "severity", type = "EncounterEventSeverity", default = nil } },
    returns = { { name = "warningInfo", type = "EncounterWarningInfo", canBeSecret = false } },
    midnightImpact = "RESTRICTED",
    protected = true,
    midnightNote = "Secret behavior: SecretArguments=AllowedWhenUntainted",
}

APIDefs["C_EncounterWarnings.GetPlayCustomSoundsWhenHidden"] = {
    key = "C_EncounterWarnings.GetPlayCustomSoundsWhenHidden",
    name = "GetPlayCustomSoundsWhenHidden",
    category = "general",
    subcategory = "c_encounterwarnings",
    func = _G["C_EncounterWarnings"] and _G["C_EncounterWarnings"]["GetPlayCustomSoundsWhenHidden"],
    funcPath = "C_EncounterWarnings.GetPlayCustomSoundsWhenHidden",
    params = {  },
    returns = { { name = "play", type = "bool", canBeSecret = false } },
    midnightImpact = "NORMAL",
}

APIDefs["C_EncounterWarnings.GetSoundKitForSeverity"] = {
    key = "C_EncounterWarnings.GetSoundKitForSeverity",
    name = "GetSoundKitForSeverity",
    category = "combat_midnight",
    subcategory = "c_encounterwarnings",
    func = _G["C_EncounterWarnings"] and _G["C_EncounterWarnings"]["GetSoundKitForSeverity"],
    funcPath = "C_EncounterWarnings.GetSoundKitForSeverity",
    params = { { name = "severity", type = "EncounterEventSeverity", default = nil } },
    returns = { { name = "soundKitID", type = "number", canBeSecret = false } },
    midnightImpact = "RESTRICTED",
    protected = true,
    midnightNote = "Secret behavior: SecretArguments=AllowedWhenUntainted",
}

APIDefs["C_EncounterWarnings.GetWarningsShown"] = {
    key = "C_EncounterWarnings.GetWarningsShown",
    name = "GetWarningsShown",
    category = "general",
    subcategory = "c_encounterwarnings",
    func = _G["C_EncounterWarnings"] and _G["C_EncounterWarnings"]["GetWarningsShown"],
    funcPath = "C_EncounterWarnings.GetWarningsShown",
    params = {  },
    returns = { { name = "shown", type = "bool", canBeSecret = false } },
    midnightImpact = "NORMAL",
}

APIDefs["C_EncounterWarnings.IsFeatureAvailable"] = {
    key = "C_EncounterWarnings.IsFeatureAvailable",
    name = "IsFeatureAvailable",
    category = "general",
    subcategory = "c_encounterwarnings",
    func = _G["C_EncounterWarnings"] and _G["C_EncounterWarnings"]["IsFeatureAvailable"],
    funcPath = "C_EncounterWarnings.IsFeatureAvailable",
    params = {  },
    returns = { { name = "isAvailable", type = "bool", canBeSecret = false } },
    midnightImpact = "NORMAL",
}

APIDefs["C_EncounterWarnings.IsFeatureEnabled"] = {
    key = "C_EncounterWarnings.IsFeatureEnabled",
    name = "IsFeatureEnabled",
    category = "general",
    subcategory = "c_encounterwarnings",
    func = _G["C_EncounterWarnings"] and _G["C_EncounterWarnings"]["IsFeatureEnabled"],
    funcPath = "C_EncounterWarnings.IsFeatureEnabled",
    params = {  },
    returns = { { name = "isAvailableAndEnabled", type = "bool", canBeSecret = false } },
    midnightImpact = "NORMAL",
}

APIDefs["C_EncounterWarnings.PlaySound"] = {
    key = "C_EncounterWarnings.PlaySound",
    name = "PlaySound",
    category = "combat_midnight",
    subcategory = "c_encounterwarnings",
    func = _G["C_EncounterWarnings"] and _G["C_EncounterWarnings"]["PlaySound"],
    funcPath = "C_EncounterWarnings.PlaySound",
    params = { { name = "severity", type = "EncounterEventSeverity", default = nil } },
    returns = { { name = "soundHandle", type = "number", canBeSecret = false } },
    midnightImpact = "RESTRICTED",
    protected = true,
    midnightNote = "Secret behavior: SecretArguments=AllowedWhenUntainted",
}

APIDefs["C_EncounterWarnings.SetPlayCustomSoundsWhenHidden"] = {
    key = "C_EncounterWarnings.SetPlayCustomSoundsWhenHidden",
    name = "SetPlayCustomSoundsWhenHidden",
    category = "combat_midnight",
    subcategory = "c_encounterwarnings",
    func = _G["C_EncounterWarnings"] and _G["C_EncounterWarnings"]["SetPlayCustomSoundsWhenHidden"],
    funcPath = "C_EncounterWarnings.SetPlayCustomSoundsWhenHidden",
    params = { { name = "play", type = "bool", default = nil } },
    returns = {  },
    midnightImpact = "RESTRICTED",
    protected = true,
    midnightNote = "Secret behavior: SecretArguments=NotAllowed",
}

APIDefs["C_EncounterWarnings.SetWarningsShown"] = {
    key = "C_EncounterWarnings.SetWarningsShown",
    name = "SetWarningsShown",
    category = "combat_midnight",
    subcategory = "c_encounterwarnings",
    func = _G["C_EncounterWarnings"] and _G["C_EncounterWarnings"]["SetWarningsShown"],
    funcPath = "C_EncounterWarnings.SetWarningsShown",
    params = { { name = "shown", type = "bool", default = nil } },
    returns = {  },
    midnightImpact = "RESTRICTED",
    protected = true,
    midnightNote = "Secret behavior: SecretArguments=NotAllowed",
}
