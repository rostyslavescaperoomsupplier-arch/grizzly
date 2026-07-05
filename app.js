
(function(){
  var I=window.I18N||{}, G=window.GRZ||{locs:[]};
  var LANG='pl';
  function cur(){return I[LANG]||I.pl||{};}

  /* ---------- i18n ---------- */
  function setLang(l){
    LANG=l; var d=cur();
    document.querySelectorAll('[data-i18n]').forEach(function(el){
      var k=el.getAttribute('data-i18n'); if(d[k]!=null) el.textContent=d[k];
    });
    document.documentElement.lang=l;
    document.querySelectorAll('#lang button').forEach(function(b){b.classList.toggle('on',b.getAttribute('data-l')===l);});
    try{localStorage.setItem('grz_lang',l);}catch(e){}
    renderOpen(); buildCalc();
  }
  var saved; try{saved=localStorage.getItem('grz_lang');}catch(e){}
  document.querySelectorAll('#lang button').forEach(function(b){b.addEventListener('click',function(){setLang(b.getAttribute('data-l'));});});

  /* ---------- theme ---------- */
  var tb=document.getElementById('themeBtn');
  if(tb)tb.addEventListener('click',function(){
    var r=document.documentElement, now=r.getAttribute('data-theme')==='light'?'':'light';
    if(now)r.setAttribute('data-theme','light');else r.removeAttribute('data-theme');
    try{localStorage.setItem('grz_theme',now);}catch(e){}
  });

  /* ---------- burger ---------- */
  var burger=document.getElementById('burger'),drawer=document.getElementById('drawer');
  if(burger){burger.addEventListener('click',function(){drawer.classList.toggle('open');});
    drawer.querySelectorAll('a,.btn').forEach(function(a){a.addEventListener('click',function(){drawer.classList.remove('open');});});}

  /* ---------- promo ---------- */
  var promo=document.getElementById('promo');
  try{if(localStorage.getItem('grz_promo')==='0'&&promo)promo.classList.add('hide');}catch(e){}
  var px=document.getElementById('promoX');
  if(px)px.addEventListener('click',function(){promo.classList.add('hide');try{localStorage.setItem('grz_promo','0');}catch(e){}});

  /* ---------- reveal ---------- */
  var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target);}});},{threshold:.12});
  document.querySelectorAll('.reveal').forEach(function(el){io.observe(el);});

  /* ---------- scroll progress + toTop ---------- */
  var pg=document.getElementById('progress'),tt=document.getElementById('toTop');
  function onScroll(){
    var h=document.documentElement, sc=h.scrollTop, max=h.scrollHeight-h.clientHeight;
    if(pg)pg.style.width=(max>0?(sc/max*100):0)+'%';
    if(tt)tt.classList.toggle('show',sc>500);
  }
  window.addEventListener('scroll',onScroll); onScroll();
  if(tt)tt.addEventListener('click',function(){window.scrollTo({top:0,behavior:'smooth'});});

  /* ---------- count-up ---------- */
  var counters=document.querySelectorAll('[data-count]');
  var cio=new IntersectionObserver(function(es){es.forEach(function(e){
    if(!e.isIntersecting)return; cio.unobserve(e.target);
    var el=e.target, end=parseInt(el.getAttribute('data-count'),10), suf=end>100?'+':'', t0=null;
    function step(ts){if(!t0)t0=ts;var p=Math.min((ts-t0)/1100,1);el.textContent=Math.floor(p*end)+suf;if(p<1)requestAnimationFrame(step);}
    requestAnimationFrame(step);
  });},{threshold:.5});
  counters.forEach(function(el){cio.observe(el);});

  /* ---------- open-now badges ---------- */
  function isOpen(o){if(!o)return null;var h=new Date().getHours();return h>=o[0]&&h<o[1];}
  function renderOpen(){
    var d=cur();
    document.querySelectorAll('[data-open]').forEach(function(el){
      var loc=G.locs.filter(function(x){return x.slug===el.getAttribute('data-open');})[0];
      if(!loc){el.textContent='';return;}
      var st=isOpen(loc.open);
      el.classList.remove('open','closed');
      if(st===true){el.classList.add('open');el.textContent='● '+(d.open_now||'Open');}
      else{el.classList.add('closed');el.textContent='● '+(d.closed_now||'Closed');}
    });
  }

  /* ---------- price tabs ---------- */
  document.querySelectorAll('.tab').forEach(function(b){
    b.addEventListener('click',function(){
      var s=b.getAttribute('data-tab');
      document.querySelectorAll('.tab').forEach(function(x){x.classList.toggle('on',x===b);});
      document.querySelectorAll('.tab-panel').forEach(function(p){p.classList.toggle('on',p.getAttribute('data-panel')===s);});
    });
  });

  /* ---------- booking modal ---------- */
  var modal=document.getElementById('bookModal');
  function openModal(){if(modal)modal.classList.add('open');}
  function closeModal(){if(modal)modal.classList.remove('open');}
  document.querySelectorAll('.js-book').forEach(function(b){b.addEventListener('click',openModal);});
  if(modal){modal.addEventListener('click',function(e){if(e.target===modal||e.target.classList.contains('modal-x'))closeModal();});}

  /* ---------- nearest finder ---------- */
  function haversine(a,b,c,d){var R=6371,dl=(c-a)*Math.PI/180,dn=(d-b)*Math.PI/180;
    var x=Math.sin(dl/2)*Math.sin(dl/2)+Math.cos(a*Math.PI/180)*Math.cos(c*Math.PI/180)*Math.sin(dn/2)*Math.sin(dn/2);
    return R*2*Math.atan2(Math.sqrt(x),Math.sqrt(1-x));}
  var fb=document.getElementById('finderBtn'),fm=document.getElementById('finderMsg');
  if(fb)fb.addEventListener('click',function(){
    var d=cur();
    if(!navigator.geolocation){document.getElementById('lokale').scrollIntoView({behavior:'smooth'});return;}
    fm.textContent=d.finder_wait||'…';
    navigator.geolocation.getCurrentPosition(function(pos){
      var la=pos.coords.latitude, ln=pos.coords.longitude, best=null;
      G.locs.forEach(function(l){var km=haversine(la,ln,l.lat,l.lng);l._km=km;if(!best||km<best._km)best=l;});
      document.querySelectorAll('[data-dist]').forEach(function(el){
        var l=G.locs.filter(function(x){return x.slug===el.getAttribute('data-dist');})[0];
        if(l&&l._km!=null)el.textContent='≈ '+l._km.toFixed(1)+' '+(d.km||'km');
      });
      document.querySelectorAll('.loc-card').forEach(function(c){c.classList.toggle('near',c.getAttribute('data-slug')===best.slug);});
      fm.textContent=(d.finder_res||'')+' '+best.short+' (≈ '+best._km.toFixed(1)+' '+(d.km||'km')+')';
      var card=document.querySelector('.loc-card.near'); if(card)card.scrollIntoView({behavior:'smooth',block:'center'});
    },function(){fm.textContent=d.finder_deny||'';document.getElementById('lokale').scrollIntoView({behavior:'smooth'});});
  });

  /* ---------- calculator ---------- */
  var cLoc=document.getElementById('calcLoc'),cItems=document.getElementById('calcItems'),
      cTot=document.getElementById('calcTotal'),cTime=document.getElementById('calcTime'),cBook=document.getElementById('calcBook');
  function buildCalc(){
    if(!cLoc)return; var d=cur(), keep=cLoc.value;
    cLoc.innerHTML=G.locs.map(function(l){return '<option value="'+l.slug+'">'+l.short+'</option>';}).join('');
    if(keep)cLoc.value=keep;
    renderItems();
  }
  function renderItems(){
    if(!cItems)return;
    var loc=G.locs.filter(function(l){return l.slug===cLoc.value;})[0]||G.locs[0];
    cItems.innerHTML=loc.services.map(function(s,i){
      return '<label class="calc-item"><input type="checkbox" data-num="'+s.num+'" data-min="'+s.min+'">'
        +'<span class="ci-name">'+s.name+'</span>'
        +'<span class="ci-price">'+s.price+'</span><span class="ci-time">'+s.time+'</span></label>';
    }).join('');
    cItems.querySelectorAll('input').forEach(function(x){x.addEventListener('change',calcSum);});
    cBook.href=loc.book_url; cBook.target=loc.book_type==='phone'?'':'_blank';
    calcSum();
  }
  function calcSum(){
    var sum=0,mn=0;
    cItems.querySelectorAll('input:checked').forEach(function(x){sum+=+x.getAttribute('data-num');mn+=+x.getAttribute('data-min');});
    cTot.textContent=sum+' zł';
    var h=Math.floor(mn/60),m=mn%60; cTime.textContent=(h?h+' g ':'')+(m?m+' min':(h?'':'0 min'));
  }
  if(cLoc){cLoc.addEventListener('change',renderItems);}

  /* ---------- reviews carousel ---------- */
  var track=document.getElementById('revTrack');
  if(track){
    var slides=track.children.length,idx=0,dotsWrap=document.getElementById('revDots'),timer;
    function go(i){idx=(i+slides)%slides;track.style.transform='translateX(-'+(idx*100)+'%)';
      dotsWrap.querySelectorAll('.rev-dot').forEach(function(dt,j){dt.classList.toggle('on',j===idx);});}
    function auto(){clearInterval(timer);timer=setInterval(function(){go(idx+1);},5000);}
    dotsWrap.querySelectorAll('.rev-dot').forEach(function(dt){dt.addEventListener('click',function(){go(+dt.getAttribute('data-i'));auto();});});
    document.querySelector('.rev-next').addEventListener('click',function(){go(idx+1);auto();});
    document.querySelector('.rev-prev').addEventListener('click',function(){go(idx-1);auto();});
    var sx=null;track.addEventListener('touchstart',function(e){sx=e.touches[0].clientX;},{passive:true});
    track.addEventListener('touchend',function(e){if(sx==null)return;var dx=e.changedTouches[0].clientX-sx;if(Math.abs(dx)>40)go(idx+(dx<0?1:-1));sx=null;auto();},{passive:true});
    auto();
  }

  /* ---------- faq ---------- */
  document.querySelectorAll('.faq-q').forEach(function(q){
    q.addEventListener('click',function(){
      var it=q.parentElement,a=it.querySelector('.faq-a'),open=it.classList.toggle('open');
      a.style.maxHeight=open?a.scrollHeight+'px':0;
    });
  });

  /* ---------- before/after ---------- */
  var baR=document.getElementById('baRange'),baB=document.getElementById('baBefore'),baH=document.getElementById('baHandle');
  if(baR){function baSet(v){baB.style.width=v+'%';baH.style.left=v+'%';}
    baR.addEventListener('input',function(){baSet(baR.value);}); baSet(50);}

  /* ---------- lightbox ---------- */
  var lb=document.getElementById('lightbox'),lbImg=document.getElementById('lbImg'),lbImgs=[],lbIdx=0;
  function lbShow(i){lbIdx=(i+lbImgs.length)%lbImgs.length;lbImg.src=lbImgs[lbIdx].src;}
  document.querySelectorAll('img.lb').forEach(function(im,i){lbImgs.push(im);
    im.addEventListener('click',function(){lb.classList.add('open');lbShow(i);});});
  if(lb){
    lb.querySelector('.lb-close').addEventListener('click',function(){lb.classList.remove('open');});
    lb.querySelector('.lb-next').addEventListener('click',function(e){e.stopPropagation();lbShow(lbIdx+1);});
    lb.querySelector('.lb-prev').addEventListener('click',function(e){e.stopPropagation();lbShow(lbIdx-1);});
    lb.addEventListener('click',function(e){if(e.target===lb)lb.classList.remove('open');});
    document.addEventListener('keydown',function(e){if(!lb.classList.contains('open'))return;
      if(e.key==='Escape')lb.classList.remove('open');if(e.key==='ArrowRight')lbShow(lbIdx+1);if(e.key==='ArrowLeft')lbShow(lbIdx-1);});
  }

  /* ---------- init ---------- */
  var start=saved||'pl';   // Polish is the default language
  buildCalc();
  setLang(start);
})();
