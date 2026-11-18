from pathlib import Path

from pxr import Ar, Gf, Plug, Usd, UsdGeom, UsdLux, UsdRender, UsdShade

package = Path("street-final.usdz").resolve()
info = Path("streetInspection/resources/plugInfo.json").resolve()
Plug.Registry().RegisterPlugins(str(info))
assert Usd.SchemaRegistry().FindAppliedAPIPrimDefinition("StreetInspectionAPI")

stage = Usd.Stage.Open(str(package), load=Usd.Stage.LoadNone)
street = stage.GetDefaultPrim()
west = "/Street/West/House"
east = "/Street/East/House"
assert street.GetPath() == "/Street"
assert UsdGeom.Mesh.Get(stage, west)
assert not UsdGeom.Mesh.Get(stage, east)
print("LoadNone: west mesh=True, east mesh=False")
stage.Load(east)
assert UsdGeom.Mesh.Get(stage, east)
assert not stage.GetCompositionErrors()

roofs = Usd.CollectionAPI.Get(street, "roofs")
members = sorted(
    Usd.CollectionAPI.ComputeIncludedPaths(roofs.ComputeMembershipQuery(), stage)
)
assert [str(p) for p in members] == [east + "/RoofFaces", west + "/RoofFaces"]
for path in members:
    house = stage.GetPrimAtPath(path.GetParentPath())
    subset = stage.GetPrimAtPath(path)
    material, _ = UsdShade.MaterialBindingAPI(subset).ComputeBoundMaterial()
    status = house.GetAttribute("inspection:status").Get()
    days = house.GetAttribute("inspection:intervalDays").Get()
    assert material.GetPath() == house.GetPath().AppendPath("Looks/GlazedTile")
    is_west = str(house.GetPath()) == west
    expected_tint = (
        Gf.Vec3f(0.85, 0.52, 0.08) if is_west else Gf.Vec3f(0.42, 0.08, 0.56)
    )
    assert Gf.IsClose(material.GetInput("tint").Get(), expected_tint, 1e-5)
    assert status == ("passed" if is_west else "pending")
    assert days == 30
    print(house.GetPath(), material.GetPrim().GetName(), status, days)

view = street.GetVariantSets().GetVariantSet("reviewMode")
assert view.GetVariantSelection() == "inspection"
assert UsdGeom.Sphere.Get(stage, "/Street/West/Marker")
stage.SetEditTarget(stage.GetSessionLayer())
view.SetVariantSelection("beauty")
assert not stage.GetPrimAtPath("/Street/West/Marker")
view.SetVariantSelection("inspection")

dash = UsdGeom.Cube.Get(stage, "/Street/Road/Dash_4")
world = UsdGeom.XformCache().GetLocalToWorldTransform(dash.GetPrim())
assert Gf.IsClose(world.ExtractTranslation(), Gf.Vec3d(3.2, 0.01, 1), 1e-6)
(camera_path,) = (
    UsdRender.Settings.Get(stage, "/Render/Review").GetCameraRel().GetTargets()
)
assert UsdGeom.Camera.Get(stage, camera_path)
assert UsdLux.DistantLight.Get(stage, "/Shot/Sun").ComputeVisibility() == "inherited"
print("camera:", camera_path, "sun: visible")

for layer in stage.GetUsedLayers():
    if not layer.anonymous:
        outer, _ = Ar.SplitPackageRelativePathOuter(layer.realPath)
        assert Path(outer).resolve() == package, layer.identifier
print("All file-backed layers resolve in the delivered USDZ.")
