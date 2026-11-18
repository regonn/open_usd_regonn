from pxr import Usd, UsdGeom

stage = Usd.Stage.Open("house.usda")
mesh = UsdGeom.Mesh.Get(stage, "/House")
points = mesh.GetPointsAttr().Get()
counts = mesh.GetFaceVertexCountsAttr().Get()
indices = mesh.GetFaceVertexIndicesAttr().Get()

print(f"{len(points)} points, {len(counts)} faces")
offset = 0
for face, count in enumerate(counts):
    print(f"face {face}: {list(indices[offset : offset + count])}")
    offset += count
