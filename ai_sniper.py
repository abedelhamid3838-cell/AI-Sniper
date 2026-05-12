import requests
import re
from concurrent.futures import ThreadPoolExecutor

S = [
    "https://raw.githubusercontent.com/iptv-org/iptv/master/streams/ar.m3u",
    "https://raw.githubusercontent.com/MoiraSama/IPTV-Arabic/main/Arabic.m3u",
    "https://raw.githubusercontent.com/tarekzort/IPTV-Daily/main/arabic.m3u",
    "https://raw.githubusercontent.com/FazzAnnas/IPTV-Arabic-List/main/Arabic.m3u"
]

H = {'User-Agent': 'Mozilla/5.0'}
T = r'beIN|OSN|alkass|SSC'

def v(n, u):
    try:
        r = requests.head(u, headers=H, timeout=5, allow_redirects=True)
        if r.status_code == 200:
            return f"{n}\n{u}\n"
    except: return None

def run():
    all_links = []
    for s in S:
        try:
            r = requests.get(s, headers=H, timeout=10)
            lines = r.text.splitlines()
            for i in range(len(lines)):
                if re.search(T, lines[i], re.IGNORECASE) and i+1 < len(lines):
                    all_links.append((lines[i], lines[i+1].strip()))
        except: continue
    
    with ThreadPoolExecutor(max_workers=50) as e:
        res = list(e.map(lambda p: v(p[0], p[1]), list(set(all_links))))
    
    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        for r in filter(None, res): f.write(r)

if __name__ == "__main__":
    run()
