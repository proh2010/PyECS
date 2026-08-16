# py_ECS_framework
It`s a library, that allow you create a ECS architecture simply and fast.
## Using

 ### Components
 You can create compoonents with a `dataclass`.
 

    from dataclasses import dataclass
    @dataclass
    class ExampleComponent():
	    x:int = 5
	    y:float = 8
### Entities
To create entity you should inheritance from `Entity`

    from py_ECS_framework import Entity
     
    class ExampleEntity(Entity):
	    def __init__(self):
		    super().__init__(ExampleComponent()) #Here you can give some components
### Systems
To create entity you should inheritance from` System` with decorator `@requires`

    from py_ECS_framework import System, requires
    @requires(ExampleComponent)
    class ExampleSystem(System):
	    def execute(self, entity, world):
		    #There you can write logic of the system
		    component = entity.get_component_by_type(ExampleComponent)
		    component.x += 1
		    component.y /= 2
### World
All systems and entities working in a world. You should create it by `World`

    world = World((ExampleComponent, )) #There is all components that you want use
    world.system_list = [ExampleSystem()]
    entity = ExampleEntity()
    world.add_entity(entity)
    world.update() #one step













