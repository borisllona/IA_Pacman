#Node.py

class Node:

    def __init__(self,_state,_parent=None,_action=None,_cost=0,depth=0):
        self.state = _state
        self.parent = _parent
        self.action = _action
        self.cost = 0
        if self.parent:
            self.cost = self.cost + self.parent.cost
        self.depth = depth

    def path(self):
        path = []
        curr = self
        while(curr.parent):
            path.append(curr.action)
            curr = curr.parent
        return list(reversed(path))
