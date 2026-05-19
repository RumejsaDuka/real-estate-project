(function () {
  'use strict';

  var mainImg = document.getElementById('galleryMainImg');
  var mainLabel = document.getElementById('galleryMainLabel');
  var mainCaption = document.getElementById('galleryMainCaption');
  var photoTiles = document.querySelectorAll('.photo-tile');

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
