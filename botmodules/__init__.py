import importlib

print("Cargando modulos...")

modules = list()
modules.append("start")
modules.append("utils")
modules.append("admin")

for m in modules:
    print("\t {}...".format(m))
    importlib.import_module('botmodules.' + m)
