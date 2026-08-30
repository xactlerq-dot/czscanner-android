[app]
title = Сканер Честного ЗНАКа
package.name = czscanner
package.domain = org.yourname
source.dir = .
source.include_exts = py,kv,png,jpg
version = 0.1
requirements = python,kivy==2.1.0,kivymd,pyzbar,Pillow,qrcode
orientation = portrait
android.permissions = CAMERA,WRITE_EXTERNAL_STORAGE
android.api = 30
android.minapi = 21
android.ndk = 23b
android.sdk = 30
