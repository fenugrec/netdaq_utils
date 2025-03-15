#
# funcs to interact with fluke 2640/2645 over serial port.
# Note, they don't expose any logging functionality on this port, only 'admin'
# functions like calibration and low level information.
#
# This needs pyserial

import sys
import argparse
import serial
import io
import struct

parser = argparse.ArgumentParser(description="Fluke NetDAQ 2640/2645 serial control tool")
parser.add_argument('-p', '--port', required=True, help='serial port name e.g. /dev/ttyUSB0')
parser.add_argument('-o', '--output', type=argparse.FileType('w'), help='Output file for cal constants')
args = parser.parse_args(sys.argv[1:])

port=args.port
calfile=args.output

def wait_prompt(ser):
    p = ser.readline().rstrip(b'\r\n')  #purge prompt
    # could be '!>', '=>', or '?>'
    if p == b'=>':
        #print("reply OK")
        return 1
    return 0


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
    bval = struct.pack('f', fval)
    if wait_prompt(ser):
        print(f"got {fval}, {bval}")
        return (fval, bval)


with serial.Serial(port, 19200, timeout=3) as ser:
    # this IOwrapper garbage doesn't work
#    sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))
#    sio.write("*IDN?\n")
#    sio.flush()
    ser.write(b"*IDN?\n")
    ver = ser.readline().rstrip(b'\r\n')
    wait_prompt(ser)
    print(f"connected to: {ver}")
    for a in range(0,61,2):
        (f, b) = get_cal_const(ser, a)
        print(f"const {a}: {f} (raw data possibly {int.from_bytes(b):08X}")
