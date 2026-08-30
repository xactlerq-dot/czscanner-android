[app]
title = Сканер Честного ЗНАКа
package.name = czscanner
package.domain = org.yourname
source.dir = .
source.include_exts = py,kv,png,jpg
version = 0.1
requirements = python==3.9,kivy==2.1.0,kivymd,pyzbar,Pillow,qrcode
orientation = portrait
android.permissions = CAMERA,WRITE_EXTERNAL_STORAGE
fullscreen = 0

[buildozer]
log_level = 2
