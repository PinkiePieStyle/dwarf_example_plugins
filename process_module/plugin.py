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

from dwarf_debugger.types.dwarf_module_info import DwarfModuleInfo
from dwarf_debugger.types.dwarf_module_import import DwarfModuleImport

from dwarf_debugger.types.dwarf_process_info import DwarfProcessInfo
from dwarf_debugger.core.dwarf_core import DwarfCore


class DwarfPlugin:
    # simple dwarfplugin

    plugin_info = {
        'name': 'ProcessModule Example',
        'description': 'Show ProcessImports',
        'version': '1.0.0',
        'author': 'Dwarf',
        'homepage': 'https://github.com/iGio90/Dwarf',
        'license': 'https://www.gnu.org/licenses/gpl-3.0',
        'min_dwarf': '2.0.0'
    }

    def __init__(self, dwarf_core: DwarfCore):
        # process_info is empty at __init__ so we must
        # connect to process_info onChanged wich is emitted
        # after core is attached to a process

        self._process_info: DwarfProcessInfo = dwarf_core.process_info
        # bad example but who cares
        # we print all imports as soon as possible
        self._process_info.onChanged.connect(self._process_info_updated)

    def _process_info_updated(self):
        # after processinfo is populated we have basic module_infos
        process_modules = self._process_info.modules

        # performance suxx but shows basic usage
        for process_module in process_modules:
            if process_module.name.lower() == self._process_info.name.lower():
                if process_module.imports:
                    # our target should have infos already
                    self._show_imports(process_module)
            else:
                # for other modules we connect to onChanged to show imports when they are populated
                process_module.onChanged.connect(self._show_imports)

    def _show_imports(self, dwarf_module_info: DwarfModuleInfo):
        if dwarf_module_info:
            print(
                'Imports for {0}\n---------------------------------------------'
                .format(dwarf_module_info.name))
            for module_import in dwarf_module_info.imports:
                print('Import {0} at {1}'.format(module_import.name,
                                                 hex(module_import.address)))

            # dwarf_module_info.exports
            # dwarf_module_info.symbols
