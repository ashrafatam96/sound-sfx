"""Build sounds.json: a machine-readable index of every sound in this repo.

Run from the repo root after adding, removing or renaming sounds:

    python scripts/build_manifest.py
"""

import json
import re
import urllib.parse
import wave
from pathlib import Path

REPO = "ashrafatam96/sound-sfx"
BRANCH = "main"
RAW_BASE = f"https://raw.githubusercontent.com/{REPO}/{BRANCH}/"
CDN_BASE = f"https://cdn.jsdelivr.net/gh/{REPO}@{BRANCH}/"

# Folder name -> stable English id and what the category is good for in a video edit.
CATEGORIES = {
    "01 انتقالات - Transitions": (
        "transitions",
        "Scene cuts, slide/swipe transitions, text or objects flying in and out.",
    ),
    "02 ضربات - Impacts": (
        "impacts",
        "Hard cuts, title slams, logo hits, beat drops, emphasising a key moment.",
    ),
    "03 تصاعد - Risers": (
        "risers",
        "Building tension before a reveal (riser) or releasing it after one (downlifter).",
    ),
    "04 واجهات ونقرات - UI & Clicks": (
        "ui-clicks",
        "App/screen demos, button presses, cursor clicks, toggles, typing, list items popping in.",
    ),
    "05 نغمات - Chimes & Tones": (
        "chimes-tones",
        "Success states, notifications, checkmarks, positive highlights, power-ups.",
    ),
    "06 تنبيهات وأخطاء - Alerts": (
        "alerts",
        "Errors, wrong answers, warnings, 'don't do this' moments.",
    ),
    "07 خيال علمي - Sci-Fi": (
        "sci-fi",
        "Tech/futuristic visuals, lasers, glitches, engines, energy and force-field effects.",
    ),
    "08 فولي وحركة - Foley": (
        "foley",
        "Real-world actions: footsteps, doors, cloth, cards, chips, dice, physical props.",
    ),
    "09 موسيقى قصيرة - Jingles": (
        "jingles",
        "Short musical stings for intros, outros, level-complete and end cards.",
    ),
}

NOISE_TOKENS = {"impact", "sci", "rpg", "casino", "digital", "interface", "music", "jingles"}


def tags_for(stem: str) -> list[str]:
    tokens = [re.sub(r"\d+$", "", t) for t in re.split(r"[_\-\s]+", stem.lower())]
    tokens = [t for t in tokens if t]
    # "s_t_e_e_l" style names in the jingles pack -> "steel"
    joined, letters = [], []
    for t in tokens:
        if len(t) == 1:
            letters.append(t)
            continue
        if letters:
            joined.append("".join(letters))
            letters = []
        joined.append(t)
    if letters:
        joined.append("".join(letters))
    tags = []
    for t in joined:
        if t not in tags:
            tags.append(t)
    meaningful = [t for t in tags if t not in NOISE_TOKENS]
    return meaningful or tags


def main() -> None:
    root = Path(__file__).resolve().parent.parent
    sounds = []
    categories = []
    for folder, (cat_id, use_for) in CATEGORIES.items():
        files = sorted((root / folder).glob("*.wav"))
        categories.append(
            {
                "id": cat_id,
                "folder": folder,
                "name_ar": folder.split(" - ")[0][3:],
                "name_en": folder.split(" - ")[1],
                "use_for": use_for,
                "count": len(files),
            }
        )
        for f in files:
            with wave.open(str(f)) as w:
                duration = w.getnframes() / w.getframerate()
            rel = f"{folder}/{f.name}"
            sounds.append(
                {
                    "id": f"{cat_id}/{f.stem}",
                    "duration_sec": round(duration, 3),
                    "tags": tags_for(f.stem),
                    "file": rel,
                    "url": RAW_BASE + urllib.parse.quote(rel),
                }
            )

    manifest = {
        "name": "sound-sfx",
        "repo": f"https://github.com/{REPO}",
        "license": "MIT",
        "format": "wav",
        "url_base": RAW_BASE,
        "cdn_base": CDN_BASE,
        "url_note": "url = url_base + percent-encoded file. Swap url_base for cdn_base to use the jsDelivr CDN.",
        "count": len(sounds),
        "categories": categories,
        "sounds": sounds,
    }
    # One sound per line keeps the file small and easy for an AI to grep or read in chunks.
    head = json.dumps({k: v for k, v in manifest.items() if k != "sounds"}, ensure_ascii=False, indent=2)
    rows = ",\n".join("    " + json.dumps(s, ensure_ascii=False) for s in sounds)
    out = root / "sounds.json"
    out.write_text(f'{head[:-2]},\n  "sounds": [\n{rows}\n  ]\n}}\n', encoding="utf-8")
    print(f"Wrote {len(sounds)} sounds to {out.name}")


if __name__ == "__main__":
    main()
