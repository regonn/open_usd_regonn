from pxr import Gf, Sdf, Usd, UsdGeom, UsdShade

source = Sdf.Layer.FindOrOpen("house_materials.usda")
stage = Usd.Stage.CreateNew("assembly.usda")
root = stage.GetRootLayer()
look = Sdf.Layer.CreateNew("look.usda")
paint = Sdf.Layer.CreateNew("paint.usda")
root.subLayerPaths = ["paint.usda", "look.usda", "house.usda"]

mesh = UsdGeom.Mesh.Get(stage, "/House")
stage.SetDefaultPrim(mesh.GetPrim())
UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.y)

with Usd.EditContext(stage, look):
    Sdf.CreatePrimInLayer(look, "/House")
    for path in ("/House/Looks", "/House/RoofFaces"):
        Sdf.CopySpec(source, path, look, path)

    wall = UsdShade.Material.Get(stage, "/House/Looks/Plaster")
    binding = UsdShade.MaterialBindingAPI.Apply(mesh.GetPrim())
    binding.Bind(wall)
    binding.SetMaterialBindSubsetsFamilyType(UsdGeom.Tokens.nonOverlapping)

with Usd.EditContext(stage, paint):
    roof = UsdShade.Material.Get(stage, "/House/Looks/GlazedTile")
    roof.GetInput("tint").Set(Gf.Vec3f(0.6, 0.12, 0.05))

stage.Save()
