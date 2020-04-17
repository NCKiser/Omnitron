import copy
import csv
import os

import pygame

import settings
from enemy import EnemyPrototype, Enemy
from settings import KEYS


class EnemyQueue:
    def __init__(self):
        self.times = dict()

    def enqueue(self, ep):
        notes_to_play = None
        try:
            notes_to_play = self.times.get(ep.appear_time)
        except KeyError as e:
            print(e)
        if notes_to_play is None:
            self.times[ep.appear_time] = list()
        self.times[ep.appear_time].append(ep)

    def dequeue(self):
        """ returns the earliest list of enemies and the time at which they are to appear"""
        min_time = self.time()
        return self.times.pop(min_time)

    def time(self):
        try:
            return min(list(self.times.keys()))
        except ValueError:
            return None

    def __str__(self):
        return str(self.times)


class Level:

    def __init__(self, level_name):
        self.current_enemies = pygame.sprite.Group()
        self.enemy_queue = EnemyQueue()
        self.populate(level_name)

    def populate(self, level_name):
        with open(os.path.join("music", level_name)) as level_file:
            print(os.path.join("music", level_name))
            for row in csv.reader(level_file):
                try:
                    if row[0] != 'appear_time' and row[0] != '#' and row[0] != '//':
                        appear_time = float(row[0])
                        key = int(row[1]) % KEYS
                        instrument = row[2].strip()
                        note = row[3].strip()
                        sprite = settings.ENEMY_SPRITES[key]
                        difficulty = int(row[4])
                        music_only = False
                        if difficulty > settings.PLAYER_DIFFICULTY:
                            music_only = True
                        try:
                            ep = EnemyPrototype(appear_time=appear_time * settings.tempo, player_key=key,
                                                note=note, instrument=instrument, sprite_option=sprite,
                                                music_only=music_only)
                            self.enemy_queue.enqueue(ep)
                        except Exception as e:
                            print("Could not create Enemy")
                            print(e)
                except IndexError as e:
                    pass
                except FileNotFoundError as f:
                    print(f)
                    print(os.path.join(instrument, note))
        print("Level:")
        print(str(self.enemy_queue))

    def shoot(self, key, time):
        try:
            key = settings.key_map[key]
        except KeyError:
            print("non-mapped key pressed")
        for enemy in self.current_enemies:
            print(key, enemy.player_key)
            if enemy.player_key == key and not enemy.dead and (enemy.play_time - enemy.TOLERANCE <= time <= enemy.end_time + enemy.TOLERANCE):
                enemy.shot_attempt(time)
                break

    def update(self, time):
        while self.enemy_queue.time() is not None and time > self.enemy_queue.time():
            print(time, self.enemy_queue.time())
            enemies = self.enemy_queue.dequeue()
            if enemies:
                for enemy in enemies:
                    self.current_enemies.add(Enemy(enemy))
        self.current_enemies.update(time)

    def draw(self, surface):
        self.current_enemies.draw(surface)

    def done(self):
        return len(self.enemy_queue.times) == 0 and len(self.current_enemies) == 0
