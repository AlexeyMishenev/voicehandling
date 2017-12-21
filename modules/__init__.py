#!/usr/bin/python3
# -*- coding: utf-8 -*-
import glob
import os

modules = glob.glob(os.path.join(os.path.dirname(__file__), "*.py"))
__all__ = [os.path.basename(f)[:-3] for f in modules if not f.endswith("__init__.py")]

funcs = {}

for module in __all__:
    __import__('modules.{module}'.format(module=module), locals(), globals())
