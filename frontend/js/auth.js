const API = "http://127.0.0.1:5000/api";

async function loginHandler() {
  const email = document.getElementById('email')?.value;
  const password = document.getElementById('password')?.value;
  if (!email || !password) { document.getElementById('login-msg').innerText = 'Fill fields'; return; }

  const res = await fetch(`${API}/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password })
  });
  const data = await res.json();
  if (res.ok) {
    localStorage.setItem('mindease_token', data.token || '');
    localStorage.setItem('mindease_user_id', data.user_id);
    localStorage.setItem('mindease_user_role', data.role || '');
    window.location.href = 'dashboard.html';
  } else {
    document.getElementById('login-msg').innerText = data.error || 'Login failed';
  }
}

async function registerHandler() {
  const name = document.getElementById('name')?.value;
  const email = document.getElementById('email')?.value;
  const password = document.getElementById('password')?.value;
  const role = document.getElementById('role')?.value || 'student';
  if (!name || !email || !password) { document.getElementById('reg-msg').innerText = 'Fill fields'; return; }

  const res = await fetch(`${API}/register`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ name, email, password, role })
  });
  const data = await res.json();
  if (res.status === 201) {
    document.getElementById('reg-msg').innerText = 'Registered. Redirecting to login...';
    setTimeout(()=> window.location.href = 'index.html', 900);
  } else {
    document.getElementById('reg-msg').innerText = data.error || 'Registration failed';
  }
}

document.getElementById('loginBtn')?.addEventListener('click', loginHandler);
document.getElementById('registerBtn')?.addEventListener('click', registerHandler);
