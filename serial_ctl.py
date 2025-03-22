#!/usr/bin/env python3

# funcs to interact with fluke 2640/2645 over serial port.
# Note, these do not expose any logging functionality on this port, only 'admin'
# functions like calibration and low level information.
#
# This needs pyserial

import argparse
import serial
import io
import struct
import collections


def wait_prompt(ser):
    p = ser.readline().rstrip(b'\r\n')  #purge prompt
    # could be '!>', '=>', or '?>'
    if p == b'=>':
        #print("reply OK")
        return 1
    return 0


cal_entry = collections.namedtuple('cal_entry', 'id func name')
cal_tbl = [
    cal_entry(0,"VDC","90 mV Gain"),
    cal_entry(2,"VDC","90 mV Offset"),
    cal_entry(4,"VDC","300 mV Gain"),
    cal_entry(6,"VDC","300 mV Offset"),
    cal_entry(8,"VDC","3V Gain"),
    cal_entry(10,"VDC","3V Offset"),
    cal_entry(12,"VDC","30V Gain"),
    cal_entry(14,"VDC","30V Offset"),
    cal_entry(16,"VDC","50V/150/300V Gain"),
    cal_entry(18,"VDC","50V/150/300V Offset"),
    cal_entry(20,"VDC","750 mV Gain"),
    cal_entry(22,"VDC","750 mV Offset"),
    cal_entry(24,"VAC","300 mV Gain"),
    cal_entry(26,"VAC","300 mV Offset"),
    cal_entry(28,"VAC","3V Gain"),
    cal_entry(30,"VAC","3V Offset"),
    cal_entry(32,"VAC","30V Gain"),
    cal_entry(34,"VAC","30V Offset"),
    cal_entry(36,"VAC","150/300 V (2640A)"),
    cal_entry(38,"VAC","150/300 V (2640A)"),
    cal_entry(40,"Res","300Ω Gain"),
    cal_entry(42,"Res","300Ω Offset"),
    cal_entry(44,"Res","3 kΩ Gain"),
    cal_entry(46,"Res","3 kΩ Offset"),
    cal_entry(48,"Res","30 kΩ Gain"),
    cal_entry(50,"Res","30 kΩ Offset"),
    cal_entry(52,"Res","300 kΩ Gain"),
    cal_entry(54,"Res","300 kΩ Offset"),
    cal_entry(56,"Res","3 MΩ Gain"),
    cal_entry(58,"Res","3 MΩ Offset"),
    cal_entry(60,"Freq","CFC"),
]

# semi-gross : convert into a dict so we can use the cal_id as Key
cald={x.id:x for x in cal_tbl}


def get_cal_const(ser, id):
    if (id & 1):
        print("error : const ID must be even")
        return
    if (id > 60):
        print("error: const ID out of range")
        return

    ser.write(f"CAL_CONST? {id}\n".encode("ascii"))
    # reply should be two lines : one with the constant like "+1.0000E+0"
    # and then the 'prompt' "=>"
    r = ser.readline().rstrip(b'\r\n')
#    print(f"got string: {r}")
    fval = float(r)
    # this value was produced from a 32-bit float. Try to recover original binary value
    bval = struct.pack('>f', fval)
    if wait_prompt(ser):
#        print(f"got {fval}, {bval}")
        return (fval, bval)

def dump_cal(ser):
    print("******* WARNING *******\n"
          "The firwmare only gives us a decimal string representation of the 32-bit float constants;\n"
          "we try to recover the original raw data but it is a lossy process due to rounding.\n"
          "Actual raw data may be different by a few LSbits. AFAIK there is no way to\n"
          "retrieve the raw data via RS232.")
    for a in range(0,61,2):
        (f, b) = get_cal_const(ser, a)
        c=cald[a]
        print(f"const {a:02}:{f:< 10}\t{c.func}\t{c.name:25}\t(raw data possibly {int.from_bytes(b):08X})")


def reboot(ser):
    ser.write(b"autarch;reboot\n")


def main():
    parser = argparse.ArgumentParser(description="Fluke NetDAQ 2640/2645 serial control tool")
    parser.add_argument('action', choices=['d','r'], help='[d]ump cal, or [r]eboot')
    parser.add_argument('-p', '--port', required=True, help='serial port name e.g. /dev/ttyUSB0')
    parser.add_argument('-o', '--output', type=argparse.FileType('w'), help='Output file for cal constants')
    args = parser.parse_args()

    port=args.port
    action=args.action
    calfile=args.output

    with serial.Serial(port, 19200, timeout=3) as ser:
# this IOwrapper garbage doesn't work
#    sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))
#    sio.write("*IDN?\n")
#    sio.flush()
        ser.write(b"*IDN?\n")
        ver = ser.readline().rstrip(b'\r\n')
        wait_prompt(ser)
        print(f"connected to: {ver}")
        if action=='r':
            reboot(ser)
            return
        elif action=='d':
            dump_cal(ser)

if __name__ == '__main__':
        main()

