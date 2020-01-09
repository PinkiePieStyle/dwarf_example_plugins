/**
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
**/

global.parse_elf_file = function() {
    var mainProc = Process.findModuleByName(Dwarf.getProcessInfo().name);
    if (isDefined(mainProc) && isString(mainProc.path)) {
        try {
            var elfFile = new ELF_File(mainProc.path);
            if (isDefined(elfFile)) {
                Dwarf.sync({ elf_info: elfFile });
            }
        } catch (error) {
            console.log(error);
        }
    }
};
