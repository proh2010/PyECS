from abc import ABC, abstractmethod

def requires(*components):
	def decorator(system_class):
		system_class._required_components = frozenset(components)
		return system_class
	return decorator

class System(ABC):
	@abstractmethod
	def execute(self, entities, world, dt):
		pass

	def get_components(self):
		return self._required_components


class SystemGroup():
	def __init__(self, *systems):
		self.systems = list(systems)
	def add_systems(self, *systems):
		for system in systems:
			if isinstance(system, System):
				self.systems.append(system)
			elif isinstance(system, SystemGroup):
				self.systems.extend(system.systems)

