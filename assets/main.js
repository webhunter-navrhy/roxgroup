(() => {
  const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* navigace */
  const nav = document.getElementById('nav');
  const onScroll = () => nav.classList.toggle('scrolled', scrollY > 30);
  onScroll();
  addEventListener('scroll', onScroll, { passive: true });

  const toggle = document.getElementById('toggle');
  const menu = document.getElementById('menu');
  const setMenu = open => {
    menu.classList.toggle('open', open);
    document.body.classList.toggle('menu-open', open);
    document.body.style.overflow = open ? 'hidden' : '';
    toggle.setAttribute('aria-expanded', String(open));
  };
  toggle.addEventListener('click', () => setMenu(!menu.classList.contains('open')));
  menu.querySelectorAll('a').forEach(a => a.addEventListener('click', () => setMenu(false)));
  addEventListener('keydown', e => { if (e.key === 'Escape') setMenu(false); });

  /* odhalování při scrollu */
  const io = new IntersectionObserver(entries => entries.forEach(e => {
    if (!e.isIntersecting) return;
    e.target.classList.add('in');
    io.unobserve(e.target);
  }), { rootMargin: '0px 0px -10% 0px', threshold: 0.05 });
  document.querySelectorAll('.reveal, .reveal-group, .gallery, .steps').forEach(el => io.observe(el));
  document.querySelectorAll('.gallery .g').forEach(g => g.style.setProperty('--d', (Math.random() * 0.45).toFixed(2) + 's'));

  /* FAQ: vždy jen jedna otevřená */
  document.querySelectorAll('.faq-list').forEach(list => {
    const items = [...list.querySelectorAll('details')];
    items.forEach(d => d.addEventListener('toggle', () => { if (d.open) items.forEach(o => { if (o !== d) o.open = false; }); }));
  });

  /* poptávkový formulář — bez backendu otevře předvyplněný e-mail */
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
      `Typ práce: ${f.get('typ')}`, '', String(f.get('zprava')).trim(), '',
      `${f.get('jmeno')}${f.get('firma') ? ', ' + f.get('firma') : ''}`, `Tel.: ${f.get('telefon')}`, `E-mail: ${f.get('email')}`
    ].join('\n');
    location.href = `mailto:${form.dataset.to}?subject=${encodeURIComponent('Poptávka — ' + f.get('typ'))}&body=${encodeURIComponent(body)}`;
    note.textContent = 'Otevřeli jsme vám e-mail s předvyplněnou poptávkou — stačí ho odeslat.';
    note.classList.add('ok');
  });
})();
