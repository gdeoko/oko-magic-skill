const { execSync: __ex } = require('child_process');
function __pw(){ try { return require('playwright'); } catch(e){}
  for (const d of [process.env.NODE_PATH, (()=>{try{return __ex('npm root -g').toString().trim()}catch(e){return ''}})(), '/opt/node22/lib/node_modules']) {
    if(d){ try { return require(require('path').join(d.split(require('path').delimiter)[0],'playwright')); } catch(e){} } }
  return require('playwright'); }
const { chromium } = __pw();
(async () => {
  const [html, tsList, outDir, total] = process.argv.slice(2);
  const fs=require('fs'); if(!fs.existsSync(outDir)) fs.mkdirSync(outDir,{recursive:true});
  const b=await chromium.launch({executablePath: (require('fs').readdirSync('/opt/pw-browsers').filter(d=>/^chromium-[0-9]+$/.test(d)).map(d=>'/opt/pw-browsers/'+d+'/chrome-linux/chrome').find(p=>require('fs').existsSync(p)) || undefined)});
  const p=await b.newPage({viewport:{width:1080,height:1920},deviceScaleFactor:1});
  await p.goto('file://'+html); await p.evaluate(async()=>{if(document.fonts)await document.fonts.ready});
  for(const ts of tsList.split(',')){ const t=parseFloat(ts)/parseFloat(total);
    await p.evaluate(t=>window.render(t), t);
    await p.screenshot({path:`${outDir}/ts${ts}.png`, omitBackground:true}); }
  await b.close(); console.log('done');
})();
