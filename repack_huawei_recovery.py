#!/usr/bin/env python3
"""
repack_huawei_recovery.py

Huawei MT6761 devices (Honor 8S) boot recovery from a dedicated
"recovery_ramdisk" partition holding an Android boot image with
kernel_size=0 — the kernel is shared with boot.img and loaded from there.

IMPORTANT: LK validates more than the plain Android fields. A boot header
constructed from scratch (zeros in the unused/Huawei fields, own cmdline)
gets rejected and the device drops to fastboot. The only reliable way is
to reuse the *stock* boot header byte-for-byte (recovery/stock_bootimg_hdr.bin
taken from the stock recovery_ramdisk image) and only patch:

  - ramdisk_size (offset 16)
  - id/sha1      (offset 576, 20 bytes)

The TWRP ramdisk is extracted from the built recovery.img and placed at
offset 2048, image is padded with zeros to the stock partition size (32 MiB).

Usage:
    python repack_huawei_recovery.py twrp-recovery.img recovery_ramdisk.img

Flash the result to the recovery_ramdisk partition.
"""
import struct
import sys
import hashlib
import os

PART_SIZE = 33554432  # stock partition size (32 MiB)


def pages(n, page):
    return (n + page - 1) // page * page


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)
    src, dst = sys.argv[1], sys.argv[2]

    here = os.path.dirname(os.path.abspath(__file__))
    hdr_path = os.path.join(here, "recovery", "stock_bootimg_hdr.bin")

    b = open(src, "rb").read()
    if b[:8] != b"ANDROID!":
        print("not a boot image")
        sys.exit(1)
    ps = int.from_bytes(b[36:40], "little")
    ks = int.from_bytes(b[8:12], "little")
    rs = int.from_bytes(b[16:20], "little")

    off = pages(2048 + ks, ps) if ks else pages(2048, ps)
    ramdisk = b[off:off + rs]
    print(f"src: kernel={ks} ramdisk={rs} page={ps}")
    print(f"ramdisk blob: {len(ramdisk)} bytes @ {off} ({ramdisk[:2].hex()})")

    hdr = bytearray(open(hdr_path, "rb").read())
    if len(hdr) != 2048:
        print("bad stock header template")
        sys.exit(1)
    # patch only what must change
    struct.pack_into("<I", hdr, 16, len(ramdisk))
    sha = hashlib.sha1()
    sha.update(struct.pack("<I", len(ramdisk)))
    sha.update(ramdisk)
    hdr[576:576 + 20] = sha.digest()

    out = bytearray(PART_SIZE)
    out[0:2048] = hdr
    out[2048:2048 + len(ramdisk)] = ramdisk
    open(dst, "wb").write(out)
    print(f"written {dst}: {len(out)} bytes (stock header, kernel_size="
          f"{int.from_bytes(hdr[8:12], 'little')}, ramdisk {len(ramdisk)})")
    print("flash to: /dev/block/platform/bootdevice/by-name/recovery_ramdisk")


if __name__ == "__main__":
    main()
