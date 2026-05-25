(function () {
  'use strict';

  var mainImg = document.getElementById('galleryMainImg');
  var mainLabel = document.getElementById('galleryMainLabel');
  var mainCaption = document.getElementById('galleryMainCaption');
  var photoTiles = document.querySelectorAll('.photo-tile');
  var galleryMain = document.getElementById('galleryMain');

  function setActivePhoto(tile) {
    if (!tile || !mainImg) return;

    var src = tile.getAttribute('data-src');
    var label = tile.getAttribute('data-label') || 'Photo';
    var caption = tile.getAttribute('data-caption') || label;

    photoTiles.forEach(function (item) {
      item.classList.toggle('active', item === tile);
      item.setAttribute('aria-pressed', item === tile ? 'true' : 'false');
    });

    mainImg.classList.add('is-changing');
    window.setTimeout(function () {
      mainImg.src = src;
      mainImg.alt = caption;
      if (mainLabel) mainLabel.textContent = label;
      if (mainCaption) mainCaption.textContent = caption;
      mainImg.classList.remove('is-changing');
    }, 140);
  }

  photoTiles.forEach(function (tile) {
    tile.setAttribute('aria-pressed', tile.classList.contains('active') ? 'true' : 'false');
    tile.addEventListener('click', function () {
      setActivePhoto(tile);
    });
  });

  if (galleryMain && mainImg) {
    galleryMain.addEventListener('mousemove', function (event) {
      var rect = galleryMain.getBoundingClientRect();
      var x = ((event.clientX - rect.left) / rect.width - 0.5) * 10;
      var y = ((event.clientY - rect.top) / rect.height - 0.5) * 10;
      mainImg.style.transform = 'scale(1.025) translate(' + x + 'px, ' + y + 'px)';
    });

    galleryMain.addEventListener('mouseleave', function () {
      mainImg.style.transform = '';
    });
  }

  var tabs = document.querySelectorAll('.prop-tab');
  var panels = document.querySelectorAll('.prop-tab-panel');

  tabs.forEach(function (tab) {
    tab.addEventListener('click', function () {
      var target = tab.getAttribute('data-tab');
      tabs.forEach(function (item) {
        item.classList.toggle('active', item === tab);
      });
      panels.forEach(function (panel) {
        panel.classList.toggle('active', panel.id === 'tab-' + target);
      });
    });
  });

  var revealItems = document.querySelectorAll('.reveal-on-scroll');
  if ('IntersectionObserver' in window) {
    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.14 });

    revealItems.forEach(function (item, index) {
      item.style.transitionDelay = Math.min(index * 65, 260) + 'ms';
      observer.observe(item);
    });
  } else {
    revealItems.forEach(function (item) {
      item.classList.add('is-visible');
    });
  }

  var calcBtn = document.getElementById('calcBtn');
  var priceEl = document.getElementById('mortgagePrice');
  var output = document.getElementById('mortgageMonthly');
  var annualCost = document.getElementById('annualCost');

  if (calcBtn && priceEl && output) {
    calcBtn.addEventListener('click', function () {
      var price = parseFloat(priceEl.value) || 0;
      if (annualCost) annualCost.value = '$' + Math.round(price * 12).toLocaleString('en-US');
      priceEl.dispatchEvent(new Event('input', { bubbles: true }));
    });
  }
}());
