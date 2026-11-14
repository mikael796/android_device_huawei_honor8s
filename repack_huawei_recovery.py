#!/usr/bin/env python3
"""
repack_huawei_recovery.py

TWRP builds a classic recovery.img (kernel + ramdisk). On Huawei MT6761
devices (Honor 8S) the recovery ramdisk lives in its own partition
"recovery_ramdisk" as a boot image with kernel_size=0 (the kernel is shared
with boot.img and loaded from there by LK).

This tool extracts the ramdisk from a built TWRP recovery.img and produces
a flashable recovery_ramdisk image:

    python repack_huawei_recovery.py twrp-recovery.img recovery_ramdisk.img

Flash the result to the recovery_ramdisk partition (via TWRP Install image
-> recovery_ramdisk, or dd if=/=of=/dev/block/platform/bootdevice/by-name/recovery_ramdisk).
"""
import struct
import sys
import hashlib


def pages(n, page):
    return (n + page - 1) // page * page


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)
    src, dst = sys.argv[1], sys.argv[2]

    b = open(src, "rb").read()
    if b[:8] != b"ANDROID!":
        print("not a boot image")
        sys.exit(1)
    ps = struct.unpack_from("<I", b, 36)[0]
    ks = struct.unpack_from("<I", b, 8)[0]
    rs = struct.unpack_from("<I", b, 16)[0]

    if ks:
        off = pages(2048 + ks, ps)  # header pages + kernel pages
    else:
        off = pages(2048, ps)
    ramdisk = b[off:off + rs]
    print(f"src: kernel={ks} ramdisk={rs} page={ps}")
    print(f"ramdisk blob: {len(ramdisk)} bytes @ {off}")

    # build Huawei-style recovery_ramdisk image: kernel_size=0
    PAGE = 2048
    PART_SIZE = 33554432  # stock partition size (32 MiB)
    hdr = bytearray(PAGE)
    hdr[0:8] = b"ANDROID!"
    struct.pack_into("<I", hdr, 8, 0)            # kernel_size = 0 (shared with boot)
    struct.pack_into("<I", hdr, 12, 0x80008000)  # kernel_addr (stock)
    struct.pack_into("<I", hdr, 16, len(ramdisk))
    struct.pack_into("<I", hdr, 20, 0x82000000)  # ramdisk_addr (stock)
    struct.pack_into("<I", hdr, 24, 0)           # second_size
    struct.pack_into("<I", hdr, 28, 0x80F00000)  # second_addr
    struct.pack_into("<I", hdr, 32, 0x80000100)  # tags_addr
    struct.pack_into("<I", hdr, 36, PAGE)        # page_size
    struct.pack_into("<I", hdr, 40, 0)           # dt_size
    hdr[64:64 + len(BOOT_CMDLINE) + 1] = BOOT_CMDLINE + b"\0"
    # id: sha1 over (kernel empty | ramdisk_size, ramdisk | second empty | dt empty)
    # per mkbootimg v0: sha1(kernel + padding + len(ramdisk) + ramdisk + ...)
    sha = hashlib.sha1()
    sha.update(struct.pack("<I", len(ramdisk)))
    sha.update(ramdisk)
    hdr[576:576 + 20] = sha.digest()

    out = bytearray(PART_SIZE)
    out[0:PAGE] = hdr
    out[PAGE:PAGE + len(ramdisk)] = ramdisk
    open(dst, "wb").write(out)
    print(f"written {dst}: {len(out)} bytes (kernel_size=0, ramdisk {len(ramdisk)})")
    print("flash to: /dev/block/platform/bootdevice/by-name/recovery_ramdisk")


BOOT_CMDLINE = b"bootopt=64S3,32N2,64N2 product.type=normal buildvariant=user"

if __name__ == "__main__":
    main()
