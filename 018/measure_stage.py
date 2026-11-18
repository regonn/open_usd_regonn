import sys
from time import perf_counter

from pxr import Usd, UsdGeom, UsdUtils

start = perf_counter()
stage = Usd.Stage.Open(sys.argv[1], load=Usd.Stage.LoadAll)
elapsed_ms = (perf_counter() - start) * 1000
errors = stage.GetCompositionErrors()
if errors:
    raise RuntimeError(str(errors[0]))

stats = UsdUtils.ComputeUsdStageStats(stage)
blocks = stage.GetPrimAtPath("/Blocks")
roof = stage.GetPrimAtPath("/Blocks/Block_255/East/House/RoofFaces")
print(f"open_ms={elapsed_ms:.1f}")
print(
    "placements:", len(blocks.GetChildren()), "roof subset:", roof.IsA(UsdGeom.Subset)
)
print("primary prims:", stats["primary"]["primCounts"]["totalPrimCount"])
print("prototypes:", stats["prototypeCount"], "instances:", stats["totalInstanceCount"])
print("used layers:", stats["usedLayerCount"])
