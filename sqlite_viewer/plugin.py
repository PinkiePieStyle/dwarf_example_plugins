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

import os

from PyQt5 import QtWidgets, QtSql

from dwarf_debugger.core.dwarf_core import DwarfCore
from dwarf_debugger.utils import get_main_window, home_path


class DwarfPlugin:
    """ DwarfPlugin
    """

    plugin_info = {
        'name': 'SQLiteViewer',
        'description': 'Simple SQLiteViewer',
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
        self._dwarf_core = dwarf_core
        self._dwarf_core.coreSync.connect(self._on_sync)

        self._sqlite_viewer = QtWidgets.QWidget()
        v_box = QtWidgets.QVBoxLayout()
        self._db_tables_combo = QtWidgets.QComboBox()
        self._db_view = QtWidgets.QTableView()
        v_box.addWidget(self._db_tables_combo)
        v_box.addWidget(self._db_view)
        self._sqlite_viewer.setLayout(v_box)

        self.db = QtSql.QSqlDatabase.addDatabase('QSQLITE')

    # ************************************************************************
    # **************************** Functions *********************************
    # ************************************************************************
    def _on_sync(self, sync_data: dict):
        if 'show_db' in sync_data:
            db_path = sync_data['show_db']
            if db_path and isinstance(db_path, str):
                try:
                    adb_class = self._dwarf_core.adb
                except:  # adb not available
                    return

                local_db_path = os.path.join(home_path(), '.tmp',
                                             os.path.basename(db_path))
                adb_class.pull(db_path, local_db_path)

                if os.path.isfile(local_db_path):
                    self._show_db(local_db_path)

    def _show_db(self, file_path):
        self.db.setDatabaseName(file_path)

        if not self.db.open():
            return

        main_window = get_main_window()
        if main_window:
            main_window.utils_dock.add_widget(self._sqlite_viewer,
                                              os.path.basename(file_path))

        for table in self.db.tables():
            self._db_tables_combo.addItem(table)

        self._db_tables_combo.currentTextChanged.connect(self._table_switched)

    def _table_switched(self, table_name):

        model = QtSql.QSqlTableModel(db=self.db)
        model.setTable(table_name)
        if not model.select():
            return

        self._db_view.setModel(model)
