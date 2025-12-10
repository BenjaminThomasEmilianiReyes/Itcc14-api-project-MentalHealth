const API_F = "http://127.0.0.1:5000/api";

async function submitPost() {
  const content = document.getElementById('forumContent').value;
  const senderId = localStorage.getItem('mindease_user_id');
  if (!senderId) { document.getElementById('forum-msg').innerText = 'Please login first'; return; }
  if (!content) { document.getElementById('forum-msg').innerText = 'Write something'; return; }

  const res = await fetch(`${API_F}/forum`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ sender_id: Number(senderId), forum_role: 'student', content })
  });
  const data = await res.json();
  document.getElementById('forum-msg').innerText = data.message || data.error;
  loadPosts();
}

async function loadPosts() {
  const res = await fetch(`${API_F}/forum`);
  const posts = await res.json();
  const out = document.getElementById('postList');
  out.innerHTML = '';
  if (!Array.isArray(posts)) { out.innerText = JSON.stringify(posts); return; }
  posts.reverse().forEach(p => {
    const div = document.createElement('div');
    div.innerHTML = `<p><strong>${p.forum_role}</strong> — ${p.content}<br><small>${new Date(p.timestamp).toLocaleString()}</small></p>`;
    out.appendChild(div);
  });
}

document.getElementById('postForum')?.addEventListener('click', submitPost);
document.getElementById('loadPosts')?.addEventListener('click', loadPosts);

window.addEventListener('load', () => {
  if (!localStorage.getItem('mindease_user_id')) {
    window.location.href = 'index.html';
  }
  loadPosts();
});
