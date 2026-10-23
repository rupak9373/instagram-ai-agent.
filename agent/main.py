"""Create an original 9:16 procedural animation and a transparent research log.
Never publishes to Instagram. No secrets or paid AI services are used.
"""
import json, math, subprocess, tempfile, urllib.parse, urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

OUT=Path("output")
OUT.mkdir(exist_ok=True)
QUERY="satisfying visual art OR kinetic sculpture OR optical illusion OR colorful design"
RSS="https://news.google.com/rss/search?q="+urllib.parse.quote(QUERY)+"&hl=en-US&gl=US&ceid=US:en"

def research():
    try:
        req=urllib.request.Request(RSS,headers={"User-Agent":"Mozilla/5.0"})
        with urllib.request.urlopen(req,timeout=12) as res:
            root=ET.fromstring(res.read(500000))
        return [{"title": (a.findtext("title") or "").strip(),
                 "url": (a.findtext("link") or "").strip()}
                for a in root.findall("./channel/item")[:15]], None
    except Exception as exc:
        return [], str(exc)[:160]

def select_theme(items):
    # Deterministic daily variety without relying on external headlines.
    themes = ["bounce_maze", "bounce_bucket", "bounce_bottle", "bounce_car"]
    day = datetime.now(timezone.utc).timetuple().tm_yday
    return themes[day % len(themes)], {"daily_rotation": day % len(themes)}

def make_frame(theme, t):
    w, h = 720, 1280
    im = Image.new("RGB", (w, h), (12, 16, 35))
    d = ImageDraw.Draw(im, "RGBA")
    colors = [(255, 100, 145), (80, 225, 255), (255, 213, 85),
              (170, 125, 255), (110, 245, 155), (255, 145, 90)]
    # Animated ball physics: gravity and perfectly elastic floor bounces.
    floor = 1010
    d.rounded_rectangle((55, 290, 665, floor + 28), radius=35,
                        outline=(110, 155, 235, 220), width=9)
    if theme == "bounce_maze":
        for j in range(4):
            y = 450 + j * 115
            d.rounded_rectangle((90 if j % 2 else 290, y, 450 if j % 2 else 630, y + 13),
                                radius=6, fill=(120, 170, 230, 190))
    elif theme == "bounce_bucket":
        d.line([(180, 680), (225, 1010), (495, 1010), (540, 680)],
               fill=(130, 225, 250, 210), width=13, joint="curve")
    elif theme == "bounce_bottle":
        d.line([(245, 420), (245, 530), (170, 610), (190, 1005),
                (530, 1005), (550, 610), (475, 530), (475, 420)],
               fill=(130, 225, 250, 210), width=13, joint="curve")
    else:
        d.rounded_rectangle((150, 755, 565, 950), radius=50,
                            outline=(130, 225, 250, 210), width=12)
        for x in (245, 490):
            d.ellipse((x-42, 925, x+42, 1009), fill=(65, 85, 130, 255),
                      outline=(180, 230, 255, 255), width=7)
    for i in range(12):
        radius = 20 + i % 3 * 5
        phase = (t * (1.35 + i * .08) + i * .39) % 2.0
        # Triangle-wave vertical travel with easing near the apex.
        bounce = 1 - (phase - 1) ** 2
        x = 115 + ((i * 73 + int(t * (38 + i * 5))) % 490)
        y = floor - radius - bounce * (310 + (i % 4) * 65)
        r, g, b = colors[i % len(colors)]
        d.ellipse((x-radius, y-radius, x+radius, y+radius), fill=(r,g,b,255))
        d.ellipse((x-radius*.55, y-radius*.65, x-radius*.12, y-radius*.2),
                  fill=(255,255,255,170))
        d.ellipse((x-radius*1.2, floor+7, x+radius*1.2, floor+16),
                  fill=(0,0,0,65))
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 37)
    except OSError:
        font = ImageFont.load_default()
    d.text((w//2, 155), "BOUNCING BALLS", font=font, anchor="mm", fill=(245,245,255,255))
    d.text((w//2, 1125), "SO SATISFYING!", font=font, anchor="mm", fill=(245,245,255,255))
    return im

def main():
    items,error=research()
    theme,scores=select_theme(items)
    plan={"created_utc":datetime.now(timezone.utc).isoformat(),"theme":theme,
          "research_method":"Google News RSS headlines, not Instagram trend analytics",
          "headlines":items[:8],"research_error":error,"scores":scores,
          "video_type":"Original algorithmic animation (not generative AI)",
          "instagram_status":"Publishing handled separately by GitHub Actions",
          "caption":"Which bouncing ball is your favorite? 🌈 #bouncingball #satisfying #reels"}
    (OUT/"plan.json").write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding="utf-8")
    with tempfile.TemporaryDirectory() as tmp:
        tmp=Path(tmp)
        for i in range(120):
            make_frame(theme,i/15).save(tmp/(f"{i:04d}.png"),compress_level=1)
        subprocess.run(["ffmpeg","-nostdin","-y","-hide_banner","-loglevel","error",
          "-framerate","15","-i",str(tmp/"%04d.png"),"-r","30","-c:v","libx264",
          "-preset","veryfast","-pix_fmt","yuv420p","-movflags","+faststart",str(OUT/"reel.mp4")],
          check=True,timeout=180)
    print("Generated",str(OUT/"reel.mp4"),"theme",theme,"headlines",len(items))

if __name__=="__main__":
    main()
