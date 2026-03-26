// Mobile nav
(function(){
  const toggle = document.querySelector('.nav-toggle');
  const navArea = document.querySelector('.nav-area');
  const overlay = document.querySelector('.nav-overlay');
  if (!toggle || !navArea) return;
  
  function closeNav() {
    toggle.classList.remove('active');
    navArea.classList.remove('open');
    if (overlay) overlay.classList.remove('visible');
    toggle.setAttribute('aria-expanded', 'false');
  }
  function openNav() {
    toggle.classList.add('active');
    navArea.classList.add('open');
    if (overlay) overlay.classList.add('visible');
    toggle.setAttribute('aria-expanded', 'true');
  }
  
  toggle.addEventListener('click', function() {
    if (navArea.classList.contains('open')) closeNav();
    else openNav();
  });
  if (overlay) overlay.addEventListener('click', closeNav);
  
  // Close on nav link click (mobile)
  navArea.querySelectorAll('a').forEach(function(link) {
    link.addEventListener('click', closeNav);
  });
})();

// Sticky header shadow
(function(){
  const header = document.querySelector('.site-header');
  if (!header) return;
  window.addEventListener('scroll', function() {
    if (window.scrollY > 10) header.classList.add('scrolled');
    else header.classList.remove('scrolled');
  }, { passive: true });
})();

// Scroll animations — stagger reveals as user scrolls
(function(){
  const els = document.querySelectorAll('.fade-up');
  if (!els.length) return;
  
  const observer = new IntersectionObserver(function(entries) {
    entries.forEach(function(entry) {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.05, rootMargin: '0px 0px 80px 0px' });
  
  els.forEach(function(el) { observer.observe(el); });
  
  // Fallback: reveal everything after 1.5s in case observer doesn't fire
  setTimeout(function() {
    els.forEach(function(el) { el.classList.add('visible'); });
  }, 1500);
})();

// Contact form handler
(function(){
  const form = document.querySelector('.contact-form form');
  if (!form) return;
  
  form.addEventListener('submit', function(e) {
    e.preventDefault();
    const btn = form.querySelector('button[type="submit"]');
    const origText = btn.textContent;
    btn.textContent = 'Sending...';
    btn.disabled = true;
    
    setTimeout(function() {
      btn.textContent = 'Message Sent!';
      btn.style.background = '#2AA5A0';
      form.reset();
      setTimeout(function() {
        btn.textContent = origText;
        btn.disabled = false;
        btn.style.background = '';
      }, 3000);
    }, 1000);
  });
})();
