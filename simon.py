#!/usr/bin/env python3
# Simon Says Game
# Author: Paweł Krzemiński
# Modified LiveWires module from "Python for absolute beginers book" by Michael Dawson

import random, time
from livewires import games, color

games.init(screen_width = 300, screen_height = 480, fps = 50)

class Wrapper(games.Sprite):

     def update(self):
        """Detect mouse click over object, debouncing included and call turn()"""
        self.count +=1
        if games.mouse.is_pressed(0) and\
                self.right > games.mouse.x > self.left and\
                self.bottom > games.mouse.y > self.top and\
                self.count > 30:
            self.turn()

        if self.is_on and self.count > 50:
            self.set_image(self.off_image)
            self.is_on = False

     def sequence_play(self):
        id = self.game.buttons.index(self)
        if self.game.sequence[self.game.seq_step] == self.id and\
                int(time.time()) > self.game.seq_last_time:
            self.game.seq_last_time = int(time.time())
            self.turn()
            self.game.seq_step+=1
            if self.game.seq_step == 50: self.game.seq_step = 0

class Button(Wrapper):
    """ RGB Button that lights up"""
    red_bmp = (games.load_image("media/red_off.bmp"),
              games.load_image("media/red_on.bmp"))
    green_bmp = (games.load_image("media/green_off.bmp"),
              games.load_image("media/green_on.bmp"))
    blue_bmp = (games.load_image("media/blue_off.bmp"),
              games.load_image("media/blue_on.bmp"))
    images = (red_bmp, green_bmp, blue_bmp)

    def __init__ ( self, x, y, img, game):
        self.off_image = Button.images[img][0]
        self.on_image = Button.images[img][1]
        super(Button, self).__init__(image = self.off_image, x=x, y=y)
        self.count = 0
        self.is_on = False
        self.game = game

   # def update(self):
   #     super(Button, self).update()

    def turn(self):
        """Change the state and image off the button"""
        if not self.is_on:
            self.is_on = True
            self.set_image(self.on_image)
            self.count = 0


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

    def turn(self):
        """Change the state and image off the button"""
        if not self.is_on:
            self.is_on = True
            self.set_image(self.on_image)
            self.sound.play()
            self.count = 0

class Game():
    def __init__(self):
        self.buttons = [Button(x=50, y=50, img=0, game=self),
                Button(x=150, y=50, img=1, game=self),
                Button(x=250, y=50, img=2, game=self),
                Instrumental(x=50, y=150, img=0, game=self),
                Instrumental(x=150, y=150, img=1, game=self),
                Instrumental(x=250, y=150, img=2, game=self)]

        for button in self.buttons:
            games.screen.add(button)

        self.seq_step = 0
        self.sequence = []
        self.seq_last_time = int(time.time()) 
        self.player_seq = []
        for i in range(50):
            self.sequence.append(random.randrange(6))

        games.mouse.is_visible = True
        games.screen.event_grab = True
        games.screen.mainloop()

    def play(self):
        pass


game = Game()
