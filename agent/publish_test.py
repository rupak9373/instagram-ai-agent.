"""Publish a public Instagram test Reel using Instagram Login API.
Only called by manual GitHub Actions workflow. No auto-post scheduling.
"""
import json,os,time,sys,urllib.request,urllib.parse,urllib.error

TOKEN=os.environ["INSTAGRAM_ACCESS_TOKEN"]
VIDEO_URL=os.environ["VIDEO_URL"]
BASE="https://graph.instagram.com/v24.0"
EXPECTED="stor.ysketch"

def request(path, data=None):
    url=BASE+"/"+path
    payload=urllib.parse.urlencode(data).encode() if data is not None else None
    req=urllib.request.Request(url,data=payload,headers={"Authorization":"Bearer "+TOKEN,"Accept":"application/json"})
    try:
        with urllib.request.urlopen(req,timeout=45) as resp:
            return json.load(resp)
    except urllib.error.HTTPError as e:
        try:
            error=json.loads(e.read().decode()).get("error",{})
            print("Instagram API failed:",e.code,error.get("message","unknown"),"code",error.get("code"))
        except Exception:
            print("Instagram API failed:",e.code)
        sys.exit(1)

def main():
    me=request("me?fields=id,username")
    if me.get("username","").lower()!=EXPECTED:
        sys.exit("Wrong Instagram account; nothing published.")
    account_id=me["id"]
    url_req=urllib.request.Request(VIDEO_URL,headers={"User-Agent":"InstagramAgent/1.0"},method="HEAD")
    try:
        with urllib.request.urlopen(url_req,timeout=30) as response:
            if response.status!=200: raise ValueError("public MP4 not accessible")
            mime=response.headers.get("Content-Type","")
            if "text/html" in mime: raise ValueError("video URL points to HTML, not MP4")
            print("Video URL available, content type:",mime)
    except Exception as e:
        sys.exit("Public video URL not reachable: "+type(e).__name__)
    caption="A little visual magic ✨ Which pattern is your favorite? #satisfying #visualart #motiongraphics #reels"
    container=request(account_id+"/media",{"media_type":"REELS","video_url":VIDEO_URL,"caption":caption,"share_to_feed":"true"})
    cid=container.get("id")
    if not cid:sys.exit("No creation ID; not published")
    print("Container created; waiting for processing...")
    for attempt in range(20):
        time.sleep(15)
        status=request(cid+"?fields=status_code,status").get("status_code")
        print("Processing:",status)
        if status=="FINISHED":break
        if status in ("ERROR","EXPIRED"):sys.exit("Instagram could not process the video.")
    else:
        sys.exit("Video processing timed out; nothing published.")
    # Explicit publishing action only after video is FINISHED
    published=request(account_id+"/media_publish",{"creation_id":cid})
    mid=published.get("id")
    if not mid:sys.exit("No media ID returned; check account before retrying.")
    print("PUBLISHED media ID:",mid)
    result=request(mid+"?fields=permalink")
    print("Instagram Reel:",result.get("permalink","https://www.instagram.com/"+EXPECTED+"/"))
if __name__=="__main__": main()
