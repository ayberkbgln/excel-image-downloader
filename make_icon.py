"""Uygulama icon'u uretir - gradient, modern gorunum."""
from PIL import Image, ImageDraw, ImageFilter
from pathlib import Path


def radial_gradient(size, c1, c2):
    """Ortadan disa radial gradient."""
    img = Image.new("RGBA", (size, size), c2)
    draw = ImageDraw.Draw(img)
    cx = cy = size // 2
    max_r = int(size * 0.7)
    for r in range(max_r, 0, -1):
        t = 1 - (r / max_r)
        col = tuple(int(c2[i] + (c1[i] - c2[i]) * t) for i in range(4))
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col)
    return img


def make(size):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    pad = size // 18
    radius = size // 4

    # Gradient arka plan (koyu mavi -> parlak mavi)
    grad = radial_gradient(size,
                           (96, 165, 250, 255),   # acik mavi (ic)
                           (37, 99, 235, 255))    # koyu mavi (dis)
    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).rounded_rectangle(
        [pad, pad, size - pad, size - pad], radius=radius, fill=255)
    bg = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    bg.paste(grad, (0, 0), mask)

    # Ust parlama efekti
    shine = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shine)
    sd.ellipse([pad * 2, pad, size - pad * 2, size // 2],
               fill=(255, 255, 255, 50))
    shine = shine.filter(ImageFilter.GaussianBlur(size // 30))
    bg = Image.alpha_composite(bg, shine)

    d = ImageDraw.Draw(bg)

    # Fotograf cercevesi - beyaz kart
    cx, cy = size // 2, int(size * 0.46)
    w = int(size * 0.56)
    h = int(w * 0.78)
    x0, y0 = cx - w // 2, cy - h // 2
    x1, y1 = cx + w // 2, cy + h // 2
    # Govde golge
    sh = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle(
        [x0 + 2, y0 + size // 60, x1 + 2, y1 + size // 60],
        radius=size // 22, fill=(0, 0, 0, 90))
    sh = sh.filter(ImageFilter.GaussianBlur(size // 80))
    bg = Image.alpha_composite(bg, sh)
    d = ImageDraw.Draw(bg)
    d.rounded_rectangle([x0, y0, x1, y1], radius=size // 22,
                        fill=(255, 255, 255, 250))

    # Resim icindeki daglar
    d.polygon(
        [(x0 + w // 10, y1 - h // 6),
         (x0 + w // 3, y0 + h // 3),
         (x0 + w // 2 + w // 12, y1 - h // 6)],
        fill=(37, 99, 235, 255))
    d.polygon(
        [(x0 + w // 2, y1 - h // 6),
         (x0 + 2 * w // 3, y0 + h // 2),
         (x1 - w // 12, y1 - h // 6)],
        fill=(96, 165, 250, 255))

    # Gunes
    r = size // 20
    sx, sy = x1 - w // 5, y0 + h // 4
    d.ellipse([sx - r, sy - r, sx + r, sy + r],
              fill=(251, 191, 36, 255))

    # Indirme oku (yesil daire + ok) - alt sag
    ax = size - pad * 3 + size // 60
    ay = size - pad * 3 + size // 60
    ar = int(size * 0.16)
    # Golge
    sh2 = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    ImageDraw.Draw(sh2).ellipse(
        [ax - ar + 2, ay - ar + 2, ax + ar + 2, ay + ar + 2],
        fill=(0, 0, 0, 110))
    sh2 = sh2.filter(ImageFilter.GaussianBlur(size // 70))
    bg = Image.alpha_composite(bg, sh2)
    d = ImageDraw.Draw(bg)
    d.ellipse([ax - ar, ay - ar, ax + ar, ay + ar],
              fill=(16, 185, 129, 255))
    # Ok (asagi dogru)
    aw = ar * 0.9
    d.polygon(
        [(ax, ay + ar // 2),
         (ax - aw // 2, ay - ar // 8),
         (ax - aw // 5, ay - ar // 8),
         (ax - aw // 5, ay - ar // 1.2),
         (ax + aw // 5, ay - ar // 1.2),
         (ax + aw // 5, ay - ar // 8),
         (ax + aw // 2, ay - ar // 8)],
        fill=(255, 255, 255, 255))

    return bg


if __name__ == "__main__":
    sizes = [16, 24, 32, 48, 64, 128, 256]
    imgs = [make(s) for s in sizes]
    out = Path(__file__).parent / "icon.ico"
    imgs[0].save(out, format="ICO", sizes=[(s, s) for s in sizes],
                 append_images=imgs[1:])
    # Preview 256px
    imgs[-1].save(Path(__file__).parent / "docs" / "icon_preview.png")
    print(f"OK: {out}")
