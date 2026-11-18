from pxr import Usd

stage = Usd.Stage.Open("street_collections.usda")
street = stage.GetDefaultPrim()
for name in ("houses", "roofs", "westSurvey"):
    collection = Usd.CollectionAPI.Get(street, name)
    query = collection.ComputeMembershipQuery()
    members = Usd.CollectionAPI.ComputeIncludedPaths(query, stage)
    print(collection.GetCollectionPath())
    for path in sorted(members):
        print("  " + str(path))

survey = Usd.CollectionAPI.Get(street, "westSurvey")
print("includes:", [str(p) for p in survey.GetIncludesRel().GetTargets()])
