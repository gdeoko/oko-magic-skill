import os,json
W=os.path.dirname(os.path.abspath(__file__))
TOTAL=json.load(open(W+"/words.json"))["total"]
FB="file://"+os.path.abspath(os.path.join(os.path.dirname(__file__),"..","..","fonts"))
# one animated graphic per clip, TOP zone (y ~150-430), varied form + position
# type: route|chips|ring|ticks|bar|stamp|badge
A=[
 {"t":1.15,"e":4.45,"type":"route","x":"c","data":{"a":"КИТАЙ","b":"РОССИЯ"}},
 {"t":4.7,"e":8.0,"type":"chips","x":"c","data":{"items":["800 CC","V-TWIN","4×4"]}},
 {"t":8.25,"e":11.3,"type":"ring","x":"r","data":{"label":"ПРОХОДИМОСТЬ","val":100,"suf":"%"}},
 {"t":11.55,"e":14.6,"type":"ticks","x":"r","data":{"items":["грязь","песок","подъёмы"]}},
 {"t":14.85,"e":17.55,"type":"bar","x":"l","data":{"label":"ХОД ПОДВЕСКИ","val":"300 ММ","fill":0.85}},
 {"t":17.8,"e":20.5,"type":"badge","x":"l","data":{"txt":"ЭЛЕКТРОУСИЛИТЕЛЬ РУЛЯ"}},
 {"t":20.8,"e":24.4,"type":"stamp","x":"r","data":{"a":"ПОД","b":"КЛЮЧ"}},
 {"t":24.65,"e":28.3,"type":"badge","x":"r","data":{"txt":"НАПРЯМУЮ С ЗАВОДА"}},
 {"t":28.6,"e":31.55,"type":"ticks","x":"l","data":{"items":["доставка","ПТС","документы"]}},
 {"t":31.8,"e":34.8,"type":"chips","x":"l","data":{"items":["ЭПТС","УЧЁТ","ГИБДД"]}},
 {"t":35.05,"e":37.35,"type":"badge","x":"c","data":{"txt":"ПИШИ ГОРОД","arrow":True}},
 {"t":37.55,"e":39.85,"type":"stamp","x":"c","data":{"a":"DIESEL","b":"CARGO"}},
]
HTML=r"""<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{font-family:'soyuz';src:url('%FB%/SoyuzGrotesk-Bold.ttf')}
@font-face{font-family:'man8';src:url('%FB%/manrope-v20-cyrillic_latin-800.ttf')}
@font-face{font-family:'mont9';src:url('%FB%/montserrat-v31-cyrillic_latin-900.ttf')}
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1920px;background:transparent;overflow:hidden}
#stage{position:absolute;inset:0;font-family:'man8'}
.box{position:absolute;top:180px}
.gl{background:linear-gradient(150deg,rgba(16,12,10,.82),rgba(26,17,12,.66));
  border:2px solid rgba(234,89,32,.55);border-radius:26px;backdrop-filter:blur(5px);
  box-shadow:0 18px 50px rgba(0,0,0,.45)}
.amb{color:#FF7A3C}.wht{color:#F6F4F1}
.chip{display:inline-block;font-family:'man8';font-size:34px;color:#F6F4F1;
  background:rgba(234,89,32,.16);border:2px solid rgba(234,89,32,.6);border-radius:16px;padding:14px 24px;margin:6px}
</style></head><body><div id="stage"></div>
<script>
const A=%A%, TOTAL=%TOTAL%;
const stage=document.getElementById('stage');
function ease(x){return 1-Math.pow(1-x,3)} function clamp(x){return Math.max(0,Math.min(1,x))}
function X(pos,w){ if(pos=='l')return 70; if(pos=='r')return 1010-w; return (1080-w)/2; }
function envelope(p){const i=ease(clamp(p/0.16)),o=ease(clamp((p-0.86)/0.14));return {op:i*(1-o),ty:(1-i)*24 - o*12};}
function el(tag,cls,html){const e=document.createElement('div'); if(cls)e.className=cls; if(html!=null)e.innerHTML=html; return e;}

function draw(a,p){
  const d=a.data; let box=el('div','box'); const env=envelope(p);
  let w=560;
  if(a.type=='chips'){
    w=760; let h='<div style="display:flex;flex-wrap:wrap;justify-content:center;width:'+w+'px">';
    d.items.forEach((it,i)=>{const s=ease(clamp((p-(0.12+i*0.12))/0.2));
      h+='<span class="chip" style="opacity:'+s+';transform:translateY('+((1-s)*20)+'px) scale('+(0.9+0.1*s)+')">'+it+'</span>';});
    h+='</div>'; box.innerHTML=h;
  } else if(a.type=='ring'){
    w=300; const g=ease(clamp((p-0.1)/0.55)); const val=Math.round(d.val*g);
    const C=2*Math.PI*82, off=C*(1-0.78*g);
    box.innerHTML='<div class="gl" style="width:300px;padding:24px;display:flex;flex-direction:column;align-items:center">'
      +'<svg width="200" height="200" viewBox="0 0 200 200"><circle cx="100" cy="100" r="82" fill="none" stroke="rgba(255,255,255,.12)" stroke-width="16"/>'
      +'<circle cx="100" cy="100" r="82" fill="none" stroke="#EA5920" stroke-width="16" stroke-linecap="round" transform="rotate(135 100 100)" stroke-dasharray="'+C+'" stroke-dashoffset="'+off+'"/>'
      +'<text x="100" y="116" text-anchor="middle" font-family="mont9" font-size="58" fill="#F6F4F1">'+val+(d.suf||'')+'</text></svg>'
      +'<div class="amb" style="font-size:28px;letter-spacing:2px;margin-top:6px">'+d.label+'</div></div>';
  } else if(a.type=='ticks'){
    w=520; let h='<div class="gl" style="width:520px;padding:26px 30px">';
    d.items.forEach((it,i)=>{const s=ease(clamp((p-(0.14+i*0.16))/0.2));
      h+='<div style="display:flex;align-items:center;gap:18px;padding:10px 0;opacity:'+(0.25+0.75*s)+';transform:translateX('+((1-s)*24)+'px)">'
        +'<svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="#FF7A3C" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round" style="transform:scale('+(0.5+0.5*s)+')"><circle cx="12" cy="12" r="9"/><path d="M8 12l3 3 5-6"/></svg>'
        +'<span class="wht" style="font-size:38px">'+it+'</span></div>';});
    h+='</div>'; box.innerHTML=h;
  } else if(a.type=='bar'){
    w=560; const g=ease(clamp((p-0.12)/0.5));
    box.innerHTML='<div class="gl" style="width:560px;padding:26px 30px">'
      +'<div style="display:flex;justify-content:space-between;align-items:baseline"><span class="amb" style="font-size:30px;letter-spacing:1px">'+d.label+'</span>'
      +'<span class="wht" style="font-family:mont9;font-size:44px">'+d.val+'</span></div>'
      +'<div style="height:18px;background:rgba(255,255,255,.14);border-radius:9px;margin-top:16px;overflow:hidden">'
      +'<div style="height:100%;width:'+(d.fill*100*g)+'%;background:linear-gradient(90deg,#EA5920,#FF9A5A);border-radius:9px"></div></div></div>';
  } else if(a.type=='stamp'){
    w=260; const r=ease(clamp(p/0.3));
    box.innerHTML='<div style="width:260px;height:260px;position:relative;transform:scale('+(0.5+0.5*r)+') rotate('+((1-r)*-30)+'deg);opacity:'+r+'">'
      +'<div style="position:absolute;inset:0;border:5px solid #EA5920;border-radius:50%;box-shadow:0 0 30px rgba(234,89,32,.5)"></div>'
      +'<div style="position:absolute;inset:22px;border:2px dashed rgba(255,122,60,.7);border-radius:50%"></div>'
      +'<div style="position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;font-family:mont9;line-height:1">'
      +'<span class="wht" style="font-size:52px">'+d.a+'</span><span class="amb" style="font-size:52px">'+d.b+'</span></div></div>';
  } else if(a.type=='route'){
    w=620; const g=clamp((p-0.12)/0.6); const dotx=60+ (620-120)*ease(g);
    box.innerHTML='<div class="gl" style="width:620px;padding:26px 30px;position:relative">'
      +'<div style="display:flex;justify-content:space-between;align-items:center">'
      +'<span class="wht" style="font-family:mont9;font-size:40px">'+d.a+'</span>'
      +'<span class="wht" style="font-family:mont9;font-size:40px">'+d.b+'</span></div>'
      +'<div style="position:relative;height:40px;margin-top:8px">'
      +'<div style="position:absolute;top:19px;left:10px;right:10px;height:3px;background:repeating-linear-gradient(90deg,rgba(255,122,60,.7) 0 14px,transparent 14px 26px)"></div>'
      +'<div style="position:absolute;top:6px;left:'+dotx+'px;width:28px;height:28px;border-radius:50%;background:#FF7A3C;box-shadow:0 0 18px #FF7A3C"></div></div></div>';
  } else if(a.type=='badge'){
    const txt=d.txt+(d.arrow?'  →':''); w=Math.min(720, 120+txt.length*22);
    const pulse=1+(d.arrow?0.04*Math.sin(p*6.28*3):0);
    box.innerHTML='<div class="gl" style="display:inline-flex;align-items:center;padding:22px 34px;border-radius:22px;transform:scale('+pulse+')">'
      +'<span class="wht" style="font-size:38px;letter-spacing:1px">'+txt.replace('→','<span class="amb">→</span>')+'</span></div>';
  }
  box.style.left=X(a.x,w)+'px';
  box.style.opacity=env.op; box.style.transform='translateY('+env.ty+'px)';
  return box;
}
window.render=function(t){
  const ts=t*TOTAL; stage.innerHTML='';
  A.forEach(a=>{ if(ts>=a.t-0.05 && ts<=a.e+0.3){ const p=(ts-a.t)/(a.e-a.t); stage.appendChild(draw(a,clamp(p))); }});
};
window.render(0);
</script></body></html>"""
html=(HTML.replace("%FB%",FB).replace("%A%",json.dumps(A,ensure_ascii=False))
          .replace("%TOTAL%",str(TOTAL)))
open(W+"/ig/html/accents.html","w").write(html)
print("accents.html built,",len(A),"accents")
