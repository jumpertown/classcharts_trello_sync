import os

CLASSCHARTS_USERNAME_ENV = 'CLASSCHARTS_USERNAME'
CLASSCHARTS_PASSWORD_ENV = 'CLASSCHARTS_PASSWORD'

TRELLO_API_KEY_ENV = 'TRELLO_API_KEY'
TRELLO_API_SECRET_ENV = 'TRELLO_API_SECRET'
TRELLO_OAUTH_TOKEN_ENV = 'TRELLO_OAUTH_TOKEN'
TRELLO_OAUTH_TOKEN_SECRET_ENV = 'TRELLO_OAUTH_TOKEN_SECRET'

STUDENT_PREFIX_ENV = 'STUDENT_'


def get_environment_config():
    """Set up a dictionary from the Classcharts environment variables."""
    config = {}

    config['classcharts_auth'] = {}
    config['classcharts_auth']['user'] = os.environ[CLASSCHARTS_USERNAME_ENV]
    config['classcharts_auth']['password'] = os.environ[CLASSCHARTS_PASSWORD_ENV]

    config['trello_auth'] = {}
    config['trello_auth']['api_key'] = os.environ[TRELLO_API_KEY_ENV]
    config['trello_auth']['api_secret'] = os.environ[TRELLO_API_SECRET_ENV]
    config['trello_auth']['oauth_token'] = os.environ[TRELLO_OAUTH_TOKEN_ENV]
    config['trello_auth']['oauth_token_secret'] = os.environ[TRELLO_OAUTH_TOKEN_SECRET_ENV]

    config['students'] = _parse_students()

    return config


def _parse_students():
    student_env = [
        os.environ[key]
        for key in os.environ.keys()
        if key.startswith(STUDENT_PREFIX_ENV)
    ]

    student_fields = [
        'classcharts_name',
        'trello_name',
        'trello_board',
        'trello_list',
        'time_slot',
    ]

    students = []
    for s in student_env:
        student = {n: v for n, v in zip(student_fields, s.split(','))}
        student['time_slot'] = int(student['time_slot'])
        students.append(student)

    return students


__all__ = (
    'CLASSCHARTS_USERNAME_ENV',
    'CLASSCHARTS_PASSWORD_ENV',
    'TRELLO_API_KEY_ENV',
    'TRELLO_API_SECRET_ENV',
    'TRELLO_OAUTH_TOKEN_ENV',
    'TRELLO_OAUTH_TOKEN_SECRET_ENV',
    'STUDENT_PREFIX_ENV',
    'get_environment_config',
)