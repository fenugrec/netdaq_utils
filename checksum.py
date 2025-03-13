# Boot image checksum algorithm from firmware

import itertools


def validate_sum(block, expected):
   s = compute_sum(block)
   return s == expected


def compute_sum(block):
   s = sum(int.from_bytes(a) for a in itertools.batched(block,2))
# this included the 16-bit checksum and its complement; adjust
   return (s - (0xffff + 0xffff))


# this skips a few locations that are mapped to special registers of the mc68302.
# Those locations are replaced with 0xff padding
def boot_sum(block):
    b2 = block[0:0xf0] + block[0x100:]
    s = sum(int.from_bytes(a) for a in itertools.batched(b2,2))
    return s - (0xffff + 0xffff) + 8*0xffff
