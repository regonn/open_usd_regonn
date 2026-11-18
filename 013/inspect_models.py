from pxr import Kind, Usd

stage = Usd.Stage.Open("street_models.usda")
print("assembly is a group:", Kind.Registry.IsA("assembly", "group"))
print("subcomponent is a component:", Kind.Registry.IsA("subcomponent", "component"))

for prim in stage.Traverse():
    kind = Usd.ModelAPI(prim).GetKind()
    if kind:
        print(
            f"{prim.GetPath()}: {kind}, model={prim.IsModel()}, group={prim.IsGroup()}"
        )

models = [str(prim.GetPath()) for prim in stage.Traverse(Usd.PrimIsModel)]
print("models:", ", ".join(models))

district = stage.GetPrimAtPath("/Street/East")
house = district.GetChild("House")
with Usd.EditContext(stage, stage.GetSessionLayer()):
    Usd.ModelAPI(district).SetKind(Kind.Tokens.component)
    print(
        "east house with component parent:",
        Usd.ModelAPI(house).GetKind(),
        house.IsModel(),
    )
    district.ClearMetadata("kind")
print("east house with group parent:", Usd.ModelAPI(house).GetKind(), house.IsModel())
