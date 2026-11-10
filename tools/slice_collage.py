import os
from PIL import Image

SRC = r"C:\Users\Светлана\Desktop\Сайты на продажу\Трекер_напоминалка VS\assets\theme-collage.jpg"
OUT = r"C:\Users\Светлана\Desktop\Сайты на продажу\Трекер_напоминалка VS\assets\collage"
os.makedirs(OUT, exist_ok=True)

im = Image.open(SRC).convert("RGB")
W, H = im.size  # 540x720
cw, ch = W // 3, H // 3  # 180x240

names = [
    "robot",     # 1 верх-лево: робо-скелет
    "flowers",   # 2 верх-центр: лилии
    "butterfly", # 3 верх-право: бабочка
    "sphere",    # 4 середина-лево: хрустальная сфера
    "eye",       # 5 середина-центр: глаз
    "hummingbird", # 6 середина-право: колибри
    "path",      # 7 низ-лево: мост/сад
    "chameleon", # 8 низ-центр: хамелеон
    "skull",     # 9 низ-право: хрустальный череп
]

n = 0
for row in range(3):
    for col in range(3):
        box = (col * cw, row * ch, (col + 1) * cw, (row + 1) * ch)
        crop = im.crop(box)
        n += 1
        crop.save(os.path.join(OUT, f"{n}-{names[n-1]}.jpg"), quality=88)
        print(f"{n}-{names[n-1]}.jpg", crop.size)
