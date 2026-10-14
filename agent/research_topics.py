"""Free research-based topic shortlist for Instagram (not an LLM or Instagram trends API).
Uses public news headlines and transparent heuristics. Never posts anything.
"""
import json, urllib.parse, urllib.request, xml.etree.ElementTree as ET
from datetime import datetime,timezone
from pathlib import Path

TOPICS = {
 "AI and technology": ["AI tools","robotics","future technology"],
 "Science and space": ["space discovery","science breakthrough","astronomy"],
 "Mystery and history": ["archaeology discovery","unexplained history"],
 "Nature and animals": ["wildlife discovery","amazing nature"],
 "Visual satisfaction": ["kinetic art","optical illusion","satisfying design"],
 "Amazing facts": ["record breaking inventions","unusual facts"],
}
def fetch(q):
 url="https://news.google.com/rss/search?q="+urllib.parse.quote(q)+"&hl=en-US&gl=US&ceid=US:en"
 try:
  req=urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0"})
  with urllib.request.urlopen(req,timeout=9) as rsp:
   root=ET.fromstring(rsp.read(250000))
  return [{"headline":(n.findtext("title") or "").strip(),"source_url":(n.findtext("link") or "").strip()} for n in root.findall("./channel/item")[:5]],None
 except Exception as e:
  return [],type(e).__name__

def main():
 results=[]
 for category,queries in TOPICS.items():
  articles=[]; failures=[]
  for query in queries:
   news,error=fetch(query)
   if error: failures.append(query+":"+error)
   articles.extend(news)
  seen=set(); unique=[]
  for article in articles:
   if article["headline"].lower() not in seen:
    unique.append(article);seen.add(article["headline"].lower())
  score=min(len(unique),10)
  results.append({"category":category,"score":score,"headlines":unique[:5],"errors":failures})
 results.sort(key=lambda r:r["score"],reverse=True)
 chosen=next((x for x in results if x["score"]>0),None)
 report={"timestamp_utc":datetime.now(timezone.utc).isoformat(),
         "method":"Public Google News RSS topic discovery; does not measure Instagram trends, virality or engagement",
         "recommendation": chosen["category"] if chosen else "No verified topic (research unavailable)",
         "topics":results,"publishing_status":"Preview research only. No auto posting."}
 Path("output").mkdir(exist_ok=True)
 Path("output/topic_research.json").write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
 print("Broad-topic research saved; selected:",report["recommendation"])

if __name__=="__main__": main()
