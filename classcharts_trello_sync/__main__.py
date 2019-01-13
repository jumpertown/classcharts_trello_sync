'''Synchronise data between Classcharts and Trello.'''
from classcharts_trello_sync.sync import sync_data


def main(*args, **vargs):
    sync_data()


if __name__ == "__main__":
    main()
