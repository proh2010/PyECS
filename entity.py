class Entity():
	def __init__(self, *components):
		self.components_types = set()
		self.components_dict = {}
		for component in components:
			self.components_types.add(type(component))
			self.components_dict[type(component)] = component

	def get_components(self):
		return self.components_types
	def add_components(self, *components):
		for component in components:
			if type(component) in self.components_types:
				self.components_dict[type(component)] += comonent
			else:
				self.components_types.add(type(component))
				self.components_dict[type(component)] = comonent
	def remove_components(self, *components):
		for component in components:
			if type(component) in self.components_types:
				self.components_types.remove(type(component))
				self.components_dict.pop(type(component))
			else:
				raise ValueError("Thre is no components with type " + str(type(component)))
	def remove_components_by_type(self, *components):
		for component in components:
			if component in self.components_types:
				self.components_types.remove(component)
				self.components_dict.pop(component)
			else:
				raise ValueError("Thre is no components with type " + str(component))
	def get_component_by_type(self, type):
		return self.components_dict[type]