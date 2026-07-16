// capture.js <htmlPath> <N> <outDir>
// Renders window.render(t in [0,1]) for N frames, screenshots each as transparent PNG.
const { chromium } = require('playwright');
(async () => {
  const [htmlPath, Nraw, outDir] = process.argv.slice(2);
  const N = parseInt(Nraw, 10);
  const fs = require('fs');
  if (!fs.existsSync(outDir)) fs.mkdirSync(outDir, { recursive: true });
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome', args: ['--force-color-profile=srgb'] });
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
