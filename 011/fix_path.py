from pxr import Sdf

assembly = Sdf.Layer.FindOrOpen("scene/assembly.usda")
index = assembly.subLayerPaths.index("./house.usda")
assembly.subLayerPaths[index] = "./geometry/house.usda"
assembly.Save()
