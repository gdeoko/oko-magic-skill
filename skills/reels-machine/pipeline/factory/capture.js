// capture.js <htmlPath> <N> <outDir>
// Renders window.render(t in [0,1]) for N frames, screenshots each as transparent PNG.
const { execSync: __ex } = require('child_process');
function __pw(){ try { return require('playwright'); } catch(e){}
  for (const d of [process.env.NODE_PATH, (()=>{try{return __ex('npm root -g').toString().trim()}catch(e){return ''}})(), '/opt/node22/lib/node_modules']) {
    if(d){ try { return require(require('path').join(d.split(require('path').delimiter)[0],'playwright')); } catch(e){} } }
  return require('playwright'); }
const { chromium } = __pw();
(async () => {
  const [htmlPath, Nraw, outDir] = process.argv.slice(2);
  const N = parseInt(Nraw, 10);
  const fs = require('fs');
  if (!fs.existsSync(outDir)) fs.mkdirSync(outDir, { recursive: true });
  const browser = await chromium.launch({ executablePath: (require('fs').readdirSync('/opt/pw-browsers').filter(d=>/^chromium-[0-9]+$/.test(d)).map(d=>'/opt/pw-browsers/'+d+'/chrome-linux/chrome').find(p=>require('fs').existsSync(p)) || undefined), args: ['--force-color-profile=srgb'] });
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  await page.goto('file://' + htmlPath);
  await page.evaluate(async () => { if (document.fonts && document.fonts.ready) await document.fonts.ready; });
  await page.waitForTimeout(120);
  for (let i = 0; i < N; i++) {
    const t = N === 1 ? 1 : i / (N - 1);
    await page.evaluate((t) => window.render(t), t);
    await page.screenshot({ path: `${outDir}/f${String(i).padStart(3, '0')}.png`, omitBackground: true });
  }
  await browser.close();
  console.log('captured', N, 'frames ->', outDir);
})();
