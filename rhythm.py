import pyxel
import random

class App:
    def __init__(self):
        pyxel.init(160, 120)
        pyxel.load("rhythm_game.pyxres")

        self.game_state = "title"  # title, game
        self.current_beat = 0
        self.target_beat = 4
        self.score = 0
        self.message = ""
        self.character_x = 80
        self.character_y = 100
        self.character_frame = 0
        self.is_jumping = False
        self.jump_speed = 0
        self.gravity = 1
        self.failed_frame = -1
        self.particles = []

        pyxel.run(self.update, self.draw)

    def update(self):
        if self.game_state == "title":
            # タイトル画面の処理
            if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A):
                self.game_state = "game"  # スペースキーでゲーム開始
                self.score = 0 # スコアを初期化
        elif self.game_state == "game":
            # ゲーム画面の処理
            self.current_beat = (self.current_beat + 0.25) % 8
            self.character_frame = (pyxel.frame_count // 15) % 4

            if pyxel.btnp(pyxel.KEY_SPACE) and not self.is_jumping:
                self.is_jumping = True
                self.jump_speed = -10

            if self.is_jumping:
                self.character_y += self.jump_speed
                self.jump_speed += self.gravity

                if self.character_y >= 100:
                    self.character_y = 100
                    self.is_jumping = False
                    self.jump_speed = 0

            if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A):
                if abs(self.current_beat - self.target_beat) < 1:
                    self.score += 10
                    self.message = "Perfect!"
                    pyxel.play(0, 0)
                    self.create_particles(self.character_x + 8, self.character_y + 8, 10)
                else:
                    self.score -= 5
                    self.message = "Miss..."
                    pyxel.play(0, 1)
                    self.failed_frame = pyxel.frame_count

            # パーティクルの更新
            for particle in self.particles:
                particle.update()
            self.particles = [particle for particle in self.particles if particle.lifetime > 0]

    def draw(self):
        if self.game_state == "title":
            # タイトル画面の描画
            pyxel.cls(7) # 背景色
            # 画像を大きく表示
            pyxel.blt(0, 0, 1, 0, 0, 160, 120, 0) # image bank 1 全体を描画

            pyxel.text(20, 100, "PRESS SPACE KEY", 0)  # 文字色を黒に設定
        elif self.game_state == "game":
            # ゲーム画面の描画
            pyxel.cls(7)
            pyxel.text(10, 10, "Score: {}".format(self.score), 0)
            pyxel.text(10, 20, self.message, 0)

            # タイミングを示すバーを一番下に描画
            bar_width = 20
            bar_x = self.current_beat * (pyxel.width / 8) - bar_width / 2
            bar_y = 110
            bar_height = 5
            pyxel.rect(bar_x, bar_y, bar_width, bar_height, 8)

            # 押すべきタイミングを示す印
            target_x = self.target_beat * (pyxel.width / 8)
            target_y = 105
            pyxel.rect(target_x - 2, target_y, 4, 10, 10)

            # キャラクターを描画
            if self.failed_frame != -1 and pyxel.frame_count - self.failed_frame < 8:
                pyxel.blt(self.character_x, self.character_y, 0, 64, 0, 16, 16, 0)
            else:
                pyxel.blt(self.character_x, self.character_y, 0, self.character_frame * 16, 0, 16, 16, 0)

            # パーティクルの描画
            for particle in self.particles:
                particle.draw()

    def create_particles(self, x, y, num):
        for _ in range(num):
            self.particles.append(Particle(x, y))

class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = random.uniform(-2, 2)
        self.vy = random.uniform(-5, -1)
        self.lifetime = 15
        self.color = random.randint(8, 15)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.5
        self.lifetime -= 1

    def draw(self):
        pyxel.pset(self.x, self.y, self.color)

App()