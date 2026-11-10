import os
from PIL import Image

BASE = r"C:\Users\Светлана\Desktop\Сайты на продажу\Трекер_напоминалка VS\assets"
src = os.path.join(BASE, "icon-new.png")
master = os.path.join(BASE, "icon-1024.png")

im = Image.open(src).convert("RGB")
im.save(master)
print("master", im.size)

# обычные иконки
im.resize((512, 512), Image.LANCZOS).save(os.path.join(BASE, "icon-512.png"))
im.resize((192, 192), Image.LANCZOS).save(os.path.join(BASE, "icon-192.png"))

# maskable: бабочка в центральных ~80%, фон — градиент из краёв оригинала
big = im.resize((512, 512), Image.LANCZOS)
edge = big.crop((0, 0, 1, 512))            # колонка x=0 → вертикальный градиент фона
bg = edge.resize((512, 512))               # растянуть колонку по ширине
inner = big.resize((410, 410), Image.LANCZOS)
bg.paste(inner, ((512 - 410) // 2, (512 - 410) // 2))
bg.save(os.path.join(BASE, "icon-maskable-512.png"))

os.remove(src)
print("done, icon-new removed")
