/* ============================================================
   LIC Management System – Admin Dashboard JavaScript
   ============================================================ */
'use strict';

(function () {
  const qs  = (sel, ctx = document) => ctx.querySelector(sel);
  const qsa = (sel, ctx = document) => [...ctx.querySelectorAll(sel)];

  /* ── Sidebar toggle ──────────────────────────────────────── */
  const sidebar  = qs('#sidebar');
  const mainWrap = qs('#adminMain');
  const toggleBtn = qs('#sidebarToggle');
  const closeBtn  = qs('#sidebarClose');
  const overlay   = qs('#sidebarOverlay');

  function openSidebar() {
    sidebar?.classList.add('open');
    overlay?.classList.add('show');
    document.body.style.overflow = 'hidden';
  }
  function closeSidebar() {
    sidebar?.classList.remove('open');
    overlay?.classList.remove('show');
    document.body.style.overflow = '';
  }

  toggleBtn?.addEventListener('click', () => {
    const isMobile = window.innerWidth <= 900;
    if (isMobile) {
      sidebar?.classList.contains('open') ? closeSidebar() : openSidebar();
    } else {
      // collapse on desktop
      sidebar?.classList.toggle('collapsed');
      mainWrap?.classList.toggle('sidebar-collapsed');
    }
  });
  closeBtn?.addEventListener('click', closeSidebar);
  overlay?.addEventListener('click', closeSidebar);

  /* ── Sidebar search ───────────────────────────────────────── */
  const sidebarSearch = qs('#sidebarSearch');
  if (sidebarSearch) {
    sidebarSearch.addEventListener('input', e => {
      const q = e.target.value.toLowerCase();
      qsa('.sidebar-link').forEach(link => {
        const text = link.textContent.toLowerCase();
        link.style.display = q && !text.includes(q) ? 'none' : '';
      });
    });
  }

  /* ── Password visibility toggle ──────────────────────────── */
  qsa('.pwd-toggle').forEach(btn => {
    btn.addEventListener('click', () => {
      const input = btn.previousElementSibling || qs('input', btn.closest('.input-icon-group'));
      if (!input) return;
      const isText = input.type === 'text';
      input.type = isText ? 'password' : 'text';
      qs('i', btn).className = isText ? 'fas fa-eye' : 'fas fa-eye-slash';
    });
  });

  /* ── Auto-dismiss flash messages ─────────────────────────── */
  qsa('.flash-alert, .alert').forEach(el => {
    setTimeout(() => {
      el.style.transition = 'opacity .5s';
      el.style.opacity = '0';
    }, 5000);
    setTimeout(() => el.remove(), 5600);
  });

  /* ── Confirm-delete forms ─────────────────────────────────── */
  // Individual confirmations are inline in templates.
  // This is a fallback for any data-confirm attribute usage:
  qsa('[data-confirm]').forEach(el => {
    el.addEventListener('click', e => {
      if (!confirm(el.dataset.confirm)) e.preventDefault();
    });
  });

  /* ── Form validation helper ───────────────────────────────── */
  function markError(field, msg) {
    field.style.borderColor = '#ef4444';
    const grp = field.closest('.form-group');
    let err = grp?.querySelector('.field-err');
    if (!err && grp) {
      err = document.createElement('span');
      err.className = 'field-err';
      err.style.cssText = 'color:#ef4444;font-size:.75rem;margin-top:4px;display:block;';
      grp.appendChild(err);
    }
    if (err) err.textContent = msg;
    field.addEventListener('input', () => {
      field.style.borderColor = '';
      if (err) err.textContent = '';
    }, { once: true });
  }

  /* ── Admin CRUD forms – basic required field check ────────── */
  qsa('form.form-card').forEach(form => {
    form.addEventListener('submit', e => {
      let ok = true;
      qsa('[required]', form).forEach(field => {
        if (!field.value.trim()) {
          markError(field, 'This field is required.');
          ok = false;
        }
      });
      // Email check
      qsa('[type="email"]', form).forEach(field => {
        if (field.value && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(field.value)) {
          markError(field, 'Enter a valid email address.');
          ok = false;
        }
      });
      // Mobile check
      qsa('[name="mobile"]', form).forEach(field => {
        if (field.value && !/^\d{10}$/.test(field.value.replace(/\s+/g, ''))) {
          markError(field, 'Enter a valid 10-digit mobile number.');
          ok = false;
        }
      });
      if (!ok) e.preventDefault();
    });
  });

  /* ── Highlight active nav link ────────────────────────────── */
  const currentPath = window.location.pathname;
  qsa('.sidebar-link').forEach(link => {
    if (link.href && link.href !== location.origin + '/' && currentPath.startsWith(new URL(link.href, location.origin).pathname)) {
      link.classList.add('active');
    }
  });

  /* ── Table row click-to-select ────────────────────────────── */
  qsa('.table-hover tbody tr').forEach(row => {
    row.style.cursor = 'pointer';
  });

})();
