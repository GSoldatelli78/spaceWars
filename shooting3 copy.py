
from turtle import right
import pygame
import random

pygame.init()

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
pygame.display.set_caption('ESSE VAI')

# Variáveis do jogo
move_left = False
move_right = False
move_up = False
move_down = False
shoot = False
troca = False

bonusLaser_dmg = 0
bonusCanhao_dmg = 0
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

    if move_left:
      dx -= self.speed
    if move_right:
      dx += self.speed
    if move_up:
      dy -= self.speed
    if move_down:
      dy += self.speed

    self.rect.x += dx
    self.rect.y += dy

  def shoot(self):
    if self.canhao_cooldown == 0 and troca:
      self.canhao_cooldown = 500
      self.shoot_dmg = 15 + bonusCanhao_dmg
      tiro = Tiro((self.rect.centerx + self.rect.size[0] * 0.7), self.rect.centery)
      tiro_group.add(tiro)
    elif self.laser_cooldown == 0 and not troca:
      self.laser_cooldown = 15
      self.shoot_dmg = 25 + bonusLaser_dmg
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
          inimigos.remove(inimigo)
          pontos += 1
          # concede um bonus por abate
          bonusLaser_dmg += 2 
          bonusCanhao_dmg += 10

def status_tela(mensagem, cor, x, y):
  texto = fonteStatus.render(mensagem, 1, cor)
  janela.blit(texto, (x, y))

# cria grupos de sprites
tiro_group = pygame.sprite.Group()

# personagens
player = Nave('player', '00', 350, 350, 7, 0, 75)

def mensagem_tela(mensagem, cor):
  pygame.time.delay(1000)
  janela.fill(black)
  texto = fonteMenu.render(mensagem, 1, cor)
  janela.blit(texto, ((largura/2 - texto.get_width()/2), (altura/2 - texto.get_height()/2)))
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
      
      botaoJogar = fonteMenu.render('Jogar', 1, white)
      janela.blit(botaoJogar, ((largura/2 - botaoJogar.get_width()/2), (altura/2 - botaoJogar.get_height()/2)))
      pygame.display.update()

      for event in pygame.event.get():
          if event.type == pygame.QUIT:
              pygame.quit()
          if event.type == pygame.MOUSEBUTTONDOWN:
              menu_mouse_x, menu_mouse_y = pygame.mouse.get_pos()
              if 760 > menu_mouse_x > 615 and 390 > menu_mouse_y > 360:
                  main()

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
      for i in range(wave_length):
        inimigo_m = Nave('inimigos','01', (random.randrange(largura + 750, largura + 1250)), (random.randrange(45, altura - 55)), 3, 30, 100)
        inimigo_g = Nave('inimigos','02', (random.randrange(largura + 50, largura + 550)), (random.randrange(55, altura - 55)), 1, 50, 200)
        inimigo_boss = Nave('inimigos','03', (largura + 1000), (altura/2 - 150), 0.5, player.life, 5000)
        inimigos.append(inimigo_m)
        inimigos.append(inimigo_g)
        print(f"Inimigos adicionados: {inimigos}")
        print(f"Lista inimigos: {len(inimigos)}")

      if (level%5) == 0:     
        inimigos.append(inimigo_boss)

      if (level%3) == 0:
        inimigo_m.life += 100
        inimigo_g.life += 150

    for inimigo in inimigos:
      inimigo.rect.centerx -= inimigo.speed
      # remove inimigos da tela quando passam do fim
      if inimigo.rect.centerx < 0:
        player.life -= inimigo.dmg
        print(player.life)
        inimigos.remove(inimigo)
      # checa a colisão do jogador com inimigos
      elif inimigo.rect.colliderect(player.rect):
        player.life -= inimigo.dmg
        print(player.life)
        inimigos.remove(inimigo)
      
      inimigo.draw()

    if player.life <= 0:
      mensagem_tela('Você MORREU!', red)

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
    if (level%5) == 0:
      status_tela(f'BOSS LEVEL!', purple, largura/2 - (texto.get_width/2), 50)

    pygame.display.update()

main_menu()
pygame.quit()
quit() 