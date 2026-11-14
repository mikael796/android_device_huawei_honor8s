#!/usr/bin/env python3
"""
repack_huawei_recovery.py

Huawei MT6761 (Honor 8S) boots recovery from a dedicated "recovery_ramdisk"
partition: an Android boot image with kernel_size=0 (the kernel is shared
with boot.img). LK in unlocked state validates only the image format and
requires an AVBf footer at the end — a plain mkbootimg-style image without
the footer is rejected (device drops to fastboot).

The only reliable recipe (proven on-device): reuse the header and footer of
a known-bootable recovery image byte-for-byte and patch only:

  - ramdisk_size (offset 16)
  - id/sha1      (offset 576, 20 bytes)

Templates live next to this script:
  recovery/foreign_bootimg_hdr.bin — 2048-byte boot header
  recovery/foreign_bootimg_ftr.bin — 64-byte AVBf footer

The TWRP ramdisk is extracted from the built recovery.img, placed at
offset 2048, image is zero-padded to the stock partition size (32 MiB).

Usage:
    python repack_huawei_recovery.py twrp-recovery.img recovery_ramdisk.img

Flash the result to the recovery_ramdisk partition.
"""
import struct
import sys
import hashlib
import os
import gzip
import io
import zlib

PART_SIZE = 33554432  # stock partition size (32 MiB)


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)
    src, dst = sys.argv[1], sys.argv[2]

    here = os.path.dirname(os.path.abspath(__file__))
    hdr_path = os.path.join(here, "recovery", "foreign_bootimg_hdr.bin")
    ftr_path = os.path.join(here, "recovery", "foreign_bootimg_ftr.bin")

    b = open(src, "rb").read()
    if b[:8] != b"ANDROID!":
        print("not a boot image")
        sys.exit(1)
    ps = int.from_bytes(b[36:40], "little")
    ks = int.from_bytes(b[8:12], "little")
    rs = int.from_bytes(b[16:20], "little")

    off = ((2048 + ks + ps - 1) // ps) * ps if ks else 2048
    ramdisk = b[off:off + rs]
    print(f"src: kernel={ks} ramdisk={rs} page={ps}")
    print(f"ramdisk blob: {len(ramdisk)} bytes @ {off} ({ramdisk[:2].hex()})")

    hdr = bytearray(open(hdr_path, "rb").read())
    ftr = open(ftr_path, "rb").read()
    if len(hdr) != 2048 or len(ftr) != 64:
        print("bad templates")
        sys.exit(1)

    struct.pack_into("<I", hdr, 16, len(ramdisk))
    pad = (-len(ramdisk)) % ps
    sha = hashlib.sha1()
    sha.update(struct.pack("<I", len(ramdisk)))
    sha.update(ramdisk)
    sha.update(b"\0" * pad)
    hdr[576:576 + 20] = sha.digest()

    out = bytearray(PART_SIZE)
    out[0:2048] = hdr
    out[2048:2048 + len(ramdisk)] = ramdisk
    out[PART_SIZE - 64:] = ftr
    open(dst, "wb").write(out)
    print(f"written {dst}: {PART_SIZE} bytes (bootable header+footer, "
          f"kernel_size=0, ramdisk {len(ramdisk)})")
    print("flash to: /dev/block/platform/bootdevice/by-name/recovery_ramdisk")


if __name__ == "__main__":
    main()
