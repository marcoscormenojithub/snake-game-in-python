from __future__ import annotations

import pygame

from snake.logic import Direcciones, EstadoJuego

Celda = 28
Margen = 16
Cabeza = 56

BG = (24, 26, 33)
TableroA = (34, 37, 47)
TableroB = (38, 42, 53)
CuerpoVivora = (72, 199, 142)
CabezaVivora = (110, 231, 183)
Comida = (255, 99, 110)
Texto = (232, 234, 240)
Muteado = (140, 146, 163)

KEY_TO_DIRECTION = {
    pygame.K_UP: Direcciones.Arriba,
    pygame.K_w: Direcciones.Arriba,
    pygame.K_DOWN: Direcciones.Abajo,
    pygame.K_s: Direcciones.Abajo,
    pygame.K_LEFT: Direcciones.Izquierda,
    pygame.K_a: Direcciones.Izquierda,
    pygame.K_RIGHT: Direcciones.Derecha,
    pygame.K_d: Direcciones.Derecha,
}


def window_size(state: EstadoJuego) -> tuple[int, int]:
    return (
        state.Ancho * Celda + Margen * 2,
        state.Alto * Celda + Margen * 2 + Cabeza,
    )


def _cell_rect(x: int, y: int, inset: int = 0) -> pygame.Rect:
    return pygame.Rect(
        Margen + x * Celda + inset,
        Margen + Cabeza + y * Celda + inset,
        Celda - inset * 2,
        Celda - inset * 2,
    )


def _center_text(screen: pygame.Surface, font: pygame.font.Font, text: str, y: int, color) -> None:
    surf = font.render(text, True, color)
    screen.blit(surf, surf.get_rect(center=(screen.get_width() // 2, y)))


def draw(
    screen: pygame.Surface,
    state: EstadoJuego,
    fonts: tuple[pygame.font.Font, pygame.font.Font],
    paused: bool,
) -> None:
    big, small = fonts
    screen.fill(BG)

    score = big.render(f"Score  {state.score}", True, Texto)
    screen.blit(score, (Margen, Margen))

    for y in range(state.Alto):
        for x in range(state.Ancho):
            color = TableroA if (x + y) % 2 == 0 else TableroB
            pygame.draw.rect(screen, color, _cell_rect(x, y))

    if state.food is not None:
        pygame.draw.circle(screen, Comida, _cell_rect(*state.food).center, Celda // 2 - 4)

    for i, (x, y) in enumerate(state.snake):
        color = CabezaVivora if i == 0 else CuerpoVivora
        pygame.draw.rect(screen, color, _cell_rect(x, y, inset=2), border_radius=8)

    if not state.alive:
        _overlay(screen, big, small, "Game Over", "Press R to restart")
    elif paused:
        _overlay(screen, big, small, "Paused", "Press P to resume")


def _overlay(screen, big, small, title: str, hint: str) -> None:
    shade = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    shade.fill((0, 0, 0, 150))
    screen.blit(shade, (0, 0))
    mid = screen.get_height() // 2
    _center_text(screen, big, title, mid - 12, Texto)
    _center_text(screen, small, hint, mid + 24, Muteado)
