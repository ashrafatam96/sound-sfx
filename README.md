# sound-sfx

Free sound effects for video editing: **715 short WAV files** (transitions, whooshes, impacts, risers, UI clicks, chimes, sci-fi, foley and jingles), organised so both people and AI tools like Claude can find the right sound quickly.

مكتبة مؤثرات صوتية مجانية لمونتاج الفيديو — 715 ملف WAV مقسمة حسب النوع.

- **Machine-readable index:** [`sounds.json`](sounds.json) — every sound with its category, duration, tags and a direct download URL.
- **License:** MIT — use it in personal and commercial videos.

## Categories

| Folder | ID | Files | Use for |
|---|---|---:|---|
| `01 انتقالات - Transitions` | `transitions` | 55 | Scene cuts, slide/swipe transitions, text or objects flying in and out |
| `02 ضربات - Impacts` | `impacts` | 122 | Hard cuts, title slams, logo hits, beat drops |
| `03 تصاعد - Risers` | `risers` | 28 | Building tension before a reveal (riser) or releasing it after (downlifter) |
| `04 واجهات ونقرات - UI & Clicks` | `ui-clicks` | 149 | Screen demos, button presses, cursor clicks, toggles, typing, items popping in |
| `05 نغمات - Chimes & Tones` | `chimes-tones` | 41 | Success states, notifications, checkmarks, power-ups |
| `06 تنبيهات وأخطاء - Alerts` | `alerts` | 8 | Errors, wrong answers, warnings |
| `07 خيال علمي - Sci-Fi` | `sci-fi` | 103 | Tech/futuristic visuals, lasers, glitches, engines, force fields |
| `08 فولي وحركة - Foley` | `foley` | 124 | Footsteps, doors, cloth, cards, chips, dice, physical props |
| `09 موسيقى قصيرة - Jingles` | `jingles` | 85 | Short musical stings for intros, outros and end cards |

All files are WAV, between 0.02 s and 5 s long.

## Go-to sounds

A short list to start from. Each ID maps to an entry in `sounds.json` (with its download URL).

| Moment in the video | Sound ID | Length |
|---|---|---:|
| Fast scene transition | `transitions/whoosh_fast` | 0.46 s |
| Soft/slow transition | `transitions/whoosh_soft` | 0.82 s |
| Slide / swipe in | `transitions/swipe` | 0.35 s |
| Text zips in | `transitions/zip_soft` | 0.28 s |
| Reverse whoosh into a cut | `transitions/whoosh_rev` | 0.55 s |
| Big title or logo hit | `impacts/boom` | 1.92 s |
| Beat drop | `impacts/bass_drop` | 0.90 s |
| Dramatic sting | `impacts/stinger` | 2.26 s |
| Subtle emphasis | `impacts/low_thud` | 0.67 s |
| Build-up before a reveal | `risers/riser` | 1.23 s |
| Swell into a cut | `risers/reverse_swell` | 0.70 s |
| Wind-down after a reveal | `risers/downlifter_01` | 0.94 s |
| Mouse click | `ui-clicks/ui_click` | 0.03 s |
| Bullet / icon pops in | `ui-clicks/pop` | 0.12 s |
| Checkmark appears | `ui-clicks/check` | 0.15 s |
| Typing text on screen | `ui-clicks/typing` | 0.99 s |
| Screenshot / camera | `ui-clicks/shutter` | 0.14 s |
| Notification | `ui-clicks/notify` | 0.50 s |
| Success / correct | `chimes-tones/ding` | 0.87 s |
| Magic / highlight | `chimes-tones/sparkle` | 0.66 s |
| Error / wrong | `alerts/interface_error_001` | 0.16 s |
| Glitch effect | `sci-fi/glitch` | 0.35 s |
| Intro / outro sting | `jingles/music_jingles_n_e_s00` | 1.73 s |

## Using these sounds with Claude (or another AI) to make videos

### 1. Point the AI at the manifest

`sounds.json` is the entry point for an AI. It is one sound per line, so it can be fetched, grepped or read in chunks:

```
https://raw.githubusercontent.com/ashrafatam96/sound-sfx/main/sounds.json
```

Each entry looks like this:

```json
{"id": "transitions/whoosh_fast", "duration_sec": 0.458, "tags": ["whoosh", "fast"], "file": "01 انتقالات - Transitions/whoosh_fast.wav", "url": "https://raw.githubusercontent.com/ashrafatam96/sound-sfx/main/01%20..."}
```

Use the `url` field as-is. The folder names contain Arabic text, spaces and `&`, so a hand-built URL will usually break; the manifest already has them percent-encoded. To use the jsDelivr CDN instead of GitHub, replace the `url_base` prefix with `cdn_base` (both are listed at the top of the file).

### 2. Example prompt

Paste something like this into Claude along with your video request:

> For sound effects, use the library at https://github.com/ashrafatam96/sound-sfx.
> Read the index at https://raw.githubusercontent.com/ashrafatam96/sound-sfx/main/sounds.json, pick sounds by `id`/`tags`/`duration_sec`, and use each sound's `url` exactly as written.
> Add a whoosh on every scene transition, a pop when each bullet point appears, a riser + impact for the main reveal, and a jingle on the end card. Keep effects around −12 dB under the voice-over.

### 3. Getting the files

**Claude Code / local projects** — clone the repo (or just the folders you need) next to your video project:

```bash
git clone --depth 1 https://github.com/ashrafatam96/sound-sfx.git
```

```bash
git clone --depth 1 --filter=blob:none --sparse https://github.com/ashrafatam96/sound-sfx.git && cd sound-sfx && git sparse-checkout set "01 انتقالات - Transitions" "02 ضربات - Impacts"
```

Always quote the paths in shell commands because of the spaces and `&`.

**Claude.ai chat** — if the code sandbox cannot download from GitHub, download the files you want from this repo and upload them into the chat, then mention which ones are which.

### 4. Examples

**Remotion** (React video) — play a sound at a specific frame directly from its URL:

```tsx
import { Audio, Sequence } from "remotion";

const WHOOSH = "https://raw.githubusercontent.com/ashrafatam96/sound-sfx/main/01%20%D8%A7%D9%86%D8%AA%D9%82%D8%A7%D9%84%D8%A7%D8%AA%20-%20Transitions/whoosh_fast.wav";

export const SceneCut = () => (
  <Sequence from={90}>
    <Audio src={WHOOSH} volume={0.6} />
  </Sequence>
);
```

**ffmpeg** — mix a whoosh at 2.5 s and an impact at 4 s over an existing video:

```bash
ffmpeg -i video.mp4 \
  -i "sound-sfx/01 انتقالات - Transitions/whoosh_fast.wav" \
  -i "sound-sfx/02 ضربات - Impacts/boom.wav" \
  -filter_complex "[1:a]adelay=2500|2500,volume=0.6[s1];[2:a]adelay=4000|4000,volume=0.8[s2];[0:a][s1][s2]amix=inputs=3:duration=first:normalize=0[a]" \
  -map 0:v -map "[a]" -c:v copy out.mp4
```

(If the video has no audio track, drop `[0:a]` and use `inputs=2`.)

### Timing tips for AI-generated edits

- Start a whoosh slightly **before** the cut (about 0.1–0.2 s) so the peak lands on the cut.
- A riser should **end** exactly where the impact starts: `riser_start = impact_time − duration_sec`.
- Use `duration_sec` from the manifest to avoid sounds running into the next scene.
- Vary similar sounds (`whoosh_fast_02`, `whoosh_fast_06`, …) so repeated transitions don't sound identical.

## Adding or renaming sounds

After changing any files, regenerate the index (Python 3, no dependencies):

```bash
python scripts/build_manifest.py
```

New folders must be added to `CATEGORIES` in [`scripts/build_manifest.py`](scripts/build_manifest.py).

## License

[MIT](LICENSE) © Ashraf Atam
