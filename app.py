"""
Resim Indirici v2 - Modern Dark UI
- Paralel indirme
- Var olan dosyayi atla (resume)
- Durdur butonu
- Log sinirli (UI donmaz)
- Hata raporu .txt
"""
import os, re, sys, threading, time, queue
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import urlopen, Request
from concurrent.futures import ThreadPoolExecutor, as_completed
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from openpyxl import load_workbook


APP_TITLE = "Resim Indirici"
APP_VER   = "v2.0"
FOOTER    = "ayberk bağlan"

BG        = "#0f172a"
BG_CARD   = "#1e293b"
BG_INPUT  = "#0b1220"
BORDER    = "#334155"
FG        = "#e2e8f0"
FG_MUTED  = "#94a3b8"
ACCENT    = "#3b82f6"
ACCENT_HO = "#2563eb"
OK_GREEN  = "#10b981"
ERR_RED   = "#ef4444"
WARN_YEL  = "#f59e0b"

MAX_LOG_LINES = 500


def resource_path(rel):
    try:
        base = sys._MEIPASS
    except Exception:
        base = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base, rel)


def download(url, dest, timeout=30):
    req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urlopen(req, timeout=timeout) as r, open(dest, "wb") as f:
        f.write(r.read())


def safe_name(s):
    return re.sub(r'[<>:"/\\|?*]', "_", str(s)).strip()


class HoverButton(tk.Canvas):
    def __init__(self, parent, text, command, bg=ACCENT, hover=ACCENT_HO,
                 fg="white", width=200, height=44, radius=10,
                 font=("Segoe UI", 10, "bold")):
        super().__init__(parent, width=width, height=height,
                         bg=parent["bg"], bd=0, highlightthickness=0)
        self.command = command
        self.bg_c = bg; self.hover_c = hover; self.fg = fg
        self.radius = radius; self.w = width; self.h = height
        self.text = text; self.font = font
        self._enabled = True
        self._draw(bg)
        self.bind("<Enter>", lambda e: self._enabled and self._draw(self.hover_c))
        self.bind("<Leave>", lambda e: self._enabled and self._draw(self.bg_c))
        self.bind("<Button-1>", lambda e: self._enabled and self.command and self.command())

    def _round_rect(self, x1, y1, x2, y2, r, **kw):
        pts = [x1+r,y1, x2-r,y1, x2,y1, x2,y1+r, x2,y2-r,
               x2,y2, x2-r,y2, x1+r,y2, x1,y2, x1,y2-r,
               x1,y1+r, x1,y1]
        return self.create_polygon(pts, smooth=True, **kw)

    def _draw(self, color):
        self.delete("all")
        self._round_rect(1, 1, self.w-1, self.h-1, self.radius, fill=color, outline=color)
        self.create_text(self.w//2, self.h//2, text=self.text,
                         fill=self.fg, font=self.font)

    def set_text(self, t):
        self.text = t; self._draw(self.bg_c)

    def set_enabled(self, val):
        self._enabled = val
        self._draw(self.bg_c if val else "#475569")


class App:
    def __init__(self, root):
        self.root = root
        root.title(f"{APP_TITLE} {APP_VER}")
        root.geometry("820x720")
        root.minsize(780, 640)
        root.configure(bg=BG)
        try:
            root.iconbitmap(resource_path("icon.ico"))
        except Exception:
            pass

        self.xlsx_path = tk.StringVar()
        self.out_path  = tk.StringVar()
        self.threads_v = tk.IntVar(value=10)
        self.skip_existing = tk.BooleanVar(value=True)
        self.single_folder = tk.BooleanVar(value=False)

        self.running = False
        self.stop_flag = threading.Event()
        self.log_queue = queue.Queue()
        self.log_count = 0

        self._setup_style()
        self._build_ui()
        self._poll_log()

    def _setup_style(self):
        style = ttk.Style()
        try: style.theme_use("clam")
        except: pass
        style.configure("Modern.Horizontal.TProgressbar",
            troughcolor=BG_INPUT, background=ACCENT,
            bordercolor=BG_INPUT, lightcolor=ACCENT, darkcolor=ACCENT,
            thickness=14)
        style.configure("TScale", background=BG_CARD, troughcolor=BG_INPUT)

    def _card(self, parent):
        return tk.Frame(parent, bg=BG_CARD, highlightbackground=BORDER,
                        highlightthickness=1)

    def _entry(self, parent, var):
        return tk.Entry(parent, textvariable=var, bg=BG_INPUT, fg=FG,
            insertbackground=FG, relief="flat", font=("Segoe UI", 10),
            highlightthickness=1, highlightbackground=BORDER,
            highlightcolor=ACCENT)

    def _build_ui(self):
        # HEADER
        h = tk.Frame(self.root, bg=BG)
        h.pack(fill="x", padx=24, pady=(22, 8))
        tk.Label(h, text="📥  " + APP_TITLE, bg=BG, fg=FG,
                 font=("Segoe UI", 20, "bold")).pack(anchor="w")
        tk.Label(h, text=f"Excel'deki URL linklerinden toplu resim indirici  •  {APP_VER}",
                 bg=BG, fg=FG_MUTED, font=("Segoe UI", 10)).pack(anchor="w")

        # AYARLAR
        card = self._card(self.root)
        card.pack(fill="x", padx=24, pady=10)
        inner = tk.Frame(card, bg=BG_CARD)
        inner.pack(fill="x", padx=18, pady=16)

        tk.Label(inner, text="EXCEL DOSYASI", bg=BG_CARD, fg=FG_MUTED,
                 font=("Segoe UI", 8, "bold")).pack(anchor="w")
        r1 = tk.Frame(inner, bg=BG_CARD)
        r1.pack(fill="x", pady=(4, 12))
        self._entry(r1, self.xlsx_path).pack(side="left", fill="x", expand=True, ipady=6)
        HoverButton(r1, "📁 Gozat", self.pick_xlsx, bg=BORDER, hover="#475569",
                    width=100, height=34).pack(side="left", padx=(8, 0))

        tk.Label(inner, text="CIKTI KLASORU", bg=BG_CARD, fg=FG_MUTED,
                 font=("Segoe UI", 8, "bold")).pack(anchor="w")
        r2 = tk.Frame(inner, bg=BG_CARD)
        r2.pack(fill="x", pady=(4, 12))
        self._entry(r2, self.out_path).pack(side="left", fill="x", expand=True, ipady=6)
        HoverButton(r2, "📂 Gozat", self.pick_out, bg=BORDER, hover="#475569",
                    width=100, height=34).pack(side="left", padx=(8, 0))

        # Opsiyonlar (thread + skip)
        opt = tk.Frame(inner, bg=BG_CARD)
        opt.pack(fill="x", pady=(4, 0))

        tl = tk.Frame(opt, bg=BG_CARD)
        tl.pack(side="left")
        tk.Label(tl, text="PARALEL INDIRME", bg=BG_CARD, fg=FG_MUTED,
                 font=("Segoe UI", 8, "bold")).pack(anchor="w")
        sl_wrap = tk.Frame(tl, bg=BG_CARD)
        sl_wrap.pack(anchor="w", pady=(4, 0))
        self.thread_lbl = tk.Label(sl_wrap, text="10 thread", bg=BG_CARD, fg=FG,
                                   font=("Segoe UI", 9, "bold"), width=10, anchor="w")
        self.thread_lbl.pack(side="right", padx=(8, 0))
        sc = ttk.Scale(sl_wrap, from_=1, to=32, orient="horizontal",
                       variable=self.threads_v, length=220,
                       command=lambda v: self.thread_lbl.config(
                           text=f"{int(float(v))} thread"))
        sc.pack(side="left")

        sk = tk.Frame(opt, bg=BG_CARD)
        sk.pack(side="right")
        cb_kw = dict(bg=BG_CARD, fg=FG, selectcolor=BG_INPUT,
                     activebackground=BG_CARD, activeforeground=FG,
                     font=("Segoe UI", 9), bd=0, highlightthickness=0,
                     anchor="w")
        tk.Checkbutton(sk, text="  Var olan dosyalari atla (resume)",
            variable=self.skip_existing, **cb_kw).pack(anchor="w", pady=(14, 0))
        tk.Checkbutton(sk, text="  Tek klasore indir (alt klasor yok)",
            variable=self.single_folder, **cb_kw).pack(anchor="w")

        # START / STOP
        bf = tk.Frame(self.root, bg=BG)
        bf.pack(fill="x", padx=24, pady=(14, 6))
        self.start_btn = HoverButton(
            bf, "▶  INDIRMEYI BASLAT", self.start,
            bg=ACCENT, hover=ACCENT_HO, width=620, height=52,
            radius=12, font=("Segoe UI", 12, "bold"))
        self.start_btn.pack(side="left", fill="x", expand=True)
        self.stop_btn = HoverButton(
            bf, "⏹  DURDUR", self.stop,
            bg=ERR_RED, hover="#dc2626", width=140, height=52,
            radius=12, font=("Segoe UI", 11, "bold"))
        self.stop_btn.pack(side="left", padx=(8, 0))
        self.stop_btn.set_enabled(False)

        # PROGRESS
        pf = tk.Frame(self.root, bg=BG)
        pf.pack(fill="x", padx=24, pady=(8, 4))
        self.progress = ttk.Progressbar(pf, style="Modern.Horizontal.TProgressbar",
            mode="determinate")
        self.progress.pack(fill="x")

        st = tk.Frame(self.root, bg=BG)
        st.pack(fill="x", padx=24, pady=(4, 6))
        self.status = tk.Label(st, text="● Hazir", bg=BG, fg=FG_MUTED,
                               font=("Segoe UI", 9), anchor="w")
        self.status.pack(side="left")
        self.counter = tk.Label(st, text="", bg=BG, fg=FG,
                                font=("Segoe UI", 9, "bold"), anchor="e")
        self.counter.pack(side="right")

        # LOG
        lc = self._card(self.root)
        lc.pack(fill="both", expand=True, padx=24, pady=(6, 10))
        lh = tk.Frame(lc, bg=BG_CARD)
        lh.pack(fill="x", padx=14, pady=(10, 4))
        tk.Label(lh, text=f"Canli Log (son {MAX_LOG_LINES} satir)", bg=BG_CARD,
                 fg=FG_MUTED, font=("Segoe UI", 8, "bold")).pack(side="left")
        tk.Button(lh, text="Temizle", bg=BG_CARD, fg=FG_MUTED, bd=0,
                  activebackground=BG_CARD, activeforeground=FG,
                  font=("Segoe UI", 8), cursor="hand2",
                  command=lambda: self.log.delete("1.0", "end")).pack(side="right")

        lw = tk.Frame(lc, bg=BG_INPUT)
        lw.pack(fill="both", expand=True, padx=14, pady=(0, 14))
        self.log = tk.Text(lw, bg=BG_INPUT, fg="#cbd5e1", bd=0,
            insertbackground=FG, font=("Consolas", 9),
            relief="flat", padx=10, pady=8, wrap="none")
        self.log.pack(side="left", fill="both", expand=True)
        sb = tk.Scrollbar(lw, command=self.log.yview, bg=BG_CARD)
        sb.pack(side="right", fill="y")
        self.log.config(yscrollcommand=sb.set)
        self.log.tag_config("ok",   foreground=OK_GREEN)
        self.log.tag_config("err",  foreground=ERR_RED)
        self.log.tag_config("info", foreground=ACCENT)
        self.log.tag_config("warn", foreground=WARN_YEL)

        # FOOTER
        f = tk.Frame(self.root, bg=BG)
        f.pack(side="bottom", fill="x", pady=(0, 10))
        tk.Label(f, text=FOOTER, bg=BG, fg=FG_MUTED,
                 font=("Segoe UI", 9, "italic")).pack()

    # ---- Helpers ----
    def pick_xlsx(self):
        p = filedialog.askopenfilename(title="Excel Sec",
            filetypes=[("Excel", "*.xlsx *.xlsm"), ("Tumu", "*.*")])
        if p:
            self.xlsx_path.set(p)
            if not self.out_path.get():
                self.out_path.set(str(Path(p).parent / "indirilen"))

    def pick_out(self):
        p = filedialog.askdirectory(title="Cikti Klasoru")
        if p:
            self.out_path.set(p)

    def log_write(self, msg, tag=None):
        self.log_queue.put((msg, tag))

    def _poll_log(self):
        # Log kuyrugunu bosalt, max satiri koru
        try:
            drained = 0
            while drained < 200:
                msg, tag = self.log_queue.get_nowait()
                self.log.insert("end", msg + "\n", tag or ())
                self.log_count += 1
                drained += 1
        except queue.Empty:
            pass
        if self.log_count > MAX_LOG_LINES:
            excess = self.log_count - MAX_LOG_LINES
            self.log.delete("1.0", f"{excess + 1}.0")
            self.log_count = MAX_LOG_LINES
        self.log.see("end")
        self.root.after(80, self._poll_log)

    def set_status(self, msg, color=FG_MUTED):
        self.status.config(text=msg, fg=color)

    def start(self):
        if self.running:
            return
        xlsx = self.xlsx_path.get().strip()
        out  = self.out_path.get().strip()
        if not xlsx or not Path(xlsx).exists():
            messagebox.showerror("Hata", "Gecerli bir Excel dosyasi sec.")
            return
        if not out:
            messagebox.showerror("Hata", "Cikti klasoru sec.")
            return
        self.running = True
        self.stop_flag.clear()
        self.start_btn.set_enabled(False)
        self.start_btn.set_text("⏳  INDIRILIYOR...")
        self.stop_btn.set_enabled(True)
        self.log.delete("1.0", "end")
        self.log_count = 0
        threading.Thread(target=self._worker, args=(xlsx, out),
                         daemon=True).start()

    def stop(self):
        if not self.running:
            return
        self.stop_flag.set()
        self.log_write("⚠ Durduruluyor... (aktif indirmeler bittikten sonra)", "warn")
        self.set_status("● Durduruluyor...", WARN_YEL)

    def _one(self, kod, url, out_p, skip, single):
        if self.stop_flag.is_set():
            return ("skip", kod, url, "durduruldu")
        m = re.search(r"Product/(.+)$", url, re.IGNORECASE)
        name = m.group(1) if m else os.path.basename(urlparse(url).path)
        name = name.replace("/", "_")
        if single:
            dest = out_p / name
        else:
            klasor = out_p / kod
            klasor.mkdir(exist_ok=True)
            dest = klasor / name
        if skip and dest.exists() and dest.stat().st_size > 0:
            return ("skip", kod, name, "mevcut")
        try:
            download(url, dest)
            return ("ok", kod, name, "")
        except Exception as e:
            return ("err", kod, url, str(e))

    def _worker(self, xlsx, out):
        try:
            out_p = Path(out)
            out_p.mkdir(parents=True, exist_ok=True)
            self.log_write("► Excel okunuyor...", "info")
            wb = load_workbook(xlsx, data_only=True, read_only=True)
            ws = wb.active

            jobs = []
            for row in ws.iter_rows(min_row=2, values_only=True):
                if not row or row[0] is None:
                    continue
                kod = safe_name(row[0])
                for cell in row[1:]:
                    if not cell:
                        continue
                    url = str(cell).strip()
                    if url.lower().startswith("http"):
                        jobs.append((kod, url))
            wb.close()

            total = len(jobs)
            if total == 0:
                self.log_write("URL bulunamadi.", "err")
                self._done(0, 0, 0, 0, None)
                return

            threads = max(1, int(self.threads_v.get()))
            skip = bool(self.skip_existing.get())
            single = bool(self.single_folder.get())
            mod = "tek klasor" if single else "kod bazli klasor"
            self.log_write(
                f"► {total} URL bulundu. {threads} paralel thread • {mod} modunda basliyor...\n",
                "info")
            self.progress.config(maximum=total, value=0)

            ok = fail = skipped = done = 0
            errors = []
            start_ts = time.time()

            with ThreadPoolExecutor(max_workers=threads) as ex:
                futs = [ex.submit(self._one, k, u, out_p, skip, single) for k, u in jobs]
                for fut in as_completed(futs):
                    status, kod, name_or_url, extra = fut.result()
                    done += 1
                    if status == "ok":
                        ok += 1
                        if ok % 5 == 0 or done < 20:
                            self.log_write(f"✓ {kod}/{name_or_url}", "ok")
                    elif status == "skip":
                        skipped += 1
                        if extra == "durduruldu":
                            pass
                        elif skipped <= 10 or skipped % 50 == 0:
                            self.log_write(f"↷ {kod}/{name_or_url} (mevcut)", "warn")
                    else:
                        fail += 1
                        errors.append(f"{name_or_url}\t{extra}")
                        self.log_write(f"✗ {name_or_url}  ({extra})", "err")

                    self.progress.config(value=done)
                    elapsed = time.time() - start_ts
                    rate = done / elapsed if elapsed > 0 else 0
                    eta = (total - done) / rate if rate > 0 else 0
                    self.set_status(
                        f"● Indiriliyor...  {done}/{total}  •  {rate:.1f}/sn  •  kalan ~{self._fmt_time(eta)}",
                        ACCENT)
                    self.counter.config(
                        text=f"OK {ok}  •  ATLANAN {skipped}  •  HATA {fail}")

            err_file = None
            if errors:
                err_file = out_p / "hatalar.txt"
                err_file.write_text("\n".join(errors), encoding="utf-8")
                self.log_write(f"\n⚠ {len(errors)} hata 'hatalar.txt' dosyasina yazildi",
                               "warn")

            self._done(total, ok, fail, skipped, err_file)

        except Exception as e:
            self.log_write(f"[KRITIK HATA] {e}", "err")
            messagebox.showerror("Hata", str(e))
            self._reset_btn()

    def _fmt_time(self, s):
        s = int(s)
        if s < 60: return f"{s}sn"
        if s < 3600: return f"{s//60}dk {s%60}sn"
        return f"{s//3600}sa {(s%3600)//60}dk"

    def _done(self, total, ok, fail, skipped, err_file):
        color = OK_GREEN if fail == 0 else (WARN_YEL if ok > 0 else ERR_RED)
        self.set_status("● Bitti", color)
        self.counter.config(
            text=f"Toplam {total}  •  OK {ok}  •  ATLANAN {skipped}  •  Hata {fail}")
        self.log_write(
            f"\n═══ BITTI ═══  Toplam={total}  OK={ok}  Atlanan={skipped}  Hata={fail}",
            "info")
        msg = (f"Indirme bitti.\n\nToplam: {total}\nBasarili: {ok}\n"
               f"Atlanan (mevcut): {skipped}\nHata: {fail}")
        if err_file:
            msg += f"\n\nHatalar: {err_file}"
        messagebox.showinfo("Tamamlandi", msg)
        self._reset_btn()

    def _reset_btn(self):
        self.running = False
        self.stop_flag.clear()
        self.start_btn.set_enabled(True)
        self.start_btn.set_text("▶  INDIRMEYI BASLAT")
        self.stop_btn.set_enabled(False)


if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()
