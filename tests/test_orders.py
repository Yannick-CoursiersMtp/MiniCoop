import importlib

import admin
import client
import coursier
import resto
import marketplace


def test_modules_importable():
    for module in (admin, client, coursier, resto, marketplace):
        assert importlib.reload(module) is not None
