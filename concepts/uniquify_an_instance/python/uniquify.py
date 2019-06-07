#!/usr/bin/env python
# -*- coding: utf-8 -*-

# IMPORT THIRD-PARTY LIBRARIES
from pxr import Tf, Usd, UsdGeom


def main():
    """Run the main execution of the current script."""
    stage = Usd.Stage.CreateInMemory()

    master = "/MyPrim"

    instances = ["/AnotherPrim/InnerPrim1", "/AnotherPrim/InnerPrim2"]
    paths = ["/AnotherPrim", "/MyPrim/SomeSphere", master]

    for path in paths + instances:
        UsdGeom.Xform.Define(stage, path)

    for instance in instances:
        prim = stage.GetPrimAtPath(instance)
        prim.GetReferences().AddReference(
            stage.GetRootLayer().identifier, primPath="/MyPrim"
        )
        prim.SetInstanceable(True)
        prim.SetTypeName("Sphere")

    try:
        prim = stage.DefinePrim("/AnotherPrim/InnerPrim1/SomePrimThatWillNotExist")
    except Tf.ErrorException:
        # XXX : Because "/AnotherPrim/InnerPrim1" is an instance,
        # DefinePrim will raise an exception
        #
        print("EXCEPTION FOUND")

    stage.DefinePrim("/AnotherPrim/InnerPrim1").SetInstanceable(False)
    # XXX : We broke the instance so now it will not raise an exception
    # If you want to, you can also do `if not prim.IsInstance(): stage.DefinePrim`
    #
    prim = stage.DefinePrim("/AnotherPrim/InnerPrim1/SomePrimThatWillNotExist")


if __name__ == "__main__":
    main()
