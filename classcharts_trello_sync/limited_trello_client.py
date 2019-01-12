from trello import TrelloClient


class LimitedTrelloClient:
    def __init__(
        self,
        api_key,
        api_secret,
        token,
        token_secret
    ):
        self.client = TrelloClient(
            api_key=api_key,
            api_secret=api_secret,
            token=token,
            token_secret=token_secret
        )

    def create_card(self, board_name, list_name, name, description, due, member_names=[]):
        board = self._get_board(board_name)
        if name in self._existing_cards(board):
            # Already created
            return

        trello_list = self._get_list(board, list_name)

        print('Adding card', name)
        new_card = trello_list.add_card(
            name=name,
            desc=description,
            due=due
        )
        for member in self._get_members(board, member_names):
            new_card.add_member(member)

    def _existing_cards(self, board):
        return[card.name for card in board.open_cards()]
    
    def _get_board(self, board_name):
        target_board = [
            board
            for board in self.client.list_boards()
            if board.name == board_name
        ]
        if not target_board:
            raise ValueError('Unknown board: {}'.format(board_name))

        return target_board[0]

    def _get_list(self, board, list_name):
        target_list = [
            trello_list
            for trello_list in board.open_lists()
            if trello_list.name == list_name
        ]
        if not target_list:
            raise ValueError('Unknown list: {}'.format(list_name))

        return target_list[0]

    def _get_members(self, board, member_names):
        return [
            member
            for member in board.all_members()
            if member.full_name in member_names
        ]


__all__ = (
    'LimitedTrelloClient',
)