-- Generated APIDefinitions for namespace: C_PhotoSharing
local _, ns = ...
local APIDefs = ns.APIDefinitions

APIDefs["C_PhotoSharing.BeginAuthorizationFlow"] = {
    key = "C_PhotoSharing.BeginAuthorizationFlow",
    name = "BeginAuthorizationFlow",
    category = "general",
    subcategory = "c_photosharing",
    func = _G["C_PhotoSharing"] and _G["C_PhotoSharing"]["BeginAuthorizationFlow"],
    funcPath = "C_PhotoSharing.BeginAuthorizationFlow",
    params = {  },
    returns = {  },
    midnightImpact = "NORMAL",
}

APIDefs["C_PhotoSharing.ClearAuthorization"] = {
    key = "C_PhotoSharing.ClearAuthorization",
    name = "ClearAuthorization",
    category = "general",
    subcategory = "c_photosharing",
    func = _G["C_PhotoSharing"] and _G["C_PhotoSharing"]["ClearAuthorization"],
    funcPath = "C_PhotoSharing.ClearAuthorization",
    params = {  },
    returns = {  },
    midnightImpact = "NORMAL",
}

APIDefs["C_PhotoSharing.CompleteAuthorizationFlow"] = {
    key = "C_PhotoSharing.CompleteAuthorizationFlow",
    name = "CompleteAuthorizationFlow",
    category = "combat_midnight",
    subcategory = "c_photosharing",
    func = _G["C_PhotoSharing"] and _G["C_PhotoSharing"]["CompleteAuthorizationFlow"],
    funcPath = "C_PhotoSharing.CompleteAuthorizationFlow",
    params = { { name = "callbackURL", type = "cstring", default = nil } },
    returns = {  },
    midnightImpact = "RESTRICTED",
    protected = true,
    midnightNote = "Secret behavior: SecretArguments=AllowedWhenUntainted",
}

APIDefs["C_PhotoSharing.GetCropRatio"] = {
    key = "C_PhotoSharing.GetCropRatio",
    name = "GetCropRatio",
    category = "general",
    subcategory = "c_photosharing",
    func = _G["C_PhotoSharing"] and _G["C_PhotoSharing"]["GetCropRatio"],
    funcPath = "C_PhotoSharing.GetCropRatio",
    params = {  },
    returns = { { name = "cropRatio", type = "number", canBeSecret = false } },
    midnightImpact = "NORMAL",
}

APIDefs["C_PhotoSharing.GetPhotoSharingAuthURL"] = {
    key = "C_PhotoSharing.GetPhotoSharingAuthURL",
    name = "GetPhotoSharingAuthURL",
    category = "general",
    subcategory = "c_photosharing",
    func = _G["C_PhotoSharing"] and _G["C_PhotoSharing"]["GetPhotoSharingAuthURL"],
    funcPath = "C_PhotoSharing.GetPhotoSharingAuthURL",
    params = {  },
    returns = { { name = "authUrl", type = "cstring", canBeSecret = false } },
    midnightImpact = "NORMAL",
}

APIDefs["C_PhotoSharing.GetStatus"] = {
    key = "C_PhotoSharing.GetStatus",
    name = "GetStatus",
    category = "general",
    subcategory = "c_photosharing",
    func = _G["C_PhotoSharing"] and _G["C_PhotoSharing"]["GetStatus"],
    funcPath = "C_PhotoSharing.GetStatus",
    params = {  },
    returns = { { name = "status", type = "PhotoSharingStatus", canBeSecret = false } },
    midnightImpact = "NORMAL",
}

APIDefs["C_PhotoSharing.IsAuthorized"] = {
    key = "C_PhotoSharing.IsAuthorized",
    name = "IsAuthorized",
    category = "general",
    subcategory = "c_photosharing",
    func = _G["C_PhotoSharing"] and _G["C_PhotoSharing"]["IsAuthorized"],
    funcPath = "C_PhotoSharing.IsAuthorized",
    params = {  },
    returns = { { name = "authorized", type = "bool", canBeSecret = false } },
    midnightImpact = "NORMAL",
}

APIDefs["C_PhotoSharing.IsEnabled"] = {
    key = "C_PhotoSharing.IsEnabled",
    name = "IsEnabled",
    category = "general",
    subcategory = "c_photosharing",
    func = _G["C_PhotoSharing"] and _G["C_PhotoSharing"]["IsEnabled"],
    funcPath = "C_PhotoSharing.IsEnabled",
    params = {  },
    returns = { { name = "enabled", type = "bool", canBeSecret = false } },
    midnightImpact = "NORMAL",
}

APIDefs["C_PhotoSharing.SetScreenshotPreviewTexture"] = {
    key = "C_PhotoSharing.SetScreenshotPreviewTexture",
    name = "SetScreenshotPreviewTexture",
    category = "combat_midnight",
    subcategory = "c_photosharing",
    func = _G["C_PhotoSharing"] and _G["C_PhotoSharing"]["SetScreenshotPreviewTexture"],
    funcPath = "C_PhotoSharing.SetScreenshotPreviewTexture",
    params = { { name = "textureObject", type = "SimpleTexture", default = nil } },
    returns = {  },
    midnightImpact = "RESTRICTED",
    protected = true,
    midnightNote = "Secret behavior: SecretArguments=AllowedWhenUntainted",
}

APIDefs["C_PhotoSharing.TakePhoto"] = {
    key = "C_PhotoSharing.TakePhoto",
    name = "TakePhoto",
    category = "general",
    subcategory = "c_photosharing",
    func = _G["C_PhotoSharing"] and _G["C_PhotoSharing"]["TakePhoto"],
    funcPath = "C_PhotoSharing.TakePhoto",
    params = {  },
    returns = {  },
    midnightImpact = "NORMAL",
}

APIDefs["C_PhotoSharing.UploadPhotoToService"] = {
    key = "C_PhotoSharing.UploadPhotoToService",
    name = "UploadPhotoToService",
    category = "combat_midnight",
    subcategory = "c_photosharing",
    func = _G["C_PhotoSharing"] and _G["C_PhotoSharing"]["UploadPhotoToService"],
    funcPath = "C_PhotoSharing.UploadPhotoToService",
    params = { { name = "optionalTitle", type = "cstring", default = "" }, { name = "optionalDescription", type = "cstring", default = "" } },
    returns = {  },
    midnightImpact = "RESTRICTED",
    protected = true,
    midnightNote = "Secret behavior: SecretArguments=AllowedWhenUntainted",
}
