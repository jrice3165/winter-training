'use strict';
(() => {
let DATA;
const $ = id => document.getElementById(id);
const esc = s => String(s).replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const store = {
  get(k, d) { try { const v = localStorage.getItem('wt_' + k); return v === null ? d : v; } catch (e) { return d; } },
  set(k, v) { try { localStorage.setItem('wt_' + k, v); } catch (e) {} },
  del(k) { try { localStorage.removeItem('wt_' + k); } catch (e) {} },
};
let tIdx = +store.get('track', 0) || 0;
let day = Math.min(+store.get('day', 0) || 0, 4);
const dogEl = $('dogname');
dogEl.value = store.get('dog', 'Sunny');
const dog = () => dogEl.value.trim() || 'your dog';
const LV = {1: 'Start here', 2: 'Building', 3: 'Advanced'};

/* ---------- week state: which drill and bonus sit on each day ---------- */
const track = () => DATA.tracks[tIdx];
const drillPool = t => t.days.map(d => d.drill).concat(t.alternates || []);
const drillById = (t, id) => drillPool(t).find(x => x.id === id);
const bonusById = id => DATA.bonusPool.find(b => b.id === id);
const defaults = t => ({
  drills: t.days.map(d => d.drill.id),
  bonuses: t.days.map(d => (DATA.bonusPool.find(b => b.title === d.bonus.title) || d.bonus).id),
});
function plan(t = track()) {
  const def = defaults(t);
  let saved = null;
  try { saved = JSON.parse(store.get('week_' + t.id, 'null')); } catch (e) {}
  const ok = saved && Array.isArray(saved.drills) && saved.drills.every(id => drillById(t, id)) &&
             Array.isArray(saved.bonuses) && saved.bonuses.every(id => bonusById(id));
  return ok ? saved : def;
}
const isChanged = (t = track()) => JSON.stringify(plan(t)) !== JSON.stringify(defaults(t));
function savePlan(p) { store.set('week_' + track().id, JSON.stringify(p)); }
function week(t = track()) {
  const p = plan(t);
  return p.drills.map((id, i) => ({drill: drillById(t, id), bonus: bonusById(p.bonuses[i])}));
}
// Next item in pool order (wrapping) that isn't already used on another day.
function nextFrom(poolIds, used, current) {
  const start = poolIds.indexOf(current);
  for (let k = 1; k <= poolIds.length; k++) {
    const id = poolIds[(start + k) % poolIds.length];
    if (!used.includes(id)) return id;
  }
  return current;
}
function swapDrill() {
  const t = track(), p = plan(t);
  const others = p.drills.filter((_, i) => i !== day);
  p.drills[day] = nextFrom(drillPool(t).map(x => x.id), others, p.drills[day]);
  savePlan(p); renderDays(); renderDay(); flash('drill');
}
function swapBonus() {
  const p = plan();
  const others = p.bonuses.filter((_, i) => i !== day);
  p.bonuses[day] = nextFrom(DATA.bonusPool.map(b => b.id), others, p.bonuses[day]);
  savePlan(p); renderDay(); flash('bonus');
}
function resetWeek() { store.del('week_' + track().id); renderDays(); renderDay(); }
function flash(id) {
  const el = $(id); el.style.animation = 'none'; void el.offsetWidth; el.style.animation = '';
}

/* ---------- rendering ---------- */
function renderTracks() {
  $('tracks').innerHTML = DATA.tracks.map((t, i) =>
    `<button class="tr" type="button" aria-pressed="${i === tIdx}" data-i="${i}">${esc(t.name)}</button>`).join('');
}
function renderDays() {
  $('days').innerHTML = week().map((d, i) =>
    `<button class="day" type="button" aria-pressed="${i === day}" data-d="${i}"><span class="lab">Day ${i + 1}</span><b>${esc(d.drill.name)}</b></button>`).join('');
  $('reset').hidden = !isChanged();
}
function renderDay() {
  const d = week()[day], x = d.drill, b = d.bonus;
  $('drill').innerHTML = `
    <div class="cardtop">
      <div class="meta"><span class="chip">Day ${day + 1} · 15 min</span><span class="chip">${LV[x.level]}</span>${x.cues.map(c => `<span class="chip cue">${esc(c)}</span>`).join('')}</div>
      <button class="btn btn2 swap" id="swapdrill" type="button" title="Swap in a different drill from this week's theme">Pick another drill</button>
    </div>
    <h3>${esc(x.name)}</h3>
    <p class="purpose">${esc(x.purpose)}</p>
    ${x.steps.length ? `<ol class="steps">${x.steps.map(s => `<li><span>${esc(s)}</span></li>`).join('')}</ol>` : ''}
    ${x.img ? `<figure style="margin:0 0 18px"><img src="${esc(x.img)}" alt="Week 13 class diagram: lap turn around a cone in three steps" style="max-width:100%;border-radius:6px;border:1px solid var(--line);background:#fff"><figcaption class="small">Week 13 class diagram</figcaption></figure>` : ''}
    ${x.next ? `<div class="note"><span class="lab">When ${esc(dog())} finds it easy</span><span>${esc(x.next)}</span></div>` : ''}
    ${x.tip ? `<div class="note"><span class="lab">Trainer tip</span><span>${esc(x.tip)}</span></div>` : ''}
    <p class="src">From: ${esc(x.source)}</p>`;
  $('bonus').innerHTML = `
    <div class="cardtop">
      <div class="meta"><span class="chip h">Humans only</span><span class="chip">${esc(b.kind)}</span></div>
      <button class="ghost" id="swapbonus" type="button">Pick another</button>
    </div>
    <h3>${esc(b.title)}</h3><p>${esc(b.text)}</p>
    ${b.link ? `<a href="${esc(b.link)}" target="_blank" rel="noopener">Open link</a>` : ''}`;
  $('gear').innerHTML = `<h3>Household gear ideas</h3><ul>${x.gear.map(g => `<li>${esc(g)}</li>`).join('')}</ul>`;
}
function renderSheet() {
  const t = track();
  $('sheet').innerHTML = `
    <h2>Winter Training · ${esc(t.name)}</h2>
    <p class="sub">${esc(dog())}'s week · one 15-minute drill a day · ${esc(t.blurb)}</p>
    <table><thead><tr><th style="width:12%">Day</th><th style="width:50%">Drill</th><th style="width:28%">Humans only</th><th style="width:10%">Done</th></tr></thead><tbody>
    ${week().map((d, i) => `<tr><td><b>Day ${i + 1}</b></td><td><b>${esc(d.drill.name)}</b><br>${esc(d.drill.steps.slice(0, 3).join(' '))}<br><i>Gear:</i> ${esc(d.drill.gear.join('; '))}</td><td><b>${esc(d.bonus.title)}</b><br>${esc(d.bonus.text)}</td><td><span class="box"></span></td></tr>`).join('')}
    </tbody></table>
    <div class="notes">Notes:</div>`;
}
function all() {
  renderTracks(); renderDays(); renderDay();
  $('tname').textContent = track().name; $('tblurb').textContent = track().blurb;
  $('pip').textContent = dog()[0].toUpperCase();
}

/* ---------- events ---------- */
$('tracks').addEventListener('click', e => { const b = e.target.closest('[data-i]'); if (!b) return; tIdx = +b.dataset.i; day = 0; store.set('track', tIdx); store.set('day', 0); all(); });
$('days').addEventListener('click', e => { const b = e.target.closest('[data-d]'); if (!b) return; day = +b.dataset.d; store.set('day', day); renderDays(); renderDay(); });
$('drill').addEventListener('click', e => { if (e.target.closest('#swapdrill')) swapDrill(); });
$('bonus').addEventListener('click', e => { if (e.target.closest('#swapbonus')) swapBonus(); });
$('reset').addEventListener('click', resetWeek);
dogEl.addEventListener('input', () => { store.set('dog', dogEl.value); $('pip').textContent = dog()[0].toUpperCase(); renderDay(); });
$('printbtn').addEventListener('click', () => { renderSheet(); document.body.classList.add('printing'); window.scrollTo(0, 0); });
$('back').addEventListener('click', () => document.body.classList.remove('printing'));
$('doprint').addEventListener('click', () => { try { window.print(); } catch (e) {} });
window.addEventListener('beforeprint', renderSheet);
fetch('data/training-curriculum.json')
  .then(r => { if (!r.ok) throw new Error(r.status); return r.json(); })
  .then(d => { DATA = d; tIdx = Math.min(tIdx, DATA.tracks.length - 1); all(); renderSheet(); })
  .catch(() => { document.querySelector('main').innerHTML = '<p style="padding:40px 0">Could not load the curriculum. Open this app through a web server (see README), not by double-clicking the file.</p>'; });
})();
