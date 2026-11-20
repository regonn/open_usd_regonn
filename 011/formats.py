from pxr import Sdf

print(sorted(Sdf.FileFormat.FindAllFileFormatExtensions()))
for ext in ("usda", "usdc", "usdz", "abc", "gltf"):
    print(ext, "->", Sdf.FileFormat.FindByExtension(ext))
