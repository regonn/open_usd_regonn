import argparse

from pxr import Sdf, Usd

parser = argparse.ArgumentParser()
parser.add_argument("version", choices=("v1", "v2"), nargs="?", default="v2")
version = parser.parse_args().version

stage = Usd.Stage.Open("street_layout.usda")
house = stage.GetPrimAtPath("/Street/West/House")
house.GetReferences().SetReferences([Sdf.Reference(f"./house-{version}.usda")])
stage.GetRootLayer().Save()

stage = Usd.Stage.Open("street_layout.usda")
for layer in stage.GetUsedLayers():
    if f"house-{version}.usda" in layer.identifier:
        print("used:", layer.realPath)
