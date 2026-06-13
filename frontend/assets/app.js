(function () {
  'use strict';

  function $(selector, root) { return (root || document).querySelector(selector); }
  function $all(selector, root) { return Array.prototype.slice.call((root || document).querySelectorAll(selector)); }

  var header = $('.site-header');
  var menuButton = $('.menu-button');
  if (menuButton && header) {
    menuButton.addEventListener('click', function () {
      var open = header.classList.toggle('menu-open');
      menuButton.setAttribute('aria-expanded', String(open));
    });
  }

  $all('.nav a, .footer a[href^="#"], .hero-actions a[href^="#"], .cards a[href^="#"], .report-actions a[href^="#"]').forEach(function (link) {
    link.addEventListener('click', function () {
      if (header) header.classList.remove('menu-open');
      if (menuButton) menuButton.setAttribute('aria-expanded', 'false');
    });
  });

  var tabs = $all('.tab');
  tabs.forEach(function (button) {
    button.addEventListener('click', function () {
      var id = button.getAttribute('data-tab');
      if (!/^[a-z0-9-]+$/.test(id || '')) return;
      tabs.forEach(function (tab) {
        tab.classList.remove('active');
        tab.setAttribute('aria-selected', 'false');
      });
      $all('.code-panel').forEach(function (panel) {
        panel.classList.remove('active');
        panel.setAttribute('hidden', '');
      });
      var selectedPanel = $('#tab-' + id);
      if (!selectedPanel) return;
      button.classList.add('active');
      button.setAttribute('aria-selected', 'true');
      selectedPanel.classList.add('active');
      selectedPanel.removeAttribute('hidden');
    });
  });

  $all('.copy-button').forEach(function (button) {
    button.addEventListener('click', function () {
      var targetId = button.getAttribute('data-copy-target');
      if (!/^[a-z0-9-]+$/.test(targetId || '')) return;
      var target = document.getElementById(targetId);
      if (!target) return;
      var text = target.textContent || '';
      function setCopied() {
        var original = button.textContent;
        button.textContent = 'Copied';
        window.setTimeout(function () { button.textContent = original; }, 1400);
      }
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(setCopied).catch(function () {});
      } else {
        var textarea = document.createElement('textarea');
        textarea.value = text;
        textarea.setAttribute('readonly', '');
        textarea.style.position = 'absolute';
        textarea.style.left = '-9999px';
        document.body.appendChild(textarea);
        textarea.select();
        try { document.execCommand('copy'); setCopied(); } catch (e) {}
        document.body.removeChild(textarea);
      }
    });
  });

  var navLinks = $all('.nav a');
  var sections = navLinks.map(function (link) {
    var href = link.getAttribute('href');
    return href && href.charAt(0) === '#' ? document.getElementById(href.slice(1)) : null;
  });
  function updateActiveNav() {
    var current = '';
    sections.forEach(function (section) {
      if (section && section.getBoundingClientRect().top < 140) current = section.id;
    });
    navLinks.forEach(function (link) {
      link.classList.toggle('active', link.getAttribute('href') === '#' + current);
    });
  }
  window.addEventListener('scroll', updateActiveNav, { passive: true });
  updateActiveNav();
})();
