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
