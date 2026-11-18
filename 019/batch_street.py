import argparse
import csv
import sys
from math import dist
from pathlib import Path

from pxr import Gf, Tf, Usd, UsdGeom, UsdShade, UsdUtils


def inspect_stage(path):
    row: dict[str, str | int] = {"file": str(path), "status": "FAIL"}
    try:
        stage = Usd.Stage.Open(str(path), load=Usd.Stage.LoadAll)
        errors = stage.GetCompositionErrors()
        row["composition_errors"] = len(errors)
        if errors:
            for error in errors:
                print(f"{path}: {error}", file=sys.stderr)
            row["reason"] = str(errors[0]).splitlines()[0]
            return row

        stats = UsdUtils.ComputeUsdStageStats(stage)
        row["primary_prims"] = stats["primary"]["primCounts"]["totalPrimCount"]
        row["instances"] = stats["totalInstanceCount"]

        west = UsdGeom.Mesh.Get(stage, "/Street/West/House")
        roof = stage.GetPrimAtPath("/Street/East/House/RoofFaces")
        material = (
            UsdShade.MaterialBindingAPI(roof).ComputeBoundMaterial()[0]
            if roof
            else None
        )
        tint = material.GetInput("tint").Get() if material else None
        if not west:
            row["reason"] = "Missing west house mesh"
        elif not isinstance(tint, Gf.Vec3f) or dist(tint, (0.42, 0.08, 0.56)) > 0.0001:
            row["reason"] = "Unexpected east roof tint"
        else:
            row["status"] = "PASS"
    except Tf.ErrorException as error:
        print(f"{path}: {error}", file=sys.stderr)
        row["reason"] = "OpenUSD error (see stderr)"
    return row


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("roots", type=Path, nargs="+")
    parser.add_argument("--export", action="store_true")
    args = parser.parse_args()
    if args.export and any(path.suffix.lower() != ".usda" for path in args.roots):
        parser.error("--export expects USDA roots")

    rows = [inspect_stage(path) for path in args.roots]
    columns = [
        "file",
        "status",
        "composition_errors",
        "primary_prims",
        "instances",
        "reason",
    ]
    with Path("report.csv").open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)

    failed = sum(row["status"] == "FAIL" for row in rows)
    print(f"PASS={len(rows) - failed} FAIL={failed}")
    if failed:
        return 1

    if args.export:
        for path in args.roots:
            output = path.with_suffix(".review.usdc")
            stage = Usd.Stage.Open(str(path))
            if not stage.GetRootLayer().Export(str(output)):
                raise RuntimeError(f"Export failed: {output}")
            print(f"exported {output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
