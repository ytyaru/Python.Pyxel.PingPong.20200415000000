#!/usr/bin/env python3
# coding: utf8
import pyxel

class App:
    def __init__(self):
        self.__window = Window()
        globals()['Window'] = self.__window
        self.__box = Box()
        pyxel.run(self.update, self.draw)
    def update(self):
        self.__box.update()
    def draw(self):
        pyxel.cls(4)
        self.__box.draw()

class Window:
    def __init__(self):
        pyxel.init(self.Width, self.Height, border_width=self.BorderWidth, caption=self.Caption, fps=60)
    @property
    def Width(self): return 256
    @property
    def Height(self): return 192
    @property
    def Caption(self): return "Ping Pong"
    @property
    def BorderWidth(self): return 0
    def update(self): pass
    def draw(self): pyxel.cls(0)

class Box:
    def __init__(self):
        self.__pc = PC()
        self.__npc = NPC()
        self.__ball = Ball()
        self.__result = 0
    def update(self):
        if 0 < self.__result: return
        self.__pc.update()
        self.__npc.update()
        self.__ball.update()
        self.__detect_collision()
    def __detect_collision(self):
        if (self.__ball.X-self.__ball.R <= self.__pc.X+self.__pc.W and \
           self.__pc.Y - (self.__ball.R*2) <= self.__ball.Y-self.__ball.R <= self.__pc.Y+self.__pc.H):
           self.__ball.reverse_vx(self.__pc.X+self.__pc.W+self.__ball.R)
        if (self.__npc.X-self.__npc.W <= self.__ball.X+self.__ball.R and \
           self.__npc.Y - (self.__ball.R*2) <= self.__ball.Y-self.__ball.R <= self.__npc.Y+self.__npc.H):
           self.__ball.reverse_vx(self.__npc.X-self.__npc.W-self.__ball.R)
        if self.__ball.X-self.__ball.R <= 0:
            self.__result = 1
        if Window.Width <= self.__ball.X+self.__ball.R:
            self.__result = 2
    def draw(self):
        pyxel.cls(0)
        self.__pc.draw()
        self.__npc.draw()
        self.__ball.draw()
        if   self.__result == 1: pyxel.text(Window.Width // 2 - (8*5/2), Window.Height // 2 - 4,'LOSE...',7)
        elif self.__result == 2: pyxel.text(Window.Width // 2 - (8*5/2), Window.Height // 2 - 4,'WIN !!!',7)

class Ball:
    def __init__(self):
        self.__x = Window.Width // 2
        self.__y = Window.Height // 2
        self.__r = 8
        self.__color = 7
        self.__vx = -1
        self.__vy = 1
    @property
    def X(self): return self.__x
    @property
    def Y(self): return self.__y
    @property
    def R(self): return self.__r
    @property
    def Color(self): return self.__color
    def update(self):
        self.__detect_collision()
        self.__move()
    def __detect_collision(self):
        if self.Y - self.R <= 0 or Window.Height <= self.Y+(self.R): 
            self.__vy *= -1
#        if self.X - self.R <= 0 or Window.Width <= self.X+(self.R): 
#            self.__vx *= -1
    def __move(self):
        self.__x += self.__vx
        self.__y += self.__vy
    def draw(self):
        pyxel.circ(self.X, self.Y, self.R, self.Color)
    def reverse_vx(self, pos):
        self.__vx *= -1
        self.__x = pos
#        print(pos)
        
class Bar:
    def __init__(self, x=0, y=0, w=4, h=32, c=7):
        self.__w = w
        self.__h = h
        self.__x = x
        self.__y = (Window.Height // 2) - (self.__h // 2)
        self.__color = c
    @property
    def X(self): return self.__x
    @property
    def Y(self): return self.__y
    @property
    def W(self): return self.__w
    @property
    def H(self): return self.__h
    @property
    def Color(self): return self.__color
    def update(self):
        self.__move()
    def __move(self):
        if   pyxel.btn(pyxel.KEY_UP):
            if -1 < self.__y: self.__y -= 1
        elif pyxel.btn(pyxel.KEY_DOWN):
            if self.__y < Window.Height - self.H: self.__y += 1;
    def draw(self):
        pyxel.rect(self.X, self.Y, self.W, self.H, self.Color)
class PC(Bar):
    def __init__(self):
        super(self.__class__, self).__init__(x=0, w=4, c=10)
class NPC(Bar):
    def __init__(self):
        super(self.__class__, self).__init__(x=Window.Width-4, c=8)


App()
