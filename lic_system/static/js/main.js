/* ============================================================
   LIC Management System – Public Website JavaScript
   ============================================================ */
'use strict';

(function () {
  /* ── Helper ──────────────────────────────────────────────── */
  const qs = (sel, ctx = document) => ctx.querySelector(sel);
  const qsa = (sel, ctx = document) => [...ctx.querySelectorAll(sel)];

  /* ── Navbar scroll effect ─────────────────────────────────── */
  const navbar = qs('.navbar');
  if (navbar) {
    const onScroll = () => navbar.classList.toggle('scrolled', window.scrollY > 30);
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  /* ── Mobile nav toggle ────────────────────────────────────── */
  const toggle = qs('.nav-toggle');
  const navLinks = qs('.nav-links');
  if (toggle && navLinks) {
    toggle.addEventListener('click', () => {
      navLinks.classList.toggle('open');
      qsa('span', toggle).forEach((s, i) => {
        if (navLinks.classList.contains('open')) {
          if (i === 0) s.style.transform = 'translateY(7px) rotate(45deg)';
          if (i === 1) s.style.opacity = '0';
          if (i === 2) s.style.transform = 'translateY(-7px) rotate(-45deg)';
        } else {
          s.style.transform = '';
          s.style.opacity = '';
        }
      });
    });
    // Close on outside click
    document.addEventListener('click', e => {
      if (!e.target.closest('.navbar')) navLinks.classList.remove('open');
    });
  }

  /* ── Active nav link ──────────────────────────────────────── */
  qsa('.nav-link').forEach(link => {
    if (link.href === window.location.href) link.classList.add('active');
  });

  /* ── Smooth scroll for anchor links ─────────────────────────── */
  qsa('a[href^="#"]').forEach(a => {
    a.addEventListener('click', e => {
      const target = qs(a.getAttribute('href'));
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        navLinks?.classList.remove('open');
      }
    });
  });

  /* ── Auto-dismiss flash messages ─────────────────────────── */
  qsa('.flash-alert').forEach(el => {
    setTimeout(() => el.style.opacity = '0', 5000);
    setTimeout(() => el.remove(), 5500);
  });

  /* ── Counter animation ─────────────────────────────────────── */
  function animateCounter(el, selector = '.counter-num') {
    const target = el.querySelector(selector);
    if (!target) return;
    const countTo = parseFloat(target.dataset.count || target.textContent.replace(/[^0-9.]/g, ''));
    if (isNaN(countTo)) return;
    
    let start = 0;
    const duration = 2000;
    const step = timestamp => {
      if (!start) start = timestamp;
      const progress = Math.min((timestamp - start) / duration, 1);
      const ease = 1 - Math.pow(1 - progress, 3);
      const current = Math.floor(ease * countTo);
      target.textContent = current.toLocaleString('en-IN');
      if (progress < 1) requestAnimationFrame(step);
      else target.textContent = countTo.toLocaleString('en-IN');
    };
    requestAnimationFrame(step);
  }

  // Hero Stats
  const heroStats = qs('.hero-stats');
  if (heroStats) {
    const io = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          qsa('.stat-item', heroStats).forEach(item => animateCounter(item, '.stat-num'));
          io.disconnect();
        }
      });
    }, { threshold: .1 });
    io.observe(heroStats);
  }

  // Footer Counters
  const counterSection = qs('.counter-section');
  if (counterSection) {
    const io = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          qsa('.counter-item', counterSection).forEach(item => animateCounter(item, '.counter-num'));
          io.disconnect();
        }
      });
    }, { threshold: .3 });
    io.observe(counterSection);
  }

  /* ── FAQ accordion ─────────────────────────────────────────── */
  qsa('.faq-item').forEach(item => {
    const btn = qs('.faq-question', item);
    const answer = qs('.faq-answer', item);
    btn.addEventListener('click', () => {
      const open = item.classList.contains('open');
      qsa('.faq-item').forEach(i => {
        i.classList.remove('open');
        qs('.faq-answer', i).style.maxHeight = '';
      });
      if (!open) {
        item.classList.add('open');
        answer.style.maxHeight = answer.scrollHeight + 'px';
      }
    });
  });

  /* ── Services filter tabs ─────────────────────────────────── */
  const tabs = qsa('.filter-tab');
  const cards = qsa('.plan-card[data-type]');
  if (tabs.length && cards.length) {
    tabs.forEach(tab => {
      tab.addEventListener('click', () => {
        tabs.forEach(t => t.classList.remove('active'));
        tab.classList.add('active');
        const type = tab.dataset.type;
        cards.forEach(card => {
          card.style.display = (type === 'all' || card.dataset.type === type) ? '' : 'none';
        });
      });
    });
  }

  /* ── Intersection observer for card animations ──────────────── */
  if ('IntersectionObserver' in window) {
    const io = new IntersectionObserver(entries => {
      entries.forEach(e => {
        if (e.isIntersecting) {
          e.target.classList.add('visible');
          io.unobserve(e.target);
        }
      });
    }, { threshold: .1 });
    qsa('[data-animate]').forEach(el => io.observe(el));
  }

  /* ── Contact form validation ──────────────────────────────── */
  const contactForm = qs('#contactForm');
  if (contactForm) {
    contactForm.addEventListener('submit', e => {
      let valid = true;
      qsa('.form-error', contactForm).forEach(el => el.textContent = '');

      const name = qs('[name="name"]', contactForm);
      if (!name.value.trim()) {
        showError(name, 'Name is required.'); valid = false;
      }

      const phone = qs('[name="phone"]', contactForm);
      if (phone && !/^\d{10}$/.test(phone.value.replace(/\s+/g,''))) {
        showError(phone, 'Enter a valid 10-digit mobile number.'); valid = false;
      }

      const email = qs('[name="email"]', contactForm);
      if (email && email.value && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value)) {
        showError(email, 'Enter a valid email address.'); valid = false;
      }

      const msg = qs('[name="message"]', contactForm);
      if (!msg.value.trim() || msg.value.trim().length < 10) {
        showError(msg, 'Message must be at least 10 characters.'); valid = false;
      }

      if (!valid) e.preventDefault();
    });

    function showError(field, msg) {
      const err = field.closest('.form-group')?.querySelector('.form-error');
      if (err) err.textContent = msg;
      field.style.borderColor = '#ef4444';
      field.addEventListener('input', () => field.style.borderColor = '', { once: true });
    }
  }

})();
