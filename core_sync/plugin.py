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

from dwarf_debugger.lib.types.dwarf_process_info import DwarfProcessInfo
from dwarf_debugger.lib.core.dwarf_core import DwarfCore


class DwarfPlugin:
    # simple dwarfplugin

    plugin_info = {
        'name': 'CoreSync Example',
        'description': 'Shows how to transfer stuff from js to py',
        'version': '1.0.0',
        'author': 'Dwarf',
        'homepage': 'https://github.com/iGio90/Dwarf',
        'license': 'https://www.gnu.org/licenses/gpl-3.0',
        'min_dwarf': '2.0.0',
        'script': 'plugin.js'
    }

    def __init__(self, dwarf_core: DwarfCore):
        self._dwarf_core = dwarf_core
        # connect to coreSync to get our data from script
        self._dwarf_core.coreSync.connect(self._on_core_sync)

    def _on_core_sync(self, sync_data: dict):
        if 'core_sync_plugin' in sync_data:
            from_plugin = sync_data['core_sync_plugin']
            if 'something' in from_plugin:
                print(from_plugin['something'])

            if 'processThreads' in from_plugin:
                if isinstance(from_plugin['processThreads'], list):
                    process_threads_data = from_plugin['processThreads']
                    for process_thread in process_threads_data:
                        if isinstance(process_thread, dict) and 'id' in process_thread:
                            print('Thread: {0}'.format(process_thread['id']))
