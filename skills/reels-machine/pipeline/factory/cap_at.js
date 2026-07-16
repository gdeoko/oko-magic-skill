const { chromium } = require('playwright');
(async () => {
  const [html, tsList, outDir, total] = process.argv.slice(2);
  const fs=require('fs'); if(!fs.existsSync(outDir)) fs.mkdirSync(outDir,{recursive:true});
  const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium-1194/chrome-linux/chrome'});
  const p=await b.newPage({viewport:{width:1080,height:1920},deviceScaleFactor:1});
  await p.goto('file://'+html); await p.evaluate(async()=>{if(document.fonts)await document.fonts.ready});
  for(const ts of tsList.split(',')){ const t=parseFloat(ts)/parseFloat(total);
    await p.evaluate(t=>window.render(t), t);
    await p.screenshot({path:`${outDir}/ts${ts}.png`, omitBackground:true}); }
  await b.close(); console.log('done');
})();
