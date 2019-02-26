class Board:
    def __init__(self, filename):
        self.data = []

        with open(filename, 'r') as f:
            for line in f:
                self.data.append(line.split())
