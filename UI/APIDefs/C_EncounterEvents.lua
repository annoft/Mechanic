-- Generated APIDefinitions for namespace: C_EncounterEvents
local _, ns = ...
local APIDefs = ns.APIDefinitions

APIDefs["C_EncounterEvents.GetEventColor"] = {
    key = "C_EncounterEvents.GetEventColor",
    name = "GetEventColor",
    category = "combat_midnight",
    subcategory = "c_encounterevents",
    func = _G["C_EncounterEvents"] and _G["C_EncounterEvents"]["GetEventColor"],
    funcPath = "C_EncounterEvents.GetEventColor",
    params = { { name = "encounterEventID", type = "number", default = nil } },
    returns = { { name = "color", type = "colorRGB", canBeSecret = false } },
    midnightImpact = "RESTRICTED",
    protected = true,
    midnightNote = "Secret behavior: SecretArguments=AllowedWhenUntainted",
}

APIDefs["C_EncounterEvents.GetEventInfo"] = {
    key = "C_EncounterEvents.GetEventInfo",
    name = "GetEventInfo",
    category = "combat_midnight",
    subcategory = "c_encounterevents",
    func = _G["C_EncounterEvents"] and _G["C_EncounterEvents"]["GetEventInfo"],
    funcPath = "C_EncounterEvents.GetEventInfo",
    params = { { name = "encounterEventID", type = "number", default = nil } },
    returns = { { name = "encounterEventInfo", type = "EncounterEventInfo", canBeSecret = false } },
    midnightImpact = "RESTRICTED",
    protected = true,
    midnightNote = "Secret behavior: SecretArguments=AllowedWhenUntainted",
}

APIDefs["C_EncounterEvents.GetEventList"] = {
    key = "C_EncounterEvents.GetEventList",
    name = "GetEventList",
    category = "general",
    subcategory = "c_encounterevents",
    func = _G["C_EncounterEvents"] and _G["C_EncounterEvents"]["GetEventList"],
    funcPath = "C_EncounterEvents.GetEventList",
    params = {  },
    returns = { { name = "encounterEventIDs", type = "table", canBeSecret = false } },
    midnightImpact = "NORMAL",
}

APIDefs["C_EncounterEvents.GetEventSound"] = {
    key = "C_EncounterEvents.GetEventSound",
    name = "GetEventSound",
    category = "combat_midnight",
    subcategory = "c_encounterevents",
    func = _G["C_EncounterEvents"] and _G["C_EncounterEvents"]["GetEventSound"],
    funcPath = "C_EncounterEvents.GetEventSound",
    params = { { name = "encounterEventID", type = "number", default = nil }, { name = "trigger", type = "EncounterEventSoundTrigger", default = nil } },
    returns = { { name = "sound", type = "EncounterEventSoundInfo", canBeSecret = false } },
    midnightImpact = "RESTRICTED",
    protected = true,
    midnightNote = "Secret behavior: SecretArguments=AllowedWhenUntainted",
}

APIDefs["C_EncounterEvents.HasEventInfo"] = {
    key = "C_EncounterEvents.HasEventInfo",
    name = "HasEventInfo",
    category = "combat_midnight",
    subcategory = "c_encounterevents",
    func = _G["C_EncounterEvents"] and _G["C_EncounterEvents"]["HasEventInfo"],
    funcPath = "C_EncounterEvents.HasEventInfo",
    params = { { name = "encounterEventID", type = "number", default = nil } },
    returns = { { name = "exists", type = "bool", canBeSecret = false } },
    midnightImpact = "RESTRICTED",
    protected = true,
    midnightNote = "Secret behavior: SecretArguments=AllowedWhenUntainted",
}

APIDefs["C_EncounterEvents.PlayEventSound"] = {
    key = "C_EncounterEvents.PlayEventSound",
    name = "PlayEventSound",
    category = "combat_midnight",
    subcategory = "c_encounterevents",
    func = _G["C_EncounterEvents"] and _G["C_EncounterEvents"]["PlayEventSound"],
    funcPath = "C_EncounterEvents.PlayEventSound",
    params = { { name = "encounterEventID", type = "number", default = nil }, { name = "trigger", type = "EncounterEventSoundTrigger", default = nil } },
    returns = { { name = "handle", type = "SoundHandle", canBeSecret = false } },
    midnightImpact = "RESTRICTED",
    protected = true,
    midnightNote = "Secret behavior: SecretArguments=AllowedWhenUntainted",
}

APIDefs["C_EncounterEvents.SetEventColor"] = {
    key = "C_EncounterEvents.SetEventColor",
    name = "SetEventColor",
    category = "combat_midnight",
    subcategory = "c_encounterevents",
    func = _G["C_EncounterEvents"] and _G["C_EncounterEvents"]["SetEventColor"],
    funcPath = "C_EncounterEvents.SetEventColor",
    params = { { name = "encounterEventID", type = "number", default = nil }, { name = "color", type = "colorRGB", default = nil } },
    returns = {  },
    midnightImpact = "RESTRICTED",
    protected = true,
    midnightNote = "Secret behavior: SecretArguments=NotAllowed",
}

APIDefs["C_EncounterEvents.SetEventSound"] = {
    key = "C_EncounterEvents.SetEventSound",
    name = "SetEventSound",
    category = "combat_midnight",
    subcategory = "c_encounterevents",
    func = _G["C_EncounterEvents"] and _G["C_EncounterEvents"]["SetEventSound"],
    funcPath = "C_EncounterEvents.SetEventSound",
    params = { { name = "encounterEventID", type = "number", default = nil }, { name = "trigger", type = "EncounterEventSoundTrigger", default = nil }, { name = "sound", type = "EncounterEventSoundInfo", default = nil } },
    returns = {  },
    midnightImpact = "RESTRICTED",
    protected = true,
    midnightNote = "Secret behavior: SecretArguments=NotAllowed",
}
