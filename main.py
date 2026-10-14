from __future__ import annotations

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
import asyncio

import pygame

from snake import ui
from snake.logic import EstadoJuego

FPS = 60
BASE_TICK_MS = 140
MIN_TICK_MS = 60


def tick_interval(score: int) -> int:
    return max(MIN_TICK_MS, BASE_TICK_MS - score * 4)


async def main() -> None:
    pygame.init()
    estado = EstadoJuego()
    pantalla = pygame.display.set_mode(ui.window_size(estado))
    pygame.display.set_caption("Snake")
    reloj = pygame.time.Clock()
    letras = (pygame.font.SysFont(None, 36), pygame.font.SysFont(None, 24))

    pausado = False
    elapsed = 0
    corriendo = True

    while corriendo:
        elapsed += reloj.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                corriendo = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    corriendo = False
                elif event.key == pygame.K_r:
                    estado.reset()
                    pausado = False
                elif event.key == pygame.K_p and estado.alive:
                    pausado = not pausado
                elif event.key in ui.KEY_TO_DIRECTION and not pausado:
                    estado.change_direction(ui.KEY_TO_DIRECTION[event.key])

        if not pausado and estado.alive:
            interval = tick_interval(estado.score)
            while elapsed >= interval:
                elapsed -= interval
                estado.step()
        else:
            elapsed = 0

        ui.draw(pantalla, estado, letras, pausado)
        pygame.display.flip()
        await asyncio.sleep(0)

    pygame.quit()


def run() -> None:
    asyncio.run(main())
