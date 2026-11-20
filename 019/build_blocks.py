from pxr import Gf, Kind, Usd, UsdGeom

for filename, share in (("blocks_plain.usda", False), ("blocks_shared.usda", True)):
    stage = Usd.Stage.CreateNew(filename)
    stage.GetRootLayer().subLayerPaths.append("./street_check.usda")
    blocks = UsdGeom.Xform.Define(stage, "/Blocks")
    Usd.ModelAPI(blocks.GetPrim()).SetKind(Kind.Tokens.group)
    stage.SetDefaultPrim(blocks.GetPrim())
    UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.y)
    UsdGeom.SetStageMetersPerUnit(stage, 0.01)
    for i in range(256):
        block = UsdGeom.Xform.Define(stage, f"/Blocks/Block_{i:03d}")
        prim = block.GetPrim()
        prim.GetReferences().AddInternalReference("/Street")
        prim.SetInstanceable(share)
        block.AddTranslateOp().Set(Gf.Vec3d(8 * (1 + i % 16), 0, -6 * (i // 16)))
    stage.GetRootLayer().Save()
