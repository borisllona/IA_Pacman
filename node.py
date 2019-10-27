import game
class Node:

	def __init__(self, state, parent=None, action=None, cost=0, depth=0):
		self.parent = parent
		self.action = action
		self.state = state
		self.cost = 0
		self.depth = 0
		if self.parent != None:
			self.cost = cost + self.parent.cost
			self.depth = depth + self.parent.depth
		

	def path(self):
		node_path = []
		current = self
		while current.parent != None:
			node_path.append(current.action)
			current = current.parent
		return list(reversed(node_path))

	def invertedpath(self):
		node_path = []
		current = self
		while current.parent != None:
			node_path.append(game.Actions.reverseDirection(current.action))
			current = current.parent
		return list(node_path)