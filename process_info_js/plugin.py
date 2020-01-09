"""
    Dwarf - Copyright (C) 2018-2020 Giovanni Rocca (iGio90)

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


class DwarfPlugin:
    # simple dwarfplugin

    # we extend plugin_info with our script to load 'script': 'path_to_script'
    plugin_info = {
        'name': 'ProcessInfo via JS Example',
        'description': 'Prints ProcessInfo from debugged process to console',
        'version': '1.0.0',
        'author': 'Dwarf',
        'homepage': 'https://github.com/iGio90/Dwarf',
        'license': 'https://www.gnu.org/licenses/gpl-3.0',
        'min_dwarf': '2.0.0',
        'script': 'plugin.js'
    }

    def __init__(self, dwarf_core: DwarfCore):
        # js only
        pass
