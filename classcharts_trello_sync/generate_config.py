'''Generate API token'''
import json
from trello import util

from classcharts_trello_sync.interactive_question import Question, YNQuestion


def configure():
    settings = {}

    settings['trello_auth'] = configure_trello_auth()
    settings['classcharts_auth'] = configure_classcharts_auth()
    settings['students'] = configure_students()

    print("# Classcharts Environment")

    print("export CLASSCHARTS_USERNAME='{}'".format(
        settings['classcharts_auth']['user']
    ))
    print("export CLASSCHARTS_USERNAME='{}'".format(
        settings['classcharts_auth']['password']
    ))

    print()

    print("export TRELLO_API_KEY='{}'".format(
        settings['trello_auth']['api_key']
    ))
    print("export TRELLO_API_SECRET='{}'".format(
        settings['trello_auth']['api_secret']
    ))
    print("export TRELLO_OAUTH_TOKEN='{}'".format(
        settings['trello_auth']['oauth_token']
    ))
    print("export TRELLO_OAUTH_TOKEN_SECRET='{}'".format(
        settings['trello_auth']['oauth_token_secret']
    ))

    print()

    for student in settings['students']:
        student_num = 1
        print("export STUDENT_{}='{},{},{},{},{}'".format(
            student_num,
            student['classcharts_name'],
            student['trello_name'],
            student['trello_board'],
            student['trello_list'],
            student['time_slot'],
        ))
        student_num += 1


def configure_trello_auth():
    """Trello OAUTH Credentials."""
    default_app_name = 'classcharts'

    key = Question(
        'Please provide the Trello API Key.',
        help_text='Available here: https://trello.com/app-key'
    ).ask()

    secret = Question(
        'Please provide the Trello API Secret.',
        help_text='Aslo available here in OAUTH section: https://trello.com/app-key'
    ).ask()

    app_name = Question(
        'What should the trello app be known as?',
        default=default_app_name
    ).ask()

    token = util.create_oauth_token(
        name=app_name,
        key=key,
        secret=secret
    )

    return {
        'api_key': key,
        'api_secret': secret,
        'oauth_token': token['oauth_token'],
        'oauth_token_secret': token['oauth_token_secret']
    }


def configure_classcharts_auth():
    """Classcharts credentials - no OAUTH caps as fas as can tell."""
    user = input('Please provide the Classcharts user email:\n')
    password = input('Please provide the Classcharts password:\n')

    return {
        'user': user,
        'password': password
    }

def configure_students():
    students = []
    while True:
        students.append(configure_student())
        more_students = YNQuestion(
            'Do you wish to configure more students?',
            default='N'
        ).ask()
        if not more_students:
            break
    
    return students

def configure_student():
    """Configure individual student."""
    default_max_slot_time = "30"

    classcharts_name = Question(
        'Full student name on Classcharts'
    ).ask()

    trello_name = Question(
        'Full student name on Trello',
        default=classcharts_name
    ).ask()

    trello_board = Question(
        'Name of the target Trello Board'
    ).ask()

    trello_list = Question(
        'Trello list for new cards on {} Trello Board'.format(trello_board)
    ).ask()

    time_slot = Question(
        'Maximum time for a homework slot in minutes',
        help_text='Between 10 and 120 minutes',
        validate=lambda x: x >= 10 and x <= 120,
        transform=int,
        default=default_max_slot_time
    ).ask()

    return {
        'classcharts_name': classcharts_name,
        'trello_name': trello_name,
        'trello_board': trello_board,
        'trello_list': trello_list,
        'time_slot': time_slot
    }


__all__ = (
    'configure',
)