(function () {
  'use strict';

  var menuBtn = document.getElementById('menu-btn');
  var menu = document.getElementById('mobile-menu');
  if (menuBtn && menu) {
    menuBtn.addEventListener('click', function () {
      var hidden = menu.classList.toggle('hidden');
      menuBtn.setAttribute('aria-expanded', String(!hidden));
      menuBtn.setAttribute('aria-label', hidden ? 'Open menu' : 'Close menu');
    });
  }

  var searchBtn = document.getElementById('search-btn');
  var searchBar = document.getElementById('search-bar');
  if (searchBtn && searchBar) {
    searchBtn.addEventListener('click', function () {
      var hidden = searchBar.classList.toggle('hidden');
      searchBtn.setAttribute('aria-expanded', String(!hidden));
      if (!hidden) {
        var input = searchBar.querySelector('input');
        if (input) input.focus();
      }
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && !searchBar.classList.contains('hidden')) {
        searchBar.classList.add('hidden');
        searchBtn.setAttribute('aria-expanded', 'false');
        searchBtn.focus();
      }
    });
  }

  document.querySelectorAll('[data-autosubmit]').forEach(function (el) {
    el.addEventListener('change', function () { el.form.submit(); });
  });

  document.querySelectorAll('[data-row]').forEach(function (row) {
    var wrap = row.parentElement;
    var prev = wrap.querySelector('[data-row-prev]');
    var next = wrap.querySelector('[data-row-next]');
    var step = function () { return row.clientWidth * 0.7; };
    if (prev) prev.addEventListener('click', function () { row.scrollBy({ left: -step(), behavior: 'smooth' }); });
    if (next) next.addEventListener('click', function () { row.scrollBy({ left: step(), behavior: 'smooth' }); });
  });

  document.querySelectorAll('[data-qty-minus], [data-qty-plus]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var wrap = btn.closest('form') || btn.parentElement;
      var input = wrap.querySelector('input[type="number"]');
      if (!input) return;
      var min = parseInt(input.min || '1', 10);
      var max = parseInt(input.max || '20', 10);
      var value = parseInt(input.value || min, 10) || min;
      value += btn.hasAttribute('data-qty-plus') ? 1 : -1;
      input.value = Math.max(min, Math.min(max, value));
      if (input.hasAttribute('data-qty-submit')) btn.closest('form').submit();
    });
  });

  document.querySelectorAll('[data-qty-submit]').forEach(function (input) {
    input.addEventListener('change', function () { input.closest('form').submit(); });
  });

  var revealEls = document.querySelectorAll('.reveal');
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if ('IntersectionObserver' in window && !reduce) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('revealed');
          io.unobserve(entry.target);
        }
      });
    }, { threshold: 0.08, rootMargin: '0px 0px -40px 0px' });
    revealEls.forEach(function (el) { io.observe(el); });
  } else {
    revealEls.forEach(function (el) { el.classList.add('revealed'); });
  }
})();