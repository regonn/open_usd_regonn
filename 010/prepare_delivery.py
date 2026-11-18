from pathlib import Path

from pxr import Sdf, Usd, UsdGeom

# その6で同じフォルダに保存した3枚のサブレイヤー
assembly = Sdf.Layer.FindOrOpen("assembly.usda")
assembly.subLayerPaths = ["./" + Path(p).as_posix() for p in assembly.subLayerPaths]
assembly.Save()

stage = Usd.Stage.Open("street_rules.usdc")
UsdGeom.SetStageMetersPerUnit(stage, UsdGeom.GetStageMetersPerUnit(stage))
stage.GetRootLayer().Save()
