(function(){
  var KEY='posle-theme', site=document.getElementById('site'), root=document.documentElement;
  function apply(d){site.classList.toggle('dark',d);root.classList.toggle('dark',d);
    var b=document.getElementById('tg'); if(b){b.setAttribute('aria-label',d?'Светлая тема':'Тёмная тема');b.setAttribute('aria-pressed',d?'true':'false');}}
  var b=document.getElementById('tg');
  if(b) b.addEventListener('click',function(){var d=!site.classList.contains('dark');apply(d);try{localStorage.setItem(KEY,d?'dark':'light')}catch(e){}});
  apply(site.classList.contains('dark'));
})();
