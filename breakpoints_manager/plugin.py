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
from dwarf_debugger.lib.core.dwarf_breakpoints_manager import DwarfBreakpointsManager
from dwarf_debugger.lib.types.dwarf_breakpoint import DwarfBreakpoint
from dwarf_debugger.lib.types.consts import DwarfBreakpointType


class DwarfPlugin:
    # simple dwarfplugin

    plugin_info = {
        'name': 'BreakpointsManager Example',
        'description': 'Simple BreakpointsManager usage example',
        'version': '1.0.0',
        'author': 'Dwarf',
        'homepage': 'https://github.com/iGio90/Dwarf',
        'license': 'https://www.gnu.org/licenses/gpl-3.0',
        'min_dwarf': '2.0.0'
    }

    def __init__(self, dwarf_core: DwarfCore):
        self._dwarf_core = dwarf_core
        self._bp_manager: DwarfBreakpointsManager = self._dwarf_core.breakpoints_manager
        self._bp_manager.onChanged.connect(self._on_breakpoints_changed)
        self._bp_manager.onBreakpoint.connect(self._on_breakpoint_hit)

    def _on_breakpoints_changed(self):
        for dwarf_breakpoint in self._bp_manager.dwarf_breakpoints:
            if dwarf_breakpoint.bp_type == DwarfBreakpointType.NATIVE:
                print('NativeBreakpoint at: ' + hex(dwarf_breakpoint.address))

    def _on_breakpoint_hit(self, dwarf_breakpoint: DwarfBreakpoint):
        if dwarf_breakpoint.bp_type == DwarfBreakpointType.NATIVE:
            print('Breaked at: ' + hex(dwarf_breakpoint.address))
            print('Breakpoint triggered: {0} times'.format(
                dwarf_breakpoint.hits))
