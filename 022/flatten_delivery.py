from pathlib import Path

from pxr import Usd, UsdUtils

stage = Usd.Stage.Open("street_delivery.usda")
flat = stage.Flatten()
texture = Path("textures/sign.png").resolve()


def relative_texture(path):
    if Path(path).resolve() == texture:
        return "./textures/sign.png"
    return path


UsdUtils.ModifyAssetPaths(flat, relative_texture)
flat.Export("street_flat.usda")
