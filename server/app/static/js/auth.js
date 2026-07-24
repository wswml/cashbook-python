/* 认证 — 珍智账 */
function toast(msg,t){const el=document.getElementById('toast');if(el){el.textContent=msg;el.className='toast '+(t||'info')+' show';setTimeout(()=>el.classList.remove('show'),2500);}}

document.getElementById('loginForm')?.addEventListener('submit', async e => {
    e.preventDefault();
    const u=document.getElementById('username').value, p=document.getElementById('password').value;
    const rm=document.getElementById('rememberMe')?.checked||false, err=document.getElementById('errorMsg');
    try {
        const r=await fetch('/api/auth/login',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({username:u,password:p})});
        const d=await r.json();
        if(d.code===200){
            if(rm){localStorage.setItem('token',d.data.access_token);localStorage.setItem('user',JSON.stringify(d.data.user));localStorage.setItem('rememberMe','true');}
            else{sessionStorage.setItem('token',d.data.access_token);sessionStorage.setItem('user',JSON.stringify(d.data.user));localStorage.removeItem('rememberMe');}
            window.location.href='/';
        } else { err.textContent=d.message; err.style.display='block'; }
    } catch(e) { err.textContent='网络错误'; err.style.display='block'; }
});

document.getElementById('registerForm')?.addEventListener('submit', async e => {
    e.preventDefault();
    const u=document.getElementById('username').value, n=document.getElementById('name').value, p=document.getElementById('password').value, p2=document.getElementById('password2').value, err=document.getElementById('errorMsg');
    if(p!==p2){err.textContent='两次密码不一致';err.style.display='block';return;}
    try {
        const r=await fetch('/api/auth/register',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({username:u,password:p,name:n})});
        const d=await r.json();
        if(d.code===200){toast('注册成功 ✨','success');setTimeout(()=>window.location.href='/login',800);}
        else{err.textContent=d.message;err.style.display='block';}
    } catch(e) { err.textContent='网络错误'; err.style.display='block'; }
});
