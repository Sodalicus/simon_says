#!/usr/bin/env python3
# Simon Says Game
# Author: Paweł Krzemiński
# Modified LiveWires module from "Python for absolute beginers book" by Michael Dawson

import random, time
from livewires import games, color

games.init(screen_width = 300, screen_height = 300, fps = 50)

class Wrapper(games.Sprite):

    def update(self):
        self.count += 1
        """Detect mouse click over object, debouncing included and call turn()"""
        if games.mouse.is_pressed(0) and\
                self.right > games.mouse.x > self.left and\
                self.bottom > games.mouse.y > self.top and\
                (time.time()-self.game.seq_last_time) > 0.5:

            self.game.seq_last_time = time.time()
            self.game.add_player_seq(self.game.buttons.index(self))
            self.turn()

        self.game.sequence_play()

        if self.is_on and self.count > 50:
            self.set_image(self.off_image)
            self.is_on = False

    def turn(self):
        """Change the state and image off the button"""
        if not self.is_on:
            self.is_on = True
            self.set_image(self.on_image)
            self.sound.play()
            self.count = 0



class Button(Wrapper):
    """ RGB Button that lights up"""
    red_bmp = (games.load_image("media/red_off.bmp"),
              games.load_image("media/red_on.bmp"),
              games.load_sound("media/red.wav"))
    green_bmp = (games.load_image("media/green_off.bmp"),
              games.load_image("media/green_on.bmp"),
              games.load_sound("media/green.wav"))
    blue_bmp = (games.load_image("media/blue_off.bmp"),
              games.load_image("media/blue_on.bmp"),
              games.load_sound("media/blue.wav"))
    media = (red_bmp, green_bmp, blue_bmp)

    def __init__ ( self, x, y, img, game):
        self.off_image = Button.media[img][0]
        self.on_image = Button.media[img][1]
        self.sound = Button.media[img][2]
        super(Button, self).__init__(image = self.off_image, x=x, y=y)
        self.count = 0
        self.is_on = False
        self.game = game

   # def update(self):
   #     super(Button, self).update()


class Instrumental(Wrapper):

    guitar = (games.load_image("media/guitar.bmp", transparent = False),
            games.load_image("media/guitar_inv.bmp", transparent = False),
            games.load_sound("media/guitar.wav"))

    drums = (games.load_image("media/drums.bmp", transparent = False),
            games.load_image("media/drums_inv.bmp", transparent = False),
            games.load_sound("media/drums.wav"))

    hat = (games.load_image("media/hat.bmp", transparent = False),
            games.load_image("media/hat_inv.bmp", transparent = False),
            games.load_sound("media/hat.wav"))

    media = (guitar, drums, hat)

    def __init__(self, x, y, img, game):
       self.on_image = Instrumental.media[img][0]
       self.off_image = Instrumental.media[img][1]
       self.sound = Instrumental.media[img][2]
       super(Instrumental, self).__init__(image = self.off_image, x=x, y=y)
       self.count = 0
       self.is_on = False
       self.game = game

class Game():
    WIDTH = 300
    HEIGHT = 300
    def __init__(self):
        self.buttons = [Button(x=50, y=50, img=0, game=self),
                Button(x=150, y=50, img=1, game=self),
                Button(x=250, y=50, img=2, game=self),
                Instrumental(x=50, y=150, img=0, game=self),
                Instrumental(x=150, y=150, img=1, game=self),
                Instrumental(x=250, y=150, img=2, game=self)]

        for button in self.buttons:
            games.screen.add(button)
        self.level = 1 
        self.seq_step =  0
        self.sequence = []
        self.seq_last_time = time.time()
        self.player_seq = []
        self.player_seq_step = 0
        self.seq_playing = True
        for i in range(15):
            self.sequence.append(random.randrange(6))
        print(self.sequence)

        self.text_level = games.Text(value = self.level, size=60, color=color.red, bottom = Game.HEIGHT-20, left = Game.WIDTH-20 )
        games.screen.add(self.text_level)

        self.text_step = games.Text(value = self.seq_step, size=60, color=color.blue, bottom = Game.HEIGHT-20, left = 20 )
        games.screen.add(self.text_step)


        games.mouse.is_visible = True
        games.screen.event_grab = True
        games.screen.mainloop()



    def sequence_play(self):
        """Play sequence if self.game.seq_playing == True, wait for a second between each iteration.
        Play that many steps as self.game.seq_step """
        for seq_id in self.sequence[:self.level]:
            if time.time()-self.seq_last_time > 1.0\
                    and self.seq_playing == True:
                self.seq_last_time = time.time()
                button = self.sequence[self.seq_step]
                self.buttons[button].turn()
                if self.seq_step < self.level: self.seq_step +=1
                if self.seq_step == self.level: 
                    self.seq_playing = False
                    self.seq_step = 0
                    self.text_level.set_color(color.green)

    def add_player_seq(self, id):
        """Add players click to player`s sequnce list, so we can compare it with main sequence later"""

        if id  == self.sequence[self.seq_step]:
            self.player_seq.append(id)
            self.seq_step +=1
            self.text_step.set_value(self.seq_step)
        elif id != self.sequence[self.seq_step]:
            self.exit_message = games.Message(value = "Failure", size = 90,\
                    color = color.red, bottom = Game.HEIGHT-30, left = 50, lifetime = 120, after_death = games.screen.quit)
            games.screen.add(self.exit_message)

        if self.seq_step == self.level:
            self.seq_step = 0
            self.text_step.set_value(self.seq_step)
            self.level += 1
            self.text_level.set_value(self.level)
            self.text_level.set_color(color.red)
            self.seq_playing = True


game = Game()
