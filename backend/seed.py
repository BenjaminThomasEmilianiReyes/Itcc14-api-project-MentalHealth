from app import app, db, User, MoodEntry, Forum, bcrypt

with app.app_context():
    db.create_all()
    # Create test student user (idempotent)
    student = User.query.filter_by(username="demostudent").first()
    if not student:
        student = User(
            username="demostudent",
            name="Demo Student",
            email="demo@my.xu.edu.ph",
            role="student",
            password_hash=bcrypt.generate_password_hash("password123").decode('utf-8')
        )
        db.session.add(student)
        db.session.commit()

    # Create test counselor user (idempotent)
    counselor = User.query.filter_by(username="democounselor").first()
    if not counselor:
        counselor = User(
            username="democounselor",
            name="Demo Counselor",
            email="counselor@xu.edu.ph",
            role="counselor",
            password_hash=bcrypt.generate_password_hash("password123").decode('utf-8')
        )
        db.session.add(counselor)
        db.session.commit()

    # Add sample mood entry if missing
    existing_mood = MoodEntry.query.filter_by(user_id=student.user_id, mood_text="Feeling better today!").first()
    if not existing_mood:
        mood = MoodEntry(
            user_id=student.user_id,
            mood="happy",
            mood_emoji="😊",
            mood_text="Feeling better today!"
        )
        db.session.add(mood)

    # Add sample forum post if missing
    existing_post = Forum.query.filter_by(sender_id=student.user_id, content="Feeling better today!").first()
    if not existing_post:
        post = Forum(
            sender_id=student.user_id,
            forum_role="student",
            content="Feeling better today!"
        )
        db.session.add(post)

    db.session.commit()
    print("Seed data ensured (idempotent).")
    print(f"Student user: username=demostudent, password=password123")
    print(f"Counselor user: username=democounselor, password=password123")
