from pathlib import Path
import importlib


class Plugin:
    __slots__ = ('module', 'name', 'usage')

    def __init__(self, module, name = None, usage = None):
        self.module = module
        self.name = name
        self.usage = usage

def load_plugin(module_name: Path) -> bool:
    try:
        module = importlib.import_module(module_name)
        name = getattr(module, "__plugin_name__", None)
        usage = getattr(module, '__plugin_usage__', None)
        load_plugins.add(Plugin(module, name, usage))
        return True
    except Exception as e:
        return False

