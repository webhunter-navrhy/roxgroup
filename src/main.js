(() => {
  /* mobilní menu */
  const toggle = document.getElementById('toggle');
  const menu = document.getElementById('menu');
  const setMenu = open => {
    menu.classList.toggle('open', open);
    document.body.style.overflow = open ? 'hidden' : '';
    toggle.setAttribute('aria-expanded', String(open));
    toggle.setAttribute('aria-label', open ? 'Zavřít menu' : 'Otevřít menu');
  };
  toggle.addEventListener('click', () => setMenu(!menu.classList.contains('open')));
  menu.querySelectorAll('a').forEach(a => a.addEventListener('click', () => setMenu(false)));
  addEventListener('keydown', e => { if (e.key === 'Escape') setMenu(false); });

  /* odhalování při scrollu */
  const io = new IntersectionObserver(entries => entries.forEach(e => {
    if (!e.isIntersecting) return;
    e.target.classList.add('in');
    io.unobserve(e.target);
  }), { rootMargin: '0px 0px -8% 0px', threshold: 0.05 });
  document.querySelectorAll('.reveal, .ask-list').forEach(el => io.observe(el));
  document.querySelectorAll('.ask-list li').forEach(li => li.querySelector('.box').style.setProperty('--d', li.style.getPropertyValue('--d')));

  /* kusovník: náhled fotky k řádku */
  const view = document.querySelector('.bom-view');
  if (view) {
    const imgs = view.querySelectorAll('img');
    const cap = document.getElementById('bom-cap');
    const rows = document.querySelectorAll('.bom-table tbody tr');
    const show = row => {
      rows.forEach(r => r.classList.toggle('on', r === row));
      imgs.forEach((im, i) => im.classList.toggle('on', i === +row.dataset.img));
      cap.textContent = 'Poz. ' + row.querySelector('.poz').textContent;
    };
    rows.forEach(r => {
      r.addEventListener('mouseenter', () => show(r));
      r.querySelector('a').addEventListener('focus', () => show(r));
    });
    show(rows[0]);
  }

  /* rejstřík služeb: zvýraznění aktuální skupiny */
  const index = document.querySelectorAll('.index a');
  if (index.length) {
    const map = new Map([...index].map(a => [a.getAttribute('href').slice(1), a]));
    const spy = new IntersectionObserver(entries => entries.forEach(e => {
      if (!e.isIntersecting) return;
      index.forEach(a => a.classList.remove('on'));
      map.get(e.target.id)?.classList.add('on');
    }), { rootMargin: '-35% 0px -60% 0px' });
    map.forEach((_, id) => { const el = document.getElementById(id); if (el) spy.observe(el); });
  }

  /* FAQ: vždy jen jedna otevřená */
  document.querySelectorAll('.faq-list').forEach(list => {
    const items = [...list.querySelectorAll('details')];
    items.forEach(d => d.addEventListener('toggle', () => { if (d.open) items.forEach(o => { if (o !== d) o.open = false; }); }));
  });

  /* poptávkový formulář – v návrhu bez backendu otevře předvyplněný e-mail */
  const form = document.getElementById('poptavka');
  if (form) form.addEventListener('submit', e => {
    e.preventDefault();
    const f = new FormData(form);
    let ok = true;
    ['jmeno', 'telefon', 'email', 'zprava'].forEach(n => {
      const bad = !String(f.get(n) || '').trim();
      form.querySelector(`[name="${n}"]`).closest('.f').classList.toggle('invalid', bad);
      if (bad) ok = false;
    });
    const note = document.getElementById('form-note');
    if (!ok) { note.textContent = 'Vyplňte prosím povinná pole označená hvězdičkou.'; note.classList.remove('ok'); return; }
    const body = [
      `Co potřebuji: ${f.get('typ')}`, `Místo a termín: ${f.get('kde') || '–'}`, '', String(f.get('zprava')).trim(), '',
      `${f.get('jmeno')}${f.get('firma') ? ', ' + f.get('firma') : ''}`, `Tel.: ${f.get('telefon')}`, `E-mail: ${f.get('email')}`
    ].join('\n');
    location.href = `mailto:${form.dataset.to}?subject=${encodeURIComponent('Poptávka – ' + f.get('typ'))}&body=${encodeURIComponent(body)}`;
    note.textContent = 'Otevřeli jsme vám e-mail s předvyplněnou poptávkou, stačí ho odeslat.';
    note.classList.add('ok');
  });
})();
