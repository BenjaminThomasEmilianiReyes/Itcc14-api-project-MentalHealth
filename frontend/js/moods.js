const API_M = "http://127.0.0.1:5000/api";

let selectedMood = null;

// Hook up mood buttons
document.addEventListener('click', (e) => {
  if (e.target?.classList?.contains('mood-btn')) {
    document.querySelectorAll('.mood-btn').forEach(b => b.classList.remove('selected'));
    e.target.classList.add('selected');
    selectedMood = e.target.getAttribute('data-mood');
    document.getElementById('moodText').value = selectedMood;
  }
});

async function submitMood() {
  const mood = document.getElementById('moodText').value;
  const userId = sessionStorage.getItem('mindease_user_id');
  if (!userId) { document.getElementById('mood-msg').innerText = 'Please login first'; return; }
  if (!mood) { document.getElementById('mood-msg').innerText = 'Select a mood'; return; }
  const token = sessionStorage.getItem('mindease_token');
  if (!token) { window.location.href = 'index.html'; return; }

  const res = await fetch(`${API_M}/moods`, {
    method: 'POST',
    headers: { 
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify({ user_id: Number(userId), mood })
  });

  if (res.status === 401 || res.status === 422) {
    // Token missing/invalid — redirect to login
    window.location.href = 'index.html';
    return;
  }

  let data = {};
  try { data = await res.json(); } catch (e) { data = {}; }
  document.getElementById('mood-msg').innerText = data.message || data.error || (res.ok ? 'Success' : 'Request failed');
  if (res.ok) loadMoods();
}

async function approveMood(entryId) {
  const token = sessionStorage.getItem('mindease_token');
  if (!token) { window.location.href = 'index.html'; return; }
  const res = await fetch(`${API_M}/moods/${entryId}/approve`, {
    method: 'POST',
    headers: { 'Authorization': `Bearer ${token}` }
  });

  if (res.status === 401 || res.status === 422) { window.location.href = 'index.html'; return; }
  let data = {};
  try { data = await res.json(); } catch (e) { data = {}; }
  alert(data.message || data.error || (res.ok ? 'Approved' : 'Request failed'));
  loadMoods();
}

async function loadMoods() {
  const token = sessionStorage.getItem('mindease_token');
  const role = sessionStorage.getItem('mindease_user_role');
  // If counselor, we fetch all moods
  const url = `${API_M}/moods`;
  const res = await fetch(url, { headers: { 'Authorization': `Bearer ${token}` } });
  if (res.status === 401 || res.status === 422) { window.location.href = 'index.html'; return; }
  const list = await res.json();
  const out = document.getElementById('moodList');
  out.innerHTML = '';
  if (!Array.isArray(list)) { out.innerText = JSON.stringify(list); return; }
  list.forEach(m => {
    const row = document.createElement('div');
    row.className = 'mood-row';
    const approvedText = m.approved ? '✅' : '⏳';
    const userName = m.username || `User #${m.user_id}`;
    let html = `<p><strong>${m.mood_emoji || m.mood}</strong> — <small>${new Date(m.date_logged).toLocaleString()}</small> by <em>${userName}</em> ${approvedText}</p>`;
    row.innerHTML = html;
    if (role === 'counselor') {
      // show approve button for unapproved moods
      if (!m.approved) {
        const btn = document.createElement('button');
        btn.innerText = 'Approve';
        btn.addEventListener('click', () => approveMood(m.entry_id));
        row.appendChild(btn);
      }
    }
    out.appendChild(row);
  });
}

document.getElementById('submitMood')?.addEventListener('click', submitMood);
document.getElementById('loadMoods')?.addEventListener('click', loadMoods);

window.addEventListener('load', () => {
  if (!sessionStorage.getItem('mindease_user_id')) {
    window.location.href = 'index.html';
  }
  loadMoods();
});
