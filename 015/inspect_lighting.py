from pxr import Gf, Usd, UsdGeom, UsdLux

stage = Usd.Stage.Open("street_lighting.usda")
camera = UsdGeom.Camera.Get(stage, "/Shot/StreetCam")
optics = camera.GetCamera(Usd.TimeCode.Default())
print("horizontal FOV:", round(optics.GetFieldOfView(Gf.Camera.FOVHorizontal), 2))

houses = Usd.CollectionAPI.Get(stage.GetDefaultPrim(), "houses")
paths = Usd.CollectionAPI.ComputeIncludedPaths(houses.ComputeMembershipQuery(), stage)
print("houses:", ", ".join(str(path) for path in sorted(paths)))

for prim in stage.GetPrimAtPath("/Shot").GetChildren():
    if prim.HasAPI(UsdLux.LightAPI):
        light = UsdLux.LightAPI(prim)
        visibility = UsdGeom.Imageable(prim).ComputeVisibility()
        print(
            prim.GetName(),
            prim.GetTypeName(),
            light.GetIntensityAttr().Get(),
            visibility,
        )
