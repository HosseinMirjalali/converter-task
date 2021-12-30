# Video Converter (DRF/Django)
## _سید حسین میرجلالی_
## مراحل کارکرد
- ساخت حساب کاربری از اندپوینت (api/create/)
- دریافت توکن jwt از اندپوینت (api/token)
- رفرش کردن توکن در اندپوینت (api/token/refresh/)
- دریافت شارژ باقیمانده در تمامی رکوئست ها در هدر Charge-Left
- ارسال POST رکوئست به اندپوینت (api/upload)
- انتخاب فرمت دلخواه در فیلد (req_format)
- دریافت پیام موفقیت آمیز بودن درخواست در صورت ولید بودن دیتا، به همراه لینک اندپوینت آبجکت جدید
- فيلد file پس از کانورت شدن حاوی فایل درخواستی و قابل دانلود خواهد بود 

## مراحل آماده سازی و اجرای پروژه
راحت ترین روش برای اجرای پروژه استفاده از داکر می باشد.<br />
در کنسول خود به دایرکتوری پروژه رفته و ایمیج های پروژه را بیلد کنید:<br />

```sh
docker-compose -f local.yml build
```

پس از دانلود و بیلد شدن ایمیج ها پروژه را اجرا کنید:<br />
```sh
docker-compose -f local.yml up
```

داکیومنتنشن Swagger در آدرس (localhost:8000/swagger) در دسترس است.<br />
برای اجرای تمام تست ها از دستور زیر استفاده کنید: (تست های کانورت سنگین و طولانی هستند)<br />

```sh
docker-compose -f local.yml run --rm django pytest
```
برای deselect کردن تست های کانورت از دستور زیر استفاده کنید:<br />
```sh
docker-compose -f local.yml run --rm django pytest -v -m conversion
```

## توضیحات بیشتر
برای آزمایش دستی کانورت ها [4 فایل سمپل](https://github.com/HosseinMirjalali/converter-task/tree/master/converter/test_video_files) در فایل های پروژه وجود دارد. (تست های کانورت نیز با همین فایل ها اجرا می شوند)<br />
احراز حویت jwt با استفاده از پکیج  [djangorestframework-simplejwt](https://github.com/jazzband/djangorestframework-simplejwt)
 انجام میشود. <br />
شارژ باقیمانده کاربر در مدل یوزر ذخیره می شود و در [تسک کانورت](https://github.com/HosseinMirjalali/converter-task/blob/master/converter/video/tasks.py#L14)
پس از کانورت موفق از حساب وی کم می شود. <br />
کاربر میتواند یک فایل از 4 فرمت (mp4 - avi - mkv - 3gp) را آپلود کرده و به هرکدام از آنها درخواست کانورت دهد. <br />
ویدیوی ارسالی برای [تسک سلری](https://github.com/HosseinMirjalali/converter-task/blob/master/converter/video/tasks.py#L14) ارسال شده و [تنظیمات کانکارنسی](https://github.com/HosseinMirjalali/converter-task/blob/master/config/settings/base.py#L285) سلری از اجرای بیش از 3 تسک بصورت همزمان جلوگیری میکند. <br />
ویوی ای پی آی آپلود، طول ویدیو و شارژ کاربر را [چک میکند](https://github.com/HosseinMirjalali/converter-task/blob/master/converter/video/api/views.py#L32) و اجازه ی کانورت ویدیویی که طول آن از مقدار شارژ وی بیشتر باشد را نمی دهد. <br />
[لینک آبجکت کانورت](https://github.com/HosseinMirjalali/converter-task/blob/master/converter/video/api/views.py#L46) شده در صورت موفق بودن درخواست بعنوان ریسپانس برای کاربر ارسال میشود. <br />
