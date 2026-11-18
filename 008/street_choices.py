from pxr import Sdf, Usd, UsdGeom

street = Usd.Stage.CreateNew("street_choices.usda")
root = street.GetRootLayer()
root.subLayerPaths.append("./street.usda")
street.SetDefaultPrim(street.GetPrimAtPath("/Street"))
UsdGeom.SetStageUpAxis(street, UsdGeom.Tokens.y)

west = street.GetPrimAtPath("/Street/West/House")
west.GetReferences().SetReferences([Sdf.Reference("./house_choices.usda")])
east = street.GetPrimAtPath("/Street/East/House")
east.GetPayloads().SetPayloads([Sdf.Payload("./house_choices.usda")])
east.GetVariantSet("roofFinish").SetVariantSelection("ocean")
root.Save()
