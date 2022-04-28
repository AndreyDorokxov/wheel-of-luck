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
            voc_elem = self.messages[elem]
            self.end_voc[voc_elem] = percent
        numb = self.end_voc.values()
        return numb  # возвращает словарь в котором ключ-игра, а значение-шанс выпадения этой игры(в процентах)
