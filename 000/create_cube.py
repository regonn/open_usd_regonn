from pathlib import Path
from tempfile import mkdtemp

import omni.usd
from pxr import Gf, Sdf, Usd, UsdGeom


def create_cube():
    stage = omni.usd.get_context().get_stage()
    if not stage:
        raise RuntimeError("Open a new stage in Kit before running this script.")

    cube = UsdGeom.Cube.Define(stage, "/World/Cube")
    cube.GetSizeAttr().Set(300)
    UsdGeom.XformCommonAPI(cube).SetTranslate(Gf.Vec3d(0, 0, 0))

    # 「Save Selected」と同様に、Cube だけを新しい USDA に書き出す。
    output = Path(mkdtemp(prefix="openusd-000-")) / "cube.usda"
    saved = Usd.Stage.CreateNew(str(output))
    root = UsdGeom.Xform.Define(saved, "/Root")
    saved.SetDefaultPrim(root.GetPrim())
    UsdGeom.SetStageUpAxis(saved, UsdGeom.GetStageUpAxis(stage))
    UsdGeom.SetStageMetersPerUnit(saved, UsdGeom.GetStageMetersPerUnit(stage))
    if not Sdf.CopySpec(
        stage.Flatten(), cube.GetPath(), saved.GetRootLayer(), "/Root/Cube"
    ):
        raise RuntimeError("Could not copy /World/Cube.")
    saved.GetRootLayer().Save()
    print(f"Saved: {output}")
    return output


create_cube()
