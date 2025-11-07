from dataclasses import asdict

from sqlalchemy import select

from fastapi_zero.models import User


def test_create_user(session, mock_db_time):
    with mock_db_time(model=User) as time:
        user = User(
            username='joao', email='email@email.com', password='password123'
        )
        session.add(user)
        session.commit()

        user_in_db = session.scalar(
            select(User).where(User.username == 'joao')
        )

    assert asdict(user_in_db) == {
        'id': 1,
        'username': 'joao',
        'email': 'email@email.com',
        'password': 'password123',
        'created_at': time,
    }
