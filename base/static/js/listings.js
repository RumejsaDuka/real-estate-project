(function () {
  'use strict';

  var grid = document.getElementById('listingsGrid');
  var gridBtn = document.getElementById('viewGrid');
  var listBtn = document.getElementById('viewList');

  if (!grid || !gridBtn || !listBtn) return;

  function setView(mode) {
    var listMode = mode === 'list';
    grid.classList.toggle('list-view', listMode);
    gridBtn.classList.toggle('active', !listMode);
    listBtn.classList.toggle('active', listMode);
  }

  gridBtn.addEventListener('click', function () { setView('grid'); });
  listBtn.addEventListener('click', function () { setView('list'); });
}());
