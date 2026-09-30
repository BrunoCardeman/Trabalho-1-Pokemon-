class TreeNode:

    def __init__(self, coord, fx, gx=None, ginasios_anteriores=None, indice=None):
        self.coord = coord
        self.indice = indice
        self.parent = None
        self.children = []   # cada nó tem a sua lista (antes era uma lista só, compartilhada)

        # frozenset = conjunto que não muda; por isso pode ser usado dentro de chaves de dict/set
        if ginasios_anteriores is None:
            self.ginasios_visitados = frozenset()
        else:
            self.ginasios_visitados = frozenset(ginasios_anteriores)

        if gx is None:  # se nao for busca heuristica
            self.priority = fx
            self.value_gx = fx
        else:
            self.priority = fx      # f(x) = g(x) + h(x)
            self.value_gx = gx      # g(x): custo percorrido da origem até este nó

    def get_ginasios_visitados(self):
        return self.ginasios_visitados

    def get_coord(self):
        return self.coord

    def get_priority(self):
        return self.priority

    def get_value_gx(self):
        return self.value_gx

    def set_parent(self, value):
        self.parent = value

    def get_parent(self):
        return self.parent

    def add_child(self, value):
        self.children.append(value)

    def remove_child(self, value):
        self.children.remove(value)

    def __lt__(self, other):
        # O heap usa isto para achar o nó de menor f.
        if self.priority != other.priority:
            return self.priority < other.priority
        # Empate no f: prefere o nó que já visitou MAIS ginásios (só afeta a velocidade)
        return len(self.ginasios_visitados) > len(other.ginasios_visitados)