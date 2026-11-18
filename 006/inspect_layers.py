from pxr import Usd, UsdGeom, UsdShade

stage = Usd.Stage.Open("assembly.usda")
root = stage.GetRootLayer()
paint_id = root.ComputeAbsolutePath("paint.usda")


def show(label):
    layers = [layer.GetDisplayName() for layer in stage.GetLayerStack(False)]
    mesh = UsdGeom.Mesh.Get(stage, "/House")
    roof = UsdShade.Material.Get(stage, "/House/Looks/GlazedTile")
    tint = tuple(round(v, 2) for v in roof.GetInput("tint").Get())
    print(f"{label}: {' > '.join(layers)}")
    print(f"  tint={tint}, faces={list(mesh.GetFaceVertexCountsAttr().Get())}")


show("original")
stage.MuteLayer(paint_id)
show("muted")
stage.UnmuteLayer(paint_id)
show("unmuted")

original_order = list(root.subLayerPaths)
root.subLayerPaths = ["look.usda", "paint.usda", "house.usda"]
show("reordered")
root.subLayerPaths = original_order
