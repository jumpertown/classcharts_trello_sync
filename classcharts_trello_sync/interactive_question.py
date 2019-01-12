class Question:
    def __init__(
        self,
        question_text,
        help_text=None,
        transform=lambda x: x,
        validate=lambda _: True,
        default=None
    ):
        self.question_text = question_text
        self.help_text = help_text

        self.transform = transform
        self.validate = validate
        self.default = default

    @property
    def mandatory(self):
        return not self.default

    def ask(self):
        while True:
            question_text = '\n'
            question_text += self.question_text
            if self.help_text:
                question_text += ' ({})'.format(self.help_text)
            if self.default:
                question_text += ' default: {}'.format(self.default)
            question_text += ':\n'

            response = input(question_text)

            if len(response) == 0:
                if self.mandatory:
                    print("Cannot leave this field blank.")
                    print(self.help_text)
                    continue
                else:
                    response = self.default

            response = response.strip()
            response = self.transform(response)

            if self.validate(response):
                return response

            print("Invalid response: {}".format(response))
            print(self.help_text)


class YNQuestion(Question):
    def __init__(self, question_text, default=None):
        super().__init__(
            question_text=question_text,
            help_text="Y of N",
            transform=lambda x: {'Y': True, 'N': False}.get(x.upper(), x),
            validate=lambda x: x in (True, False),
            default=default
        )


__all__ = (
    'Question',
    'YNQuestion',
)
