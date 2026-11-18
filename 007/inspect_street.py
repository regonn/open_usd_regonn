from pxr import Usd

stage = Usd.Stage.Open("street.usda", load=Usd.Stage.LoadNone)
east_path = "/Street/East/House"


def inspect(label):
    west_roof = stage.GetPrimAtPath("/Street/West/House/RoofFaces")
    east_house = stage.GetPrimAtPath(east_path)
    east_roof = stage.GetPrimAtPath(east_path + "/RoofFaces")
    print(
        f"{label}: westRoof={bool(west_roof)}, eastHouse={bool(east_house)}, "
        f"eastLoaded={east_house.IsLoaded()}, eastRoof={bool(east_roof)}"
    )


inspect("open")
stage.Load(east_path)
inspect("load")
stage.Unload(east_path)
inspect("unload")
