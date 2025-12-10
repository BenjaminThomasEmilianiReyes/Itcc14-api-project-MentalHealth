const API = "http://127.0.0.1:5000/api";

let userId = null;

async function login() {
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    const res = await fetch(`${API}/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password })
    });

    const data = await res.json();

    if (res.ok) {
        userId = data.user_id;
        document.getElementById("login-status").innerText = "Login successful!";
    } else {
        document.getElementById("login-status").innerText = data.error;
    }
}

async function createMood() {
    const mood = document.getElementById("mood").value;

    const res = await fetch(`${API}/moods`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user_id: userId, mood })
    });

    const data = await res.json();

    document.getElementById("mood-status").innerText = data.message || data.error;
}

async function loadMoods() {
    const res = await fetch(`${API}/moods`);
    const moods = await res.json();

    const list = document.getElementById("mood-list");
    list.innerHTML = "";

    moods.forEach(m => {
        list.innerHTML += `<p><strong>${m.mood}</strong> - ${m.date_logged}</p>`;
    });
}

async function createForumPost() {
    const content = document.getElementById("forum-content").value;

    const res = await fetch(`${API}/forum`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            sender_id: userId,
            forum_role: "student",
            content
        })
    });

    const data = await res.json();
    document.getElementById("forum-status").innerText = data.message || data.error;
}

async function loadForum() {
    const res = await fetch(`${API}/forum`);
    const posts = await res.json();

    const list = document.getElementById("forum-list");
    list.innerHTML = "";

    posts.forEach(p => {
        list.innerHTML += `
            <p>
                <strong>${p.forum_role}</strong>: ${p.content} 
                <br><small>${p.timestamp}</small>
            </p>`;
    });
}
