import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
# D = per-run working root (holds the client logo + candidate cover frames); override via env.
D=os.environ.get("FACTORY_ROOT", os.getcwd())
W=os.environ.get("REEL_WORKDIR", D)
F=os.path.abspath(os.path.join(os.path.dirname(__file__),"..","..","fonts"))  # repo fonts
AMBER=(234,89,32); AMBER2=(255,138,72); WHITE=(246,244,241); INK=(12,10,8)
m9=lambda s: ImageFont.truetype(F+"/montserrat-v31-cyrillic_latin-900.ttf",s)
m7=lambda s: ImageFont.truetype(F+"/montserrat-v31-cyrillic_latin-700.ttf",s)
man=lambda s: ImageFont.truetype(F+"/manrope-v20-cyrillic_latin-800.ttf",s)
rub=lambda s: ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",s)
def sp(n): return f"{int(n):,}".replace(","," ")
# --- background: hero quad frame, cinematic grade ---
bg=Image.open(W+"/cover_cand/b05.jpg").convert("RGB").resize((1080,1920),Image.LANCZOS)
bg=ImageEnhance.Contrast(bg).enhance(1.12); bg=ImageEnhance.Color(bg).enhance(1.14)
# warm amber push in highlights
ov=Image.new("RGB",(1080,1920),(30,14,4)); bg=Image.blend(bg,Image.composite(ov,bg,Image.new("L",(1080,1920),26)),0.35) if False else bg
# gradient scrim bottom->up + top slight
scrim=Image.new("L",(1080,1920),0); sd=ImageDraw.Draw(scrim)
for y in range(1920):
    a=0
    if y>780: a=int(min(232,(y-780)/(1920-780)*252))
    if y<360: a=max(a,int((360-y)/360*120))
    sd.line([(0,y),(1080,y)],fill=a)
bg=Image.composite(Image.new("RGB",(1080,1920),(6,6,9)),bg,scrim)
d=ImageDraw.Draw(bg)
# --- top brand row: real logo + wordmark ---
logo=Image.open(D+"/logo/logo_hd.png").convert("RGBA")
lr=logo.resize((120,120),Image.LANCZOS); bg.paste(lr,(70,80),lr)
d.text((205,96),"DIESEL",font=m9(58),fill=WHITE)
d.text((205,158),"CARGO",font=m7(38),fill=AMBER2)
# --- eyebrow ---
d.text((72,1055),"ПРЕМИАЛЬНЫЙ КВАДРОЦИКЛ · 800 CC · 4×4",font=man(33),fill=AMBER2)
# --- title ---
d.text((68,1100),"ПРЕМИУМ",font=m9(150),fill=WHITE)
d.text((68,1250),"КВАДРО",font=m9(150),fill=WHITE)
# amber underline accent
d.rounded_rectangle([74,1420,470,1436],8,fill=AMBER)
d.text((72,1452),"ПОД КЛЮЧ ИЗ КИТАЯ",font=m9(78),fill=AMBER2)
# --- price pill ---
pre="от "; num=sp(995000)+" ";
pf=m9(96); pre_f=m7(52); rf=rub(88)
prew=d.textlength(pre,font=pre_f); numw=d.textlength(num,font=pf); rw=d.textlength("₽",font=rf)
pw=prew+numw+rw+96; x0=72
d.rounded_rectangle([x0,1580,x0+pw,1580+150],36,fill=AMBER)
d.text((x0+48,1618),pre,font=pre_f,fill=INK)
d.text((x0+48+prew,1596),num,font=pf,fill=INK)
d.text((x0+48+prew+numw,1600),"₽",font=rf,fill=INK)
# --- sub line ---
d.text((72,1772),"доставка · таможня · документы · учёт",font=man(36),fill=WHITE)
# watermark
d.text((72,1856),"dieselcompany.pro",font=m7(34),fill=(210,205,200))
bg.save(W+"/cover.jpg",quality=93)
print("cover ok", os.path.getsize(W+"/cover.jpg")//1024,"KB")
