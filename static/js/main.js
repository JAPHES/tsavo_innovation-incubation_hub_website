(() => {
  const header = document.querySelector('[data-header]');
  const toggle = document.querySelector('[data-nav-toggle]');
  const menu = document.querySelector('[data-nav-menu]');
  const dropdowns = [...(menu?.querySelectorAll('[data-nav-dropdown]') || [])];
  document.querySelectorAll('[data-dismiss-message]').forEach((button) => {
    button.addEventListener('click', () => button.closest('.alert')?.remove());
  });
  const desktopHover = window.matchMedia('(min-width: 1081px) and (hover: hover) and (pointer: fine)');
  const closeDropdowns = () => dropdowns.forEach((dropdown) => { dropdown.open = false; });

  const closeMenu = () => {
    if (!toggle || !menu) return;
    closeDropdowns();
    toggle.setAttribute('aria-expanded', 'false');
    menu.classList.remove('open');
    document.body.classList.remove('nav-open');
  };

  toggle?.addEventListener('click', () => {
    const open = toggle.getAttribute('aria-expanded') === 'true';
    if (open) { closeMenu(); return; }
    toggle.setAttribute('aria-expanded', String(!open));
    menu.classList.toggle('open', !open);
    document.body.classList.toggle('nav-open', !open);
  });
  dropdowns.forEach((dropdown) => dropdown.addEventListener('toggle', () => {
    if (dropdown.open) dropdowns.filter((item) => item !== dropdown).forEach((item) => { item.open = false; });
  }));
  dropdowns.forEach((dropdown) => {
    dropdown.addEventListener('pointerenter', (event) => {
      if (desktopHover.matches && event.pointerType === 'mouse') dropdown.open = true;
    });
    dropdown.addEventListener('pointerleave', (event) => {
      if (desktopHover.matches && event.pointerType === 'mouse') dropdown.open = false;
    });
  });
  menu?.querySelectorAll('a').forEach((link) => link.addEventListener('click', closeMenu));
  document.addEventListener('click', (event) => { if (!header?.contains(event.target)) closeMenu(); });
  document.addEventListener('keydown', (event) => {
    if (event.key !== 'Escape') return;
    const openDropdown = dropdowns.find((dropdown) => dropdown.open);
    if (openDropdown) {
      openDropdown.open = false;
      openDropdown.querySelector('summary')?.focus();
    } else if (menu?.classList.contains('open')) {
      closeMenu();
      toggle?.focus();
    }
  });
  window.addEventListener('resize', () => { if (window.innerWidth > 1080) closeMenu(); });
  window.addEventListener('scroll', () => header?.classList.toggle('scrolled', window.scrollY > 8), { passive: true });

  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const revealItems = document.querySelectorAll('.reveal');
  if (reducedMotion || !('IntersectionObserver' in window)) {
    revealItems.forEach((item) => item.classList.add('visible'));
  } else {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.14 });
    revealItems.forEach((item) => observer.observe(item));
  }
})();
