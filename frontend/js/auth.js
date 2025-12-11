const API = "http://127.0.0.1:5000/api";

// Profanity list for client-side validation (matches backend)
const PROFANITY_LIST = ["badword1", "badword2", "fu", "shit", "asshole", "bastard", "foulword"];

function checkProfanity(text) {
    if (!text) return false;
    const textLower = text.toLowerCase().replace(/[^a-z0-9]/g, ' ');
    for (const word of textLower.split(/\s+/)) {
        if (PROFANITY_LIST.includes(word)) {
            return true;
        }
    }
    return false;
}

// Function to handle login process
async function login() {
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    const statusMsg = document.getElementById("login-msg");

    const res = await fetch(`${API}/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password })
    });

    const data = await res.json();

    if (res.ok) {
        // Store session data in sessionStorage
        sessionStorage.setItem('mindease_token', data.token);
        sessionStorage.setItem('mindease_user_id', data.user_id);
        sessionStorage.setItem('mindease_user_role', data.role);
        sessionStorage.setItem('mindease_username', data.username);
        
        // Redirect to dashboard without adding a history entry (prevents back to login)
        window.location.replace('dashboard.html');
        
    } else {
        statusMsg.innerText = data.error;
    }
}

// Attach login function to the login button on the index/login page
// This assumes an element with id="loginBtn" exists and is calling this code
if (document.getElementById("loginBtn")) {
    document.getElementById("loginBtn").addEventListener('click', login);
}


// Function to handle registration process
async function register() {
    const username = document.getElementById("username").value;
    const name = document.getElementById("name").value;
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    const role = document.getElementById("role").value;
    const statusMsg = document.getElementById("reg-msg");

    if (!username || !name || !email || !password) {
        statusMsg.innerText = "All fields are required";
        return;
    }

    if (checkProfanity(username)) {
        statusMsg.innerText = "Username contains disallowed language";
        return;
    }

    const res = await fetch(`${API}/register`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, name, email, password, role })
    });

    const data = await res.json();

    if (res.ok) {
        statusMsg.innerText = "Account created! Redirecting to login...";
        setTimeout(() => {
            window.location.replace('index.html');
        }, 1200);
    } else {
        statusMsg.innerText = data.error || "Registration failed";
    }
}

// Attach register function to the register button on the register page
if (document.getElementById("registerBtn")) {
    document.getElementById("registerBtn").addEventListener('click', register);
}


// --- Functions below need the token for authorization headers ---

// Helper function to get token and set auth header
function getAuthHeaders() {
    const token = sessionStorage.getItem('mindease_token');
    return {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}`
    };
}


async function createMood() {
    const userId = sessionStorage.getItem('mindease_user_id');
    const mood = document.getElementById("mood").value;

    const res = await fetch(`${API}/moods`, {
        method: "POST",
        headers: getAuthHeaders(),
        body: JSON.stringify({ user_id: parseInt(userId), mood })
    });

    const data = await res.json();
    document.getElementById("mood-status").innerText = data.message || data.error;
}

async function loadMoods() {
    // Requires authorization header now
    const res = await fetch(`${API}/moods`, {
        headers: { "Authorization": `Bearer ${sessionStorage.getItem('mindease_token')}` }
    });
    const moods = await res.json();

    const list = document.getElementById("mood-list");
    list.innerHTML = "";

    moods.forEach(m => {
        list.innerHTML += `<p><strong>${m.mood}</strong> - ${m.date_logged} (Approved: ${m.approved})</p>`;
    });
}

async function createForumPost() {
    const content = document.getElementById("forum-content").value;

    // The backend now gets sender_id and forum_role from the JWT token,
    // so we only need to send the content.
    const res = await fetch(`${API}/forum`, {
        method: "POST",
        headers: getAuthHeaders(),
        body: JSON.stringify({ content })
    });

    const data = await res.json();
    document.getElementById("forum-status").innerText = data.message || data.error;
}

async function loadForum() {
    // Assumed endpoint exists now (GET /api/forum)
    const res = await fetch(`${API}/forum`, {
        headers: { "Authorization": `Bearer ${sessionStorage.getItem('mindease_token')}` }
    }); 
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
