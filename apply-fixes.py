#!/usr/bin/env python3
"""Apply all fixes to Hinderliter Hearing website files."""
import re, os

BASE = "/home/user/workspace/hinderliter-hearing-proof"

# ==========================================
# SHARED COMPONENT TEMPLATES
# ==========================================

TOP_BAR = '''  <!-- Top Bar -->
  <div class="top-bar">
    <div class="container">
      <div class="top-bar__left">
        <span class="top-bar__item">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>
          751 Chestnut St., Suite 203, Birmingham, MI 48009
        </span>
        <span class="top-bar__item">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
          <a href="tel:248-430-4416">248-430-4416</a>
        </span>
      </div>
      <div class="top-bar__right">
        <a href="https://link.clover.com/urlshortener/t2t9LL" class="top-bar__cta" target="_blank" rel="noopener noreferrer" style="background:#E8A317;">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="14" height="14"><rect x="1" y="4" width="22" height="16" rx="2" ry="2"/><line x1="1" y1="10" x2="23" y2="10"/></svg>
          Pay Online
        </a>
        <a href="tel:248-430-4416" class="top-bar__cta">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="14" height="14"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
          Call or Text Us
        </a>
      </div>
    </div>
  </div>'''

HEADER_NAV = '''  <!-- Header -->
  <header class="header">
    <div class="container">
      <a href="index.html" class="header__logo" aria-label="Hinderliter Hearing Services Home">
        <img src="assets/logo.png" alt="Hinderliter Hearing Services logo" style="height:54px;width:auto;">
      </a>
      <nav class="header__nav" aria-label="Main navigation">
        <a href="index.html">Home</a>
        <div class="nav-dropdown">
          <a href="about.html" class="nav-dropdown__trigger">About <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" width="12" height="12"><polyline points="6 9 12 15 18 9"/></svg></a>
          <div class="nav-dropdown__menu">
            <a href="about.html">About Us</a>
            <a href="https://www.hinderliterhearing.com/patient-journey/" target="_blank" rel="noopener noreferrer">Patient Journey</a>
          </div>
        </div>
        <div class="nav-dropdown">
          <a href="services.html" class="nav-dropdown__trigger">Services <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" width="12" height="12"><polyline points="6 9 12 15 18 9"/></svg></a>
          <div class="nav-dropdown__menu">
            <a href="services.html#hearing-tests">Hearing Tests</a>
            <a href="services.html#hearing-aids">Hearing Aid Services</a>
            <a href="services.html#hearing-repair">Hearing Aid Repair</a>
            <a href="services.html#hearing-protection">Hearing Protection</a>
            <a href="services.html#tinnitus">Tinnitus Treatment</a>
            <a href="https://link.clover.com/urlshortener/t2t9LL" target="_blank" rel="noopener noreferrer">Pay Online</a>
          </div>
        </div>
        <a href="hearing-aids.html">Hearing Aids</a>
        <a href="reviews.html">Reviews</a>
        <a href="learn-more.html">Learn More</a>
        <a href="contact.html">Contact</a>
        <a href="tel:248-430-4416" class="header__phone" aria-label="Call 248-430-4416">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
          248-430-4416
        </a>
      </nav>
      <button class="header__mobile-toggle" aria-label="Toggle navigation menu" aria-expanded="false">
        <span></span>
      </button>
    </div>
    <div class="mobile-overlay"></div>
  </header>'''

FOOTER = '''  <!-- Footer -->
  <footer class="footer">
    <div class="container">
      <div class="footer__grid">
        <div class="footer__brand">
          <img src="assets/logo.png" alt="Hinderliter Hearing Services" style="height:60px;width:auto;">
          <p>Giving the gift of hearing since 2003. Comprehensive audiology care in Birmingham, MI.</p>
          <div class="footer__social" style="display:flex;gap:var(--space-3);margin-top:var(--space-4);">
            <a href="https://www.google.com/search?q=Hinderliter+Hearing+Services" target="_blank" rel="noopener noreferrer" aria-label="Google Business Profile" style="display:flex;align-items:center;justify-content:center;width:36px;height:36px;border-radius:50%;background:rgba(255,255,255,0.1);transition:background var(--transition-fast);" onmouseover="this.style.background='rgba(255,255,255,0.2)'" onmouseout="this.style.background='rgba(255,255,255,0.1)'">
              <svg width="20" height="20" viewBox="0 0 24 24"><path fill="#fff" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92a5.06 5.06 0 0 1-2.2 3.32v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.1z"/><path fill="#fff" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/><path fill="#fff" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18A10.04 10.04 0 0 0 1.09 12c0 1.62.39 3.14 1.09 4.49l3.66-2.84z"/><path fill="#fff" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/></svg>
            </a>
            <a href="https://www.facebook.com/hinderliterhearing/" target="_blank" rel="noopener noreferrer" aria-label="Facebook" style="display:flex;align-items:center;justify-content:center;width:36px;height:36px;border-radius:50%;background:rgba(255,255,255,0.1);transition:background var(--transition-fast);" onmouseover="this.style.background='rgba(255,255,255,0.2)'" onmouseout="this.style.background='rgba(255,255,255,0.1)'">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="#fff"><path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/></svg>
            </a>
          </div>
          <div class="footer__award">
            <img src="assets/nextdoor-award.jpg" alt="Nextdoor Neighborhood Favorite Award" width="100" height="80">
          </div>
        </div>
        <div>
          <h3 class="footer__heading">Quick Links</h3>
          <div class="footer__links">
            <a href="index.html">Home</a>
            <a href="about.html">About Us</a>
            <a href="services.html">Services</a>
            <a href="hearing-aids.html">Hearing Aids</a>
            <a href="reviews.html">Reviews</a>
            <a href="learn-more.html">Learn More</a>
            <a href="contact.html">Contact</a>
          </div>
        </div>
        <div>
          <h3 class="footer__heading">Services</h3>
          <div class="footer__links">
            <a href="services.html#hearing-tests">Hearing Tests</a>
            <a href="services.html#hearing-aids">Hearing Aid Services</a>
            <a href="services.html#hearing-repair">Hearing Aid Repair</a>
            <a href="services.html#hearing-protection">Hearing Protection</a>
            <a href="services.html#tinnitus">Tinnitus Treatment</a>
            <a href="hearing-aids.html">Hearing Aids</a>
            <a href="https://link.clover.com/urlshortener/t2t9LL" target="_blank" rel="noopener noreferrer">Pay Online</a>
          </div>
        </div>
        <div>
          <h3 class="footer__heading">Contact Us</h3>
          <div class="footer__contact-item">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>
            <span>751 Chestnut St., Suite 203<br>Birmingham, MI 48009</span>
          </div>
          <div class="footer__contact-item">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
            <a href="tel:248-430-4416">248-430-4416</a>
          </div>
          <div class="footer__contact-item">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="3" width="20" height="14" rx="2" ry="2"/><polyline points="22,4 12,13 2,4"/></svg>
            <a href="mailto:kristin@hinderliterhearing.com">kristin@hinderliterhearing.com</a>
          </div>
          <div class="footer__contact-item">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
            <span>Mon&ndash;Thu: 8am&ndash;5pm<br>Fri: 9am&ndash;3pm</span>
          </div>
        </div>
      </div>
      <div class="footer__bottom">
        <p>&copy; 2026 Hinderliter Hearing Services. All rights reserved.</p>
      </div>
    </div>
  </footer>'''


def replace_section(html, start_comment, end_after, new_content):
    """Replace a section from a comment marker to the end of its block."""
    pattern = re.compile(
        re.escape(start_comment) + r'.*?' + re.escape(end_after),
        re.DOTALL
    )
    return pattern.sub(new_content, html, count=1)


def replace_topbar_header_footer(html):
    """Replace top bar, header nav, and footer in an HTML file."""
    
    # Replace top bar (from <!-- Top Bar --> to closing </div> before <!-- Header -->)
    html = re.sub(
        r'  <!-- Top Bar -->.*?(?=\n  <!-- Header -->)',
        TOP_BAR + '\n\n',
        html, flags=re.DOTALL
    )
    
    # Replace header (from <!-- Header --> to </header> including mobile overlay div)
    html = re.sub(
        r'  <!-- Header -->.*?<div class="mobile-overlay"></div>\s*</header>',
        HEADER_NAV,
        html, flags=re.DOTALL
    )
    
    # Replace footer (from <!-- Footer --> to </footer>)
    html = re.sub(
        r'  <!-- Footer -->.*?</footer>',
        FOOTER,
        html, flags=re.DOTALL
    )
    
    return html


# ==========================================
# PROCESS EACH EXISTING FILE
# ==========================================

for filename in ['index.html', 'about.html', 'services.html', 'reviews.html', 'contact.html']:
    filepath = os.path.join(BASE, filename)
    with open(filepath, 'r') as f:
        html = f.read()
    
    html = replace_topbar_header_footer(html)
    
    with open(filepath, 'w') as f:
        f.write(html)
    
    print(f"Updated: {filename}")

print("\nAll existing files updated with new nav, footer, phone numbers, and Pay Online button.")
