[app]
title = OKWin AI Predictor
package.name = okwinpredictor
package.domain = org.okwin
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0.0
requirements = python3,kivy==2.3.0
orientation = portrait
fullscreen = 0

# Android SDK / NDK setup
android.api = 31
android.minapi = 21
android.ndk = 25b
android.ndk_api = 21
android.archs = arm64-v8a
android.allow_backup = True
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 0
