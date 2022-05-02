class Wheel:
    def __init__(self, list_value):
        self.value = list_value
        self.summ = 0
        self.end_voc = []

    def calculate(self):
        print(self.value)
        for i in self.value:
            self.summ += i
        for i in self.value:
            percent = int(i) / self.summ
            percent = format(percent, '.2f')
            percent = float(percent)
            self.end_voc.append(percent)
        numb = self.end_voc
        return numb
