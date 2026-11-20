import argparse

from pxr import Sdf, UsdUtils

parser = argparse.ArgumentParser()
parser.add_argument("file", nargs="?", default="street_delivery.usda")
path = parser.parse_args().file
layer = Sdf.Layer.FindOrOpen(path)
print("layer deps:", sorted(layer.GetExternalReferences()))

sublayers, references, payloads = UsdUtils.ExtractExternalReferences(path)
print("sublayers:", sublayers)
print("references+assets:", references)
print("payloads:", payloads)
