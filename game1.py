import os
import cfg
import sys
import pygame
import random
from modules import *


'''��Ϸ��ʼ��'''
def initGame():
  # ��ʼ��pygame, ����չʾ����
  pygame.init()
  screen = pygame.display.set_mode(cfg.SCREENSIZE)
  pygame.display.set_caption('catch coins ���� �Ÿ�')
  # ���ر�Ҫ����Ϸ�ز�
  game_images = {}
  for key, value in cfg.IMAGE_PATHS.items():
      if isinstance(value, list):
          images = []
          for item in value: images.append(pygame.image.load(item))
          game_images[key] = images
      else:
          game_images[key] = pygame.image.load(value)
  game_sounds = {}
  for key, value in cfg.AUDIO_PATHS.items():
      if key == 'bgm': continue
      game_sounds[key] = pygame.mixer.Sound(value)
  # ���س�ʼ������
  return screen, game_images, game_sounds


'''������'''
def main():
  # ��ʼ��
  screen, game_images, game_sounds = initGame()
  # ���ű�������
  pygame.mixer.music.load(cfg.AUDIO_PATHS['bgm'])
  pygame.mixer.music.play(-1, 0.0)
  # �������
  font = pygame.font.Font(cfg.FONT_PATH, 40)
  # ����hero
  hero = Hero(game_images['hero'], position=(375, 520))
  # ����ʳ����
  food_sprites_group = pygame.sprite.Group()
  generate_food_freq = random.randint(10, 20)
  generate_food_count = 0
  # ��ǰ����/��ʷ��߷�
  score = 0
  highest_score = 0 if not os.path.exists(cfg.HIGHEST_SCORE_RECORD_FILEPATH) else int(open(cfg.HIGHEST_SCORE_RECORD_FILEPATH).read())
  # ��Ϸ��ѭ��
  clock = pygame.time.Clock()
  while True:
      # --��䱳��
      screen.fill(0)
      screen.blit(game_images['background'], (0, 0))
      # --����ʱ��Ϣ
      countdown_text = 'Count down: ' + str((90000 - pygame.time.get_ticks()) // 60000) + ":" + str((90000 - pygame.time.get_ticks()) // 1000 % 60).zfill(2)
      countdown_text = font.render(countdown_text, True, (0, 0, 0))
      countdown_rect = countdown_text.get_rect()
      countdown_rect.topright = [cfg.SCREENSIZE[0]-30, 5]
      screen.blit(countdown_text, countdown_rect)
      # --�������
      for event in pygame.event.get():
          if event.type == pygame.QUIT:
              pygame.quit()
              sys.exit()
      key_pressed = pygame.key.get_pressed()
      if key_pressed[pygame.K_a] or key_pressed[pygame.K_LEFT]:
          hero.move(cfg.SCREENSIZE, 'left')
      if key_pressed[pygame.K_d] or key_pressed[pygame.K_RIGHT]:
          hero.move(cfg.SCREENSIZE, 'right')
      # --�������ʳ��
      generate_food_count += 1
      if generate_food_count > generate_food_freq:
          generate_food_freq = random.randint(10, 20)
          generate_food_count = 0
          food = Food(game_images, random.choice(['gold',] * 10 + ['apple']), cfg.SCREENSIZE)
          food_sprites_group.add(food)
      # --����ʳ��
      for food in food_sprites_group:
          if food.update(): food_sprites_group.remove(food)
      # --��ײ���
      for food in food_sprites_group:
          if pygame.sprite.collide_mask(food, hero):
              game_sounds['get'].play()
              food_sprites_group.remove(food)
              score += food.score
              if score > highest_score: highest_score = score
      # --��hero
      hero.draw(screen)
      # --��ʳ��
      food_sprites_group.draw(screen)
      # --��ʾ�÷�
      score_text = f'Score: {score}, Highest: {highest_score}'
      score_text = font.render(score_text, True, (0, 0, 0))
      score_rect = score_text.get_rect()
      score_rect.topleft = [5, 5]
      screen.blit(score_text, score_rect)
      # --�ж���Ϸ�Ƿ����
      if pygame.time.get_ticks() >= 90000:
          break
      # --������Ļ
      pygame.display.flip()
      clock.tick(cfg.FPS)
  # ��Ϸ����, ��¼��߷ֲ���ʾ��Ϸ��������
  fp = open(cfg.HIGHEST_SCORE_RECORD_FILEPATH, 'w')
  fp.write(str(highest_score))
  fp.close()
  return showEndGameInterface(screen, cfg, score, highest_score)


'''run'''
if __name__ == '__main__':
  while main():
      pass