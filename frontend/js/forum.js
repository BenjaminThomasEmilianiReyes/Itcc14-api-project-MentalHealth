const API_F = "http://127.0.0.1:5000/api";

async function submitPost() {
  const content = document.getElementById('forumContent').value;
  const senderId = sessionStorage.getItem('mindease_user_id');
  if (!senderId) { document.getElementById('forum-msg').innerText = 'Please login first'; return; }
  if (!content) { document.getElementById('forum-msg').innerText = 'Write something'; return; }

  const token = sessionStorage.getItem('mindease_token');
  if (!token) { window.location.href = 'index.html'; return; }
  const res = await fetch(`${API_F}/forum`, {
    method: 'POST',
    headers: { 
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify({ content })
  });

  if (res.status === 401 || res.status === 422) { window.location.href = 'index.html'; return; }
  let data = {};
  try { data = await res.json(); } catch (e) { data = {}; }
  document.getElementById('forum-msg').innerText = data.message || data.error || (res.ok ? 'Posted' : 'Request failed');
  loadPosts();
}

async function replyToPost(forumId, textarea) {
  const content = textarea.value;
  if (!content) { alert('Write a reply'); return; }
  const token = sessionStorage.getItem('mindease_token');
  if (!token) { window.location.href = 'index.html'; return; }
  const res = await fetch(`${API_F}/forum/${forumId}/reply`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
    body: JSON.stringify({ content })
  });

  if (res.status === 401 || res.status === 422) { window.location.href = 'index.html'; return; }
  let data = {};
  try { data = await res.json(); } catch (e) { data = {}; }
  alert(data.message || data.error || (res.ok ? 'Reply posted' : 'Request failed'));
  loadPosts();
}

async function loadPosts() {
  const token = sessionStorage.getItem('mindease_token');
  const role = sessionStorage.getItem('mindease_user_role');
  const res = await fetch(`${API_F}/forum`, {
    headers: { 'Authorization': `Bearer ${token}` }
  });
  if (res.status === 401 || res.status === 422) { window.location.href = 'index.html'; return; }
  const posts = await res.json();
  const out = document.getElementById('postList');
  out.innerHTML = '';
  if (!Array.isArray(posts)) { out.innerText = JSON.stringify(posts); return; }
  posts.reverse().forEach(p => {
    const div = document.createElement('div');
    const userName = p.username || `User #${p.sender_id}`;
    div.innerHTML = `<p><strong>${userName}</strong> (${p.forum_role}) — ${p.content}<br><small>${new Date(p.timestamp).toLocaleString()}</small></p>`;
    // If counselor, add reply UI under each post
    if (role === 'counselor') {
      const ta = document.createElement('textarea');
      ta.placeholder = 'Write a reply...';
      const btn = document.createElement('button');
      btn.innerText = 'Reply';
      btn.addEventListener('click', () => replyToPost(p.forum_id, ta));
      div.appendChild(ta);
      div.appendChild(btn);
    }
    out.appendChild(div);
  });
}

document.getElementById('postForum')?.addEventListener('click', submitPost);
document.getElementById('loadPosts')?.addEventListener('click', loadPosts);

window.addEventListener('load', () => {
  if (!sessionStorage.getItem('mindease_user_id')) {
    window.location.href = 'index.html';
  }
  loadPosts();
});
