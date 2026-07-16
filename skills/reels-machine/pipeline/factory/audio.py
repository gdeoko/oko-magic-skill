import os,json,subprocess
W=os.path.dirname(os.path.abspath(__file__)); VO=W+"/vo"; SFX=W+"/sfx"
T=json.load(open(W+"/timing.json")); SS=T["seg_start"]; DUR=T["segdurs"]
ENDCARD=2.4
TOTAL=round(T["content_end"]+ENDCARD,3)
ORDER=["s1","s2","s3","s4","s5","s6"]
# --- inputs ---
inp=[]; f=[]; amix_labels=[]
def add(path): inp.extend(["-i",path]); return len(inp)//2-1
# music input 0
mi=add(f"{SFX}/music.mp3")
# VO segment inputs
voi={s:add(f"{VO}/{s}.mp3") for s in ORDER}
# SFX inputs (logical, varied). (file, offset, gain)
SFXPLAN=[
 ("whoosh_a",SS["s1"]-0.15,0.5),          # into hook
 ("splash",  SS["s2"]+0.35,0.55),         # water/river clip b04
 ("engine",  SS["s2"]+0.1,0.28),          # power (800cc) bed, low
 ("pop",     SS["s2"]+DUR["s2"]*0.40,0.6),# spec chip 1
 ("pop",     SS["s2"]+DUR["s2"]*0.52,0.6),# spec chip 2
 ("pop",     SS["s2"]+DUR["s2"]*0.64,0.6),# spec chip 3
 ("whoosh_b",SS["s3"]-0.12,0.55),         # transition to suspension
 ("whoosh_a",SS["s4"]-0.12,0.5),          # transition
 ("riser",   SS["s4"]-0.55,0.5),          # build into price
 ("impact",  SS["s4"]+0.28,0.7),          # price pill slam
 ("tick",    SS["s4"]+0.9,0.4),
 ("tick",    SS["s4"]+1.5,0.4),
 ("tick",    SS["s4"]+2.1,0.4),
 ("whoosh_b",SS["s5"]-0.12,0.5),          # transition to checklist
 ("check",   SS["s5"]+DUR["s5"]*0.24,0.6),# checklist row 1
 ("check",   SS["s5"]+DUR["s5"]*0.42,0.6),# row 2
 ("check",   SS["s5"]+DUR["s5"]*0.60,0.6),# row 3
 ("whoosh_a",SS["s6"]-0.12,0.5),          # transition to CTA
 ("shimmer", T["content_end"]+0.15,0.55), # endcard logo reveal
]
sfxi=[]
for name,off,g in SFXPLAN:
    sfxi.append((add(f"{SFX}/{name}.mp3"),off,g))
# --- filters ---
# music: loop-safe trim, fade in/out, base volume
f.append(f"[{mi}]atrim=0:{TOTAL},asetpts=N/SR/TB,"
         f"volume=0.16,afade=t=in:st=0:d=1.3,afade=t=out:st={TOTAL-1.6:.2f}:d=1.6[mus]")
# VO: delay each to its start, mix
volabels=[]
for s in ORDER:
    off=int(SS[s]*1000)
    f.append(f"[{voi[s]}]adelay={off}|{off},volume=1.35[vo{s}]"); volabels.append(f"[vo{s}]")
f.append("".join(volabels)+f"amix=inputs={len(volabels)}:normalize=0:dropout_transition=0,alimiter=limit=0.95,asplit=2[voduck][vo]")
# duck music under VO
f.append("[mus][voduck]sidechaincompress=threshold=0.04:ratio=7:attack=12:release=320:makeup=1[musd]")
# SFX delays
slabels=[]
for k,(i,off,g) in enumerate(sfxi):
    off_ms=max(0,int(off*1000))
    f.append(f"[{i}]adelay={off_ms}|{off_ms},volume={g}[sx{k}]")
    slabels.append(f"[sx{k}]")
# final mix: ducked music + VO + all SFX
allmix="[musd][vo]"+"".join(slabels)
f.append(allmix+f"amix=inputs={2+len(slabels)}:normalize=0:dropout_transition=0,"
         f"atrim=0:{TOTAL},alimiter=limit=0.97,aresample=48000[aout]")
fc=";".join(f)
cmd=["ffmpeg","-y"]+inp+["-filter_complex",fc,"-map","[aout]","-c:a","aac","-b:a","192k",W+"/audio.m4a","-loglevel","error"]
open(W+"/audio_cmd.txt","w").write(" ".join(cmd))
r=subprocess.run(cmd,capture_output=True,text=True)
if r.returncode!=0: print("AUDIO ERR:",r.stderr[-1200:])
else:
    d=subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",W+"/audio.m4a"],capture_output=True,text=True).stdout.strip()
    print("AUDIO OK",d,"s | TOTAL",TOTAL)
