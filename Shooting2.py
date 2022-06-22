import pygame
import math
import random

pygame.init()

# Fontes
fonteStatus = pygame.font.SysFont('Unispace', 30)


# Cores
purple = (101,57,163)
black = (0,0,0)
green = (0,255,0)
red = (255,0,0)
white = (255,255,255)

# Setup do display
largura = 1366
altura = 768
dimensao = (largura, altura)
janela = pygame.display.set_mode(dimensao)
pygame.display.set_caption('Shooter')

# variaveis de movimentação
vel_padrao = 5

class Nave(object):
  def __init__(self, char_type, img_number, x, y, speed, life, dano):

      # carrega a imagem
      self.char_type = char_type
      self.img_number = img_number
      self.image = pygame.image.load(f'imagens/{self.char_type}/{self.img_number}.png').convert_alpha()

      # configura o personagem
      self.rect = self.image.get_rect()
      self.rect.center = (x, y)
      self.speed = speed
      self.life = life
      self.dano = dano

  def draw(self):
    janela.blit(self.image, self.rect)

class Tiro(object):
  def __init__(self, x, y, mouse_x, mouse_y):

    self.image = pygame.image.load('imagens/icones/tiro.png')
    self.rect = self.image.get_rect()
    self.x = x
    self.y = y
    self.mouse_x = mouse_x
    self.mouse_y = mouse_y
    self.lifetime = 50
    self.speed = 15
    self.angle = math.atan2(mouse_y - self.y, mouse_x - self.x)
    self.x_vel = math.cos(self.angle) * self.speed
    self.y_vel = math.sin(self.angle) * self.speed
    self.radius = 4

  def draw(self, draw):
    self.x += int(self.x_vel)
    self.y += int(self.y_vel)

    janela.blit(self.image, (self.x, self.y))
    self.lifetime -= 1

def status_tela(mensagem, cor, x, y):
    
    texto = fonteStatus.render(mensagem, 1, cor)
    janela.blit(texto, (x, y))

def main():
  global laser

  # FPS
  FPS = 60
  clock = pygame.time.Clock()

  rodando = True

  player = Nave('player','00', 200, 200, vel_padrao, 0, 5)
  
  tiros = []
  inimigos = []
  level = 0
  wave_length = 0

  while rodando:
    janela.fill(black)

    if len(inimigos) == 0:
      pygame.time.delay(1500)
      level += 1
      wave_length += 1
      player.life += 10
      for i in range(wave_length):
        inimigo_p = Nave('inimigos','00', (random.randrange(largura + 750, largura + 1050)), (random.randrange(25, altura)), 6, 5, 1)
        inimigo_m = Nave('inimigos','01', (random.randrange(largura + 450, largura + 750)), (random.randrange(25, altura)), 4, 10, 3)
        inimigo_g = Nave('inimigos','02', (random.randrange(largura + 100, largura + 450)), (random.randrange(25, altura)), 2, 20, 5)
        inimigos.append(inimigo_p)
        inimigos.append(inimigo_m)
        inimigos.append(inimigo_g)     

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        rodando = False

      if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1:
          x, y = pygame.mouse.get_pos()
          laser = Tiro(player.rect.centerx, player.rect.centery, x, y)
          tiros.append(laser) 

    for tiro in tiros:
      if tiro.lifetime <= 0:
        tiros.remove(tiro)
      tiro.draw(janela)

    for inimigo in inimigos:
      inimigo.rect.centerx -= inimigo.speed
      if inimigo.rect.centerx <= -50:
        player.life -= inimigo.dano
        print(player.life)
        inimigos.remove(inimigo)
      elif inimigo.rect.colliderect(player.rect):
        player.life -= inimigo.dano
        print(player.life)
        inimigos.remove(inimigo)
      elif inimigo.rect.colliderect(laser.rect):
        inimigos.remove(inimigo)

      inimigo.draw()

    status_tela(f'Vida: {player.life}', red, 50, 50)
    status_tela(f'Level: {level}', green, 50, 75)

      # botão pressionado
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
      player.rect.centery -= vel_padrao
    if keys[pygame.K_s]:
      player.rect.centery += vel_padrao
    if keys[pygame.K_a]:
      player.rect.centerx -= vel_padrao
    if keys[pygame.K_d]:
      player.rect.centerx += vel_padrao

    player.draw()

    clock.tick(FPS)
    pygame.display.update()

main()
pygame.quit()
quit()