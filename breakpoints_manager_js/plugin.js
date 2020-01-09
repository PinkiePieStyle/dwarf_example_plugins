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

console.log("BreakpointsManager via JS Example: Script loaded");

var dwarfBreakpointsManager = Dwarf.getBreakpointManager();

function list_breakpoints() {
    //we enable debugmode here to show output
    Dwarf.enableDebug();

    //trace logs to console when Dwarf is in DebugMode
    trace("list_breakpoints()"); //shows 05:58:48 [JS TRACE] -> list_breakpoints()

    //disable debugmode
    Dwarf.disableDebug();

    //now real example
    var dwarfBreakpoints = dwarfBreakpointsManager.getBreakpoints();
    dwarfBreakpoints.forEach(function (dwarfBreakpoint) {
        console.log("Breakpoint at: " + dwarfBreakpoint.getAddress() + " triggered: " + dwarfBreakpoint.getHits() + " times");
    });
}

//DIRTY: move to global
global.list_breakpoints = list_breakpoints;

//TODO: show correct usage via Dwarf.registerGlobalFunction()
/*
    function list_breakpoints() {

    }

    //make our function available
    //throws error if function already exists
    Dwarf.registerGlobalFunction(list_breakpoints);

*/
