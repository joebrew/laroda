(function(){
document.querySelectorAll('a[data-lang]').forEach(function(a){a.addEventListener('click',function(){try{localStorage.setItem('laroda-lang',a.dataset.lang)}catch(e){}})});
var c=document.getElementById('carousel');if(!c)return;
var s=c.querySelectorAll('.slide'),dots=document.getElementById('dots'),
    count=document.getElementById('count'),i=0,timer,hover=false,focus=false,
    paused=matchMedia('(prefers-reduced-motion: reduce)').matches,
    pad=function(n){return (n<10?'0':'')+n};
s.forEach(function(_,n){var b=document.createElement('button');b.type='button';b.setAttribute('aria-label',(c.dataset.photo||'Photo')+' '+(n+1));b.onclick=function(){go(n);tick()};dots.appendChild(b)});
var d=dots.querySelectorAll('button');
var pause=document.createElement('button');pause.type='button';pause.className='pause';
count.parentNode.insertBefore(pause,count.nextSibling);
function go(n){s[i].classList.remove('on');d[i].removeAttribute('aria-current');i=(n+s.length)%s.length;s[i].classList.add('on');d[i].setAttribute('aria-current','true');count.textContent=pad(i+1)+' / '+pad(s.length)}
// Auto-advance only while the user hasn't paused it and isn't hovering over or focused on the photos.
function tick(){clearInterval(timer);if(!paused&&!hover&&!focus)timer=setInterval(function(){go(i+1)},5000)}
function setPaused(p){paused=p;pause.textContent=p?(c.dataset.play||'Play'):(c.dataset.pause||'Pause');tick()}
pause.onclick=function(){setPaused(!paused)};
c.querySelector('.prev').onclick=function(){go(i-1);tick()};
c.querySelector('.next').onclick=function(){go(i+1);tick()};
c.addEventListener('mouseenter',function(){hover=true;tick()});
c.addEventListener('mouseleave',function(){hover=false;tick()});
[c,dots].forEach(function(el){
  el.addEventListener('focusin',function(){focus=true;tick()});
  el.addEventListener('focusout',function(e){if(!c.contains(e.relatedTarget)&&!dots.contains(e.relatedTarget)){focus=false;tick()}});
  el.addEventListener('keydown',function(e){if(e.key==='ArrowLeft'){go(i-1);tick()}if(e.key==='ArrowRight'){go(i+1);tick()}});
});
go(0);setPaused(paused);
})();
