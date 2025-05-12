import pygame
import os

# pygame setup
DISPLAY = (1280, 720)
IDLE_TIME = 10


def carregar_sprites(pasta):
    return [
        pygame.image.load(os.path.join(pasta, img)).convert_alpha()
        for img in sorted(os.listdir(pasta))
        if img.endswith(".png")
    ]


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode(DISPLAY)
    clock = pygame.time.Clock()
    pygame.display.set_caption("Controle de Personagem com AFD")
    running = True
    dt = 0

    # variaveis de controle
    estado = "idle"
    frame = 0
    player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
    vel = 300
    tempo_anim = 0
    timing = {"idle": 0.2, "move": 0.5}
    tempo_idle = 0
    anim_idle = False

    # carregar sprites partindo da pasta
    sprites = {
        # "left": carregar_sprites("sprites/left"),
        # "right": carregar_sprites("sprites/right"),
        # "up": carregar_sprites("sprites/up"),
        # "down": carregar_sprites("sprites/down"),
        "idle": carregar_sprites("sprites/idle"),
    }

    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        movimento = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            estado = "up"
            player_pos.y -= vel * dt

        elif keys[pygame.K_s]:
            player_pos.y += vel * dt
        elif keys[pygame.K_a]:
            player_pos.x -= vel * dt
        elif keys[pygame.K_d]:
            player_pos.x += vel * dt
        else:
            estado = "idle"

        if estado == "idle":
            tempo_idle += dt
        elif estado != "idle" or tempo_idle >= IDLE_TIME:
            tempo_idle = 0  # resetar caso esteja se movendo

        tempo_anim += dt
        intervalo_anim = timing[estado]
        if estado != "idle":
            if tempo_anim >= intervalo_anim:
                tempo_anim = 0
                frame = (frame + 1) % len(sprites[estado])
        else:
            if tempo_idle < IDLE_TIME:
                frame = 0
            elif tempo_idle >= IDLE_TIME:
                if tempo_anim >= intervalo_anim:
                    tempo_anim = 0
                    frame += 1
                    if frame >= len(sprites["idle"]):
                        frame = 0
                        tempo_idle = 0

        # Atualiza o frame da animação
        sprite = sprites[estado][frame]

        screen.fill("black")
        screen.blit(sprite, player_pos)
        pygame.display.flip()

        # limits FPS to 60
        # dt is delta time in seconds since last frame, used for framerate-
        # independent physics.
        dt = clock.tick(60) / 1000

    pygame.quit()
