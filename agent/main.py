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
    words=" ".join(i["title"].lower() for i in items)
    keywords={"kinetic_rings":["kinetic","sculpture","ring","motion"],
              "color_orbits":["color","rainbow","palette","design"],
              "optical_waves":["optical","illusion","wave","geometry"]}
    scores={key:sum(words.count(word) for word in kws) for key,kws in keywords.items()}
    day=datetime.now(timezone.utc).timetuple().tm_yday
    themes=list(keywords)
    theme=max(themes,key=lambda k:(scores[k], (day+themes.index(k))%3))
    return theme,scores

def make_frame(theme,t):
    w,h=720,1280
    image=Image.new("RGB",(w,h),(12,13,32))
    d=ImageDraw.Draw(image,"RGBA")
    for y in range(0,h,12):
        pulse=int(12*math.sin(y/130+t))
        d.rectangle((0,y,w,y+12),fill=(20+pulse//3,19+pulse//3,45+pulse//2,255))
    cx,cy=w//2,h//2
    for i in range(18):
        a=t*1.3+i*2*math.pi/18
        r=145+35*math.sin(t*.7+i*.5)
        if theme=="color_orbits":r=100+i*12
        x=cx+math.cos(a)*r;y=cy+math.sin(a)*r
        s=22+int(12*(1+math.sin(t+i)))
        d.ellipse((x-s,y-s,x+s,y+s),fill=((i*31+int(t*40))%256,(100+i*17)%256,(250-i*9)%256,235))
    for j in range(8):
        r=75+j*37
        if theme=="kinetic_rings":
            d.arc((cx-r,cy-r,cx+r,cy+r),int(t*75+j*35),int(t*75+j*35+160),fill=(80+j*16,210-j*12,240,175),width=7)
        elif theme=="optical_waves":
            pts=[(x,int(cy+(j-4)*64+18*math.sin(x/37+t*3+j*.6))) for x in range(0,w+1,10)]
            d.line(pts,fill=(125+j*12,155+j*8,230,170),width=5)
    try:font=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",32)
    except OSError:font=ImageFont.load_default()
    d.text((w//2,140),theme.replace("_"," ").upper(),font=font,anchor="mm",fill=(245,245,255,255))
    d.text((w//2,h-150),"Watch the patterns flow",font=font,anchor="mm",fill=(235,238,255,255))
    return image

def main():
    items,error=research()
    theme,scores=select_theme(items)
    plan={"created_utc":datetime.now(timezone.utc).isoformat(),"theme":theme,
          "research_method":"Google News RSS headlines, not Instagram trend analytics",
          "headlines":items[:8],"research_error":error,"scores":scores,
          "video_type":"Original algorithmic animation (not generative AI)",
          "instagram_status":"NOT CONNECTED; PREVIEW ONLY",
          "caption":"What pattern did you like most? ✨ #satisfying #visualart #reels"}
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
