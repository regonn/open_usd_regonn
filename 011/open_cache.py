from pathlib import Path

from pxr import Sdf, Tf, Usd

path = str(Path("houses.abc").resolve(strict=True))
for label, open_file in [("Layer", Sdf.Layer.FindOrOpen), ("Stage", Usd.Stage.Open)]:
    try:
        result = open_file(path)
    except Tf.ErrorException as error:
        print(label, error)
    else:
        print(label, result)
