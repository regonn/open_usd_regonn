from pxr import Gf, Usd

stage = Usd.Stage.Open("release-src/street_rules.usdc")
district = stage.GetPrimAtPath("/DistrictTile")
district.GetAttribute("inputs:tint").Set(Gf.Vec3f(0.42, 0.08, 0.56))
stage.GetRootLayer().Save()
