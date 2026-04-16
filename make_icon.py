"""Uygulama icon'u uretir."""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

def make(size):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    # Yuvarlak arka plan - mavi gradient hissi
    pad = size // 16
    # Dis halka
    d.rounded_rectangle(
        [pad, pad, size - pad, size - pad],
        radius=size // 5,
        fill=(37, 99, 235, 255),  # mavi
    )
    # Ic parlak kisim
    d.rounded_rectangle(
        [pad * 2, pad * 2, size - pad * 2, size - pad * 2],
        radius=size // 6,
        fill=(59, 130, 246, 255),
    )

    # Resim cercevesi (mini foto ikonu)
    cx, cy = size // 2, size // 2
    w = size // 2
    h = int(w * 0.72)
    x0, y0 = cx - w // 2, cy - h // 2
    x1, y1 = cx + w // 2, cy + h // 2
    d.rounded_rectangle([x0, y0, x1, y1], radius=size // 20,
                        fill=(255, 255, 255, 245))
    # Dag siluetleri
    d.polygon(
        [(x0 + w // 10, y1 - h // 6),
         (x0 + w // 3, y0 + h // 3),
         (x0 + w // 2, y1 - h // 6)],
        fill=(37, 99, 235, 255),
    )
    d.polygon(
        [(x0 + w // 2, y1 - h // 6),
         (x0 + 2 * w // 3, y0 + h // 2),
         (x1 - w // 12, y1 - h // 6)],
        fill=(59, 130, 246, 255),
    )
    # Gunes
    r = size // 22
    sx, sy = x1 - w // 5, y0 + h // 4
    d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(251, 191, 36, 255))

    # Indirme oku (alt-sag kose)
    ax = size - pad * 3
    ay = size - pad * 3
    ar = size // 7
    d.ellipse([ax - ar, ay - ar, ax + ar, ay + ar],
              fill=(16, 185, 129, 255))
    # Ok
    d.polygon(
        [(ax, ay + ar // 2),
         (ax - ar // 2, ay - ar // 6),
         (ax - ar // 5, ay - ar // 6),
         (ax - ar // 5, ay - ar // 1),
         (ax + ar // 5, ay - ar // 1),
         (ax + ar // 5, ay - ar // 6),
         (ax + ar // 2, ay - ar // 6)],
        fill=(255, 255, 255, 255),
    )
    return img

sizes = [16, 24, 32, 48, 64, 128, 256]
imgs = [make(s) for s in sizes]
out = Path(__file__).parent / "icon.ico"
imgs[0].save(out, format="ICO", sizes=[(s, s) for s in sizes],
             append_images=imgs[1:])
print(f"OK: {out}")
