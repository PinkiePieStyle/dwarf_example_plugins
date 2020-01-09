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

from PyQt5.QtWidgets import QMenu

from dwarf_debugger.lib.utils import (translate, show_message_box)

from dwarf_debugger.lib.types.consts import DwarfBreakpointType
from dwarf_debugger.lib.types.dwarf_breakpoint import DwarfBreakpoint
from dwarf_debugger.lib.types.dwarf_process_info import DwarfProcessInfo
from dwarf_debugger.lib.core.dwarf_core import DwarfCore
from dwarf_debugger.lib.core.dwarf_api import DwarfApi


class DwarfPlugin:
    # simple dwarfplugin

    # required - also shown in PluginAboutDialog
    # we have a german translation for the plugin so we extend plugin_info with 'languages'
    # pluginmanager loads translation from 'lang' subfolder
    plugin_info = {
        'name': 'Example',
        'description': 'Hello World example Plugin',
        'version': '1.0.0',
        'author': 'Dwarf',
        'homepage': 'https://github.com/iGio90/Dwarf',
        'license': 'https://www.gnu.org/licenses/gpl-3.0',
        'min_dwarf': '2.0.0',
        'languages': [
            'german'
        ]
    }

    @property
    def main_menu(self):
        """
            used on init
            populates the dwarf topmenu
        """
        return self._plugin_menu

    def __init__(self, dwarf_core:DwarfCore):
        super().__init__()

        # core
        self._dwarf_core:DwarfCore = dwarf_core
        # connect to coresync wich gives access to full data from sync
        self._dwarf_core.coreSync.connect(self._on_core_sync)

        # connect to breakpoints_manager
        self._breakpoints_manager = self._dwarf_core.breakpoints_manager
        self._breakpoints_manager.onChanged.connect(self._on_bpman_update)

        # dwarf_api
        self._dwarf_api:DwarfApi = self._dwarf_core.dwarf_api

        # at plugin->init() process_info in core is empty
        # after target is started and first coresync is done u can access process_info
        # or connect to onChanged an get infos then
        # Example: we want name and pid from debugged process so we connect to process_info
        self._dwarf_core.process_info.onChanged.connect(self._process_info_updated)

        # create main menu
        # dwarf is appending 'About' entry to this menu wich shows basic plugininfos
        self._plugin_menu = QMenu()
        self._plugin_menu.addAction('Hello World', self._on_hello_world)

        # create sub_menu DwarfTopMenu->Plugins->PluginName->SubMenu
        plugin_sub_menu = QMenu('SubMenu', self._plugin_menu)
        # DwarfTopMenu->Plugins->'Example'->'SubMenu'->'Hello World from SubMenu'
        plugin_sub_menu.addAction(
            'Hello World from SubMenu', self._on_hello_world)

        self._plugin_menu.addMenu(plugin_sub_menu)

    def _on_hello_world(self):
        # show MessageBox
        # we are using translate('what', 'english_fallback') here
        show_message_box(translate('hello_msg', 'Hello World'))

    def _on_core_sync(self, sync_data:dict):
        """
            * raw JS->PY syncdata

            Handling Breakpoints the harder way
        """
        # raw breakpoints
        if 'breakpoints' in sync_data:
            raw_breakpoints = sync_data['breakpoints']
            for raw_breakpoint in raw_breakpoints:
                if 'bpType' in raw_breakpoint:
                    if DwarfBreakpointType(raw_breakpoint['bpType']) == DwarfBreakpointType.NATIVE:
                        if 'bpEnabled' in raw_breakpoint and raw_breakpoint['bpEnabled']:
                            print('Breakpoint at: 0x{0:x}'.format(int(raw_breakpoint['bpAddress'], 16)))
                            # disable breakpoint
                            self._dwarf_api.disableBreakpoint(raw_breakpoint['bpID'])
                            if 'bpHits' in raw_breakpoint and raw_breakpoint['bpHits'] == 2:
                                # delete breakpoint
                                self._dwarf_api.removeBreakpoint(raw_breakpoint['bpID'])
                                # or
                                self._dwarf_api.removeBreakpointAtAddress(int(raw_breakpoint['bpAddress'], 16))

    def _on_bpman_update(self):
        """
            * Called when BreakpointsManager updates

            Handling Breakpoints from BreakpointsManager
        """
        dwarf_breakpoints = self._breakpoints_manager.dwarf_breakpoints
        for dwarf_breakpoint in dwarf_breakpoints:
            if dwarf_breakpoint.bp_type == DwarfBreakpointType.NATIVE:
                if dwarf_breakpoint.enabled:
                    print('Breakpoint at: 0x{0:x}'.format(dwarf_breakpoint.address))
                    # disable breakpoint
                    dwarf_breakpoint.enabled = False

                    if dwarf_breakpoint.hits == 2:
                        # delete breakpoint
                        dwarf_breakpoint.remove()

    def _process_info_updated(self):
        """
            process_info in dwarf_core has infos now
        """
        process_info:DwarfProcessInfo = self._dwarf_core.process_info
        print('Current Process: {0} - {1}'.format(process_info.name, process_info.process_id))
