from globals import *
from PPlay.sprite import Sprite
from Personagens.player import Player
from Personagens.fantasgua import Fantasgua
from Personagens.pingoso import Pingoso

import random
def create_enemies(level):
    """Cria inimigos aleatoriamente com base no nível."""
    enemies = []
    qtdd_fantasgua = random.randint(0, quantidade_inimigos(level))
    qtdd_pingoso = quantidade_inimigos(level) - qtdd_fantasgua

    print("Fantasgua: ", qtdd_fantasgua)
    print("Pingoso: ", qtdd_pingoso)

    for _ in range(qtdd_fantasgua):
        enemy = Fantasgua(random.randint(0, janela.width), janela.height/2)
        enemies.append(enemy)

    for _ in range(qtdd_pingoso):
        enemy = Pingoso(random.randint(0, janela.width), janela.height/2)
        enemies.append(enemy)

    return enemies

def Play():
    player = Player((janela.width / 2) - 60, (janela.height / 2) + 60)  # Ajusta a posição inicial do player
    level = 1
    enemies = []  # Começa sem inimigos no nível 1
    porta = True  # Porta aparece no nível 1
    porta_sprite = Sprite("templates/porta.png")
    porta_sprite.set_position((janela.width / 2) - 60, (janela.height / 5) * 1)  # Define a posição inicial da porta

    last_key = ""  # Variável para guardar a última tecla pressionada
    
    while True:
        delta_time = janela.delta_time()

        # Movimento do player
        if teclado.key_pressed("W"):
            player.move("W", limites_W, limites_S, limites_A, limites_D, delta_time)
            last_key = "W"
        
        if teclado.key_pressed("S"):
            player.move("S", limites_W, limites_S, limites_A, limites_D, delta_time)
            last_key = "S"
        
        if teclado.key_pressed("A"):
            player.move("A", limites_W, limites_S, limites_A, limites_D, delta_time)
            last_key = "A"

        if teclado.key_pressed("D"):
            player.move("D", limites_W, limites_S, limites_A, limites_D, delta_time)
            last_key = "D"

        # Verifica se não há inimigos
        if len(enemies) == 0 and level > 1:
            porta = True
        else:
            porta = False

        # Movimento dos inimigos
        for enemy in enemies:
            enemy.follow_player(player, delta_time)

        # Condição para voltar ao menu
        if teclado.key_pressed("ESC"):
            return "Menu"  # Retorna ao menu

        # Passar de Fase - Lógica para nível 1
        if level == 1 and player.colide_porta(porta_sprite):
            level += 1
            player.current_sprite.x = (janela.width / 2) - (player.current_sprite.width / 2)
            player.current_sprite.y = (janela.height / 2) - (player.current_sprite.height / 2)
            print(f"Avançou para o nível {level}")

            # Gera inimigos para o nível 2
            enemies = create_enemies(level)

        # Passar de Fase - A partir do nível 2
        if level > 1 and player.colide_porta(porta_sprite) and porta:
            level += 1
            player.current_sprite.x = (janela.width / 2) - (player.current_sprite.width / 2)
            player.current_sprite.y = (janela.height / 2) - (player.current_sprite.height / 2)
            print(f"Avançou para o nível {level}")

            # Gera inimigos para o próximo nível
            enemies = create_enemies(level)

        # Desenho na tela
        arena.draw()
        player.draw()
        for enemy in enemies:
            enemy.draw()
        
        # Renderiza a porta
        if porta:
            porta_sprite.draw()


        janela.update()
