from abc import ABC, abstractmethod

def requires(*components):
	def decorator(system_class):
		system_class._required_components = frozenset(components)
		return system_class
	return decorator

class system(ABC):
	@abstractmethod
	def execute(self, entity, world):
		pass

	def get_components(self):
		return self. _required_components

