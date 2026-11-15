# Honor 8S (MT6761) TWRP — omni (twrp-7.1 branch)
# Built from stock firmware images: boot.img kernel, vendor recovery.fstab

DEVICE_PATH := device/huawei/honor8s

# Inherit from those products. Most specific first.
$(call inherit-product, $(SRC_TARGET_DIR)/product/full_base_telephony.mk)
$(call inherit-product, $(SRC_TARGET_DIR)/product/embedded.mk)

# Omni/TWRP common
$(call inherit-product, vendor/omni/config/common.mk)

PRODUCT_COPY_FILES += \
    $(DEVICE_PATH)/recovery/root/etc/recovery.fstab:root/system/etc/recovery.fstab \
    $(DEVICE_PATH)/recovery/root/etc/recovery.fstab:recovery/root/etc/recovery.fstab \
    $(DEVICE_PATH)/recovery/root/init.recovery.honor8s.rc:recovery/root/init.recovery.honor8s.rc \
    $(DEVICE_PATH)/recovery/root/init.recovery.qcom.rc:recovery/root/init.recovery.qcom.rc \
    $(DEVICE_PATH)/recovery/root/init.recovery.mt6761.rc:recovery/root/init.recovery.mt6761.rc \
    $(DEVICE_PATH)/recovery/root/init.recovery.usb.rc:recovery/root/init.recovery.usb.rc \
    $(DEVICE_PATH)/recovery/root/ueventd.rc:recovery/root/ueventd.rc

## Device identifier. This must come after all inclusions
PRODUCT_NAME := omni_honor8s
PRODUCT_DEVICE := honor8s
PRODUCT_BRAND := HUAWEI
PRODUCT_MODEL := Honor 8S
PRODUCT_MANUFACTURER := HUAWEI

PRODUCT_BUILD_PROP_OVERRIDES += \
    PRODUCT_NAME=honor8s \
    TARGET_DEVICE=honor8s
