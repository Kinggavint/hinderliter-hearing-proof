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

    // Close mobile nav when a non-trigger link is clicked
    mobileNav.querySelectorAll('a:not(.nav-dropdown__trigger)').forEach(link => {
      link.addEventListener('click', () => {
        mobileNav.classList.remove('open');
        mobileToggle.classList.remove('open');
        if (mobileOverlay) mobileOverlay.classList.remove('open');
        mobileToggle.setAttribute('aria-expanded', 'false');
        document.body.style.overflow = '';
      });
    });
  }

  /* === Desktop Dropdown Navigation === */
  document.querySelectorAll('.nav-dropdown').forEach(dropdown => {
    const trigger = dropdown.querySelector('.nav-dropdown__trigger');
    const menu = dropdown.querySelector('.nav-dropdown__menu');
    if (!trigger || !menu) return;

    let closeTimeout;

    // Desktop: show on hover
    dropdown.addEventListener('mouseenter', () => {
      if (window.innerWidth > 900) {
        clearTimeout(closeTimeout);
        dropdown.classList.add('is-open');
      }
    });

    dropdown.addEventListener('mouseleave', () => {
      if (window.innerWidth > 900) {
        closeTimeout = setTimeout(() => {
          dropdown.classList.remove('is-open');
        }, 150);
      }
    });

    // Desktop: also toggle on click for accessibility
    trigger.addEventListener('click', (e) => {
      if (window.innerWidth > 900) {
        // Allow navigation to the parent page (About, Services)
        // The dropdown just enhances with sub-links on hover
        return;
      }
      // Mobile: toggle dropdown submenu
      e.preventDefault();
      const wasOpen = dropdown.classList.contains('open');
      // Close all other dropdowns first
      document.querySelectorAll('.nav-dropdown.open').forEach(d => {
        if (d !== dropdown) d.classList.remove('open');
      });
      dropdown.classList.toggle('open', !wasOpen);
    });
  });

  // Close desktop dropdowns when clicking outside
  document.addEventListener('click', (e) => {
    if (!e.target.closest('.nav-dropdown')) {
      document.querySelectorAll('.nav-dropdown.is-open').forEach(d => d.classList.remove('is-open'));
    }
  });

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
