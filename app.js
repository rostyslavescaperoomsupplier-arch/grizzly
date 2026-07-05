
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
  if(baR){function baSet(v){baB.style.clipPath='inset(0 '+(100-v)+'% 0 0)';baH.style.left=v+'%';}
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

  /* ---------- hairstyle constructor ---------- */
  var kForm=document.getElementById('konstrForm');
  if(kForm){
    var STYLES=['Fade','Undercut','Pompadour','Tekstura','Crew cut','Grzywka','Zaczesane do tyłu','Przedziałek','Loki','Irokez','Jeżyk','Kok','Na łyso'];
    var COLORS=['Naturalny','Brąz','Rozjaśnienie','Platyna / siwy','Cover'];
    var HCOL={'Naturalny':'#22221e','Brąz':'#4a3324','Rozjaśnienie':'#c2a877','Platyna / siwy':'#d3d0c8','Cover':'#3b3b37'};
    var TINT={'Naturalny':'grayscale(1) contrast(1.04)','Brąz':'sepia(.55) saturate(1.5) brightness(.92) contrast(1.02)','Rozjaśnienie':'grayscale(.1) sepia(.28) brightness(1.26) contrast(.95)','Platyna / siwy':'grayscale(1) brightness(1.32) contrast(.9)','Cover':'grayscale(1) brightness(.72) contrast(1.12)'};
    var HAIR={
     'Fade':'M74,114 C68,74 94,50 120,50 C146,50 172,74 166,114 C160,88 150,72 120,72 C90,72 80,88 74,114 Z',
     'Undercut':'M84,88 C86,52 154,52 156,88 C150,62 90,62 84,88 Z',
     'Pompadour':'M80,84 C78,42 116,28 134,42 C154,44 162,66 158,86 C150,58 96,58 80,84 Z',
     'Tekstura':'M76,90 l7,-16 8,13 9,-19 8,17 10,-21 10,19 9,-15 7,13 5,9 C150,60 92,60 76,90 Z',
     'Crew cut':'M78,74 C80,52 100,46 120,46 C140,46 160,52 162,74 C150,60 90,60 78,74 Z',
     'Grzywka':'M74,110 C72,70 96,50 120,50 C144,50 168,70 166,110 C160,84 150,72 120,72 C104,72 92,78 84,88 L90,102 96,88 102,102 108,88 114,102 120,88 126,100 Z',
     'Zaczesane do tyłu':'M80,80 C78,50 116,42 130,52 C150,54 160,72 155,92 C150,66 96,64 80,80 Z',
     'Przedziałek':'M76,98 C74,64 98,50 120,50 C144,50 168,66 166,100 C160,78 150,66 121,66 L118,58 115,66 C104,68 84,78 76,98 Z',
     'Loki':'M74,94 q2,-13 12,-14 q3,-11 15,-9 q6,-9 19,-6 q9,-4 18,3 q12,0 15,12 q7,4 5,16 C150,64 92,64 74,94 Z',
     'Irokez':'M109,40 C107,32 133,32 131,40 L128,90 112,90 Z',
     'Jeżyk':'M82,72 C84,56 100,50 120,50 C140,50 156,56 158,72 C150,62 90,62 82,72 Z',
     'Kok':'M80,84 C80,54 104,48 120,48 C138,48 158,58 156,86 C150,62 96,62 80,84 Z',
     'Na łyso':''
    };
    var PHOTO={'Loki':'assets/style/dlugie_nb.jpg','Kok':'assets/style/dlugie_nb.jpg','Na łyso':'assets/style/lyso_nb.jpg','Pompadour':'assets/style/srednie_nb.jpg','Zaczesane do tyłu':'assets/style/srednie_nb.jpg','Tekstura':'assets/style/srednie_nb.jpg','Grzywka':'assets/style/srednie_nb.jpg','Przedziałek':'assets/style/srednie_nb.jpg'};
    function photoFor(st){return PHOTO[st]||'assets/style/krotkie_nb.jpg';}
    var ksel={style:'Fade',color:'Naturalny'};
    var vid=document.getElementById('krVideo'), kimg=document.getElementById('krImg'),
        ov=document.getElementById('krOverlay'), hair=document.getElementById('krHair'),
        stage=document.getElementById('krStage'), stream=null;

    function kRender(){
      kForm.innerHTML='';
      var r1=document.createElement('div'); r1.className='kcat';
      r1.innerHTML='<div class="kcat-h">Fryzura</div>';
      var w1=document.createElement('div'); w1.className='kchips';
      STYLES.forEach(function(o){var b=document.createElement('button');b.type='button';b.className='kchip'+(ksel.style===o?' on':'');b.textContent=o;b.addEventListener('click',function(){ksel.style=o;kRender();kResult();});w1.appendChild(b);});
      r1.appendChild(w1); kForm.appendChild(r1);
      var r2=document.createElement('div'); r2.className='kcat';
      r2.innerHTML='<div class="kcat-h">Kolor włosów</div>';
      var pal=document.createElement('div'); pal.className='kpalette';
      COLORS.forEach(function(o){var b=document.createElement('button');b.type='button';b.className='kswatch'+(ksel.color===o?' on':'');b.title=o;b.innerHTML='<span class="ksw-dot" style="background:'+HCOL[o]+'"></span><span class="ksw-l">'+o+'</span>';b.addEventListener('click',function(){ksel.color=o;kRender();kResult();});pal.appendChild(b);});
      r2.appendChild(pal); kForm.appendChild(r2);
    }
    function shade(hex,amt){var n=parseInt(hex.slice(1),16);var r=Math.max(0,Math.min(255,(n>>16)+amt));var g=Math.max(0,Math.min(255,((n>>8)&255)+amt));var b=Math.max(0,Math.min(255,(n&255)+amt));return '#'+((1<<24)+(r<<16)+(g<<8)+b).toString(16).slice(1);}
    function drawHair(){
      var hp=HAIR[ksel.style];
      if(!hp){ hair.innerHTML=''; ov.style.display='none'; return; }
      ov.style.display='';
      var base=HCOL[ksel.color], lite=shade(base,34), drk=shade(base,-30);
      var defs='<defs><linearGradient id="hg" x1="0" y1="0" x2="0.2" y2="1">'
        +'<stop offset="0" stop-color="'+lite+'"/><stop offset=".5" stop-color="'+base+'"/><stop offset="1" stop-color="'+drk+'"/></linearGradient>'
        +'<clipPath id="hc"><path d="'+hp+'"/></clipPath>'
        +'<filter id="hb" x="-10%" y="-10%" width="120%" height="120%"><feGaussianBlur stdDeviation="0.6"/></filter></defs>';
      var strands='';
      for(var i=0;i<30;i++){var x=62+i*3.9, w1=Math.sin(i*1.3)*4, w2=Math.sin(i*0.7+1)*5;
        strands+='<path d="M'+x.toFixed(1)+',36 q'+w1.toFixed(1)+',32 '+w2.toFixed(1)+',64" stroke="'+lite+'" stroke-width="0.65" fill="none" opacity="'+(0.22+0.16*Math.abs(Math.sin(i))).toFixed(2)+'"/>';
        strands+='<path d="M'+(x+1.6).toFixed(1)+',40 q'+(w1*0.8).toFixed(1)+',30 '+(w2*0.9).toFixed(1)+',58" stroke="'+drk+'" stroke-width="0.5" fill="none" opacity="0.2"/>';}
      hair.innerHTML=defs
        +'<path d="'+hp+'" fill="url(#hg)" filter="url(#hb)"/>'
        +'<g clip-path="url(#hc)">'+strands+'</g>'
        +'<path d="'+hp+'" fill="none" stroke="'+drk+'" stroke-width="0.9" opacity=".55"/>';
    }
    function kResult(){
      var src=photoFor(ksel.style);
      if(kimg.getAttribute('src')!==src) kimg.src=src;
      kimg.style.filter=TINT[ksel.color]||'grayscale(1)';
      drawHair();
      var lyso=ksel.style==='Na łyso', svc=[],price=0;
      if(lyso){svc.push(['Głowa na łyso','od 60 zł']);price+=60;}
      else{svc.push(['Grizzly Cut — strzyżenie','od 90 zł']);price+=90;}
      if(ksel.color==='Rozjaśnienie'){svc.push(['Rozjaśnianie','od 200 zł']);price+=200;}
      else if(ksel.color!=='Naturalny'){svc.push(['COVER — koloryzacja','od 70 zł']);price+=70;}
      var parts=[ksel.style]; if(ksel.color!=='Naturalny')parts.push(ksel.color);
      var T=function(id){return document.getElementById(id);};
      T('krTitle').textContent=parts.join(' · ');
      T('krAdvice').textContent='Przymierz look na sobie w kamerze i pokaż go barberowi w Grizzly — dopniemy detale pod Twój typ włosów i zarost.';
      T('krServices').innerHTML=svc.map(function(x){return '<div class="kserv"><span>'+x[0]+'</span><b>'+x[1]+'</b></div>';}).join('');
      T('krPrice').textContent=price+' zł';
    }

    /* camera */
    var camOn=document.getElementById('krCamOn'),camOff=document.getElementById('krCamOff'),
        snap=document.getElementById('krSnap'),scale=document.getElementById('krScale');
    function startCam(){
      if(!navigator.mediaDevices||!navigator.mediaDevices.getUserMedia){alert('Kamera niedostępna w tej przeglądarce.');return;}
      navigator.mediaDevices.getUserMedia({video:{facingMode:'user'},audio:false}).then(function(st){
        stream=st; vid.srcObject=st; var p=vid.play(); if(p&&p.catch)p.catch(function(){});
        stage.classList.add('cam');
        function manual(){ stage.classList.remove('ar'); ov.style.left='50%'; ov.style.top='14%'; ov.style.width=scale.value+'%'; ov.style.transform='translateX(-50%)'; }
        if(window.startGrizzlyCam){
          window.__hairMul=(scale.value/82);
          stage.classList.add('ar'); ov.style.transform='none';
          window.startGrizzlyCam(vid,ov,null,function(){ manual(); });
        } else { manual(); }
      }).catch(function(){ alert('Nie udało się włączyć kamery. Sprawdź uprawnienia (kłódka w pasku adresu).'); });
    }
    function stopCam(){ if(window.stopGrizzlyCam)window.stopGrizzlyCam(); if(stream){stream.getTracks().forEach(function(t){t.stop();});stream=null;} vid.srcObject=null; stage.classList.remove('cam'); stage.classList.remove('ar'); }
    if(camOn)camOn.addEventListener('click',startCam);
    if(camOff)camOff.addEventListener('click',stopCam);
    if(scale)scale.addEventListener('input',function(){ if(stage.classList.contains('ar')){window.__hairMul=scale.value/82;} else {ov.style.width=scale.value+'%';} });

    /* drag overlay */
    (function(){
      var drag=false,ox=0,oy=0,sl=50,st=14;
      function down(e){if(stage.classList.contains('ar'))return;drag=true;var p=e.touches?e.touches[0]:e;ox=p.clientX;oy=p.clientY;sl=parseFloat(ov.style.left)||50;st=parseFloat(ov.style.top)||14;ov.style.transform='none';if(e.cancelable)e.preventDefault();}
      function move(e){if(!drag)return;var p=e.touches?e.touches[0]:e;var r=stage.getBoundingClientRect();
        ov.style.left=Math.max(2,Math.min(98,sl+((p.clientX-ox)/r.width*100)))+'%';
        ov.style.top=Math.max(0,Math.min(78,st+((p.clientY-oy)/r.height*100)))+'%';}
      function up(){drag=false;}
      ov.addEventListener('mousedown',down); window.addEventListener('mousemove',move); window.addEventListener('mouseup',up);
      ov.addEventListener('touchstart',down,{passive:false}); window.addEventListener('touchmove',move,{passive:false}); window.addEventListener('touchend',up);
    })();

    /* snapshot */
    if(snap)snap.addEventListener('click',function(){
      if(!stream){alert('Najpierw włącz kamerę.');return;}
      try{
        var r=stage.getBoundingClientRect(),c=document.createElement('canvas');
        c.width=Math.round(r.width);c.height=Math.round(r.height);var cx=c.getContext('2d');
        var vw=vid.videoWidth||c.width,vh=vid.videoHeight||c.height,sc=Math.max(c.width/vw,c.height/vh);
        cx.save();cx.translate(c.width,0);cx.scale(-1,1);
        cx.drawImage(vid,(c.width-vw*sc)/2,(c.height-vh*sc)/2,vw*sc,vh*sc);cx.restore();
        var svgStr=new XMLSerializer().serializeToString(hair);
        var im=new Image();
        im.onload=function(){ cx.drawImage(im,ov.offsetLeft,ov.offsetTop,ov.offsetWidth,ov.offsetHeight);
          var a=document.createElement('a');a.download='grizzly-look.png';a.href=c.toDataURL('image/png');a.click(); };
        im.onerror=function(){alert('Nie udało się zapisać zdjęcia.');};
        im.src='data:image/svg+xml;charset=utf-8,'+encodeURIComponent(svgStr);
      }catch(err){alert('Nie udało się zapisać zdjęcia.');}
    });

    kRender(); kResult();
  }

  /* ---------- init ---------- */
  var start=saved||'pl';   // Polish is the default language
  buildCalc();
  setLang(start);
})();
