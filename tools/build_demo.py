import base64, os, re

ROOT = r"C:\Users\Светлана\Desktop\Сайты на продажу\Трекер_напоминалка VS"
DIST = os.path.join(ROOT, "dist")
os.makedirs(DIST, exist_ok=True)

def read(p):
    with open(os.path.join(ROOT, p), encoding="utf-8") as f:
        return f.read()

def data_uri(p):
    ext = "image/png" if p.endswith(".png") else "image/jpeg"
    with open(os.path.join(ROOT, p), "rb") as f:
        return "data:%s;base64," + base64.b64encode(f.read()).decode()

def uri_for(p):
    ext = "image/png" if p.endswith(".png") else "image/jpeg"
    with open(os.path.join(ROOT, p), "rb") as f:
        return "data:" + ext + ";base64," + base64.b64encode(f.read()).decode()

html = read("index.html")

# 1) убрать CSP (иначе заблокирует инлайн-скрипты) и manifest
html = re.sub(r'\s*<meta http-equiv="Content-Security-Policy".*?>', "", html, flags=re.S)
html = re.sub(r'\s*<link rel="manifest"[^>]*>', "", html)

# 2) favicon → data URI
html = re.sub(r'<link rel="icon"[^>]*href="assets/icon-192.png"[^>]*>',
              '<link rel="icon" type="image/png" href="' + uri_for("assets/icon-192.png") + '">', html)
html = re.sub(r'<link rel="icon"[^>]*icon-512[^>]*>\n?', "", html)
html = re.sub(r'\s*<link rel="apple-touch-icon"[^>]*>',
              '<link rel="apple-touch-icon" href="' + uri_for("assets/icon-192.png") + '">', html)

# 3) CSS → <style>, c заменой url(...) на data URI
css = read("css/styles.css")
def css_repl(m):
    path = m.group(1).replace("../", "assets/")
    return "url(" + uri_for(path) + ")"
css = re.sub(r'url\("\.\./([^"]+)"\)', css_repl, css)
html = re.sub(r'\s*<link rel="stylesheet" href="css/styles.css">',
              "<style>\n" + css + "\n</style>", html)

# 4) скрипты → инлайн
replaceInline = {'env/config.js': read('env/config.js')}

scripts = re.findall(r'<script src="([^"]+)"></script>', html)
for src_path in scripts:
    code = src_path.replace("../", "")
    body = replaceInline.get(src_path) or read(os.path.join("js", os.path.basename(src_path)))
    if os.path.basename(src_path) == "app.js":
        body = body.replace("registerSW();", "/* registerSW отключён в демо-файле */")
    body = body.replace("</script", "<\\/script")
    html = html.replace('<script src="%s"></script>' % src_path, "<script>\n" + body + "\n</script>")

# 5) data URI в JS (иконка уведомлений, лого-коллаж)
def js_repl(m):
    p = m.group(0).strip("'")
    return uri_for(p)
html = re.sub(r"assets/(collage/3-butterfly\.png|icon-192\.png)", js_repl, html)

out = os.path.join(DIST, "Crystal-demo.html")
with open(out, "w", encoding="utf-8") as f:
    f.write(html)
print("OK:", out, round(os.path.getsize(out) / 1024, 1), "KB")
