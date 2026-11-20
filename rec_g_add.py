#!/usr/bin/env python3
"""REC-G｜Issue「卵を足す」を、その私書箱の eggs.txt に書き写す。

Curator が Issue にラベル「足す / Add」を貼ると、Actions がこれを動かす。
Issue の本文は誰でも書けるので、ここでは
  ・部屋番号は 3けたの数字だけ、その部屋に eggs.txt があるときだけ
  ・書き足すのは http(s) で始まる行だけ（｜のあとの表示名は 60字まで）
に絞ってから書く。

使い方（Actions の中で）:  python3 rec_g_add.py "$GITHUB_EVENT_PATH"
"""
import json
import os
import re
import sys

MARK = "# ── 管理人からの便り"
MAX_LINES = 20


def section(body, label):
    """Issue フォームの本文から「### 見出し」の下の中身を取り出す。"""
    m = re.search(r"^###\s*" + re.escape(label) + r"[^\n]*\n(.*?)(?=^###\s|\Z)", body, re.S | re.M)
    return m.group(1).strip() if m else ""


def clean_line(line):
    line = re.sub(r"[\x00-\x1f\x7f]", "", line).strip()
    m = re.match(r"^(https?://[^\s｜|<>\"']+)\s*(?:[｜|]\s*(.*))?$", line)
    if not m:
        return None
    url, name = m.group(1), (m.group(2) or "").strip()
    name = re.sub(r"[<>]", "", name)[:60]
    return f"{url} ｜ {name}" if name else url


def main(event_path):
    with open(event_path, encoding="utf-8") as f:
        ev = json.load(f)
    body = (ev.get("issue") or {}).get("body") or ""
    room = section(body, "部屋番号")
    if not re.fullmatch(r"\d{3}", room):
        sys.exit(f"部屋番号が読めない：{room!r}")
    eggs_txt = os.path.join("box", room, "rec-g", "eggs.txt")
    if not os.path.exists(eggs_txt):
        sys.exit(f"{eggs_txt} がない（その部屋の集卵所がまだない）")

    lines = [clean_line(x) for x in section(body, "並べたいページ").splitlines()]
    lines = [x for x in lines if x][:MAX_LINES]
    with open(eggs_txt, encoding="utf-8") as f:
        text = f.read()
    have = {re.sub(r"^https?://", "", l.split()[0]).rstrip("/").lower()
            for l in text.splitlines() if re.match(r"https?://", l.strip())}
    nest = os.path.join("box", room, "nest.json")          # 札にもう書いてある卵も足さない
    if os.path.exists(nest):
        try:
            j = json.load(open(nest, encoding="utf-8"))
            for x in j.get("feeds", []) + j.get("links", []):
                u = x if isinstance(x, str) else (x or {}).get("url", "")
                have.add(re.sub(r"^https?://", "", u).rstrip("/").lower())
        except Exception:
            pass
    new = [l for l in lines if re.sub(r"^https?://", "", l.split()[0]).rstrip("/").lower() not in have]
    if not new:
        print("足す卵なし（もう並んでいるか、URL が読めなかった）")
        open(os.environ.get("GITHUB_OUTPUT", os.devnull), "a").write("added=0\n")
        return
    block = "\n".join(new) + "\n"
    if MARK in text:                                      # 管理人の便りより上に書き足す
        i = text.index(MARK)
        head = text[:i].rstrip("\n") + "\n"
        text = head + block + "\n" + text[i:]
    else:
        text = text.rstrip("\n") + "\n" + block
    with open(eggs_txt, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"{eggs_txt} に {len(new)} 個")
    with open(os.environ.get("GITHUB_OUTPUT", os.devnull), "a") as f:
        f.write(f"added={len(new)}\nroom={room}\n")


if __name__ == "__main__":
    main(sys.argv[1])
