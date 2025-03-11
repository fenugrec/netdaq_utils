Internal register defs loader for MC68302 and similar.

(c) fenugrec 2025
GPLv3

# Intro
This could work on other mc68k processors where a set of internal MMIO registers can be mapped to various addresses; the datasheet documents these in a table with each reg being at "Base + X". The value of 'Base' can vary accross hardware.

Example:
base = 0x40 0000
watchdog register 'WRR' is at base+84A, thus 0x40 084A.

This script will prompt for the Base value and define registers.

# Assumptions
- csv file with register defs, placed in script dir. This could be improved
- memory region already created in ghidra (don't forget to mark Volatile)

# Expanding / adding support
The raw data for vectors and registers are stored in .csv files.

Feel free to expand or improve this, PR's are more than welcome.

# Using
The cleanest way is to use this script as the very first step after importing the .bin file.
1. Open Script Manager
2. One of the buttons top-right is "Manage Script directories"
3. Add the directory containing this script.
4. Refresh the list of scripts, this should appear in one of the categories. Search for 'mc68'
5. Run script

