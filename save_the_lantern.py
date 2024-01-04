import pyxel
import PyxelUniversalFont as puf

fire_list = []
enemy_list = []

class App:
    def __init__(self):
        pyxel.init(240, 180)
        
        pyxel.colors[7] = 0xFFFFFF
        pyxel.colors[12] = 0xE03B90
        pyxel.colors[6] = 0x66DCE9
        pyxel.colors[10] = 0xFCEE7C

        self.chara_x = 0
        self.chara_y = 100
        self.ene_delete_count = 0
        self.ene_reached = 0

        pyxel.load("./vis.pyxres")
        self.writer = puf.Writer("misaki_gothic.ttf")

        for i in range(5):
            enemy_list.append(Enemy(200+i*15+pyxel.rndi(2, 20), 150, 1))

        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        if pyxel.btnp(pyxel.KEY_SPACE):
            if self.ene_reached == 0:
                if len(fire_list) < 6:
                    fire_list.append(Fire(self.chara_x, self.chara_y))
        
        if len(fire_list) > 0:
            for i in reversed(range(len(fire_list))):
                fire_list[i].update()
                if fire_list[i].frame <= 0:
                    fire_list.pop(i)
        if self.ene_reached == 0:
            if pyxel.btn(pyxel.KEY_W):
                self.chara_y -= 1 + self.ene_delete_count/10
            elif pyxel.btn(pyxel.KEY_S):
                self.chara_y += 1 + self.ene_delete_count/10
            if self.chara_y < 0:
                self.chara_y = 0
            elif self.chara_y > 140:
                self.chara_y = 140

            if pyxel.btn(pyxel.KEY_A):
                self.chara_x -= 1 + self.ene_delete_count/10
            elif pyxel.btn(pyxel.KEY_D):
                self.chara_x += 1 + self.ene_delete_count/10
            if self.chara_x < 0:
                self.chara_x = 0


            

            if len(enemy_list) > 0:
                for i in reversed(range(len(enemy_list))):
                    enemy_list[i].update()
                    if enemy_list[i].x <= 10:
                        self.ene_reached = 1

            if len(fire_list) > 0 and len(enemy_list) > 0:
                for i in range(len(fire_list)):
                    if fire_list[i].y > 150:
                        for j in reversed(range(len(enemy_list))):
                            diff = enemy_list[j].x - fire_list[i].x
                            if diff < 10 and diff > 0:
                                enemy_list.pop(j)
                                self.ene_delete_count += 1
                                
            if len(enemy_list) < 6:
                for i in range(6 - len(enemy_list)):
                    enemy_list.append(Enemy(240+i*15+pyxel.rndi(2, 20), 150, 1+self.ene_delete_count/10))

    def draw(self):
        pyxel.cls(7)

        #self.draw_color()

        pyxel.rect(0, 0, 240, 160, 5)
        pyxel.rect(0, 160, 240, 20, 3)
        self.writer.draw(10, 10, "save the lantern!", 20, 12)

        # moon 
        pyxel.circ(200, 60, 20, 10)
        pyxel.circ(190, 50, 25, 5)

        #self.writer.draw(190, 10, "score", 12, 12)
        #self.writer.draw(190, 20, str(self.ene_delete_count), 12, 12)
        pyxel.text(190, 10, "score: "+str(self.ene_delete_count), 12)


        if pyxel.frame_count % 60 > 30:
            pyxel.blt(10, 144, 0, 32, 120, 16, 16, 0)
        else:
            pyxel.blt(10, 144, 0, 48, 120, 16, 16, 0)

        if len(enemy_list) > 0:
            for i in reversed(range(len(enemy_list))):
                enemy_list[i].draw()

        if len(fire_list) > 0:
            for i in reversed(range(len(fire_list))):
                fire_list[i].draw()
        self.draw_chara(self.chara_x, self.chara_y)

        if self.ene_reached == 1:
            self.writer.draw(11, 70, "GAME OVER", 50, 12)

    def draw_chara(self, x, y):
        if pyxel.frame_count % 30 > 15:
            pyxel.blt(x, y, 0, 0, 136, -32, 16, 5)
        else:
            pyxel.blt(x, y, 0, 0, 152, -32, 16, 5)

    def draw_color(self):
        for i in range(16):
            pyxel.rect(10+i*15, 185, 10, 10, i)

class Fire:
    def __init__(self, x, y):
        self.x = x + 32
        self.y = y + 10
        self.frame = 100

    def update(self):
        self.frame -= 5
        self.x += 2
        self.y += 3
        if self.y >= 160:
            self.frame = 0

    def draw(self):
        if pyxel.frame_count % 10 > 5:
            pyxel.blt(self.x, self.y, 0, 32, 136, -16, 16, 0)
        else:
            pyxel.blt(self.x, self.y, 0, 32, 152, -16, 16, 0)
        

class Enemy:
    def __init__(self, x, y, move):
        self.x = x
        self.y = y
        self.move = move
        self.move_frame = pyxel.rndi(20, 60)

    def update(self):
        if pyxel.frame_count % self.move_frame < self.move_frame/3:
            self.x -= self.move

    def draw(self):
        if pyxel.frame_count % 30 > 15:
            pyxel.blt(self.x, self.y, 0, 48, 136, 16, 16, 0)
        else:
            pyxel.blt(self.x, self.y, 0, 48, 152, 16, 16, 0)
App()
