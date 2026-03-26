/* Hinderliter Hearing Services — Main JS */

document.addEventListener('DOMContentLoaded', () => {

  /* === Scroll Animations (Intersection Observer) === */
  const fadeEls = document.querySelectorAll('.fade-up');
  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });

    fadeEls.forEach(el => observer.observe(el));
  } else {
    // Fallback: show everything
    fadeEls.forEach(el => el.classList.add('visible'));
  }

  /* === Mobile Navigation === */
  const mobileToggle = document.querySelector('.header__mobile-toggle');
  const mobileNav = document.querySelector('.header__nav');
  const mobileOverlay = document.querySelector('.mobile-overlay');

  if (mobileToggle && mobileNav) {
    mobileToggle.addEventListener('click', () => {
      const isOpen = mobileNav.classList.toggle('open');
      mobileToggle.classList.toggle('open');
      if (mobileOverlay) mobileOverlay.classList.toggle('open');
      mobileToggle.setAttribute('aria-expanded', isOpen);
      document.body.style.overflow = isOpen ? 'hidden' : '';
    });

    if (mobileOverlay) {
      mobileOverlay.addEventListener('click', () => {
        mobileNav.classList.remove('open');
        mobileToggle.classList.remove('open');
        mobileOverlay.classList.remove('open');
        mobileToggle.setAttribute('aria-expanded', 'false');
        document.body.style.overflow = '';
      });
    }

    // Close mobile nav when a link is clicked
    mobileNav.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', () => {
        mobileNav.classList.remove('open');
        mobileToggle.classList.remove('open');
        if (mobileOverlay) mobileOverlay.classList.remove('open');
        mobileToggle.setAttribute('aria-expanded', 'false');
        document.body.style.overflow = '';
      });
    });
  }

  /* === Active Nav Link === */
  const currentPage = window.location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.header__nav a').forEach(link => {
    const href = link.getAttribute('href');
    if (href === currentPage || (currentPage === '' && href === 'index.html')) {
      link.classList.add('active');
    }
  });

  /* === Header scroll shadow === */
  const header = document.querySelector('.header');
  if (header) {
    let lastScroll = 0;
    window.addEventListener('scroll', () => {
      const scrollY = window.scrollY;
      if (scrollY > 10) {
        header.style.boxShadow = '0 2px 16px rgba(0,0,0,0.08)';
      } else {
        header.style.boxShadow = 'var(--shadow-sm)';
      }
      lastScroll = scrollY;
    }, { passive: true });
  }

  /* === Force all fade-ups visible after timeout (safety net) === */
  setTimeout(() => {
    fadeEls.forEach(el => el.classList.add('visible'));
  }, 2500);

  /* === Smooth scroll for anchor links === */
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth' });
      }
    });
  });

});

  /* === Mobile Dropdown Toggles === */
  document.querySelectorAll('.nav-dropdown__trigger').forEach(trigger => {
    trigger.addEventListener('click', function(e) {
      if (window.innerWidth <= 900) {
        e.preventDefault();
        const dropdown = this.closest('.nav-dropdown');
        dropdown.classList.toggle('open');
      }
    });
  });
