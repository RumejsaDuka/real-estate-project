/* ============================================================
   REALESTATE — SCRIPT.JS
   ============================================================ */

(function () {
  'use strict';

  /* ── NAVBAR: Scroll state ── */
  const navbar = document.getElementById('navbar');

  function handleNavbarScroll() {
    if (window.scrollY > 60) {
      navbar.classList.add('scrolled');
    } else {
      navbar.classList.remove('scrolled');
    }
  }

  if (navbar) {
    window.addEventListener('scroll', handleNavbarScroll, { passive: true });
    handleNavbarScroll();
  }

  /* ── NAVBAR: Mobile toggle ── */
  const navToggle = document.getElementById('navToggle');
  const navLinks  = document.querySelector('.nav-links');

  if (navToggle && navLinks) {
    navToggle.addEventListener('click', function () {
      const isOpen = navLinks.classList.toggle('open');
      navToggle.classList.toggle('open', isOpen);
      navToggle.setAttribute('aria-expanded', isOpen);
      document.body.style.overflow = isOpen ? 'hidden' : '';
    });

    navLinks.querySelectorAll('.nav-link').forEach(function (link) {
      link.addEventListener('click', function () {
        navLinks.classList.remove('open');
        navToggle.classList.remove('open');
        navToggle.setAttribute('aria-expanded', 'false');
        document.body.style.overflow = '';
      });
    });
  }

  /* ── PROPERTY CARDS: Scroll-triggered reveal ── */
  const cards = document.querySelectorAll('.property-card');

  if (cards.length && 'IntersectionObserver' in window) {
    const cardObserver = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            const card  = entry.target;
            const index = parseInt(card.getAttribute('data-index'), 10) || 0;
            setTimeout(function () {
              card.classList.add('visible');
            }, index * 90);
            cardObserver.unobserve(card);
          }
        });
      },
      { threshold: 0.08, rootMargin: '0px 0px -40px 0px' }
    );
    cards.forEach(function (card) {
      cardObserver.observe(card);
    });
  } else {
    cards.forEach(function (card) {
      card.classList.add('visible');
    });
  }

  /* ── SEARCH BAR ── */
  const searchBtn = document.getElementById('searchBtn');

  if (searchBtn) {
    searchBtn.addEventListener('click', function () {
      const location = document.getElementById('location');
      const price    = document.getElementById('price');
      const query    = location ? location.value.trim() : '';
      const maxPrice = price    ? price.value           : '';
      const params   = new URLSearchParams();
      if (query)    params.set('location', query);
      if (maxPrice) params.set('maxPrice',  maxPrice);
      const dest = 'listings.html' + (params.toString() ? '?' + params.toString() : '');
      window.location.href = dest;
    });

    const locationInput = document.getElementById('location');
    if (locationInput) {
      locationInput.addEventListener('keydown', function (e) {
        if (e.key === 'Enter') searchBtn.click();
      });
    }
  }

  /* ── ACTIVE NAV LINK ── */
  (function highlightCurrentPage() {
    const currentFile = window.location.pathname.split('/').pop() || 'index.html';
    document.querySelectorAll('.nav-link').forEach(function (link) {
      const href = link.getAttribute('href');
      if (href === currentFile) {
        link.classList.add('active');
      } else {
        link.classList.remove('active');
      }
    });
  }());

}());

/* ============================================================
   REALESTATE — PROPERTY.JS
   ============================================================ */

(function () {
  'use strict';

  /* ── GALLERY DATA ──
     Merr src nga img brenda çdo thumbnail button.
     Disa button nuk kanë data-src, ndaj marrim src nga img[src] direkt.
  ── */
  var galleryImages = (function () {
    var thumbBtns = document.querySelectorAll('.gallery-thumb');
    var images    = [];
    thumbBtns.forEach(function (btn) {
      var dataSrc = btn.getAttribute('data-src');
      var imgEl   = btn.querySelector('img');
      var src     = dataSrc || (imgEl ? imgEl.getAttribute('src') : '');
      var alt     = btn.getAttribute('data-alt') || (imgEl ? imgEl.getAttribute('alt') : '') || '';
      if (src) {
        images.push({ src: src, alt: alt });
      }
    });
    return images;
  }());

  var currentIndex = 0;

  /* ── GALLERY: switch main image ── */
  function setGalleryImage(index, fromLightbox) {
    if (galleryImages.length === 0) return;
    if (index < 0)                    index = galleryImages.length - 1;
    if (index >= galleryImages.length) index = 0;
    currentIndex = index;

    var mainImg   = document.getElementById('galleryMainImg');
    var counter   = document.getElementById('galleryCounter');
    var thumbBtns = document.querySelectorAll('.gallery-thumb');

    if (mainImg) {
      mainImg.classList.add('fading');
      setTimeout(function () {
        mainImg.src = galleryImages[index].src;
        mainImg.alt = galleryImages[index].alt;
        mainImg.classList.remove('fading');
      }, 180);
    }

    if (counter) {
      counter.textContent = (index + 1) + ' / ' + galleryImages.length;
    }

    thumbBtns.forEach(function (btn, i) {
      btn.classList.toggle('active', i === index);
    });

    if (fromLightbox) {
      setLightboxImage(index);
    }
  }

  /* ── GALLERY: thumbnail clicks ── */
  document.querySelectorAll('.gallery-thumb').forEach(function (btn, i) {
    btn.addEventListener('click', function () {
      setGalleryImage(i, false);
    });
  });

  /* ── GALLERY: prev/next arrows ── */
  var prevBtn = document.getElementById('galleryPrev');
  var nextBtn = document.getElementById('galleryNext');

  if (prevBtn) {
    prevBtn.addEventListener('click', function () {
      setGalleryImage(currentIndex - 1, false);
    });
  }
  if (nextBtn) {
    nextBtn.addEventListener('click', function () {
      setGalleryImage(currentIndex + 1, false);
    });
  }

  /* ── LIGHTBOX ── */
  var lightbox         = document.getElementById('lightbox');
  var lightboxBackdrop = document.getElementById('lightboxBackdrop');
  var lightboxImg      = document.getElementById('lightboxImg');
  var lightboxCaption  = document.getElementById('lightboxCaption');
  var lightboxClose    = document.getElementById('lightboxClose');
  var lightboxPrev     = document.getElementById('lightboxPrev');
  var lightboxNext     = document.getElementById('lightboxNext');
  var lightboxDots     = document.getElementById('lightboxDots');
  var expandBtn        = document.getElementById('galleryExpand');

  if (lightboxDots && galleryImages.length) {
    galleryImages.forEach(function (img, i) {
      var dot = document.createElement('button');
      dot.className = 'lightbox-dot' + (i === 0 ? ' active' : '');
      dot.setAttribute('aria-label', 'Photo ' + (i + 1));
      dot.addEventListener('click', function () { setLightboxImage(i); });
      lightboxDots.appendChild(dot);
    });
  }

  function openLightbox(index) {
    if (!lightbox || !lightboxBackdrop) return;
    setLightboxImage(index);
    lightbox.classList.add('open');
    lightboxBackdrop.classList.add('open');
    document.body.style.overflow = 'hidden';
  }

  function closeLightbox() {
    if (!lightbox || !lightboxBackdrop) return;
    lightbox.classList.remove('open');
    lightboxBackdrop.classList.remove('open');
    document.body.style.overflow = '';
  }

  function setLightboxImage(index) {
    if (galleryImages.length === 0) return;
    if (index < 0)                    index = galleryImages.length - 1;
    if (index >= galleryImages.length) index = 0;
    currentIndex = index;

    if (lightboxImg) {
      lightboxImg.classList.add('fading');
      setTimeout(function () {
        lightboxImg.src = galleryImages[index].src;
        lightboxImg.alt = galleryImages[index].alt;
        lightboxImg.classList.remove('fading');
      }, 140);
    }

    if (lightboxCaption) {
      lightboxCaption.textContent = galleryImages[index].alt;
    }

    document.querySelectorAll('.lightbox-dot').forEach(function (dot, i) {
      dot.classList.toggle('active', i === index);
    });

    setGalleryImage(index, false);
  }

  if (expandBtn) {
    expandBtn.addEventListener('click', function () { openLightbox(currentIndex); });
  }
  if (lightboxClose) {
    lightboxClose.addEventListener('click', closeLightbox);
  }
  if (lightboxBackdrop) {
    lightboxBackdrop.addEventListener('click', closeLightbox);
  }
  if (lightboxPrev) {
    lightboxPrev.addEventListener('click', function () { setLightboxImage(currentIndex - 1); });
  }
  if (lightboxNext) {
    lightboxNext.addEventListener('click', function () { setLightboxImage(currentIndex + 1); });
  }

  var galleryMain = document.getElementById('galleryMain');
  if (galleryMain) {
    galleryMain.addEventListener('click', function (e) {
      if (e.target.closest('.gallery-nav') || e.target.closest('.gallery-expand')) return;
      openLightbox(currentIndex);
    });
    galleryMain.style.cursor = 'zoom-in';
  }

  document.addEventListener('keydown', function (e) {
    if (!lightbox || !lightbox.classList.contains('open')) return;
    if (e.key === 'Escape')     closeLightbox();
    if (e.key === 'ArrowLeft')  setLightboxImage(currentIndex - 1);
    if (e.key === 'ArrowRight') setLightboxImage(currentIndex + 1);
  });

  /* ── TABS ── */
  var tabBtns   = document.querySelectorAll('.prop-tab');
  var tabPanels = document.querySelectorAll('.prop-tab-panel');

  tabBtns.forEach(function (btn) {
    btn.addEventListener('click', function () {
      var target = btn.getAttribute('data-tab');

      tabBtns.forEach(function (b) { b.classList.remove('active'); });
      tabPanels.forEach(function (p) { p.classList.remove('active'); });

      btn.classList.add('active');
      var panel = document.getElementById('tab-' + target);
      if (panel) panel.classList.add('active');
    });
  });

  /* ── READ MORE ── */
  var readMoreBtn = document.getElementById('readMoreBtn');
  var descMore    = document.getElementById('descMore');

  if (readMoreBtn && descMore) {
    readMoreBtn.addEventListener('click', function () {
      var expanded = descMore.classList.toggle('visible');
      readMoreBtn.classList.toggle('expanded', expanded);
      readMoreBtn.innerHTML = expanded
        ? 'Read Less <i class="fas fa-chevron-up"></i>'
        : 'Read More <i class="fas fa-chevron-down"></i>';
    });
  }

  /* ── FLOOR PLAN TOGGLE ── */
  var fpLevelBtns = document.querySelectorAll('.fp-level-btn');
  var fpDiagram   = document.getElementById('fpDiagram');

  var floorData = {
    ground: [
      { name: 'Living Room',   size: '820 sqft', col: '1 / 3', row: '1 / 2', cls: 'fp-room-large' },
      { name: 'Kitchen',       size: '420 sqft', col: '3 / 4', row: '1 / 2', cls: '' },
      { name: 'Dining Room',   size: '360 sqft', col: '1 / 2', row: '2 / 3', cls: '' },
      { name: 'Guest Suite 1', size: '280 sqft', col: '2 / 3', row: '2 / 3', cls: '' },
      { name: 'Guest Suite 2', size: '280 sqft', col: '3 / 4', row: '2 / 3', cls: '' },
      { name: 'Garage',        size: '680 sqft', col: '1 / 2', row: '3 / 4', cls: 'fp-room-accent' },
      { name: 'Cinema',        size: '340 sqft', col: '2 / 3', row: '3 / 4', cls: '' },
      { name: 'Wine Cellar',   size: '160 sqft', col: '3 / 4', row: '3 / 4', cls: '' }
    ],
    upper: [
      { name: 'Primary Suite',  size: '1,100 sqft', col: '1 / 3', row: '1 / 2', cls: 'fp-room-large' },
      { name: 'Walk-in Closet', size: '280 sqft',   col: '3 / 4', row: '1 / 2', cls: '' },
      { name: 'Bedroom 3',      size: '260 sqft',   col: '1 / 2', row: '2 / 3', cls: '' },
      { name: 'Bedroom 4',      size: '260 sqft',   col: '2 / 3', row: '2 / 3', cls: '' },
      { name: 'Gym Room',       size: '310 sqft',   col: '3 / 4', row: '2 / 3', cls: '' },
      { name: 'Laundry',        size: '120 sqft',   col: '1 / 2', row: '3 / 4', cls: '' },
      { name: 'Office',         size: '200 sqft',   col: '2 / 3', row: '3 / 4', cls: '' },
      { name: 'Storage',        size: '140 sqft',   col: '3 / 4', row: '3 / 4', cls: 'fp-room-accent' }
    ],
    roof: [
      { name: 'Observation Deck', size: '1,400 sqft', col: '1 / 3', row: '1 / 3', cls: 'fp-room-large' },
      { name: 'Bar Area',         size: '220 sqft',   col: '3 / 4', row: '1 / 2', cls: '' },
      { name: 'Jacuzzi',          size: '160 sqft',   col: '3 / 4', row: '2 / 3', cls: 'fp-room-accent' },
      { name: 'Plant Terrace',    size: '380 sqft',   col: '1 / 4', row: '3 / 4', cls: '' }
    ]
  };

  function renderFloorPlan(level) {
    if (!fpDiagram) return;
    var rooms = floorData[level] || floorData.ground;
    fpDiagram.innerHTML = '';
    rooms.forEach(function (room) {
      var div = document.createElement('div');
      div.className = 'fp-room' + (room.cls ? ' ' + room.cls : '');
      div.style.gridColumn = room.col;
      div.style.gridRow    = room.row;
      div.innerHTML =
        '<span class="fp-room-name">' + room.name + '</span>' +
        '<span class="fp-room-size">' + room.size + '</span>';
      fpDiagram.appendChild(div);
    });
  }

  fpLevelBtns.forEach(function (btn) {
    btn.addEventListener('click', function () {
      fpLevelBtns.forEach(function (b) { b.classList.remove('active'); });
      btn.classList.add('active');
      renderFloorPlan(btn.getAttribute('data-level'));
    });
  });

  /* ── TOUR TYPE TOGGLE ── */
  var tourTypeBtns = document.querySelectorAll('.tour-type-btn');
  tourTypeBtns.forEach(function (btn) {
    btn.addEventListener('click', function () {
      tourTypeBtns.forEach(function (b) { b.classList.remove('active'); });
      btn.classList.add('active');
    });
  });

  /* ── TOUR FORM SUBMIT ── */
  var tourSubmitBtn = document.getElementById('tourSubmitBtn');
  var tourForm      = document.querySelector('.tour-form');
  var tourSuccess   = document.getElementById('tourSuccess');

  if (tourSubmitBtn && tourForm && tourSuccess) {
    tourSubmitBtn.addEventListener('click', function () {
      var name  = document.getElementById('tourName');
      var email = document.getElementById('tourEmail');
      var date  = document.getElementById('tourDate');
      var time  = document.getElementById('tourTime');

      var valid = true;
      [name, email, date, time].forEach(function (field) {
        if (field && !field.value.trim()) {
          field.style.borderColor = '#E74C3C';
          valid = false;
        } else if (field) {
          field.style.borderColor = '';
        }
      });

      if (!valid) return;

      tourForm.style.display = 'none';
      tourSuccess.classList.add('visible');
    });
  }

  /* ── SAVE BUTTON ── */
  var btnSave = document.getElementById('btnSave');
  if (btnSave) {
    btnSave.addEventListener('click', function () {
      var saved = btnSave.classList.toggle('saved');
      var icon  = btnSave.querySelector('i');
      var label = btnSave.querySelector('span');
      if (icon)  icon.className   = saved ? 'fas fa-heart' : 'far fa-heart';
      if (label) label.textContent = saved ? 'Saved' : 'Save';
    });
  }

  /* ── SHARE BUTTON ── */
  var btnShare = document.getElementById('btnShare');
  if (btnShare) {
    btnShare.addEventListener('click', function () {
      if (navigator.share) {
        navigator.share({ title: document.title, url: window.location.href }).catch(function () {});
      } else {
        navigator.clipboard.writeText(window.location.href).then(function () {
          var label = btnShare.querySelector('span');
          if (label) {
            label.textContent = 'Copied!';
            setTimeout(function () { label.textContent = 'Share'; }, 2000);
          }
        }).catch(function () {});
      }
    });
  }

  /* ── PRINT ── */
  var btnPrint = document.getElementById('btnPrint');
  if (btnPrint) {
    btnPrint.addEventListener('click', function () { window.print(); });
  }

  /* ── MORTGAGE CALCULATOR ── */
  var mortgageMonthly = document.getElementById('mortgageMonthly');
  var brkPI           = document.getElementById('brkPI');
  var brkTotal        = document.getElementById('brkTotal');

  function calcMortgage() {
    var price  = parseFloat(document.getElementById('mortgagePrice').value) || 0;
    var down   = parseFloat(document.getElementById('mortgageDown').value)   || 0;
    var rate   = parseFloat(document.getElementById('mortgageRate').value)   || 0;
    var term   = parseInt(document.getElementById('mortgageTerm').value, 10) || 30;

    var principal   = price - down;
    var monthlyRate = rate / 100 / 12;
    var numPayments = term * 12;
    var pi = 0;

    if (monthlyRate === 0) {
      pi = principal / numPayments;
    } else {
      pi = principal * (monthlyRate * Math.pow(1 + monthlyRate, numPayments))
           / (Math.pow(1 + monthlyRate, numPayments) - 1);
    }

    var tax   = 14200 / 12;
    var hoa   = 420;
    var total = pi + tax + hoa;

    function fmt(n) { return '$' + Math.round(n).toLocaleString('en-US'); }

    if (mortgageMonthly) mortgageMonthly.textContent = fmt(pi);
    if (brkPI)           brkPI.textContent            = fmt(pi);
    if (brkTotal)        brkTotal.textContent          = fmt(total);
  }

  ['mortgagePrice', 'mortgageDown', 'mortgageRate', 'mortgageTerm'].forEach(function (id) {
    var el = document.getElementById(id);
    if (el) el.addEventListener('input', calcMortgage);
  });

  calcMortgage();

  /* ── SIMILAR PROPERTIES: scroll reveal ── */
  var similarCards = document.querySelectorAll('.similar-section .property-card');

  if (similarCards.length && 'IntersectionObserver' in window) {
    var obs = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          var card  = entry.target;
          var index = parseInt(card.getAttribute('data-index'), 10) || 0;
          setTimeout(function () { card.classList.add('visible'); }, index * 100);
          obs.unobserve(card);
        }
      });
    }, { threshold: 0.08 });
    similarCards.forEach(function (card) { obs.observe(card); });
  } else {
    similarCards.forEach(function (card) { card.classList.add('visible'); });
  }

}());

// about
/* =============================================
   about.js — Grand Realty About Page Scripts
   ============================================= */

(function () {

  // ── Navbar: mobile toggle ──
  const navToggle = document.getElementById('navToggle');
  const navLinks  = document.getElementById('navLinks');

  if (navToggle && navLinks) {
    navToggle.addEventListener('click', function () {
      navLinks.classList.toggle('open');
      navToggle.classList.toggle('active');
    });
  }

  // ── Navbar: shrink on scroll ──
  const navbar = document.getElementById('navbar');

  window.addEventListener('scroll', function () {
    if (navbar) {
      navbar.classList.toggle('scrolled', window.scrollY > 50);
    }
  });

  // ── Fade-in on scroll ──
  const fadeEls = document.querySelectorAll(
    '.value-card, .team-card, .story-highlight'
  );

  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.15 });

    fadeEls.forEach(function (el) {
      el.classList.add('fade-up');
      observer.observe(el);
    });
  }

})();