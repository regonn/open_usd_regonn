import argparse

from pxr import Usd

parser = argparse.ArgumentParser()
parser.add_argument("target", choices=["reference", "tint"])
target = parser.parse_args().target

stage = Usd.Stage.Open("street_check.usda")
if target == "reference":
    west = stage.GetPrimAtPath("/Street/West/House")
    west.GetReferences().ClearReferences()
else:
    tile = stage.GetPrimAtPath("/Street/East/House/Looks/GlazedTile")
    tile.GetAttribute("inputs:tint").Clear()
stage.GetRootLayer().Save()
