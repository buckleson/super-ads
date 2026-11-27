const { chromium } = require('playwright');
(async () => {
  const dir = process.argv[2];
  const b = await chromium.launch();
  const ctx = await b.newContext({ viewport: { width: 1280, height: 720 }, recordVideo: { dir: dir + '/video', size: { width: 1280, height: 720 } } });
  const p = await ctx.newPage();
  await p.goto('file://' + dir + '/player.html');
  await p.waitForFunction(() => window.__done === true, null, { timeout: 120000, polling: 250 });
  const v = p.video(); await ctx.close(); console.log(await v.path()); await b.close();
})();
