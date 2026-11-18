from pxr import Usd, UsdShade

stage = Usd.Stage.Open("street_choices.usda")
east = stage.GetPrimAtPath("/Street/East/House").GetVariantSet("roofFinish")


def show(label):
    print(label)
    for side in ("West", "East"):
        path = f"/Street/{side}/House"
        house = stage.GetPrimAtPath(path)
        selected = house.GetVariantSet("roofFinish").GetVariantSelection()
        tile = UsdShade.Material.Get(stage, path + "/Looks/GlazedTile")
        tint = tuple(round(v, 2) for v in tile.GetInput("tint").Get())
        print(f"  {side}: {selected} {tint}")


show("saved")
with Usd.EditContext(stage, stage.GetSessionLayer()):
    east.SetVariantSelection("terracotta")
    show("preview")
    east.ClearVariantSelection()
show("restored")
