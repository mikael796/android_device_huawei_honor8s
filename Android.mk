LOCAL_PATH := $(call my-dir)

ifeq ($(TARGET_DEVICE),honor8s)
include $(call all-subdir-makefiles,$(LOCAL_PATH))
endif
