from abc import ABC, abstractmethod

def requires(*components):
	def decorator(system_class):
		system_class._required_components = frozenset(components)
		return system_class
	return decorator
def global_system():
	def decorator(system_class):
		system_class._is_global = True
		return system_class
	return decorator

class System(ABC):
	_is_global = False
	@abstractmethod
	def execute(self, target, world, dt):
		pass
	@classmethod
	def get_components(cls):
		return cls._required_components

class SystemGroup():
	def __init__(self, *systems):
		self.systems = list(systems)
	def add_systems(self, *systems):
		for system in systems:
			if isinstance(system, System):
				self.systems.append(system)
			elif isinstance(system, SystemGroup):
				self.systems.extend(system.systems)

