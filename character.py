import pygame
import os
import time

# pygame setup
DISPLAY = (1280, 720)
IDLE_TIME = 10

# alfabeto:
PULO = "w"
ANDAR_ESQUERDA = "a"
ANDAR_DIREITA = "d"
SENTAR = "s"
SOCO_SERIO = "k"
CARECADA = "adk"


def carregar_sprites(pasta):
    return [
        pygame.image.load(os.path.join(pasta, img)).convert_alpha()
        for img in sorted(os.listdir(pasta))
        if img.endswith(".png")
    ]


# Controle de animações
def timer_animacao():
    timing = {
        "idle": 0.2,
        "left": 0.1,
        "right": 0.1,
        "up": 0.1,
        "down": 0.2,
        "carecada": 0.1,
        "serious_punch": 0.05,
    }

    return timing


# Carregar sprites
def load_sprites():
    sprites = {
        "left": carregar_sprites("sprites/left"),
        "right": carregar_sprites("sprites/right"),
        "up": carregar_sprites("sprites/jump"),
        "down": carregar_sprites("sprites/sit"),
        "idle": carregar_sprites("sprites/idle"),
        "carecada": carregar_sprites("sprites/carecada"),
        "serious_punch": carregar_sprites("sprites/serious_punch"),
    }

    return sprites


def game_mode():
    pygame.init()
    screen = pygame.display.set_mode(DISPLAY)
    clock = pygame.time.Clock()
    pygame.display.set_caption("Controle de Personagem com AFD")
    running = True
    dt = 0

    timing = timer_animacao()
    sprites = load_sprites()

    # Variáveis de controle
    estado = "idle"
    frame = 0
    player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
    vel = 90
    tempo_anim = 0
    tempo_idle = 0
    speed_special = -30

    animacao_especial = False  # Flag para impedir interrupção das animações especiais

    # Controle de pulo
    gravity = 1000
    speed_y = 0
    jump_force = -500
    ground = True
    chao_y = screen.get_height() / 2

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()

        if keys[pygame.K_ESCAPE]:
            break

        if not animacao_especial:
            # Detecção de teclas
            if (keys[pygame.K_w] or keys[pygame.K_UP]) and ground:
                estado = "up"
                ground = False
                speed_y = jump_force
                frame = 0
            elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
                estado = "down"
            elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
                estado = "left"
                player_pos.x -= vel * dt
            elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                estado = "right"
                player_pos.x += vel * dt
            elif keys[pygame.K_l]:
                estado = "carecada"
                frame = 0
                animacao_especial = True
            elif keys[pygame.K_k]:
                estado = "serious_punch"
                frame = 0
                animacao_especial = True
            elif estado != "down":
                estado = "idle"

        # Lógica de pulo
        if not ground:
            estado = "up"
            speed_y += gravity * dt
            player_pos.y += speed_y * dt
            if player_pos.y >= chao_y:
                player_pos.y = chao_y
                speed_y = 0
                ground = True
        else:
            if (
                animacao_especial
                and estado == "carecada"
                and frame <= len(sprites["carecada"]) / 2
            ):
                estado = "carecada"
                player_pos.x += speed_special * dt
                speed_special += 10
            elif (
                animacao_especial
                and estado == "carecada"
                and frame > len(sprites["carecada"]) / 2
            ):
                estado = "carecada"
                player_pos.x += speed_special * dt
                speed_special -= 10

        # Controle do tempo de animação
        tempo_anim += dt
        intervalo_anim = timing[estado]

        # Atualização de animação
        if estado == "down":
            if tempo_anim >= intervalo_anim:
                tempo_anim = 0
                if frame < len(sprites["down"]) - 1:
                    frame += 1
        elif estado == "idle":
            tempo_idle += dt
            if tempo_idle < IDLE_TIME:
                frame = 0
            elif tempo_anim >= intervalo_anim:
                tempo_anim = 0
                frame += 1
                if frame >= len(sprites["idle"]):
                    frame = 0
                    tempo_idle = 0
        elif estado in ["carecada", "serious_punch"]:
            if tempo_anim >= intervalo_anim:
                tempo_anim = 0
                if frame < len(sprites[estado]) - 1:
                    frame += 1
                else:
                    frame = 0
                    speed_special = -30
                    animacao_especial = False
                    estado = "idle"
        else:
            if tempo_anim >= intervalo_anim:
                tempo_anim = 0
                frame = (frame + 1) % len(sprites[estado])

        # Desenho na tela
        sprite = sprites[estado][frame]
        screen.fill("black")
        screen.blit(sprite, player_pos)
        pygame.display.flip()

        dt = clock.tick(60) / 1000

    pygame.quit()


def afd_mode(input: str):
    sequencia = list(input)
    pygame.init()
    screen = pygame.display.set_mode(DISPLAY)
    clock = pygame.time.Clock()
    pygame.display.set_caption("Controle de Personagem com AFD")
    time.sleep(0.5)
    running = True
    dt = 0

    timing = timer_animacao()
    sprites = load_sprites()

    buffer = []  # Armazena os últimos comandos
    estado = "idle"
    frame = 0
    player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
    vel = 90
    tempo_anim = 0
    gravity = 1000
    speed_y = 0
    jump_force = -500
    ground = True
    chao_y = screen.get_height() / 2

    animacao_especial = False

    def processar_comando(cmd):
        nonlocal estado, frame, ground, speed_y, animacao_especial, player_pos

        if cmd == "w" and ground:
            estado = "up"
            ground = False
            speed_y = jump_force
            frame = 0
            animacao_especial = True
        elif cmd == "s":
            estado = "down"
            frame = 0
            animacao_especial = True
        elif cmd == "a":
            estado = "left"
            player_pos.x -= vel * dt
        elif cmd == "d":
            estado = "right"
            player_pos.x += vel * dt
        elif cmd == "k":
            estado = "serious_punch"
            frame = 0
            animacao_especial = True
        else:
            estado = "idle"

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or not sequencia:
                running = False

        if not animacao_especial and sequencia:
            # se ele estiver sentado ou em idle e no chao
            if estado == "idle" and ground:
                comando_atual = sequencia.pop(0)
                buffer.append(comando_atual)

                # Detecta combo especial "carecada"
                if len(buffer) >= 3 and buffer[-3:] == ["a", "d", "k"]:
                    estado = "carecada"
                    frame = 0
                    animacao_especial = True
                    buffer = []  # Limpa buffer após executar o combo
                else:
                    # Executa normalmente o comando atual
                    processar_comando(comando_atual)

        # Atualiza pulo
        if not ground:
            speed_y += gravity * dt
            player_pos.y += speed_y * dt
            if player_pos.y >= chao_y:
                player_pos.y = chao_y
                speed_y = 0
                ground = True
                animacao_especial = False
                estado = "idle"
                frame = 0

        # Atualiza animação
        tempo_anim += dt
        intervalo_anim = timing.get(estado, 0.1)

        if tempo_anim >= intervalo_anim and estado != "idle":
            tempo_anim = 0
            if frame < len(sprites[estado]) - 1:
                frame += 1
            else:
                frame = 0
                animacao_especial = False
                estado = "idle"

        screen.fill("black")
        screen.blit(sprites[estado][frame], player_pos)
        pygame.display.flip()

        dt = clock.tick(60) / 1000

    pygame.quit()


def afd_menu():
    print("Digite a sequência de comandos:")
    print("s = sentar, a = esquerda, d = direita, w = pulo, k = soco, adk = carecada")
    entrada = input("Comando: ").lower()

    alfabeto = set([PULO, ANDAR_ESQUERDA, SENTAR, ANDAR_DIREITA, SOCO_SERIO])

    if entrada:
        if set(entrada) - alfabeto:
            print("Caracteres inválidos!")
        else:
            afd_mode(entrada)


if __name__ == "__main__":
    op = -1
    while True:
        print("===== MENU PRINCIPAL =====")
        print("1 - Rodar como jogo")
        print("2 - Rodar partindo de uma string base")
        print("0 - Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            game_mode()
        elif opcao == "2":
            afd_menu()
        elif opcao == "0":
            print("Saindo do programa.")
            break
        else:
            print("Opção inválida. Tente novamente.")
