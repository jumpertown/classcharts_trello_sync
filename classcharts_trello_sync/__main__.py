'''Synchronise data between Classcharts and Trello.'''
from .sync import sync_data


def main():
    sync_data()


if __name__ == "__main__":
    main()
