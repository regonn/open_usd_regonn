import sys
from pathlib import Path

from pxr import Ar, Sdf, Usd, UsdGeom, UsdShade

package = Path(sys.argv[1]).resolve()
archive = Sdf.ZipFile.Open(str(package))
names = archive.GetFileNames()
infos = [archive.GetFileInfo(name) for name in names]
print("first:", names[0])
print("files:", len(names), "bytes:", package.stat().st_size)
print("member bytes:", sum(i.size for i in infos))
print("stored:", all(i.compressionMethod == 0 for i in infos))
print("unencrypted:", all(not i.encrypted for i in infos))
print("aligned:", all(i.dataOffset % 64 == 0 for i in infos))

stage = Usd.Stage.Open(str(package))
print("root:", stage.GetDefaultPrim().GetPath())
for side in ("West", "East"):
    house = f"/Street/{side}/House"
    mesh = UsdGeom.Mesh.Get(stage, house)
    points_spec = mesh.GetPointsAttr().GetPropertyStack()[0]
    outer, inner = Ar.SplitPackageRelativePathOuter(points_spec.layer.realPath)
    if Path(outer) != package or inner != "geometry/house.usda":
        raise ValueError(f"Unexpected geometry source: {points_spec.layer.realPath}")
    faces = stage.GetPrimAtPath(house + "/RoofFaces")
    material, _ = UsdShade.MaterialBindingAPI(faces).ComputeBoundMaterial()
    tint = tuple(round(v, 2) for v in material.GetInput("tint").Get())
    print(f"{side}: {inner}, tint={tint}")
