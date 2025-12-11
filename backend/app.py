import os
from flask import Flask, request, jsonify, make_response, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt
from flask_cors import CORS
from datetime import datetime
import re

basedir = os.path.abspath(os.path.dirname(__file__))
frontend_dir = os.path.abspath(os.path.join(basedir, '..', 'frontend'))

app = Flask(__name__, static_folder=frontend_dir, static_url_path='')
CORS(app)

basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'instance', 'mindease.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'

app.config['JWT_SECRET_KEY'] = 'mindease_secret_key'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# JWT error handlers: return consistent JSON and HTTP codes for common token issues
@jwt.unauthorized_loader
def missing_token_callback(error_string):
    print(f"DEBUG: unauthorized_loader called with: {error_string}")
    return jsonify(error="Missing or malformed Authorization header"), 401

@jwt.invalid_token_loader
def invalid_token_callback(error_string):
    print(f"DEBUG: invalid_token_loader called with: {error_string}")
    return jsonify(error="Invalid token"), 422

@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    print(f"DEBUG: expired_token_loader called")
    return jsonify(error="Token has expired"), 401

@jwt.revoked_token_loader
def revoked_token_callback(jwt_header, jwt_payload):
    print(f"DEBUG: revoked_token_loader called")
    return jsonify(error="Token has been revoked"), 401

@jwt.needs_fresh_token_loader
def needs_fresh_token_callback(jwt_header, jwt_payload):
    print(f"DEBUG: needs_fresh_token_loader called")
    return jsonify(error="Fresh token required"), 401

# Optional: convert generic 422 responses to JSON so frontend can handle them
@app.errorhandler(422)
def handle_unprocessable_entity(err):
    return jsonify(error=getattr(err, 'description', 'Unprocessable Entity')), 422

PROFANITY = {
    "badword1", "badword2", "fu", "shit", "asshole", "bastard", "foulword" 
}

def has_profanity(text: str) -> bool:
    if not text:
        return False
    text_lower = re.sub(r'[^a-z0-9]', ' ', text.lower())
    for token in text_lower.split():
        if token in PROFANITY:
            return True
    return False

ALLOWED_MOODS = {
    "happy": "😊",
    "sad": "😢",
    "angry": "😡",
    "neutral": "😐",
    "anxious": "😰",
    "excited": "🤩"
}

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    role = db.Column(db.String(50), nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

class MoodEntry(db.Model):
    entry_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    mood = db.Column(db.String(50), nullable=False)
    mood_emoji = db.Column(db.String(10), nullable=False)
    mood_text = db.Column(db.String(200), nullable=True)
    approved = db.Column(db.Boolean, default=False) 
    date_logged = db.Column(db.DateTime, default=datetime.utcnow)

class Forum(db.Model):
    forum_id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    forum_role = db.Column(db.String(50))
    content = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class ForumReply(db.Model):
    __tablename__ = 'forum_replies'
    reply_id = db.Column(db.Integer, primary_key=True)
    forum_id = db.Column(db.Integer, db.ForeignKey('forum.forum_id'), nullable=False)
    replier_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

def add_no_cache_headers(resp):
    resp.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    resp.headers["Pragma"] = "no-cache"
    resp.headers["Expires"] = "0"
    return resp

def validate_email_for_role(email: str, role: str) -> bool:
    if role == 'student':
        return email.lower().endswith('@my.xu.edu.ph')
    if role == 'counselor':
        return email.lower().endswith('@xu.edu.ph')
    return False

@app.route('/')
def serve_index():
    return send_from_directory(frontend_dir, 'index.html')

@app.route('/health')
def health_check():
    return jsonify(status="ok"), 200

@app.route('/<path:filename>')
def serve_static(filename):
    # Don't serve API routes through the static handler
    if filename.startswith('api/'):
        return jsonify(error="Not found"), 404
    
    # Try to serve the file from the frontend directory
    try:
        return send_from_directory(frontend_dir, filename)
    except FileNotFoundError:
        # If file doesn't exist, serve index.html for client-side routing
        return send_from_directory(frontend_dir, 'index.html')

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json() or {}

    required = ('username', 'name', 'email', 'password', 'role')
    if not all(k in data for k in required):
        return jsonify(error="Missing required fields"), 400

    username = data['username'].strip()
    email = data['email'].strip()
    role = data['role'].strip().lower()

    if has_profanity(username):
        return jsonify(error="Username contains disallowed language"), 400

    if User.query.filter_by(email=email).first():
        return jsonify(error="Email already registered"), 409

    if User.query.filter_by(username=username).first():
        return jsonify(error="Username already taken"), 409

    if not validate_email_for_role(email, role):
        return jsonify(error=f"Invalid email domain for role '{role}'"), 400

    hashed_pw = bcrypt.generate_password_hash(data['password']).decode('utf-8')

    user = User(
        username=username,
        name=data['name'],
        email=email,
        role=role,
        password_hash=hashed_pw
    )

    try:
        db.session.add(user)
        db.session.commit()
        return jsonify(message="User registered successfully"), 201
    except Exception as e:
        db.session.rollback()
        return jsonify(error="Registration failed. Please try again with different credentials."), 400

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json() or {}

    identifier = data.get('email') or data.get('username')
    if not identifier or not data.get('password'):
        return jsonify(error="Missing credentials"), 400

    user = User.query.filter((User.email == identifier) | (User.username == identifier)).first()

    if user and user.check_password(data['password']):
        token = create_access_token(identity=str(user.user_id), additional_claims={'user_id': user.user_id, 'role': user.role})
        # Added username to login response so frontend can display it easily
        return jsonify(token=token, user_id=user.user_id, role=user.role, username=user.username), 200

    return jsonify(error="Invalid credentials"), 401

@app.route('/api/moods', methods=['POST'])
@jwt_required()
def create_mood():
    claims = get_jwt()
    user_id_from_token = claims.get('user_id')
    payload = request.get_json() or {}

    user_id = payload.get('user_id')
    if not user_id or int(user_id) != int(user_id_from_token):
        return jsonify(error="You can only create moods for your own account"), 403

    mood_key = payload.get('mood')
    if not mood_key or mood_key not in ALLOWED_MOODS:
        return jsonify(error=f"Invalid mood. Allowed: {list(ALLOWED_MOODS.keys())}"), 400

    mood_text_data = payload.get('mood_text', None)
    mood = MoodEntry(
        user_id=user_id,
        mood=mood_key,
        mood_emoji=ALLOWED_MOODS[mood_key],
        mood_text=mood_text_data
    )
    db.session.add(mood)
    db.session.commit()

    return jsonify(message="Mood entry added successfully", mood_emoji=mood.mood_emoji), 201

@app.route('/api/moods', methods=['GET'])
@jwt_required()
def list_moods():
    claims = get_jwt()
    role = claims.get('role')

    if role == 'counselor':
        student_id = request.args.get('student_id')
        if student_id:
            moods = MoodEntry.query.filter_by(user_id=student_id).order_by(MoodEntry.date_logged.desc()).all()
        else:
            moods = MoodEntry.query.order_by(MoodEntry.date_logged.desc()).all()
    else:
        user_id = claims.get('user_id')
        moods = MoodEntry.query.filter_by(user_id=user_id).order_by(MoodEntry.date_logged.desc()).all()

    # Build user lookup dict to avoid N+1 queries
    user_ids = set(m.user_id for m in moods)
    users = {u.user_id: u for u in User.query.filter(User.user_id.in_(user_ids)).all()} if user_ids else {}

    result = [
        {
            "entry_id": m.entry_id,
            "user_id": m.user_id,
            "username": users.get(m.user_id, {}).username if m.user_id in users else "Unknown",
            "name": users.get(m.user_id, {}).name if m.user_id in users else "Unknown",
            "mood": m.mood,
            "mood_emoji": m.mood_emoji,
            "mood_text": m.mood_text,
            "approved": bool(m.approved),
            "date_logged": m.date_logged.isoformat()
        }
        for m in moods
    ]
    resp = make_response(jsonify(result), 200)
    return add_no_cache_headers(resp)

@app.route('/api/moods/<int:entry_id>/approve', methods=['POST'])
@jwt_required()
def approve_mood(entry_id):
    claims = get_jwt()
    role = claims.get('role')

    if role != 'counselor':
        return jsonify(error="Only counselors can approve moods"), 403

    mood = MoodEntry.query.get(entry_id)
    if not mood:
        return jsonify(error="Mood entry not found"), 404

    mood.approved = True
    db.session.commit()

    return jsonify(message="Mood approved"), 200

@app.route('/api/forum', methods=['GET'])
@jwt_required()
def list_forum_posts():
    # List all posts for all users
    posts = Forum.query.order_by(Forum.timestamp.desc()).all()
    
    # Build user lookup dict to avoid N+1 queries
    user_ids = set(p.sender_id for p in posts)
    users = {u.user_id: u for u in User.query.filter(User.user_id.in_(user_ids)).all()} if user_ids else {}

    result = [
        {
            "forum_id": p.forum_id,
            "sender_id": p.sender_id,
            "username": users.get(p.sender_id, {}).username if p.sender_id in users else "Unknown",
            "name": users.get(p.sender_id, {}).name if p.sender_id in users else "Unknown",
            "forum_role": p.forum_role,
            "content": p.content,
            "timestamp": p.timestamp.isoformat(),
            # Optional: Fetch replies for each post in a production environment, 
            # but for simplicity now, we just list posts.
        }
        for p in posts
    ]
    resp = make_response(jsonify(result), 200)
    return add_no_cache_headers(resp)


@app.route('/api/forum', methods=['POST'])
@jwt_required()
def create_forum_post():
    data = request.get_json() or {}
    claims = get_jwt()

    if not all(k in data for k in ('content',)):
        return jsonify(error="Missing required fields"), 400

    post = Forum(
        sender_id=claims.get('user_id'),
        forum_role=claims.get('role', 'student'),
        content=data['content']
    )
    db.session.add(post)
    db.session.commit()

    return jsonify(message="Forum post created successfully", forum_id=post.forum_id), 201


# --- NEW ENDPOINT FOR COUNSELOR REPLIES ---
@app.route('/api/forum/<int:forum_id>/reply', methods=['POST'])
@jwt_required()
def reply_to_forum_post(forum_id):
    data = request.get_json() or {}
    claims = get_jwt()
    role = claims.get('role')

    if role != 'counselor':
        return jsonify(error="Only counselors can reply to forum posts"), 403

    if not all(k in data for k in ('content',)):
        return jsonify(error="Missing required fields"), 400

    # Ensure the parent post exists
    post = Forum.query.get(forum_id)
    if not post:
        return jsonify(error="Forum post not found"), 404

    reply = ForumReply(
        forum_id=forum_id,
        replier_id=claims.get('user_id'),
        content=data['content']
    )
    db.session.add(reply)
    db.session.commit()

    return jsonify(message="Reply posted successfully", reply_id=reply.reply_id), 201


def create_database_tables():
    db.create_all()

if __name__ == '__main__':
    if not os.path.exists(os.path.join(basedir, 'instance')):
        os.makedirs(os.path.join(basedir, 'instance'))
        
    with app.app_context():
        create_database_tables()
        
    app.run(debug=True)
