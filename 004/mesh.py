from pxr import Gf, Usd, UsdGeom

stage = Usd.Stage.CreateNew("house.usda")
UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.y)
mesh = UsdGeom.Mesh.Define(stage, "/House")
stage.SetDefaultPrim(mesh.GetPrim())

points = [
    Gf.Vec3f(-1, 0, 0),
    Gf.Vec3f(1, 0, 0),  # 0, 1: 壁の下端
    Gf.Vec3f(1, 2, 0),
    Gf.Vec3f(-1, 2, 0),  # 2, 3: 軒
    Gf.Vec3f(0, 3, 0),  # 4: 屋根の頂点
]
counts = [4, 3]
indices = [0, 1, 2, 3, 3, 2, 4]

valid, reason = UsdGeom.Mesh.ValidateTopology(indices, counts, len(points))
if not valid:
    raise ValueError(reason)

mesh.CreatePointsAttr(points)
mesh.CreateFaceVertexCountsAttr(counts)
mesh.CreateFaceVertexIndicesAttr(indices)
mesh.CreateSubdivisionSchemeAttr(UsdGeom.Tokens.none)

# 面の順番に合わせて壁と屋根に色を割り当てる
colors = mesh.CreateDisplayColorPrimvar(UsdGeom.Tokens.uniform)
colors.Set([Gf.Vec3f(0.15, 0.55, 0.85), Gf.Vec3f(0.9, 0.28, 0.1)])
stage.GetRootLayer().Save()
