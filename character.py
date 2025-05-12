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
    vel = 90
    tempo_anim = 0
    timing = {"idle": 0.2, "left": 0.1, "right": 0.1, "up": 0.1, "down": 0.2, "carecada": 0.2, "serious_punch": 0.2}
    tempo_idle = 0
    anim_idle = False

    #jump control
    gravity = 1000
    speed_y = 0
    jump_force = -500
    ground = True
    chao_y = screen.get_height() / 2

    # carregar sprites partindo da pasta
    sprites = {
        "left": carregar_sprites("sprites/left"),
        "right": carregar_sprites("sprites/right"),
        "up": carregar_sprites("sprites/jump"),
        "down": carregar_sprites("sprites/sit"),
        "idle": carregar_sprites("sprites/idle"),
        "carecada": carregar_sprites("sprites/carecada"),
        "serious_punch": carregar_sprites("sprites/serious_punch"),
    }

    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        #pula
        if keys[pygame.K_w] and ground:
            estado = "up"
            ground = False
            speed_y = jump_force
        #senta
        elif keys[pygame.K_s]:
            estado = "down"
        #esquerda
        elif keys[pygame.K_a]:
            estado = "left"
            player_pos.x -= vel * dt
        
        #direita
        elif keys[pygame.K_d]:
            estado = "right"
            player_pos.x += vel * dt
        elif keys[pygame.K_l]:
            estado = "carecada"
        elif keys[pygame.K_k]:
            estado = "serious_punch"
        #se nao estiver sentado, fica em idle
        elif estado != "down":
            estado = "idle"

        if estado == "idle":
            tempo_idle += dt
        elif estado != "idle" or tempo_idle >= IDLE_TIME:
            tempo_idle = 0  # resetar caso esteja se movendo
        if not ground:
            estado = "up"
            speed_y += gravity * dt
            player_pos.y += speed_y * dt
            if player_pos.y >= chao_y:
                player_pos.y = chao_y
                speed_y = 0
                ground = True

        tempo_anim += dt
        intervalo_anim = timing[estado]
        
        if estado == "down":
            if tempo_anim >= intervalo_anim:
                tempo_anim = 0
                if frame < len(sprites["down"]) - 1:
                    frame += 1
        elif estado == "up": 
            if tempo_anim >= intervalo_anim:
                tempo_anim = 0
                frame = (frame + 1) % len(sprites[estado])
        elif estado == "idle":
            if tempo_idle < IDLE_TIME:
                frame = 0
            elif tempo_idle >= IDLE_TIME:
                if tempo_anim >= intervalo_anim:
                    tempo_anim = 0
                    frame += 1
                    if frame >= len(sprites["idle"]):
                        frame = 0
                        tempo_idle = 0
        #usado para esquerda e direita
        else:
            if tempo_anim >= intervalo_anim:
                tempo_anim = 0
                frame = (frame + 1) % len(sprites[estado])
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
