from pxr import Usd, UsdShade

stage = Usd.Stage.Open("house_materials.usda")
for path in ("/House", "/House/RoofFaces"):
    prim = stage.GetPrimAtPath(path)
    material, _ = UsdShade.MaterialBindingAPI(prim).ComputeBoundMaterial()
    shader, _, _ = material.ComputeSurfaceSource()
    roughness = shader.GetInput("roughness").Get()
    print(
        f"{path} -> {material.GetPath()} ({shader.GetIdAttr().Get()}, {roughness:.2f})"
    )
