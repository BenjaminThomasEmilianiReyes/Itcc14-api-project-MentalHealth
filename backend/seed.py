from mindease.app import db, User, MoodEntry, Forum, bcrypt

with db.app.app_context():
    db.create_all()

    user = User(
        name="Demo Student",
        email="demo@student.com",
        role="student",
        password_hash=bcrypt.generate_password_hash("12345").decode('utf-8')
    )
    db.session.add(user)
    db.session.commit()

    mood = MoodEntry(user_id=user.user_id, mood="Happy")
    db.session.add(mood)

    post = Forum(sender_id=user.user_id, forum_role="student", content="Feeling better today!")
    db.session.add(post)

    db.session.commit()
    print("Seed data added successfully!")
