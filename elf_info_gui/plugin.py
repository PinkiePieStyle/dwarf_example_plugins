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
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem

from dwarf_debugger.types.consts import DwarfPlatform
from dwarf_debugger.types.dwarf_process_info import DwarfProcessInfo
from dwarf_debugger.core.dwarf_core import DwarfCore
from dwarf_debugger.core.dwarf_api import DwarfApi
from dwarf_debugger.ui.lists.dwarf_listview import DwarfListView
from dwarf_debugger.utils import get_main_window


class DwarfPlugin:
    """ DwarfPlugin
    """

    plugin_info = {
        'name': 'ElfInfo',
        'description': 'Shows Infos from ELFParser in ui',
        'version': '1.0.0',
        'author': 'Dwarf',
        'homepage': 'https://github.com/iGio90/Dwarf',
        'license': 'https://www.gnu.org/licenses/gpl-3.0',
        'min_dwarf': '2.0.0',
        'script': 'plugin.js'
    }

    # ************************************************************************
    # **************************** Init **************************************
    # ************************************************************************
    def __init__(self, dwarf_core: DwarfCore):
        # process_info is empty at __init__ so we must
        # connect to process_info onChanged wich is emitted
        # after core is attached to a process

        self._process_info: DwarfProcessInfo = dwarf_core.process_info
        self._process_info.onChanged.connect(self._process_info_updated)

        self._dwarf_api: DwarfApi = dwarf_core.dwarf_api
        dwarf_core.coreSync.connect(self._on_sync)

        self._main_widget = DwarfListView(search_enabled=False)

        self._init_ui()

    def _init_ui(self):
        self._main_widget.setRootIsDecorated(True)
        self._main_widget.setExpandsOnDoubleClick(True)

        self._elf_mdl = QStandardItemModel(0, 2)
        self._elf_mdl.setHeaderData(0, Qt.Horizontal, 'Name')
        self._elf_mdl.setHeaderData(1, Qt.Horizontal, 'Value')
        self._main_widget.setModel(self._elf_mdl)

        main_window = get_main_window()
        if main_window:
            main_window.utils_dock.add_widget(self._main_widget, 'ELFInfo')


    # ************************************************************************
    # **************************** Functions *********************************
    # ************************************************************************
    def _process_info_updated(self):
        if self._process_info.platform == DwarfPlatform.OS_LINUX:
            self._main_widget.clear()

            self._elf_mdl.insertRow(
                0, [QStandardItem('File'),
                    QStandardItem(self._process_info.name)])

    def _on_sync(self, sync_data: dict):
        if 'elf_info' in sync_data and isinstance(sync_data['elf_info'], dict):
            self._process_data(sync_data['elf_info'])

    def on_script_loaded(self, loaded:bool):
        if loaded:
            self._dwarf_api.evaluateFunction('parse_elf_file()')

    def _process_data(self, elf_info_json: dict):
        parent_item = self._elf_mdl.item(0)

        ident_titles = [
            'EI_MAG0', 'EI_MAG1', 'EI_MAG2', 'EI_MAG3', 'EI_CLASS', 'EI_DATA',
            'EI_VERSION', 'EI_OSABI', 'EI_ABIVERSION', 'EI_PAD'
        ]

        if 'endian' in elf_info_json:
            parent_item.appendRow([
                QStandardItem('Endian'),
                QStandardItem(elf_info_json['endian'])
            ])

        if 'is64bit' in elf_info_json:
            txt = 'No'
            if elf_info_json['is64bit']:
                txt = 'Yes'
            parent_item.appendRow([QStandardItem('64Bit'), QStandardItem(txt)])

        if 'header' in elf_info_json:
            elf_header = QStandardItem('ELF Header')
            parent_item.appendRow([elf_header])
            for entry in elf_info_json['header']:
                if entry == 'e_ident':
                    ident_item = QStandardItem(entry)
                    ident_value = QStandardItem(str(elf_info_json['header'][entry]))
                    elf_header.appendRow([ident_item, ident_value])
                    counter = 0
                    for i in elf_info_json['header'][entry]:
                        if counter >= len(ident_titles):
                            counter = len(ident_titles) - 1
                        ident_item.appendRow([
                            QStandardItem(ident_titles[counter]),
                            QStandardItem(str(i))
                        ])
                        counter += 1
                else:
                    elf_header.appendRow([
                        QStandardItem(entry),
                        QStandardItem(hex(elf_info_json['header'][entry]))
                    ])

        if 'programheaders' in elf_info_json:
            prog_headers_item = QStandardItem('Program Headers')
            parent_item.appendRow([prog_headers_item])
            i = 1
            for header in elf_info_json['programheaders']:
                header_item = QStandardItem("%d" % i)
                prog_headers_item.appendRow([header_item])
                i += 1
                for entry in header:
                    header_item.appendRow([
                        QStandardItem(entry),
                        QStandardItem(hex(header[entry]))
                    ])

        if 'sectionheaders' in elf_info_json:
            sect_headers = QStandardItem('Section Headers')
            parent_item.appendRow([sect_headers])
            i = 1
            for header in elf_info_json['sectionheaders']:
                txt = header['name']
                if not txt:
                    txt = 'NULL'
                header_item = QStandardItem(txt)
                sect_headers.appendRow([header_item])
                i += 1
                for entry in header:
                    if entry == 'name':
                        continue
                    elif entry == 'data' and header[entry]:
                        data_item = QStandardItem('Data')
                        header_item.appendRow(data_item)
                        base = 0

                        for process_module in self._process_info.modules:
                            if process_module.name.lower() == self._process_info.name.lower():
                                base = process_module.base_address
                                break

                        for ptr in header[entry]:
                            if int(ptr):
                                virtual_address = hex(int(base, 16) + int(ptr))
                                file_offset = hex(int(ptr))
                                if self._main_widget.uppercase_hex:
                                    virtual_address = virtual_address.upper().replace('0X', '0x')
                                    file_offset = file_offset.upper().replace('0X', '0x')

                                data_item.appendRow([
                                    QStandardItem(virtual_address),
                                    QStandardItem('FileOffset: ' + file_offset)
                                ])
                    else:
                        header_item.appendRow([QStandardItem(entry), QStandardItem(hex(header[entry]))])

            self._main_widget.expandAll()
            self._main_widget.resizeColumnToContents(0)
            self._main_widget.resizeColumnToContents(1)
            self._main_widget.collapseAll()
            self._main_widget.expandToDepth(1)
