from __future__ import annotations

import random
from dataclasses import dataclass, field
from enum import Enum

Punto = tuple[int, int]


class Direcciones(Enum):
    Arriba = (0, -1)
    Abajo = (0, 1)
    Izquierda = (-1, 0)
    Derecha = (1, 0)

    def opposite(self) -> Direcciones:
        dx, dy = self.value
        return Direcciones((-dx, -dy))


@dataclass
class EstadoJuego:
    Ancho: int = 20
    Alto: int = 20
    wrap: bool = False
    rng: random.Random = field(default_factory=random.Random)
    snake: list[Punto] = field(default_factory=list)  # head first
    direction: Direcciones = Direcciones.Derecha
    food: Punto | None = None
    score: int = 0
    alive: bool = True
    _pending: Direcciones | None = field(default=None, repr=False)

    def __post_init__(self) -> None:
        if not self.snake:
            self.reset()

    def reset(self) -> None:
        cx, cy = self.Ancho // 2, self.Alto // 2
        self.snake = [(cx, cy), (cx - 1, cy), (cx - 2, cy)]
        self.direction = Direcciones.Derecha
        self._pending = None
        self.score = 0
        self.alive = True
        self.food = self._spawn_food()

    def change_direction(self, new: Direcciones) -> None:
        # It compare against the direction applied on the last step, so two quick
        #esto compara contra la direccion aplicada en el ultimo paso,
        # inputs within one tick cannot produce a 180-degree turn.
        #comandos sin ticket no pueden hacer giros 180 grados.
        if new != self.direction.opposite():
            self._pending = new

    def step(self) -> None:
        if not self.alive:
            return
        if self._pending is not None:
            self.direction = self._pending
            self._pending = None

        dx, dy = self.direction.value
        hx, hy = self.snake[0]
        head = (hx + dx, hy + dy)

        if self.wrap:
            head = (head[0] % self.Ancho, head[1] % self.Alto)
        elif not (0 <= head[0] < self.Ancho and 0 <= head[1] < self.Alto):
            self.alive = False
            return

        eating = head == self.food
        # The tail moves away this tick unless the snake grows.
        #la cola se mueve a pesar de que cresca la vivora
        body = self.snake if eating else self.snake[:-1]
        if head in body:
            self.alive = False
            return

        self.snake.insert(0, head)
        if eating:
            self.score += 1
            self.food = self._spawn_food()
        else:
            self.snake.pop()

    def _spawn_food(self) -> Punto | None:
        occupied = set(self.snake)
        free = [
            (x, y)
            for x in range(self.Ancho)
            for y in range(self.Alto)
            if (x, y) not in occupied
        ]
        return self.rng.choice(free) if free else None
