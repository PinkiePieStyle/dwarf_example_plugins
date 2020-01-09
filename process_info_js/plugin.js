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

console.log("ProcessInfo via JS Example: Script loaded");

// our script is loaded after core is attached so we have something to show on js side
var processInfo = Dwarf.getProcessInfo();
console.log(JSON.stringify(processInfo));

/*
    console shows something like this

    ProcessInfo via JS Example: Script loaded
    {
        "name":"target.exe",
        "spawned":true,
        "pid":2388,
        "threadId":15828,
        "architecture":1, // here: ARCH_X86 -> see Documentation or DwarfArch in dwarfcore/src/consts.ts
        "platform":1, // here: OS_WINDOWS -> see Documentation or DwarfPlatform in dwarfcore/src/consts.ts
        "page_size":4096,
        "pointer_size":4,
        "java_available":false,
        "objc_available":false
    }
*/
