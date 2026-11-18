from pathlib import Path

from pxr import Ar, Sdf

assembly = Sdf.Layer.FindOrOpen("scene/assembly.usda")
resolver = Ar.GetResolver()
library = Path("scene/geometry").resolve()
context = Ar.DefaultResolverContext([str(library)])
with Ar.ResolverContextBinder(context):
    for authored in ("./house.usda", "house.usda"):
        identifier = resolver.CreateIdentifier(authored, assembly.resolvedPath)
        resolved = resolver.Resolve(identifier)
        location = "(missing)"
        if resolved:
            path = Path(str(resolved))
            if path.is_relative_to(Path.cwd()):
                path = path.relative_to(Path.cwd())
            location = path.as_posix()
        print(f"{authored} -> {location}")
