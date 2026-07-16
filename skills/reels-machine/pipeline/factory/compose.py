import os,json,subprocess
W=os.path.dirname(os.path.abspath(__file__))
T=json.load(open(W+"/timing.json")); SS=T["seg_start"]
def run(c,label=""):
    r=subprocess.run(c,capture_output=True,text=True)
    if r.returncode!=0: print("ERR",label,r.stderr[-800:])
    return r.returncode
# endcard.mp4 is pre-rendered (animated). Concat base + endcard.
open(W+"/vlist.txt","w").write(f"file '{W}/base.mp4'\nfile '{W}/endcard.mp4'\n")
run(["ffmpeg","-y","-f","concat","-safe","0","-i",W+"/vlist.txt","-c","copy",W+"/vfull.mp4"],"concat")
# overlays: 4 hero infographics (itsoffset) + accents (top) + subtitles (bottom), both full length
HERO=[("spec",SS["s2"]),("susp",SS["s3"]),("price",SS["s4"]),("check",SS["s5"])]
inp=["-i",W+"/vfull.mp4"]
for name,off in HERO:
    inp+=["-itsoffset",f"{off:.3f}","-i",f"{W}/ig/{name}.mov"]
inp+=["-i",f"{W}/ig/accents.mov","-i",f"{W}/ig/subs.mov"]  # offset 0
parts=[]; prev="[0:v]"
for i,(name,off) in enumerate(HERO):
    out=f"[o{i}]"; parts.append(f"{prev}[{i+1}:v]overlay=0:0:eof_action=pass:format=auto{out}"); prev=out
ai=len(HERO)+1  # accents input
parts.append(f"{prev}[{ai}:v]overlay=0:0:eof_action=pass:format=auto[oa]")
si=ai+1          # subs input
parts.append(f"[oa][{si}:v]overlay=0:0:eof_action=pass:format=auto[v]")
fc=";".join(parts)
cmd=["ffmpeg","-y"]+inp+["-i",W+"/audio.m4a","-filter_complex",fc,
     "-map","[v]","-map",f"{si+1}:a","-c:v","libx264","-preset","medium","-crf","20",
     "-pix_fmt","yuv420p","-c:a","aac","-b:a","192k","-movflags","+faststart",W+"/reel.mp4","-loglevel","error"]
open(W+"/compose_cmd.txt","w").write(" ".join(cmd))
run(cmd,"compose")
d=subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",W+"/reel.mp4"],capture_output=True,text=True).stdout.strip()
sz=os.path.getsize(W+"/reel.mp4")//1024//1024 if os.path.exists(W+"/reel.mp4") else 0
print("REEL",d,"s",sz,"MB")
