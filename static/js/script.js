(function(){
  var nav = document.getElementById('siteNav');
  var toggle = document.getElementById('navToggle');
  var panel = document.getElementById('navMobilePanel');

  function onScroll(){
    if(window.scrollY > 8){ nav.classList.add('is-scrolled'); }
    else{ nav.classList.remove('is-scrolled'); }
  }
  window.addEventListener('scroll', onScroll, {passive:true});
  onScroll();

  toggle.addEventListener('click', function(){
    var open = panel.classList.toggle('is-open');
    toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
  });

  panel.querySelectorAll('a').forEach(function(a){
    a.addEventListener('click', function(){
      panel.classList.remove('is-open');
      toggle.setAttribute('aria-expanded', 'false');
    });
  });
})();

// ============================================================
// PAGE LOADER — plays once per browser session, then gets out
// of the way so navigating between pages stays fast.
// ============================================================
(function(){
  var loader = document.getElementById('pageLoader');
  if(!loader) return;

  var reduceMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var alreadyShown = false;
  try{ alreadyShown = sessionStorage.getItem('oisLoaderShown') === '1'; }catch(e){}

  if(alreadyShown){
    loader.classList.add('is-skipped');
    return;
  }

  var minDuration = reduceMotion ? 150 : 1400;
  var start = Date.now();

  function finish(){
    var wait = Math.max(0, minDuration - (Date.now() - start));
    setTimeout(function(){
      loader.classList.add('is-done');
      try{ sessionStorage.setItem('oisLoaderShown', '1'); }catch(e){}
      setTimeout(function(){ loader.classList.add('is-skipped'); }, 550);
    }, wait);
  }

  if(document.readyState === 'complete'){
    finish();
  }else{
    window.addEventListener('load', finish);
    setTimeout(finish, 4000); // safety net: never trap someone behind a slow asset
  }

  // Restored from back/forward cache — never re-show mid-navigation
  window.addEventListener('pageshow', function(e){
    if(e.persisted){ loader.classList.add('is-skipped'); }
  });
})();
