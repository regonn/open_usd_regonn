import argparse
from pathlib import Path

from pxr import Plug, Usd

parser = argparse.ArgumentParser()
parser.add_argument("--register", action="store_true")
args = parser.parse_args()
if args.register:
    info = Path("streetInspection/resources/plugInfo.json").resolve()
    Plug.Registry().RegisterPlugins(str(info))

schema = "StreetInspectionAPI"
definition = Usd.SchemaRegistry().FindAppliedAPIPrimDefinition(schema)
print("schema known:", bool(definition))
stage = Usd.Stage.Open("street_inspection.usda")
for side in ("West", "East"):
    house = stage.GetPrimAtPath(f"/Street/{side}/House")
    status = house.GetAttribute("inspection:status")
    days = house.GetAttribute("inspection:intervalDays")
    print(
        side,
        house.GetTypeName(),
        status.Get() if status else None,
        days.Get() if days else None,
    )
