class World():
	def __init__(self, components_list):
		self._entities_list = dict() #dict (ID:entity)
		self.system_list = [] #list of systems
		self._to_delete = [] #for delition
		self._to_add = []
		self._free_ids = []
		self._next_id = 0
		if not(isinstance(components_list,tuple)):
			raise TypeError(f"Components must be a tuple, not {str(type(components_list))}")
		self._components_list = components_list #components

		#for responce entities
		self._request_entities_list = dict()
		self.dt = 0

	#updates all entities
	def update(self):
		#removes all entities from to_delete
		for ids in self._to_delete:
			self._free_ids.append(ids)
			self._entities_list.pop(ids)
		self._to_delete = []
		for ids, entity in self._to_add:
			self._entities_list[ids] = entity

		self._to_add = []

		#system loop
		for system in self.system_list:
			components_need = self.components_to_hash(system.get_components())
			entities = []
			entities_ids = []
			for entity in self._entities_list.keys():
				entity_components = self.components_to_hash(self._entities_list[entity].get_components())
				if entity_components & components_need == components_need:
					entities_ids.append(entity)
					entities.append(self._entities_list[entity])

			#loop for request entitiies
			for entity in self._request_entities_list.keys():
				entity_components = self.components_to_hash(self._request_entities_list[entity].get_components())
				if entity_components & components_need == components_need:
					entities_ids.append(entity)
					entities.append(self._request_entities_list[entity])
			system.execute(zip(entities, entities_ids), self, self.dt)

		self._request_entities_list = dict()
		self.dt += 1

	#adds entity to deletion list
	def delete_entity(self, entity_id):
		self._to_delete.append(entity_id)

	#adds entity
	def add_entity(self, entity):
		#choose new id
		if self._free_ids:
			new_id = self._free_ids[-1]
			self._free_ids.pop()
		else:
			new_id = self._next_id
			self._next_id += 1
		#add new entity
		self._to_add.append((new_id, entity))
		

	def components_to_hash(self, components):
		mask = 0
		for i, component in enumerate(self._components_list):
			if component in components:
				mask |= (1 << i)
		return mask

	def add_system_group(self, sistem_group):
		self.system_list.extend(sistem_group.systems)

	def add_request_entity(self, entity):
		if self._free_ids:
			new_id = self._free_ids[-1]
			self._free_ids.pop()
		else:
			new_id = self._next_id
			self._next_id += 1
		self._request_entities_list[new_id] = entity


