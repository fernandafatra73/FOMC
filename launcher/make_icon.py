"""Buat fomc.ico (16/24/32/48/64/128 px) tanpa library tambahan: 3 candle di latar gelap."""
import struct, sys

BG = (0x1c, 0x19, 0x11)
BORDER = (0xdc, 0xaa, 0x3f)
UP = (0x3b, 0x82, 0xf6)
DOWN = (0xe0, 0x44, 0x3a)

# candle dalam koordinat 0..1: (x tengah, wick atas, body atas, body bawah, wick bawah, warna)
CANDLES = [
    (0.27, 0.40, 0.50, 0.78, 0.86, UP),
    (0.50, 0.18, 0.28, 0.58, 0.70, DOWN),
    (0.73, 0.14, 0.22, 0.52, 0.62, UP),
]

def render(n):
    px = [[None] * n for _ in range(n)]
    r = max(2, n // 6)  # radius sudut
    for y in range(n):
        for x in range(n):
            # sudut membulat
            cx = min(max(x, r), n - 1 - r)
            cy = min(max(y, r), n - 1 - r)
            if (x - cx) ** 2 + (y - cy) ** 2 > r * r:
                continue
            edge = (x - cx) ** 2 + (y - cy) ** 2 > (r - max(1, n // 32)) ** 2 or \
                x < max(1, n // 32) or y < max(1, n // 32) or x >= n - max(1, n // 32) or y >= n - max(1, n // 32)
            px[y][x] = BORDER if edge else BG
    bw = max(2, round(n * 0.16))
    ww = max(1, round(n * 0.035))
    for (cxr, wt, bt, bb, wb, col) in CANDLES:
        cx = cxr * n
        for y in range(round(wt * n), round(wb * n)):
            for x in range(round(cx - ww / 2), round(cx - ww / 2) + ww):
                if 0 <= x < n and 0 <= y < n:
                    px[y][x] = col
        for y in range(round(bt * n), round(bb * n)):
            for x in range(round(cx - bw / 2), round(cx - bw / 2) + bw):
                if 0 <= x < n and 0 <= y < n:
                    px[y][x] = col
    return px

def dib(n):
    px = render(n)
    header = struct.pack('<IiiHHIIiiII', 40, n, n * 2, 1, 32, 0, 0, 0, 0, 0, 0)
    rows = b''
    for y in range(n - 1, -1, -1):
        for x in range(n):
            c = px[y][x]
            rows += bytes((c[2], c[1], c[0], 255)) if c else b'\0\0\0\0'
    mask_row = ((n + 31) // 32) * 4
    mask = b''
    for y in range(n - 1, -1, -1):
        bits = bytearray(mask_row)
        for x in range(n):
            if px[y][x] is None:
                bits[x // 8] |= 0x80 >> (x % 8)
        mask += bytes(bits)
    return header + rows + mask

sizes = [16, 24, 32, 48, 64, 128]
images = [dib(n) for n in sizes]
out = struct.pack('<HHH', 0, 1, len(sizes))
offset = 6 + 16 * len(sizes)
for n, img in zip(sizes, images):
    out += struct.pack('<BBBBHHII', n % 256, n % 256, 0, 0, 1, 32, len(img), offset)
    offset += len(img)
out += b''.join(images)
open(sys.argv[1], 'wb').write(out)
print('ico bytes', len(out))
