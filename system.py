from abc import ABC, abstractmethod

def requires(*components):
	def decorator(system_class):
		system_class._required_components = frozenset(components)
		return system_class
	return decorator

class System(ABC):
	@abstractmethod
	def execute(self, entities, entities_ids, world):
		pass

	def get_components(self):
		return self. _required_components


class SystemGroup():
	def __init__(self, *systems):
		self.systems = list(systems)

