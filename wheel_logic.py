import random


class Wheel:
    def __init__(self, messages):  # сразу передается словать messages
        self.messages = messages
        self.summ = 0
        self.end_voc = {}

    def calculate(self):
        for item in list(self.messages):
            self.summ += item
        for elem in self.messages:
            percent = int(elem) / self.summ
            percent = format(percent, '.2f')
            percent = float(percent)
            percent = percent * 100
            percent = int(percent)
            self.percent = percent
            voc_elem = self.messages[elem]
            self.end_voc[voc_elem] = percent
        return self.end_voc  # возвращает словарь в котором ключ-игра, а значение-шанс выпадения этой игры(в процентах)

    def rand_value(self):
        games = list(self.end_voc.keys())
        keys = list(self.end_voc.values())
        rand_elem = random.choices(games, weights=keys)
        for elem in rand_elem:
            return elem  # возвращиет название случайно выпавшей игры, учитывая вероятность выпадения
