from pxr import Usd, UsdShade

stage = Usd.Stage.Open("street.usdz")
print("root:", stage.GetDefaultPrim().GetPath())
for side in ("West", "East"):
    path = f"/Street/{side}/House/RoofFaces"
    faces = stage.GetPrimAtPath(path)
    tile, _ = UsdShade.MaterialBindingAPI(faces).ComputeBoundMaterial()
    tint = tuple(round(v, 2) for v in tile.GetInput("tint").Get())
    years = tile.GetPrim().GetAttribute("study:serviceYears").Get()
    print(f"{side}: {tile.GetPrim().GetName()}, tint={tint}, years={years}")
