"""
Test the different following functions
"""
# pylint: disable=redefined-outer-name
from datetime import datetime, timedelta
from app.models import User, Post
from app import db

def test_follow(test_app): # pylint: disable=unused-argument
    """
    Test that follow apends new users to followed
    Test that unfollow removes the user from followed
    """
    user1 = User(username='Derpy', email='derpy@st.com')
    user2 = User(username='Brian', email='brian.d@gmail.com')

    db.session.add(user1)
    db.session.add(user2)
    db.session.commit()

    assert user1.followed.all() == []

    user1.follow(user2)
    db.session.commit()

    assert user1.is_following(user2) is True
    assert user1.followed.count() == 1
    assert user1.followed.first().username == "Brian"
    assert user2.followers.count() == 1
    assert user2.followers.first().username == "Derpy"

    user1.unfollow(user2)
    db.session.commit()
    assert user1.is_following(user2) is not True
    assert user1.followed.count() == 0
    assert user1.followers.count() == 0

def test_follow_posts(test_app): # pylint: disable=unused-argument
    """
    Test that all personal and posts from followed users are shown.
    """
    # create four users
    user1 = User(username='Derpy', email='derpy@st.com')
    user2 = User(username='Brian', email='brian.d@gmail.com')
    user3 = User(username='Homage', email='homage@tpt.com')
    user4 = User(username='Gilda', email='gilda@gs.com')
    db.session.add_all([user1, user2, user3, user4])

    # create four posts
    now = datetime.utcnow()
    post1 = Post(body="post from Derpy", author=user1,
                 timestamp=now + timedelta(seconds=1))
    post2 = Post(body="post from Brian", author=user2,
                 timestamp=now + timedelta(seconds=4))
    post3 = Post(body="post from Homage", author=user3,
                 timestamp=now + timedelta(seconds=3))
    post4 = Post(body="post from Gilda", author=user4,
                 timestamp=now + timedelta(seconds=2))
    db.session.add_all([post1, post2, post3, post4])
    db.session.commit()

    # setup the followers
    user1.follow(user2)  # Derpy follows Brian
    user1.follow(user4)  # Derpy follows Gilda
    user2.follow(user3)  # Brian follows Homage
    user3.follow(user4)  # Homage follows Gilda
    db.session.commit()

    # check the followed posts of each user
    follow1 = user1.followed_posts().all()
    follow2 = user2.followed_posts().all()
    follow3 = user3.followed_posts().all()
    follow4 = user4.followed_posts().all()
    assert follow1 == [post2, post4, post1]
    assert follow2 == [post2, post3]
    assert follow3 == [post3, post4]
    assert follow4 == [post4]
