const { chromium } = require('playwright');
(async () => {
  const [html, Nraw, outDir] = process.argv.slice(2); const N=parseInt(Nraw);
  const fs=require('fs'); if(!fs.existsSync(outDir)) fs.mkdirSync(outDir,{recursive:true});
  const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium-1194/chrome-linux/chrome'});
  const p=await b.newPage({viewport:{width:1080,height:1920},deviceScaleFactor:1});
  await p.goto('file://'+html); await p.evaluate(async()=>{if(document.fonts)await document.fonts.ready}); await p.waitForTimeout(120);
  for(let i=0;i<N;i++){const t=N===1?1:i/(N-1); await p.evaluate(t=>window.render(t),t);
    await p.screenshot({path:`${outDir}/f${String(i).padStart(3,'0')}.png`});}
  await b.close(); console.log('opaque',N);
})();
