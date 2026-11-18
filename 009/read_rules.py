from pxr import Usd

stage = Usd.Stage.Open("street_rules.usda")


def show(label):
    print(label)
    for side in ("West", "East"):
        house = stage.GetPrimAtPath(f"/Street/{side}/House")
        tile = stage.GetPrimAtPath(str(house.GetPath()) + "/Looks/GlazedTile")
        finish = house.GetVariantSet("roofFinish").GetVariantSelection()
        color = tuple(round(v, 2) for v in tile.GetAttribute("inputs:tint").Get())
        years = tile.GetAttribute("study:serviceYears").Get()
        print(f"  {side}: {finish}, tint={color}, years={years}")


show("saved")
east_tile = stage.GetPrimAtPath("/Street/East/House/Looks/GlazedTile")
with Usd.EditContext(stage, stage.GetSessionLayer()):
    east_tile.GetInherits().SetInherits([])
    show("east without inherits")
    east_tile.GetInherits().ClearInherits()
show("restored")
