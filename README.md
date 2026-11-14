# TWRP device tree — HONOR 8S (MediaTek MT6761, armv7)

Device tree for building TWRP recovery for Honor 8S from stock firmware parts.
No manifests / dependencies included — meant to be dropped into a TWRP (omni)
source tree at `device/huawei/honor8s` and built directly.

## What works
- Touch panel (MTK `tpd` driver is inside the stock kernel — nothing extra needed)
- MTP + ADB over USB (configfs gadget, HUAWEI VID/PID — `init.recovery.usb.rc`)
- USB OTG mass storage (`/devices/platform/mt_usb*`)
- microSD (`/dev/block/mmcblk1p1`)
- Mount/backup/format/flash of all partitions (`recovery.fstab`)
- Brightness control (`/sys/class/leds/lcd-backlight/brightness`)

## Layout
```
AndroidProducts.mk            lunch targets: omni_honor8s-{user,userdebug,eng}
omni_honor8s.mk               product makefile
BoardConfig.mk                board/recovery/TWRP flags
kernel/Image.gz-dtb           stock kernel blob from boot.img: gzip(Image + appended MTK DTB) — MTK LK expects appended DTB, keep as-is
recovery/root/etc/recovery.fstab
recovery/root/init.recovery.honor8s.rc
recovery/root/init.recovery.usb.rc
recovery/root/ueventd.rc
repack_huawei_recovery.py     post-build repacker (see below)
```

## Build
In your omni/TWRP tree:
```
repo sync etc...
lunch omni_honor8s-eng
mka adbd recoveryimage
```
Output: `out/target/product/honor8s/recovery.img`

## IMPORTANT — how Huawei recovery boots on this device
The recovery ramdisk lives in a **separate `recovery_ramdisk` partition** and
the **kernel is shared with boot.img** (stock recovery image has
`kernel_size = 0`; LK loads the kernel from boot and the ramdisk from
recovery_ramdisk). So do NOT flash a full TWRP recovery.img into `boot` or
`recovery` partitions raw.

After building, repack:
```
python device/huawei/honor8s/repack_huawei_recovery.py \
    out/target/product/honor8s/recovery.img \
    twrp-recovery_ramdisk.img
```
The result is a stock-format image with `kernel_size=0` + the TWRP ramdisk.
Flash it to `recovery_ramdisk`:
```
adb shell dd if=twrp-recovery_ramdisk.img \
    of=/dev/block/platform/bootdevice/by-name/recovery_ramdisk
```
(or via fastboot/SP Flash Tool, or from the stock erecovery shell).

## Partitions (from stock vendor fstab)
system, vendor, product, version, odm, cust, cache, userdata(f2fs), log,
nvdata, misc, boot, recovery, recovery_ramdisk, recovery_vendor, vbmeta,
dtbo{,1,2}, lk, lk2, logo, frp, nvram, proinfo, seccfg, expdb, tee1/2,
scp1/2, sspm_1/2, md1img, md1dsp, md1arm7, md3img, spmfw, boot_para,
protect1/2, nvcfg, persist. All exposed for backup/flash in TWRP.

Stock /data is FBE (aes-256-xts) — decryption is not enabled; TWRP mounts
data raw for file backup/restore and full partition images.

## Notes
- Kernel: prebuilt stock (boot.img). If you later want a custom kernel,
  replace `kernel/Image.gz-dtb` (gzip'd Image + appended DTB, MTK style).
- Theme: 720x1280 (lcd density 320). If the panel is 720x1520 and the UI is
  offset, switch `TW_THEME` and/or set `TW_Y_OFFSET`.
- USB VID 12d1:107f (HUAWEI) kept from stock so host-side drivers behave.
