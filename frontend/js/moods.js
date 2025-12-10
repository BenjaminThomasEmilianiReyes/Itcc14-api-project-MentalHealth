const API_M = "http://127.0.0.1:5000/api";

async function submitMood() {
  const mood = document.getElementById('moodText').value;
  const userId = localStorage.getItem('mindease_user_id');
  if (!userId) { document.getElementById('mood-msg').innerText = 'Please login first'; return; }
  if (!mood) { document.getElementById('mood-msg').innerText = 'Type your mood'; return; }

  const res = await fetch(`${API_M}/moods`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ user_id: Number(userId), mood })
  });
  const data = await res.json();
  document.getElementById('mood-msg').innerText = data.message || data.error;
}

async function loadMoods() {
  const res = await fetch(`${API_M}/moods`);
  const list = await res.json();
  const out = document.getElementById('moodList');
  out.innerHTML = '';
  if (!Array.isArray(list)) { out.innerText = JSON.stringify(list); return; }
  list.reverse().forEach(m => {
    const p = document.createElement('p');
    p.innerHTML = `<strong>${m.mood}</strong> — <small>${new Date(m.date_logged).toLocaleString()}</small>`;
    out.appendChild(p);
  });
}

document.getElementById('submitMood')?.addEventListener('click', submitMood);
document.getElementById('loadMoods')?.addEventListener('click', loadMoods);

window.addEventListener('load', () => {
  if (!localStorage.getItem('mindease_user_id')) {
    window.location.href = 'index.html';
  }
  loadMoods();
});
