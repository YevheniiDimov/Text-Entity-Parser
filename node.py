class Node:
    def __init__(self, name="node", value="abstract", children=[]):
        self.name = name
        self.value = value
        self.children = children

    def get_hierarchy(self, level=0):
        ret = '\t'*level + f"{self.name}: {self.value}\n"
        for child in self.children:
            ret += child.get_hierarchy(level+1)
        return ret

    def __str__(self):
        return self.get_hierarchy()

    def remove_by_name_first(self, name):
        for child in self.children:
            if child.name == name:
                self.children.remove(child)
                return

    def get_duplicates(self, tokens={}):
        for child in self.children:
            if child.name in tokens:
                tokens[child.name] += 1
            else:
                tokens.update({child.name: 1})
            tokens.update(child.get_duplicates(tokens))
        
        return tokens

    def get_definite(self):
        definite = []
        for child in self.children:
            if len(child.children) == 0:
                definite.append(child)
            else:
                definite += child.get_definite()

        return definite

    def get_path(self):
        if self.parent:
            if self.value == 'abstract':
                return self.parent.get_path()
            return self.parent.get_path() + [f"{self.name}: {self.value}"]
        return [f"{self.name}: {self.value}"]
    
    def str_flatten(self):
        definite = self.get_definite()
        text = ""
        for node in definite:
            text += " — ".join(node.get_path()) + '\n'
        return text

    def assign_parent(self):
        if not hasattr(self, 'parent'):
            self.parent = None
        for child in self.children:
            child.parent = self
            child.assign_parent()

    def remove_duplicates(self):
        tokens = self.get_duplicates()
        for token, count in tokens.items():
            if count > 1:
                self.remove_by_name_first(token)
    
    def to_json(self):
        return '{"name": "' + self.name + '", "value": "' + self.value + '", children: [' + ",".join([child.to_json() for child in self.children]) + ']}'