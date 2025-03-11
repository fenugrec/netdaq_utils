# MC68k internal register definer
#
# (c) 2025 fenugrec
# GPLv3
#
# this goes a bit beyond the basic "ImportSymbolsScript"
#
# @category: Data

import csv
import os	#for os.path.join
import collections
import glob


#open definitions file and apply at base address
def define_regs(base, csv_filename):
    with open(csv_filename, 'rb') as f:
        reader = csv.DictReader(f)
        for row in reader:
            offs = int(row['base_offset'], base=16)
            regname = row['regname']

			# create as Primary label
            addr = toAddr(base + offs)
            createLabel(addr, regname, 1)
            setEOLComment(addr, row['comment'])


def get_builtin_defs():
#for some reason the "current directory" for open() is not the script's location.
    script_location = os.path.dirname(sourceFile.getAbsolutePath())
    flist = [os.path.basename(a) for a in glob.glob(os.path.join(script_location, '*.csv'))]
    fname = askChoice("register defs", "Select register definition CSV file", flist, flist[0])
    return os.path.join(script_location, fname)


def main():
    csvfile = get_builtin_defs()
    base = askInt("Base address", "base address of IO regs:")
    define_regs(base, csvfile)


if __name__ == "__main__":
  main()
