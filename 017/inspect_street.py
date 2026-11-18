import sys

from pxr import Usd, UsdGeom, UsdShade, UsdUtils

stage = Usd.Stage.Open(sys.argv[1])
stats = UsdUtils.ComputeUsdStageStats(stage)
types = stats["primary"]["primCountsByType"]
print("root:", stage.GetRootLayer().GetDisplayName())
print("direct sublayers:", list(stage.GetRootLayer().subLayerPaths))
print("composition errors:", len(stage.GetCompositionErrors()))
print("prims:", stats["totalPrimCount"], "meshes:", types.get("Mesh", 0))

west = stage.GetPrimAtPath("/Street/West/House")
print("west exists:", bool(west), "is mesh:", bool(west) and west.IsA(UsdGeom.Mesh))

roof = stage.GetPrimAtPath("/Street/East/House/RoofFaces")
material, _ = UsdShade.MaterialBindingAPI(roof).ComputeBoundMaterial()
print("east roof material:", material.GetPath())
tint = material.GetInput("tint").GetAttr()
print("resolved tint:", tint.Get())
defaults = [spec for spec in tint.GetPropertyStack() if spec.HasDefaultValue()]
for spec in defaults[:2]:
    print("  ", spec.layer.GetDisplayName(), spec.path, spec.default)
