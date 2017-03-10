# -*- coding: utf-8 -*-
'''
模型-视图-控制器模式 2017-3-10
'''
quotes = ('A man is not complete until he is married. Then he is finished.',
          'As I said before, I never repeat myself.',
          'Behind a successful man is an exhausted woman.',
          'Black holes really suck...',
          'Facts are stubborn thing.')


class QuoteModel:
    def get_quote(delf, n):
        try:
            value = quotes[n]
        except IndexError as err:
            value = 'NOT FOUND!'
        return value


class QuoteTerminalView:
    def show(self, quote):
        print 'And the quote is: {}'.format(quote)

    def error(self, msg):
        print 'Error: {}'.format(msg)

    def select_quote(self):
        return raw_input('Which quote number would you like to see?')


class QuoteTerminaController:
    def __init__(self):
        self.model = QuoteModel()
        self.view = QuoteTerminalView()

    def run(self):
        valid_input = False
        while not valid_input:
            try:
                n = self.view.select_quote()
                n = int(n)
                valid_input = True
            except ValueError as err:
                self.view.error("Incrrect index {}".format(n))
            else:
                quote = self.model.get_quote(n)
                self.view.show(quote)


def main():
    controller = QuoteTerminaController()
    while True:
        controller.run()

if __name__ == "__main__":
    main()
