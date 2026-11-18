from pxr import Gf, Usd, UsdShade

asset = Usd.Stage.CreateNew("house_choices.usda")
house = asset.DefinePrim("/House")
house.GetReferences().AddReference("./assembly.usda")
asset.SetDefaultPrim(house)

finish = house.GetVariantSets().AddVariantSet("roofFinish")
colors = {"terracotta": (0.6, 0.12, 0.05), "ocean": (0.03, 0.16, 0.28)}
for name, color in colors.items():
    finish.AddVariant(name)
    finish.SetVariantSelection(name)
    with finish.GetVariantEditContext():
        tile = UsdShade.Material.Get(asset, "/House/Looks/GlazedTile")
        tile.GetInput("tint").Set(Gf.Vec3f(*color))

finish.SetVariantSelection("terracotta")
asset.GetRootLayer().Save()
