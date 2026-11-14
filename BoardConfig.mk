# Honor 8S (MT6761) BoardConfig — TWRP

# ---------- architecture (MediaTek MT6761, 32-bit) ----------
TARGET_ARCH := arm
TARGET_ARCH_VARIANT := armv7-a-neon
TARGET_CPU_ABI := armeabi-v7a
TARGET_CPU_ABI2 := armeabi
TARGET_CPU_VARIANT := cortex-a53
TARGET_CPU_SMP := true

# ---------- kernel (stock prebuilt from boot.img) ----------
TARGET_PREBUILT_KERNEL := device/huawei/honor8s/kernel/Image.gz-dtb
BOARD_KERNEL_IMAGE := Image.gz-dtb

BOARD_KERNEL_PAGESIZE := 2048
BOARD_KERNEL_BASE := 0x40000000
BOARD_KERNEL_TAGS_ADDR := 0x40F00000
BOARD_MKBOOTIMG_ARGS := --base 0x40000000 --pagesize 2048 --kernel_offset 0x00008000 --ramdisk_offset 0x04000000 --tags_offset 0x00F00000 --dtb_offset 0x04080000

BOARD_KERNEL_CMDLINE := bootopt=64S3,32N2,64N2 product.type=normal androidboot.selinux=permissive buildvariant=user

# ---------- filesystems ----------
TARGET_USERIMAGES_USE_EXT4 := true
TARGET_USERIMAGES_USE_F2FS := true
BOARD_HAS_LARGE_FILESYSTEM := true
BOARD_SUPPRESS_BUILD_EMMC_ERASE := true
BOARD_SUPPRESS_SECURE_ERASE := true

# ---------- recovery ----------
TARGET_RECOVERY_PIXEL_FORMAT := "RGBA_8888"
TARGET_RECOVERY_FSTAB := device/huawei/honor8s/recovery/root/etc/recovery.fstab
RECOVERY_SDCARD_ON_DATA := false
BOARD_HAS_NO_SELECT_BUTTON := true
BOARD_RECOVERY_SWIPE := true

# ---------- TWRP ----------
TW_THEME := 720x1280
TW_INPUT_BLACKLIST := "hbtp_vm"

TW_BRIGHTNESS_PATH := "/sys/class/leds/lcd-backlight/brightness"
TW_MAX_BRIGHTNESS := 255
TW_DEFAULT_BRIGHTNESS := 168
TW_NO_SCREEN_BLANK_ON_BOOT := true
TW_NO_BATT_PERCENT := true

# MTP + adb over configfs (see init.recovery.usb.rc)
TW_INCLUDE_NTFS_3G := true
TW_INCLUDE_FUSE_EXFAT := true

# USB OTG mass storage
TW_HAS_USB_STORAGE := true

# no crypto: stock /data is FBE; TWRP mounts it raw for backup/flash
TW_INCLUDE_CRYPTO := false

TW_DEFAULT_LANGUAGE := en
