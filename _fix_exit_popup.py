"""Fix exit popup: disable on mobile, increase desktop engagement gate."""
import os
fpath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'index.html')
content = open(fpath).read()

old_js = """(function(){
  var shown = false; var modal = document.getElementById('exitOverlay');
  function show(){ if(shown) return; shown = true; modal.classList.add('show'); try{ sessionStorage.setItem('bb_exit_shown','1'); }catch(e){} }
  function hide(){ modal.classList.remove('show'); }
  try{ if(sessionStorage.getItem('bb_exit_shown') === '1') shown = true; }catch(e){}
  document.addEventListener('mouseout', function(e){ if(!e.relatedTarget && e.clientY < 10) show(); });
  var lastY = window.scrollY, lastT = Date.now(), engaged = false;
  setTimeout(function(){ engaged = true; }, 15000);
  window.addEventListener('scroll', function(){
    var y = window.scrollY, t = Date.now(); var dy = lastY - y, dt = t - lastT;
    if(engaged && dy > 160 && dt < 350 && y < 300) show();
    lastY = y; lastT = t;
  }, { passive: true });
  if(!shown){ history.pushState({exit:true}, ''); window.addEventListener('popstate', function(){ if(!shown){ show(); history.pushState({exit:true}, ''); } }); }
  document.getElementById('exitClose').addEventListener('click', hide);
  document.getElementById('exitNo').addEventListener('click', hide);
  modal.addEventListener('click', function(e){ if(e.target === modal) hide(); });
})();"""

new_js = """(function(){
  var isMobile = /iPhone|iPad|iPod|Android|Mobile|webOS|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
  var modal = document.getElementById('exitOverlay');
  if(!modal) return;
  var shown = false;
  function show(){ if(shown) return; shown = true; modal.classList.add('show'); try{ sessionStorage.setItem('bb_exit_shown','1'); }catch(e){} }
  function hide(){ modal.classList.remove('show'); }
  try{ if(sessionStorage.getItem('bb_exit_shown') === '1') shown = true; }catch(e){}

  // Mobile: NO exit intent. Touch devices don't have leave-page semantics. popstate fires erroneously on mobile.
  // Desktop: only mouseout-top-edge, requires 30s engagement first.
  if(!isMobile){
    var engaged = false;
    setTimeout(function(){ engaged = true; }, 30000);
    document.addEventListener('mouseout', function(e){
      if(engaged && !e.relatedTarget && e.clientY < 10) show();
    });
  }

  var c = document.getElementById('exitClose');
  if(c) c.addEventListener('click', hide);
  var n = document.getElementById('exitNo');
  if(n) n.addEventListener('click', hide);
  modal.addEventListener('click', function(e){ if(e.target === modal) hide(); });
})();"""

if old_js in content:
    content = content.replace(old_js, new_js, 1)
    open(fpath, 'w').write(content)
    print("FIX APPLIED: exit popup now mobile-aware (disabled on mobile)")
else:
    print("FAILED: original block not found exactly")

# Verify
final = open(fpath).read()
print(f"isMobile detection: {'isMobile' in final}")
print(f"popstate exit intent removed: {'popstate' not in final.split('exitOverlay')[1].split('redtrack')[0] if 'redtrack' in final.lower() else 'check manual'}")
print(f"30s engagement gate: {'30000' in final}")
print(f"15s engagement gate gone: {'15000' not in final or final.count('15000') == 0}")
