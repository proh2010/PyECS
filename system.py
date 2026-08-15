from abc import ABC, abstractmetod

def requires(*components):
	def decorator(system_class):
		system_class._required_components = components
		return system_class
	return decorator

class system(ABC):
	def __init__():
