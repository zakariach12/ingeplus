/* INGEPLUS — scripts du site */
(function () {
  document.documentElement.classList.remove('no-js');

  // Images : si le fichier local manque, on essaie la copie sur ingeplus.ma, sinon on masque.
  document.querySelectorAll('img[data-fb]').forEach(function (img) {
    function fail() {
      if (img.dataset.fb) { var fb = img.dataset.fb; img.dataset.fb = ''; img.src = fb; }
      else { img.style.visibility = 'hidden'; }
    }
    img.addEventListener('error', fail);
    if (img.complete && img.naturalWidth === 0 && img.getAttribute('src')) fail();
  });

  // En-tête : ombre au défilement + bouton haut de page
  var header = document.querySelector('.site-header');
  var toTop = document.querySelector('.to-top');
  function onScroll() {
    var y = window.scrollY;
    if (header) header.classList.toggle('scrolled', y > 10);
    if (toTop) toTop.classList.toggle('show', y > 700);
  }
  window.addEventListener('scroll', onScroll, { passive: true }); onScroll();

  // Menu mobile
  var burger = document.querySelector('.burger');
  var menu = document.querySelector('.menu');
  if (burger && menu) {
    burger.addEventListener('click', function () {
      var open = menu.classList.toggle('open');
      burger.setAttribute('aria-expanded', open);
      document.body.style.overflow = open ? 'hidden' : '';
    });
    menu.querySelectorAll('.has-sub > a').forEach(function (a) {
      a.addEventListener('click', function (e) {
        if (window.innerWidth <= 980) { e.preventDefault(); a.parentElement.classList.toggle('sub-open'); }
      });
    });
  }

  // Apparition au défilement
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
    }, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });
    document.querySelectorAll('.reveal').forEach(function (el) { io.observe(el); });

    // Compteurs
    var co = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (!e.isIntersecting) return;
        var el = e.target, n = +el.dataset.count, s = el.dataset.suffix || '', i = 0;
        var t = setInterval(function () { i++; el.textContent = i + (i === n ? s : ''); if (i >= n) clearInterval(t); }, Math.max(30, 900 / n));
        co.unobserve(el);
      });
    }, { threshold: 0.6 });
    document.querySelectorAll('[data-count]').forEach(function (el) { co.observe(el); });
  } else {
    document.querySelectorAll('.reveal').forEach(function (el) { el.classList.add('in'); });
  }

  // Filtres projets
  var filterBtns = document.querySelectorAll('.filters button');
  filterBtns.forEach(function (b) {
    b.addEventListener('click', function () {
      filterBtns.forEach(function (x) { x.classList.remove('on'); x.setAttribute('aria-pressed', 'false'); });
      b.classList.add('on'); b.setAttribute('aria-pressed', 'true');
      document.querySelectorAll('.proj').forEach(function (p) {
        p.classList.toggle('hide', b.dataset.f !== 'all' && p.dataset.c !== b.dataset.f);
      });
    });
  });

  // Visionneuse projets
  var lb = document.querySelector('.lightbox');
  if (lb) {
    var items = Array.prototype.slice.call(document.querySelectorAll('.proj'));
    var lbImg = lb.querySelector('img'), lbCat = lb.querySelector('.lb-cat'),
        lbTitle = lb.querySelector('.lb-title'), lbLoc = lb.querySelector('.lb-loc'), idx = 0;
    function visible() { return items.filter(function (p) { return !p.classList.contains('hide'); }); }
    function show(p) {
      var img = p.querySelector('img');
      lbImg.src = img.currentSrc || img.src; lbImg.alt = img.alt;
      lbCat.textContent = p.dataset.cat; lbTitle.textContent = p.dataset.title; lbLoc.textContent = p.dataset.loc;
    }
    function open(p) { idx = visible().indexOf(p); show(p); lb.classList.add('open'); document.body.style.overflow = 'hidden'; lb.querySelector('.lb-close').focus(); }
    function close() { lb.classList.remove('open'); document.body.style.overflow = ''; }
    function step(d) { var v = visible(); idx = (idx + d + v.length) % v.length; show(v[idx]); }
    items.forEach(function (p) { p.addEventListener('click', function () { open(p); }); });
    lb.querySelector('.lb-close').addEventListener('click', close);
    lb.querySelector('.lb-prev').addEventListener('click', function () { step(-1); });
    lb.querySelector('.lb-next').addEventListener('click', function () { step(1); });
    lb.addEventListener('click', function (e) { if (e.target === lb) close(); });
    document.addEventListener('keydown', function (e) {
      if (!lb.classList.contains('open')) return;
      if (e.key === 'Escape') close(); if (e.key === 'ArrowLeft') step(-1); if (e.key === 'ArrowRight') step(1);
    });
  }

  // Formulaire de contact : envoi via contact.php, repli sur la messagerie si PHP indisponible
  var form = document.getElementById('contact-form');
  if (form) {
    var status = form.querySelector('.form-status');
    var params = new URLSearchParams(location.search);
    var pre = params.get('expertise');
    if (pre) { var sel = form.querySelector('select[name="service"]'); if (sel) sel.value = pre; }

    function mailtoFallback(fd) {
      var body = 'Nom : ' + fd.get('nom') + '\nSociété : ' + (fd.get('societe') || '-') + '\nE-mail : ' + fd.get('email') +
        '\nTéléphone : ' + (fd.get('tel') || '-') + '\nVille du projet : ' + (fd.get('ville') || '-') + '\nExpertise : ' + fd.get('service') + '\n\n' + fd.get('message');
      location.href = 'mailto:contact@ingeplus.ma?subject=' + encodeURIComponent('Demande de projet – ' + fd.get('service')) + '&body=' + encodeURIComponent(body);
    }
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var btn = form.querySelector('button[type="submit"]'), fd = new FormData(form);
      btn.disabled = true; btn.firstChild.textContent = 'Envoi en cours… ';
      status.className = 'form-status';
      fetch(form.action, { method: 'POST', body: fd, headers: { 'Accept': 'application/json' } })
        .then(function (r) { return r.json().catch(function () { throw new Error('nojson'); }); })
        .then(function (res) {
          if (res.ok) { status.className = 'form-status ok'; status.textContent = 'Merci ! Votre demande a bien été envoyée. Notre équipe vous recontacte rapidement.'; form.reset(); }
          else { status.className = 'form-status err'; status.textContent = res.error || 'Une erreur est survenue. Merci de réessayer ou de nous appeler.'; }
        })
        .catch(function () { mailtoFallback(fd); status.className = 'form-status ok'; status.textContent = 'Votre messagerie s’ouvre pour finaliser l’envoi à contact@ingeplus.ma.'; })
        .finally(function () { btn.disabled = false; btn.firstChild.textContent = 'Envoyer ma demande '; });
    });
  }

  var y = document.getElementById('year'); if (y) y.textContent = new Date().getFullYear();
})();
