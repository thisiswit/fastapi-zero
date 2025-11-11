from http import HTTPStatus

from fastapi_zero.schemas import UserPublic


def test_root_deve_retornar_ok_e_ola_mundo(client):
    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Olá Mundo!'}


def test_create_user(client):
    response = client.post(
        '/users/',
        json={
            'username': 'Alice',
            'email': 'alice@email.com',
            'password': 'securepassword',
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'username': 'Alice',
        'email': 'alice@email.com',
    }


def test_read_users(client):
    response = client.get('/users')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_read_users_with_users(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/')
    assert response.json() == {'users': [user_schema]}


def test_update_user(client, user):
    response = client.put(
        '/users/1',
        json={
            'username': 'bob',
            'email': 'bob@example.com',
            'password': 'mynewpassword',
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'bob',
        'email': 'bob@example.com',
        'id': 1,
    }


def test_delete_user(client, user):
    response = client.delete('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted successfully'}


def test_update_user_inexistente_deve_retornar_404_not_found(client):
    response = client.put(
        '/users/999',
        json={
            'username': 'Ana',
            'email': 'ana@email.com',
            'password': 'passwordd',
        },
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {
        'detail': 'User not found',
    }


def test_delete_user_inexistente_deve_retornar_404_not_found(client):
    response = client.delete('/users/999')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {
        'detail': 'User not found',
    }


def test_update_integrity_error(client, user):
    client.post(
        '/users/',
        json={
            'username': 'fausto',
            'email': 'fausto@exemple.com',
            'password': 'secret',
        },
    )

    response = client.put(
        f'/users/{user.id}',
        json={
            'username': 'fausto',
            'email': 'bob@exemple.com',
            'password': 'mynewpassword',
        },
    )
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {
        'detail': 'Username or Email already exists',
    }


# def test_create_user_should_return_409_username_exists__exercicio(
#         client, user):
#     response = client.post(
#         '/users/',
#         json={
#             'username': user.username,
#             'email': 'alice@example.com',
#             'password': 'secret',
#         },
#     )
#     assert response.status_code == HTTPStatus.CONFLICT
#     assert response.json() == {'detail': 'Username already exists'}


def test_create_user_should_return_409_email_exists__exercicio(client, user):
    response = client.post(
        '/users/',
        json={
            'username': 'alice',
            'email': user.email,
            'password': 'secret',
        },
    )
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Email already exists!'}


def test_delete_user_should_return_not_found(client):
    response = client.delete('/users/666')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_update_user_should_return_not_found(client):
    response = client.put(
        '/users/666',
        json={
            'username': 'bob',
            'email': 'bob@example.com',
            'password': 'mynewpassword',
        },
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_get_user_should_return_not_found(client):
    response = client.get('/users/666')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_get_user(client, user):
    response = client.get(f'/users/{user.id}')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': user.username,
        'email': user.email,
        'id': user.id,
    }
