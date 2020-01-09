"""
    DwarfPluginTemplate
"""

from dwarf_debugger.lib.utils import (translate, dwarf_log, is_core)
from dwarf_debugger.lib.types.consts import DwarfLogType
from dwarf_debugger.lib.core.dwarf_core import DwarfCore
from dwarf_debugger.lib.core.dwarf_api import DwarfApi


class DwarfPlugin:
    """ DwarfPlugin
    """

    # required
    plugin_info = {
        'name': '',
        'description': '',
        'version': '1.0.0',
        'author': '',
        'homepage': '',
        'license': '',
        'min_dwarf': '2.0.0',
        'script': 'plugin.js',
        'languages': [

        ]
    }

    def __init__(self, dwarf_core):
        if not is_core(dwarf_core):
            dwarf_log(DwarfLogType.ERROR, 'No DwarfCore')
            raise Exception(self.plugin_info['name'] + ': init() failed')

        self._dwarf_core: DwarfCore = dwarf_core
        self._dwarf_api: DwarfApi = self._dwarf_core.dwarf_api

        # UserCode

