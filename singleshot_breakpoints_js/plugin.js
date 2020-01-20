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

var dwarfApi = Dwarf.getApi();

/*
create Breakpoint
var dwarfBreakpoint = Dwarf.getBreakpointManager().addNativeBreakpoint(findExport('open'));
var dwarfBreakpoint = dwarfApi.addNativeBreakpoint(findExport('open'));
var dwarfBreakpoint = addBreakpoint('native', findExport('open'));
*/
var dwarfBreakpoint = dwarfApi.addBreakpoint('native', findExport('open'));

if (isDefined(dwarfBreakpoint)) {
    if (!dwarfBreakpoint.isSingleShot()) {
        dwarfBreakpoint.setSingleShot(true);
    }
    console.log('SingleShot breakpoint created');
}