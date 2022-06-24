import pygame
import random

pygame.init()
pygame.mixer.init()

# Sons
som_morte = pygame.mixer.Sound('sons/som_Morte.mp3')
som_dano = pygame.mixer.Sound('sons/som_Dano.mp3')
som_canhao = pygame.mixer.Sound('sons/som_canhao.mp3')
som_laser = pygame.mixer.Sound('sons/som_Laser.mp3')
som_explosao = pygame.mixer.Sound('sons/som_Explosao.mp3')

som_laser.set_volume(0.1)
som_canhao.set_volume(0.2)
som_explosao.set_volume(0.4)
som_dano.set_volume(0.5)
som_morte.set_volume(0.6)

# Música
pygame.mixer.music.load('sons/musica.mp3')
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(-1)

# Fontes
fonteStatus = pygame.font.SysFont('Unispace', 30)
fontePontos = pygame.font.SysFont('Unispace', 40)
fonteMenu2 = pygame.font.SysFont('Unispace', 50)
fonteMenu = pygame.font.SysFont('Unispace', 70)
fonteTitulo = pygame.font.SysFont('Unispace', 80)

# Cores
purple = (101,57,163)
black = (0,0,0)
green = (0,255,0)
red = (255,0,0)
white = (255,255,255)
blue = (0,0,255)
magenta = (255,0,255)
orange = (255, 102, 0)

# Setup do display
largura = 1366
altura = 768
dimensao = (largura, altura)
janela = pygame.display.set_mode(dimensao)
pygame.display.set_caption('Space Wars')

# Variáveis do jogo
move_left = False
move_right = False
move_up = False
move_down = False
shoot = False
troca = False

bonusLaser_dmg = 0
bonusCanhao_dmg = 0
cd_mod = 0
laserCooldown = 0
canhaoCooldowm = 0

inimigos = []
level = 0
wave_length = 0
pontos = 0

class Nave(pygame.sprite.Sprite):
  def __init__(self, char_type, img_number, x, y, speed, dmg, life):
      pygame.sprite.Sprite.__init__(self)
      # carrega as imagens
      self.char_type = char_type
      self.img_number = img_number
      self.image = pygame.image.load(f'imagens/{self.char_type}/{self.img_number}.png').convert_alpha()

      # configura o personagem
      self.rect = self.image.get_rect()
      self.rect.center = (x, y)
      self.speed = speed 
      self.life = life
      self.laser_cooldown = 0
      self.canhao_cooldown = 0
      self.dmg = dmg
      self.shoot_dmg = 0

  def draw(self):
    janela.blit(self.image, self.rect)

  def move(self, move_left, move_right, move_up, move_down):
    dx = 0
    dy = 0

    if move_left and player.rect.left > (largura - largura):
      dx -= self.speed
    if move_right and player.rect.right < largura:
      dx += self.speed
    if move_up and player.rect.top > (altura - altura):
      dy -= self.speed
    if move_down and player.rect.bottom < altura:
      dy += self.speed

    self.rect.x += dx
    self.rect.y += dy

  def shoot(self):
    if self.canhao_cooldown == 0 and troca:
      self.canhao_cooldown = 300
      self.shoot_dmg = 25 + bonusCanhao_dmg
      pygame.mixer.Sound.play(som_canhao)
      tiro = Tiro((self.rect.centerx + self.rect.size[0] * 0.7), self.rect.centery)
      tiro_group.add(tiro)
    elif self.laser_cooldown == 0 and not troca:
      self.laser_cooldown = 20 - cd_mod
      self.shoot_dmg = 25 + bonusLaser_dmg
      pygame.mixer.Sound.play(som_laser)
      tiro = Tiro((self.rect.centerx + self.rect.size[0] * 0.7), self.rect.centery)
      tiro_group.add(tiro)
      
  def update(self):
    if self.laser_cooldown > 0:
      self.laser_cooldown -= 1
    if self.canhao_cooldown > 0:
      self.canhao_cooldown -= 1
    
class Tiro(pygame.sprite.Sprite):
  def __init__(self, x, y):
    pygame.sprite.Sprite.__init__(self)
    # carrega a imagem
    if troca:
      img_number = '00'
    if not troca:
      img_number = '01'
    self.img_number = img_number
    self.image = pygame.image.load(f'imagens/icones/{self.img_number}.png').convert_alpha()

    # configura o tiro
    self.rect = self.image.get_rect()
    self.rect.center = (x, y)
    self.speed = 10
    
  def update(self):
    global bonusLaser_dmg
    global bonusCanhao_dmg
    global pontos

    # atira
    self.rect.x += self.speed

    # remove os tiros fora da tela
    if self.rect.left > largura:
      self.kill()

    # calcula colisão dos tiros
    for inimigo in inimigos:
      if pygame.sprite.spritecollide(inimigo, tiro_group, False):
        if not troca:
          self.kill()
        inimigo.life -= player.shoot_dmg
        print('Enemy HP: ', inimigo.life)
        if inimigo.life <= 0:
          pygame.mixer.Sound.play(som_explosao)
          inimigos.remove(inimigo)
          pontos += 1
          # concede um bonus por abate
          bonusLaser_dmg += 1 
          bonusCanhao_dmg += 15

def status_tela(mensagem, cor, x, y):
  global texto_status
  texto_status = fonteStatus.render(mensagem, 1, cor)
  janela.blit(texto_status, (x, y))

# cria grupos de sprites
tiro_group = pygame.sprite.Group()

# personagens
player = Nave('player', '00', 350, 350, 5, 0, 75)

def mensagem_tela(mensagem, cor):
  pygame.time.delay(1000)
  janela.fill(black)
  texto = fonteMenu.render(mensagem, 1, cor)
  janela.blit(texto, ((largura/2 - texto.get_width()/2), (altura/2 - texto.get_height()/2)))
  status_tela(f'Sua pontuação: {pontos}', white, (largura/2 - (texto_status.get_width()/2 - 50)), (altura/1.7 - texto_status.get_height()/2))
  pygame.display.update()    
  pygame.time.delay(5000)

def main_menu():
  global level 
  global wave_length 
  global pontos 

  janela.fill(black)

  inimigos.clear()
  level = 0
  wave_length = 0
  pontos = 0

  # Setup do looping do jogo
  FPS = 60
  clock = pygame.time.Clock()
  rodando = True

  while rodando:
    clock.tick(FPS)
    
    botaoJogar = fonteMenu.render('Pressione ENTER para jogar', 1, white)
    janela.blit(botaoJogar, ((largura/2 - botaoJogar.get_width()/2), (altura/2.2 - botaoJogar.get_height()/2)))
    botaoBotoes = fonteMenu2.render('Como jogar', 1, white)
    janela.blit(botaoBotoes, ((largura/2 - botaoBotoes.get_width()/2), (altura/1.7 - botaoBotoes.get_height()/2)))
    pygame.display.update()

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
          pygame.quit()
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RETURN:
          main()
      if event.type == pygame.MOUSEBUTTONDOWN:
        menu_mouse_x, menu_mouse_y = pygame.mouse.get_pos()
        print(menu_mouse_x, menu_mouse_y)
        if 785 > menu_mouse_x > 585 and 465 > menu_mouse_y > 435:
          comandos()
      
def comandos():
  # Setup do looping do jogo
  FPS = 60
  clock = pygame.time.Clock()
  rodando = True

  while rodando:
    clock.tick(FPS)
    janela.fill(white)

    teclas = pygame.image.load('imagens/teclas/teclas.png')

    janela.blit(teclas, (0,0))
    
    botaoVoltar = fonteMenu.render('Voltar', 1, black)
    janela.blit(botaoVoltar, ((largura - 200), (altura - 100)))
    pygame.display.update()

    
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
          pygame.quit()
      if event.type == pygame.MOUSEBUTTONDOWN:
        op_mouse_x, op_mouse_y = pygame.mouse.get_pos()
        print(op_mouse_x, op_mouse_y)
        if 1310 > op_mouse_x > 1165 and 710 > op_mouse_y > 670:
          main_menu()
    
def main():
  global inimigos
  global move_left
  global move_right
  global move_up
  global move_down
  global shoot
  global troca
  global level
  global wave_length
  global pontos
  global cd_mod

# FPS
  FPS = 60
  clock = pygame.time.Clock()

  rodando = True

  while rodando:
    clock.tick(FPS)
    janela.fill(black)

    # desenha e configura personagens e icones
    player.draw()
    player.move(move_left, move_right, move_up, move_down)
    player.update()  

    # desenha grupos
    tiro_group.update()
    tiro_group.draw(janela)

    if shoot:
      player.shoot()

    # gera inimigos
    if len(inimigos) == 0:
      level += 1
      wave_length += 1
      player.life += 25
      pontos += 10
      for i in range(wave_length):
        inimigo_m = Nave('inimigos','01', (random.randrange(largura + 750, largura + 1250)), (random.randrange(45, altura - 55)), 3, 30, 100)
        inimigo_g = Nave('inimigos','02', (random.randrange(largura + 50, largura + 550)), (random.randrange(55, altura - 55)), 1, 50, 200)
        inimigo_boss = Nave('inimigos','03', (largura + 1000), (altura/2 - 150), 0.5, player.life, 3500)
        inimigos.append(inimigo_m)
        inimigos.append(inimigo_g)
        print(f"Inimigos adicionados: {inimigos}")
        print(f"Lista inimigos: {len(inimigos)}")

      if (level%5) == 0:     
        inimigo_boss.life += 1500
        inimigos.append(inimigo_boss)

      if (level%2) == 0:
        inimigo_m.life += 25
        inimigo_g.life += 100
        cd_mod += 1

      if level == (6, 11, 16, 21, 26, 31):
        pontos += 100

    for inimigo in inimigos:
      inimigo.rect.centerx -= inimigo.speed
      # remove inimigos da tela quando passam do fim
      if inimigo.rect.centerx < 0:
        player.life -= inimigo.dmg
        pygame.mixer.Sound.play(som_dano)
        print(player.life)
        inimigos.remove(inimigo)
      # checa a colisão do jogador com inimigos
      elif inimigo.rect.colliderect(player.rect):
        player.life -= inimigo.dmg
        pygame.mixer.Sound.play(som_dano)
        print(player.life)
        inimigos.remove(inimigo)
      
      inimigo.draw()

    if player.life <= 0:
      pygame.mixer.Sound.play(som_morte)
      mensagem_tela('Você MORREU!', red)
      main_menu()

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()

      # botões pressionados
      if event.type == pygame.QUIT:
        rodando = False
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT:
          move_left = True
        if event.key == pygame.K_RIGHT:
          move_right = True
        if event.key == pygame.K_UP:
          move_up = True
        if event.key == pygame.K_DOWN:
          move_down = True
        if event.key == pygame.K_SPACE:
          shoot = True
        if event.key == pygame.K_2:
          troca = True

      # botões soltos
      if event.type == pygame.KEYUP:
        if event.key == pygame.K_LEFT:
          move_left = False
        if event.key == pygame.K_RIGHT:
          move_right = False
        if event.key == pygame.K_UP:
          move_up = False
        if event.key == pygame.K_DOWN:
          move_down = False
        if event.key == pygame.K_SPACE:
          shoot = False
        if event.key == pygame.K_1:
          troca = False

    # mostra informações na tela
    status_tela(f'Vida: {player.life}', red, 50, 50)
    status_tela(f'Level: {level}', green, 50, 75)
    status_tela(f'Pontuação: {pontos}', white, largura - 350, 75)
    if troca:
      status_tela(f'Arma: Canhão', orange, largura - 350, 50)
    if not troca:
      status_tela(f'Arma: Laser', magenta, largura - 350, 50)      

    pygame.display.update()

main_menu()
pygame.quit()
quit() 