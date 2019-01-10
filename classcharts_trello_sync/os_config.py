import os


def parse_students():
    student_env = [
        os.environ[key]
        for key in os.environ.keys()
        if key.startswith('STUDENT_')
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

config = {}

config['classcharts_auth'] = {}
config['classcharts_auth']['user'] = os.environ['CLASSCHARTS_USERNAME']
config['classcharts_auth']['password'] = os.environ['CLASSCHARTS_PASSWORD']

config['trello_auth'] = {}
config['trello_auth']['api_key'] = os.environ['TRELLO_API_KEY']
config['trello_auth']['api_secret'] = os.environ['TRELLO_API_SECRET']
config['trello_auth']['oauth_token'] = os.environ['TRELLO_OAUTH_TOKEN']
config['trello_auth']['oauth_token_secret'] = os.environ['TRELLO_OAUTH_TOKEN_SECRET']

config['students'] = parse_students()
