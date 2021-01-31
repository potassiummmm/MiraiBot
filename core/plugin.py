from pathlib import Path
import importlib

loaded_plugins = set()
plugin_dir_setting = set()


class Plugin:
    __slots__ = ('module', 'name', 'usage')

    def __init__(self, module, name=None, usage=None):
        self.module = module
        self.name = name
        self.usage = usage


def load_plugin(module_name: str) -> bool:
    try:
        module = importlib.import_module(module_name)
        name = getattr(module, "__plugin_name__", None)
        usage = getattr(module, '__plugin_usage__', None)
        loaded_plugins.add(Plugin(module, name, usage))
        return True
    except Exception as e:
        print(e)
        return False


class PluginDir:
    __slots__ = 'dir_name'

    def __init__(self, dir_name):
        self.dir_name = dir_name


def load_plugins(plugin_dir: Path) -> int:
    count = 0
    plugin_dir_setting.add(PluginDir('.'.join(plugin_dir.parts)))
    for path in plugin_dir.iterdir():
        if path.name.startswith('_'):
            continue
        if path.is_file() and path.suffix != '.py':
            continue
        if path.is_dir() and not (path / '__init__.py').exists():
            continue
        if load_plugin(f'{".".join(plugin_dir.parts)}.{path.stem}'):
            count += 1
    return count
