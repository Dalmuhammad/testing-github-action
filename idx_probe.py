"""Diagnosa 403 IDX: coba beberapa 'sidik jari' browser, dengan/tanpa warm-up, dan tampilkan siapa yang menolak.

Jalankan:  python idx_probe.py            (pakai tanggal 2026-09-29)
           python idx_probe.py 2026-09-24
"""
import sys
import time

from curl_cffi import requests

HOME = "https://www.idx.co.id/"
URL = "https://www.idx.co.id/primary/TradingSummary/GetStockSummary"
PARAMS = {"length": 1, "start": 0, "date": sys.argv[1] if len(sys.argv) > 1 else "2026-09-29"}
HEADERS = {"Accept": "application/json, text/plain, */*", "Referer": HOME}


def show(label, r):
    print(
        f"{label:<28} status={r.status_code}  server={r.headers.get('server')}  "
        f"cf-mitigated={r.headers.get('cf-mitigated')}  type={r.headers.get('content-type')}"
    )
    print(f"{'':<28} body[:150]={r.text[:150]!r}")


for imp in ["chrome", "edge", "firefox", "safari"]:
    for warmup in (False, True):
        label = f"{imp} {'+warmup' if warmup else 'direct'}"
        try:
            s = requests.Session(impersonate=imp)
            if warmup:
                s.get(HOME, timeout=30)  # ambil cookie dulu seperti browser
                time.sleep(2)
            show(label, s.get(URL, params=PARAMS, headers=HEADERS, timeout=30))
        except Exception as e:
            print(f"{label:<28} ERROR {type(e).__name__}: {e}")
        time.sleep(2)

print("\nStatus 200 + body berisi JSON  -> kombinasi itu bisa dipakai.")
print("cf-mitigated=challenge          -> Cloudflare minta JS challenge, perlu browser sungguhan (Playwright).")
