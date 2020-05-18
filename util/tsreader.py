class TSReader:
    def __init__(self, filename):
        self.freader = open(filename, 'r')
        for line in self.freader:
            if line[0] == '#':
                continue
            elif line[0] == '@':
                tokens = line.split()
                # potentially handle other tags
                # but we only care for either
                # @data or @classLabel
                if tokens[0] == '@data':
                    break
                elif tokens[0] == '@classLabel':
                    self.classes = tokens[2:]

    def read(self):
        for line in self.freader:
            # : separates dimensions
            dimensions = line.split(':')
            curr_class = dimensions.pop()
            # get all values
            values = map(lambda s: s.split(','), dimensions)
            # convert from string to float
            values = [[float(v) for v in dims] for dims in values]
            yield zip(*values), curr_class

class TSVReader:
    def __init__(self, fname):
        self.fname = fname

    def read(self):
        with open(self.fname, 'r') as freader:
            for line in freader:
                data = line.split()
                yield list(map(float,data[1:])), data[0]
