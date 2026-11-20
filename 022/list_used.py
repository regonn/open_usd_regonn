from pxr import Usd, UsdGeom

stage = Usd.Stage.Open("street_delivery.usda")
for layer in stage.GetUsedLayers():
    print(layer.identifier, "->", layer.realPath)

house = UsdGeom.Mesh.Get(stage, "/Street/West/House")
print("roof height:", house.GetPointsAttr().Get()[-1][1])
print("roof color:", tuple(round(v, 2) for v in house.GetDisplayColorAttr().Get()[1]))
