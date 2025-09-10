import random
from datetime import datetime, timedelta, timezone

import click
from flask.cli import with_appcontext

from app import db
from app.models import Post, User


@click.command("seed-db")
@with_appcontext
def seed_db_command():
    """Seed the database with sample data."""
    # First flush existing data
    db.session.query(Post).delete()
    db.session.query(User).delete()
    db.session.commit()

    # Create users
    users = []
    for i in range(50):
        user = User(username=f"user{i}", email=f"user{i}@example.com")
        user.set_password(f"password{i}")
        db.session.add(user)

    # Commit users first to get IDs assigned
    db.session.commit()

    # Reload the users from database
    users = User.query.all()

    # Create posts
    now = datetime.now(timezone.utc)
    for i in range(100):
        post_time = now - timedelta(days=random.randint(0, 30))
        post = Post(
            body=f"This is test post #{i} with some content.",
            author=random.choice(users),
            timestamp=post_time,
        )
        db.session.add(post)

    # Create posts
    now = datetime.now(timezone.utc)
    for i in range(100):
        post_time = now - timedelta(days=random.randint(0, 30))
        post = Post(
            body=f"This is test post #{i} with some content.",
            author=random.choice(users),
            timestamp=post_time,
        )
        db.session.add(post)

    # Create follow relationships
    for user in users:
        # Get all other users by ID comparison
        potential_follows = [u for u in users if u.id != user.id]
        num_to_follow = random.randint(0, len(potential_follows))
        to_follow = random.sample(potential_follows, num_to_follow)

        for other in to_follow:
            user.follow(other)

    db.session.commit()
    print(f"Created {len(users)} users with {len(Post.query.all())} posts")
    # print(f"Added {sum(len(u.following) for u in users)} follow relationships")


# Register with Flask app in __init__.py or app factory
def init_app(app):
    app.cli.add_command(seed_db_command)
