# Python Debugging Toolkit

یه ابزار سبک برای دیباگ اسکریپت‌های Python — بدون هیچ dependency خارجی.

## امکانات
- ردیابی خط‌به‌خط اجرا (line-by-line trace)
- نمایش متغیرهای محلی در هر خط
- نمایش توابع فراخوانی‌شده و مقدار بازگشتی‌شان
- نمایش exception در لحظه رخ دادن
- لاگ خطاها به فرمت JSON (با اطلاعات دقیق محل crash)
- بررسی متغیرها در لحظه crash با --inspect

## ساختار پروژه

```
debugging/
├── main.py                  ← نقطه ورود
├── debugger/
│   ├── cli.py               ← رابط خط فرمان
│   ├── tracer.py            ← ردیابی اجرا با sys.settrace
│   ├── logger.py            ← لاگ خطاها در JSON
│   └── inspector.py         ← بررسی متغیرهای frame
├── examples/
│   ├── buggy_program.py     ← مثال: برنامه با ZeroDivisionError
│   └── test.py              ← مثال: تست مستقیم tracer
├── tests/
│   └── test_all.py          ← unit tests کامل
└── logs/
    └── errors.json          ← خطاهای لاگ‌شده
```

## نحوه استفاده

```bash
# اجرای ساده
python main.py examples/buggy_program.py

# با trace خط‌به‌خط
python main.py examples/buggy_program.py --trace

# با نمایش متغیرها
python main.py examples/buggy_program.py --trace --vars

# با بررسی متغیرها در لحظه crash
python main.py examples/buggy_program.py --inspect
```

## اجرای تست‌ها

```bash
python -m pytest tests/ -v
# یا
python tests/test_all.py
```
