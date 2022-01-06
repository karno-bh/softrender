import typing as t


class Model:

    def __init__(self) -> None:
        super().__init__()
        self.vertexes: [] = []
        self.faces: [] = []

    def load(self, file_name):
        with open(file_name) as f:
            while True:
                line = f.readline()
                if not line:
                    break
                data = [d.strip() for d in line.split()]
                cmd = data and data[0]
                if cmd == 'v':
                    self.vertexes.append([float(coord) for coord in data[1:4]])
                elif cmd == 'f':
                    self.faces.append([[int(comp) for comp in c_idx.split('/')] for c_idx in data[1:4]])
            pass
