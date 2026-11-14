# Honor 8S (MT6761) TWRP
# Built from stock firmware images: boot.img kernel, vendor recovery.fstab

DEVICE_PATH := device/huawei/honor8s

# Inherit from those products. Most specific first.
$(call inherit-product, $(SRC_TARGET_DIR)/product/base_vendor.mk)

# Inline kernel: stock Image.gz-dtb from boot.img (kernel + appended MTK DTB)
TARGET_PREBUILT_KERNEL := $(DEVICE_PATH)/kernel/Image.gz-dtb

PRODUCT_COPY_FILES += \
    $(DEVICE_PATH)/recovery/root/etc/recovery.fstab:root/system/etc/recovery.fstab \
    $(DEVICE_PATH)/recovery/root/etc/recovery.fstab:recovery/root/etc/recovery.fstab \
    $(DEVICE_PATH)/recovery/root/init.recovery.honor8s.rc:recovery/root/init.recovery.honor8s.rc \
    $(DEVICE_PATH)/recovery/root/init.recovery.usb.rc:recovery/root/init.recovery.usb.rc \
    $(DEVICE_PATH)/recovery/root/ueventd.rc:recovery/root/ueventd.rc

PRODUCT_NAME := omni_Honor8S
PRODUCT_DEVICE := honor8s
PRODUCT_BRAND := HUAWEI
PRODUCT_MODEL := Honor 8S
PRODUCT_MANUFACTURER := HUAWEI

PRODUCT_DEFAULT_PROPERTY_OVERRIDES += \
    ro.product.device=honor8s

PRODUCT_BUILD_PROP_OVERRIDES += \
    PRODUCT_NAME=honor8s \
    TARGET_DEVICE=honor8s
