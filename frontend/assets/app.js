(function () {
  'use strict';

  var tabs = document.querySelectorAll('.tab');

  tabs.forEach(function (button) {
    button.addEventListener('click', function () {
      var id = button.getAttribute('data-tab');
      if (!/^[a-z0-9-]+$/.test(id || '')) return;

      tabs.forEach(function (tab) {
        tab.classList.remove('active');
        tab.setAttribute('aria-selected', 'false');
      });

      document.querySelectorAll('.code-panel').forEach(function (panel) {
        panel.classList.remove('active');
        panel.setAttribute('hidden', '');
      });

      var selectedPanel = document.getElementById('tab-' + id);
      if (!selectedPanel) return;

      button.classList.add('active');
      button.setAttribute('aria-selected', 'true');
      selectedPanel.classList.add('active');
      selectedPanel.removeAttribute('hidden');
    });
  });
})();
