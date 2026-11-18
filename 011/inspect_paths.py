from pathlib import Path

from pxr import Ar, Sdf, Usd

assembly = Sdf.Layer.FindOrOpen("scene/assembly.usda")
authored = next(p for p in assembly.subLayerPaths if Path(p).name == "house.usda")
resolver = Ar.GetResolver()
identifier = resolver.CreateIdentifier(authored, assembly.resolvedPath)
resolved = resolver.Resolve(identifier)

location = "(missing)"
if resolved:
    location = Path(str(resolved)).relative_to(Path.cwd()).as_posix()
print("authored:", authored)
print("resolved:", location)

stage = Usd.Stage.Open("scene/street_rules.usdc")
print("root:", stage.GetDefaultPrim().GetPath())
for side in ("West", "East"):
    prim = stage.GetPrimAtPath(f"/Street/{side}/House")
    counts = prim.GetAttribute("faceVertexCounts")
    values = counts.Get() if counts else None
    print(f"{side} faces:", list(values) if values is not None else [])
