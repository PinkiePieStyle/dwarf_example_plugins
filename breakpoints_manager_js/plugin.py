"""
    Dwarf - Copyright (C) 2019 Giovanni Rocca (iGio90)

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>
"""

from dwarf_debugger.lib.core.dwarf_core import DwarfCore
from dwarf_debugger.lib.core.dwarf_api import DwarfApi
from dwarf_debugger.lib.core.dwarf_breakpoints_manager import DwarfBreakpointsManager


class DwarfPlugin:
    # simple dwarfplugin

    # we extend plugin_info with our script to load 'script': 'path_to_script'
    plugin_info = {
        'name': 'BreakpointsManager via JS Example',
        'description': 'Simple BreakpointsManager usage example',
        'version': '1.0.0',
        'author': 'Dwarf',
        'homepage': 'https://github.com/iGio90/Dwarf',
        'license': 'https://www.gnu.org/licenses/gpl-3.0',
        'min_dwarf': '2.0.0',
        'script': 'plugin.js'
    }

    def __init__(self, dwarf_core: DwarfCore):
        # for example only
        # we connect to onBreakpoint to execute our scriptfunction from pyside later
        # wich ensures there are breakpoints to show
        self._dwarf_core = dwarf_core
        self._bp_manager: DwarfBreakpointsManager = self._dwarf_core.breakpoints_manager
        self._bp_manager.onBreakpoint.connect(self._on_breakpoint_hit)

    def _on_breakpoint_hit(self):
        dwarf_api: DwarfApi = self._dwarf_core.dwarf_api
        dwarf_api.evaluateFunction('list_breakpoints()')
        """
            shows something like this in console
            06:10:59 [JS TRACE] -> list_breakpoints()
            06:10:59 [JS TRACE] -> DwarfCore::disableDebug()
            Breakpoint at: 0x1001644 triggered: 1 times
        """
