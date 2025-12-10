from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)  

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mindease.db'
app.config['JWT_SECRET_KEY'] = 'mindease_secret_key'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    role = db.Column(db.String(50), nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

class MoodEntry(db.Model):
    entry_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    mood = db.Column(db.String(50), nullable=False)
    date_logged = db.Column(db.DateTime, default=datetime.utcnow)

class Forum(db.Model):
    forum_id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    forum_role = db.Column(db.String(50))
    content = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# Routes
@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()

    # Validate fields
    if not all(k in data for k in ('name', 'email', 'password', 'role')):
        return jsonify(error="Missing required fields"), 400

    # Check duplicate email
    if User.query.filter_by(email=data['email']).first():
        return jsonify(error="Email already registered"), 409

    hashed_pw = bcrypt.generate_password_hash(data['password']).decode('utf-8')

    user = User(
        name=data['name'],
        email=data['email'],
        role=data['role'],
        password_hash=hashed_pw
    )

    db.session.add(user)
    db.session.commit()

    return jsonify(message="User registered successfully"), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()

    user = User.query.filter_by(email=data['email']).first()

    if user and user.check_password(data['password']):
        token = create_access_token(identity=user.user_id)
        return jsonify(token=token, user_id=user.user_id, role=user.role), 200

    return jsonify(error="Invalid credentials"), 401

@app.route('/api/moods', methods=['POST'])
def create_mood():
    data = request.get_json()

    if not all(k in data for k in ('user_id', 'mood')):
        return jsonify(error="Missing required fields"), 400

    mood = MoodEntry(user_id=data['user_id'], mood=data['mood'])
    db.session.add(mood)
    db.session.commit()

    return jsonify(message="Mood entry added successfully"), 201

@app.route('/api/moods', methods=['GET'])
def list_moods():
    moods = MoodEntry.query.all()
    result = [
        {
            "entry_id": m.entry_id,
            "user_id": m.user_id,
            "mood": m.mood,
            "date_logged": m.date_logged
        }
        for m in moods
    ]
    return jsonify(result), 200

@app.route('/api/forum', methods=['POST'])
def create_forum_post():
    data = request.get_json()

    if not all(k in data for k in ('sender_id', 'forum_role', 'content')):
        return jsonify(error="Missing required fields"), 400

    post = Forum(
        sender_id=data['sender_id'],
        forum_role=data['forum_role'],
        content=data['content']
    )

    db.session.add(post)
    db.session.commit()

    return jsonify(message="Forum post created successfully"), 201

@app.route('/api/forum', methods=['GET'])
def get_forum_posts():
    posts = Forum.query.all()

    result = [
        {
            "forum_id": p.forum_id,
            "sender_id": p.sender_id,
            "forum_role": p.forum_role,
            "content": p.content,
            "timestamp": p.timestamp
        }
        for p in posts
    ]
    return jsonify(result), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  
    app.run(debug=True)
