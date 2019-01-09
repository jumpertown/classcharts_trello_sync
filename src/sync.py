from datetime import date, timedelta

from classcharts_client import ClasschartsClient
from limited_trello_client import LimitedTrelloClient
from os_config import config


def sync_data(*args, **kwargs):
    classcharts_client = ClasschartsClient(
        username=config['classcharts_auth']['user'],
        password=config['classcharts_auth']['password']
    )

    trello_client = LimitedTrelloClient(
        api_key=config['trello_auth']['api_key'],
        api_secret=config['trello_auth']['api_secret'],
        token=config['trello_auth']['oauth_token'],
        token_secret=config['trello_auth']['oauth_token_secret']
    )

    all_homework = classcharts_client.query_due_range(
        date.today() - timedelta(days=7),
        date.today() + timedelta(days=90)
    )

    due_homework = [homework for homework in all_homework if not homework.done]

    for student in config['students']:
        for homework in due_homework:
            if homework.student != student['classcharts_name']:
                continue

            num_slots = homework.completion_time_minutes // student['time_slot']
            if homework.completion_time_minutes % student['time_slot'] != 0:
                num_slots += 1
            
            for slot in range(1, num_slots + 1):
                card_name = '{}: {} (due: {})'.format(
                    homework.lesson,
                    homework.title,
                    homework.due_date.strftime('%d/%m')
                )
                if num_slots > 1:
                    card_name += ' slot {}'.format(slot)

                if student['trello_name']:
                    members = [student['trello_name']]
                else:
                    members = []

                trello_client.create_card(
                    board_name=student['trello_board'],
                    list_name=student['trello_list'],
                    name=card_name,
                    description=homework.description,
                    due=homework.due_date.strftime('%Y-%m-%d'),
                    member_names=members
                )
