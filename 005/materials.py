from shutil import copyfile

from pxr import Gf, Sdf, Usd, UsdGeom, UsdShade


def make_material(stage, path, color, roughness):
    material = UsdShade.Material.Define(stage, path)
    shader = UsdShade.Shader.Define(stage, path + "/Surface")
    shader.CreateIdAttr("UsdPreviewSurface")

    tint = material.CreateInput("tint", Sdf.ValueTypeNames.Color3f)
    tint.Set(Gf.Vec3f(*color))
    diffuse = shader.CreateInput("diffuseColor", Sdf.ValueTypeNames.Color3f)
    diffuse.ConnectToSource(tint)
    shader.CreateInput("roughness", Sdf.ValueTypeNames.Float).Set(roughness)

    surface = shader.CreateOutput("surface", Sdf.ValueTypeNames.Token)
    material.CreateSurfaceOutput().ConnectToSource(surface)
    return material


copyfile("house.usda", "house_materials.usda")
stage = Usd.Stage.Open("house_materials.usda")
mesh = UsdGeom.Mesh.Get(stage, "/House")
UsdGeom.Scope.Define(stage, "/House/Looks")

wall = make_material(stage, "/House/Looks/Plaster", (0.8, 0.65, 0.42), 0.85)
roof = make_material(stage, "/House/Looks/GlazedTile", (0.03, 0.16, 0.28), 0.2)

binding = UsdShade.MaterialBindingAPI.Apply(mesh.GetPrim())
binding.Bind(wall)
roof_faces = binding.CreateMaterialBindSubset("RoofFaces", [1])
UsdShade.MaterialBindingAPI.Apply(roof_faces.GetPrim()).Bind(roof)

stage.GetRootLayer().Save()
