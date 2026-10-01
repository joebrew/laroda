(function(){
document.querySelectorAll('a[data-lang]').forEach(function(a){a.addEventListener('click',function(){try{localStorage.setItem('laroda-lang',a.dataset.lang)}catch(e){}})});
var c=document.getElementById('carousel');if(!c)return;
var s=c.querySelectorAll('.slide'),dots=document.getElementById('dots'),
    count=document.getElementById('count'),i=0,timer,pad=function(n){return (n<10?'0':'')+n};
s.forEach(function(_,n){var b=document.createElement('button');b.setAttribute('aria-label',(c.dataset.photo||'Photo')+' '+(n+1));b.onclick=function(){go(n);restart()};dots.appendChild(b)});
var d=dots.querySelectorAll('button');
function go(n){s[i].classList.remove('on');d[i].removeAttribute('aria-current');i=(n+s.length)%s.length;s[i].classList.add('on');d[i].setAttribute('aria-current','true');count.textContent=pad(i+1)+' / '+pad(s.length)}
function restart(){clearInterval(timer);if(!matchMedia('(prefers-reduced-motion: reduce)').matches)timer=setInterval(function(){go(i+1)},5000)}
c.querySelector('.prev').onclick=function(){go(i-1);restart()};
c.querySelector('.next').onclick=function(){go(i+1);restart()};
c.addEventListener('mouseenter',function(){clearInterval(timer)});
c.addEventListener('mouseleave',restart);
document.addEventListener('keydown',function(e){if(e.key==='ArrowLeft'){go(i-1);restart()}if(e.key==='ArrowRight'){go(i+1);restart()}});
go(0);restart();
})();
