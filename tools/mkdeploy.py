import os, shutil

ROOT = r"C:\Users\Светлана\Desktop\Сайты на продажу\Трекер_напоминалка VS"
DEP = os.path.join(ROOT, "deploy")

if os.path.exists(DEP):
    shutil.rmtree(DEP)
os.makedirs(DEP, exist_ok=True)

items = [
    "index.html", "manifest.webmanifest", "sw.js",
    "css", "js", "env",
    os.path.join("assets", "collage"),
    os.path.join("assets", "icon-192.png"),
    os.path.join("assets", "icon-512.png"),
    os.path.join("assets", "icon-maskable-512.png"),
    os.path.join("assets", "icon-1024.png"),
    os.path.join("assets", "icon.svg"),
    os.path.join("assets", "theme-collage.jpg"),
]

for it in items:
    src = os.path.join(ROOT, it)
    dst = os.path.join(DEP, it)
    print("COPY:", it, "exists:", os.path.exists(src))
    if os.path.isfile(src):
        shutil.copy2(src, dst)
    elif os.path.isdir(src):
        shutil.copytree(src, dst)
    else:
        print("  !! MISSING, skipped")
        continue

for junk in (".gitignore", "config.example.js", "README.md"):
    p = os.path.join(DEP, "env", junk)
    if os.path.exists(p):
        os.remove(p)

total = sum(os.path.getsize(os.path.join(dp, f)) for dp, dn, fn in os.walk(DEP) for f in fn)
print("deploy folder ready:", DEP, "size:", round(total / 1024), "KB")
