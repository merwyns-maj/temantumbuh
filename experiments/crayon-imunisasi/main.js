// Entry: ?test=model renders the model sheet; otherwise the film
import { makeComp } from './gl.js';
import { BOIL } from './crayon.js';
const Q = new URLSearchParams(location.search);
const comp = makeComp(document.getElementById('gl'));
window.DUR = 1;
await document.fonts.load('400 40px "Patrick Hand"');
const M = await import('./film.js');
if (Q.get('test') === 'model') {
  window.DUR = 1;
  window.render = t => { BOIL.step = Math.floor(t * 12); M.modelSheet(comp); };
} else {
  window.DUR = M.DUR; window.EV = M.EV; window.SUBS = M.SUBS;
  window.render = t => { BOIL.step = Math.floor(t * 12 + 1e-6); M.frame(comp, t); };
}
window.READY = true;
