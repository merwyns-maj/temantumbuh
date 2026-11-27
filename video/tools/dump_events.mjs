// Write the episode's sound events and length: node <lemo>/core/render/dump_events.mjs films/<film> out.json
// (copied next to the engine's render scripts by the workflow, so it imports page.mjs from the same folder)
import fs from 'fs';
import { openDemo, closeServer } from './page.mjs';
const [dir, out] = process.argv.slice(2);
const { browser, page } = await openDemo(dir, { w: 640, h: 360 });
const data = await page.evaluate(() => ({ dur: window.DUR, ev: window.EV || [] }));
await browser.close(); closeServer();
fs.writeFileSync(out, JSON.stringify(data));
console.log(`events: ${data.ev.length}, length ${data.dur} s`);
