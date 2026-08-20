

# PyECS

**Py_ECS_framework** — это минималистичный ECS-фреймворк на Python.  
Он позволяет строить игровую логику через **компоненты, сущности и системы**.

---

## Особенности

- Простой API, вдохновлённый классическим ECS
- Поддержка **глобальных систем** (например, для физики или рендеринга)
- **Группы систем** для удобной компоновки
- **Быстрая фильтрация** через битовые маски
- **Автоматическое удаление** сущностей (отложенное)
- **Запросные сущности** (живут один кадр)
- Работа с **дельта-временем (`dt`)**

---

## Установка

```bash
pip install py-ECS-framework
```
---

## Быстрый старт

### 1. Компоненты

Компоненты — это просто **dataclass'ы** с данными.

```python
from dataclasses import dataclass

@dataclass
class Position:
    x: float = 0.0
    y: float = 0.0

@dataclass
class Velocity:
    x: float = 0.0
    y: float = 0.0

@dataclass
class Health:
    value: int = 100
```

---

### 2. Сущности

Наследуйся от `Entity` и передай компоненты в `super().__init__()`.

```python
from py_ECS_framework import Entity

class Player(Entity):
    def __init__(self):
        super().__init__(
            Position(10, 20),
            Velocity(5, 3),
            Health(100)
        )
```

---

### 3. Системы

Системы — это классы, наследующие от `System`.  
Используй **декораторы**:
- `@requires(...)` — какие компоненты нужны
- `@global_system` — система получает **все** подходящие сущности сразу (удобно для физики, рендеринга)

```python
from py_ECS_framework import System, requires, global_system

# Обычная система (одна сущность за раз)
@requires(Position, Velocity)
class MovementSystem(System):
    def execute(self, entity, world, dt):
        pos = entity[0].get_component_by_type(Position)
        vel = entity[0].get_component_by_type(Velocity)
        pos.x += vel.x * dt
        pos.y += vel.y * dt

# Глобальная система (все сущности сразу)
@requires(Position, Health)
@global_system
class DeathSystem(System):
    def execute(self, entities, world, dt):
        for entity, entity_id in entities:
            health = entity.get_component_by_type(Health)
            if health.value <= 0:
                world.delete_entity(entity_id)
```

**Важно:**  
- Если система **не помечена** как `@global_system`, в `execute` первым аргументом приходит **одна сущность**.
- Если помечена — приходит **список пар** вида `(entity, entity_id)` для всех подходящих сущностей.

---

### 4. Мир (World)

Создай мир, зарегистрируй компоненты, добавь системы и сущности.

```python
from py_ECS_framework import World

# Все типы компонентов, которые будут использоваться
world = World((Position, Velocity, Health))

# Добавляем системы (порядок важен!)
world.system_list.append(MovementSystem())
world.system_list.append(DeathSystem())

# Создаём сущность
player = Player()
world.add_entity(player)

# Игровой цикл
import time

while True:
    dt = 0.016  # 60 FPS
    world.update()
    time.sleep(dt)
```

---

### 5. Группы систем

Группируй системы для удобства:

```python
from py_ECS_framework import SystemGroup

physics_group = SystemGroup(
    MovementSystem(),
    GravitySystem()
)

logic_group = SystemGroup(
    DeathSystem(),
    SpawnSystem()
)

world.add_system_group(physics_group)
world.add_system_group(logic_group)
```

---

### 6. Запросные сущности (однокадровые)

Иногда нужно создать сущность, которая живёт **только один кадр** (например, событие или запрос на звук).

```python
# В системе
world.add_request_entity(Entity(CollisionEvent(a, b)))
```

Такие сущности автоматически удаляются в конце `update()`.

---

## Как это работает внутри

1. **World** хранит все сущности и системы.
2. При вызове `update()` системы выполняются **в порядке добавления**
3. Фильтруются только те сущности, у которых есть **все** нужные компоненты.
4. Обычные системы получают сущности **по одной**.  
   Глобальные (`@global_system`) — **все сразу**.
5. Сущности, помеченные на удаление, удаляются после всех систем.
6. Запросные сущности удаляются в конце кадра.
---

## Лицензия

MIT

