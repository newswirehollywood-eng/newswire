#!/usr/bin/env python3
"""
REEL MAKER: turns a story into a 1080x1920 vertical video (Instagram Reels,
Facebook video, TikTok, YouTube Shorts) from our branded card plus animated
headline text and on-screen captions. Free: uses ffmpeg only.

Plain English: you give it a small recipe file (JSON) with the brand, the
story's card image and 3 to 5 short "beats" (each beat is one screen of big
text plus one caption line). It builds a ~5 second shot per beat, slides the
text up and fades it in, and stitches them into one MP4 with a silent audio
track (some apps reject video with no audio track at all).

Run:  python3 tools/reels/make_reel.py recipe.json out.mp4

Recipe example:
{
  "brand": "newswire",                       # newswire | hna | gospel
  "card": "docs/img/my-story-card.jpg",      # 1080x1080 branded card
  "beats": [
    {"big": "RUSSELL BRAND\\nFOUND GUILTY", "cap": "London jury, Nov 5"},
    ...
  ],
  "end": "newswirehollywood.com"
}
Images: only our cards, licensed or free-licensed images. Never another
outlet's photo.
"""
import json, os, subprocess, sys, tempfile

BRANDS = {
    "newswire": {"bg": "0x0A0003", "accent": "0xD1002E", "rule": "0xB8860B", "name": "NEWSWIRE HOLLYWOOD"},
    "hna": {"bg": "0x0C0811", "accent": "0xFF2E88", "rule": "0xFFC233", "name": "HOLLYWOOD NEWS ACCESS"},
    "gospel": {"bg": "0x0A0A0C", "accent": "0xF0B429", "rule": "0xF0B429", "name": "GOSPEL NEWS ACCESS"},
}
BOLD = "/usr/share/fonts/opentype/inter/InterDisplay-Bold.otf"
if not os.path.exists(BOLD):
    BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/opentype/inter/Inter-SemiBoldItalic.otf"
if not os.path.exists(REG):
    REG = BOLD
BEAT = 5.0


def esc(t):
    # drawtext reads text from a file, so only the file needs writing; no escaping games.
    return t


def shot(i, beat, b, card, tmp, end_text):
    """One beat: card (first beat) or brand background, plus animated text."""
    out = os.path.join(tmp, "s%d.mp4" % i)
    tf = os.path.join(tmp, "t%d.txt" % i)
    cf = os.path.join(tmp, "c%d.txt" % i)
    open(tf, "w").write(beat["big"].replace("\\n", "\n"))
    open(cf, "w").write(beat.get("cap", ""))
    lines = beat["big"].count("\n") + beat["big"].count("\\n") + 1
    size = 104 if lines <= 3 else 86
    # Text slides up 60px and fades in over 0.6s.
    slide = "if(lt(t,0.6),(1-t/0.6)*60,0)"
    alpha = "if(lt(t,0.6),t/0.6,1)"
    first = i == 0
    v = []
    if first:
        inputs = ["-loop", "1", "-t", str(BEAT), "-i", card]
        # Slow push-in on the card, placed in the middle of the tall frame.
        v.append("[0:v]scale=1080:1080,zoompan=z='min(zoom+0.0009,1.08)':d=%d:s=1080x1080:fps=30,"
                 "pad=1080:1920:0:420:color=%s[bg]" % (int(BEAT * 30), b["bg"]))
        ty = "1440+%s" % slide
        big_draw = ""  # the card already carries the headline
    else:
        inputs = ["-f", "lavfi", "-t", str(BEAT), "-i", "color=c=%s:s=1080x1920:r=30" % b["bg"]]
        v.append("[0:v]drawbox=x=80:y=300:w=140:h=14:color=%s:t=fill[bg]" % b["accent"])
        ty = "(h-text_h)/2-120+%s" % slide
        big_draw = ("drawtext=fontfile=%s:textfile=%s:fontcolor=white:fontsize=%d:line_spacing=14:"
                    "x=80:y='%s':alpha='%s'," % (BOLD, tf, size, ty, alpha))
    cap_y = "1640" if not first else "1560"
    chain = ("[bg]%s"
             "drawbox=x=0:y=1600:w=1080:h=4:color=%s:t=fill,"
             "drawtext=fontfile=%s:textfile=%s:fontcolor=0xF2E9DA:fontsize=46:x=80:y=%s:alpha='%s',"
             "drawtext=fontfile=%s:text='%s':fontcolor=white:fontsize=40:x=80:y=1800,"
             "drawtext=fontfile=%s:text='%s':fontcolor=%s:fontsize=34:x=w-tw-80:y=1806,"
             "format=yuv420p[v]") % (
        big_draw, b["rule"], REG if not first else BOLD, cf, "1640" if not first else "1530",
        "if(lt(t,0.9),max(0,(t-0.3)/0.6),1)", BOLD, b["name"], REG, end_text, b["accent"])
    v.append(chain)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error"] + inputs +
                   ["-filter_complex", ";".join(v), "-map", "[v]", "-t", str(BEAT), "-r", "30",
                    "-c:v", "libx264", "-preset", "medium", "-crf", "20", out], check=True)
    return out


def main():
    recipe = json.load(open(sys.argv[1]))
    out = sys.argv[2]
    b = BRANDS[recipe.get("brand", "newswire")]
    end_text = recipe.get("end", "newswirehollywood.com")
    with tempfile.TemporaryDirectory() as tmp:
        shots = [shot(i, beat, b, recipe["card"], tmp, end_text) for i, beat in enumerate(recipe["beats"])]
        # Crossfade the shots together (0.4s each), then add a silent stereo track.
        n = len(shots)
        args = []
        for s in shots:
            args += ["-i", s]
        fc, last, off = [], "[0:v]", 0.0
        for k in range(1, n):
            off += BEAT - 0.4
            fc.append("%s[%d:v]xfade=transition=fade:duration=0.4:offset=%.2f[x%d]" % (last, k, off, k))
            last = "[x%d]" % k
        total = BEAT * n - 0.4 * (n - 1)
        fc_s = ";".join(fc) if fc else "[0:v]null[x0]"
        last = last if fc else "[x0]"
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error"] + args +
                       ["-f", "lavfi", "-t", "%.2f" % total, "-i", "anullsrc=r=44100:cl=stereo",
                        "-filter_complex", fc_s, "-map", last, "-map", "%d:a" % n,
                        "-c:v", "libx264", "-profile:v", "high", "-pix_fmt", "yuv420p", "-preset", "medium",
                        "-crf", "21", "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart",
                        "-shortest", out], check=True)
    print(out)


if __name__ == "__main__":
    main()
