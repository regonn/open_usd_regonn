from pxr import Usd

stage = Usd.Stage.Open("street_delivery.usda")
panel = "/Street/Billboard/Panel"
stage.Unload("/Street/Billboard")
print("unloaded:", bool(stage.GetPrimAtPath(panel)))
stage = Usd.Stage.Open("street_delivery.usda")
print("reopened:", bool(stage.GetPrimAtPath(panel)))

stage.GetRootLayer().Export("street_no_billboard.usda")
copy = Usd.Stage.Open("street_no_billboard.usda")
copy.GetPrimAtPath("/Street/Billboard").GetPayloads().ClearPayloads()
copy.GetRootLayer().Save()
copy = Usd.Stage.Open("street_no_billboard.usda")
print("payload cleared:", bool(copy.GetPrimAtPath(panel)))
