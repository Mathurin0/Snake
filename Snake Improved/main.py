import tkinter as tk
import random

WIDTH = 500
HEIGHT = 500
SNAKE_BLOCK = 10

class Snake:
    def __init__(self):
        # Variables de la fenetre
        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT)
        self.canvas.pack()

        self.init_game()

    def init_game(self):
        # Variables du serpent
        self.snake_positions = [(250, 250)]
        self.snake_segments = []
        self.obstacles_positions = []
        self.direction = "Right"
        self.last_direction = "Right"
        self.score = 0
        self.is_game_over = False

        # Variables pour les bonus et malus
        self.obstacle_reset_counter = 0
        self.speed_modifier = 1
        self.obstacle_modifier = 1
        self.bonus_time = 0
        self.malus_time = 0
        self.bonus_type = 0
        self.malus_type = 0
        self.controls_inverted = False
        self.bonus_position = self.create_bonus()
        self.malus_position = self.create_malus()

        # Nouriture du serpent
        self.food_positions = [self.create_food()]
        
        self.canvas.bind_all("<Key>", self.on_key_press)
        
        # Demarage du jeu 
        self.move_snake()

    def create_obstacle(self):
        self.obstacle_reset_counter = 0
        self.obstacles_positions = []
        # Un obstacle supplementaire est ajoute tous les 5 points
        for i in range(int(self.score/5)*self.obstacle_modifier):
            x = random.randint(0, (WIDTH - SNAKE_BLOCK) // SNAKE_BLOCK) * SNAKE_BLOCK
            y = random.randint(0, (HEIGHT - SNAKE_BLOCK) // SNAKE_BLOCK) * SNAKE_BLOCK
            self.obstacles_positions.append((x, y))

    def create_food(self):
        x = random.randint(0, (WIDTH - SNAKE_BLOCK) // SNAKE_BLOCK) * SNAKE_BLOCK
        y = random.randint(0, (HEIGHT - SNAKE_BLOCK) // SNAKE_BLOCK) * SNAKE_BLOCK
        self.canvas.create_rectangle(x, y, x + SNAKE_BLOCK, y + SNAKE_BLOCK, fill="red")
        return (x, y)

    def create_bonus(self):
        if self.speed_modifier == 1.5:
            self.speed_modifier = 1
        if self.obstacle_modifier == 0:
            self.obstacle_modifier = 1

        x = random.randint(0, (WIDTH - SNAKE_BLOCK) // SNAKE_BLOCK) * SNAKE_BLOCK
        y = random.randint(0, (HEIGHT - SNAKE_BLOCK) // SNAKE_BLOCK) * SNAKE_BLOCK
        
        bonus_randomizer = random.randint(1, 100)
        
        if bonus_randomizer <= 50: # Reduit la vitesse de 50% pendant 10 s
            self.canvas.create_rectangle(x, y, x + SNAKE_BLOCK, y + SNAKE_BLOCK, fill="green")
            self.bonus_type = 1
        elif bonus_randomizer <= 90: # Plus d'obstacles pendant 20 s
            self.canvas.create_rectangle(x, y, x + SNAKE_BLOCK, y + SNAKE_BLOCK, fill="white")
            self.bonus_type = 2
        elif bonus_randomizer <= 100: # + 1 Fruit bonus jusqu'a la fin du jeu
            self.canvas.create_rectangle(x, y, x + SNAKE_BLOCK, y + SNAKE_BLOCK, fill="orange")
            self.bonus_type = 3

        return (x, y)


    def create_malus(self):
        if self.speed_modifier == 0.5:
            self.speed_modifier = 1
        if self.obstacle_modifier == 2:
            self.obstacle_modifier = 1
        self.controls_inverted = False

        x = random.randint(0, (WIDTH - SNAKE_BLOCK) // SNAKE_BLOCK) * SNAKE_BLOCK
        y = random.randint(0, (HEIGHT - SNAKE_BLOCK) // SNAKE_BLOCK) * SNAKE_BLOCK
        
        bonus_randomizer = random.randint(1, 100)
        
        if bonus_randomizer <= 50: # Augmente la vitesse de 50% pendant 10 s
            self.canvas.create_rectangle(x, y, x + SNAKE_BLOCK, y + SNAKE_BLOCK, fill="blue")
            self.malus_type = 1
        elif bonus_randomizer <= 90: # 2 fois plus d'obstacles pendant 20 s
            self.canvas.create_rectangle(x, y, x + SNAKE_BLOCK, y + SNAKE_BLOCK, fill="peru")
            self.malus_type = 2
        elif bonus_randomizer <= 100: # Controles inverses pendant (haut/bas et gauche/droite) pendant 10 s
            self.canvas.create_rectangle(x, y, x + SNAKE_BLOCK, y + SNAKE_BLOCK, fill="orchid")
            self.malus_type = 3

        return (x, y)

    def move_snake(self):
        self.canvas.delete("all")

        # Deplacement du serpent
        if self.direction == "Up":
            if self.snake_positions[0][1] - SNAKE_BLOCK < 0:
                self.game_over()
                return
            new_position = (self.snake_positions[0][0], self.snake_positions[0][1] - SNAKE_BLOCK)
        elif self.direction == "Down":
            if self.snake_positions[0][1] + SNAKE_BLOCK > HEIGHT:
                self.game_over()
                return
            new_position = (self.snake_positions[0][0], self.snake_positions[0][1] + SNAKE_BLOCK)
        elif self.direction == "Left":
            if self.snake_positions[0][0] - SNAKE_BLOCK < 0:
                self.game_over()
                return
            new_position = (self.snake_positions[0][0] - SNAKE_BLOCK, self.snake_positions[0][1])
        elif self.direction == "Right":
            if self.snake_positions[0][0] + SNAKE_BLOCK > WIDTH:
                self.game_over()
                return
            new_position = (self.snake_positions[0][0] + SNAKE_BLOCK, self.snake_positions[0][1])
            
        self.snake_positions.insert(0, new_position)

        self.last_direction = self.direction
        
        # Creation de la nouriture (une ou plusieurs fois en fonction des bonus)
        i = 0
        is_food_eaten = False
        for position in self.food_positions:
            if new_position == position:
                self.food_positions[i] = self.create_food()
                self.score += 1
                is_food_eaten = True
            else:
                self.canvas.create_rectangle(position[0], position[1], position[0] + SNAKE_BLOCK, position[1] + SNAKE_BLOCK, fill="red")
            i += 1

        if not is_food_eaten:
            self.snake_positions.pop()

        # Creation des bonus
        if self.bonus_type != 0:
            # Si on est a la position du bonus on applique son effet
            if new_position == self.bonus_position:
                if self.bonus_type == 1:
                    if self.speed_modifier == 0.5:
                        self.malus_time = 0
                        self.malus_position = self.create_malus()
                    self.speed_modifier = 1.5
                    self.bonus_time = 10000
                elif self.bonus_type == 2:
                    if self.obstacle_modifier == 2:
                        self.malus_time = 0
                        self.malus_position = self.create_malus()
                    self.obstacle_modifier = 0
                    self.bonus_time = 20000
                    self.create_obstacle()
                elif self.bonus_type == 3:
                    self.food_positions.append(self.create_food())
                    self.bonus_position = self.create_bonus()
                self.bonus_type = 0
            # Sinon on l affiche a l ecran
            else:
                if self.bonus_type == 1:
                    self.canvas.create_rectangle(self.bonus_position[0], self.bonus_position[1], self.bonus_position[0] + SNAKE_BLOCK, self.bonus_position[1] + SNAKE_BLOCK, fill="green")
                elif self.bonus_type == 2:
                    self.canvas.create_rectangle(self.bonus_position[0], self.bonus_position[1], self.bonus_position[0] + SNAKE_BLOCK, self.bonus_position[1] + SNAKE_BLOCK, fill="white")
                elif self.bonus_type == 3:
                    self.canvas.create_rectangle(self.bonus_position[0], self.bonus_position[1], self.bonus_position[0] + SNAKE_BLOCK, self.bonus_position[1] + SNAKE_BLOCK, fill="orange")

        # Creation des malus
        if self.malus_type != 0:
            # Si on est a la position du malus on applique son effet
            if new_position == self.malus_position:
                if self.malus_type == 1:
                    if self.speed_modifier == 1.5:
                        self.bonus_time = 0
                        self.bonus_position = self.create_bonus()
                    self.speed_modifier = 0.5
                    self.malus_time = 10000
                elif self.malus_type == 2:
                    if self.obstacle_modifier == 0:
                        self.bonus_time = 0
                        self.bonus_position = self.create_bonus()
                    self.obstacle_modifier = 2
                    self.malus_time = 10000
                    self.create_obstacle()
                elif self.malus_type == 3:
                    self.controls_inverted = True
                    self.malus_time = 10000
                self.malus_type = 0
            # Sinon on l affiche a l ecran
            else:
                if self.malus_type == 1:
                    self.canvas.create_rectangle(self.malus_position[0], self.malus_position[1], self.malus_position[0] + SNAKE_BLOCK, self.malus_position[1] + SNAKE_BLOCK, fill="blue")
                elif self.malus_type == 2:
                    self.canvas.create_rectangle(self.malus_position[0], self.malus_position[1], self.malus_position[0] + SNAKE_BLOCK, self.malus_position[1] + SNAKE_BLOCK, fill="peru")
                elif self.malus_type == 3:
                    self.canvas.create_rectangle(self.malus_position[0], self.malus_position[1], self.malus_position[0] + SNAKE_BLOCK, self.malus_position[1] + SNAKE_BLOCK, fill="orchid")

        # Affichage du serpent a l ecran
        for position in self.snake_positions:
            self.canvas.create_rectangle(position[0], position[1], position[0] + SNAKE_BLOCK, position[1] + SNAKE_BLOCK, fill="green")
            
        # Creation des obstacles
        self.obstacle_reset_counter += 1
        if self.obstacle_reset_counter == 100:
            self.create_obstacle()
        
        # Gestion de la defaite
        for position in self.obstacles_positions:
            self.canvas.create_rectangle(position[0], position[1], position[0] + SNAKE_BLOCK, position[1] + SNAKE_BLOCK, fill="brown")
            if new_position == position:
                self.game_over()
                return

        if self.snake_positions[0][0] < 0 or self.snake_positions[0][0] >= WIDTH or self.snake_positions[0][1] < 0 or self.snake_positions[0][1] >= HEIGHT:
            self.game_over()
            return
            
        if len(self.snake_positions) != len(set(self.snake_positions)):
            self.game_over()
            return
        # Fin gestion de la defaite
            
        timetowait = (100 - self.score) * self.speed_modifier

        # Gestion de la fin du temps d un bonus
        if self.bonus_time > 0:
            self.bonus_time -= timetowait
            if self.bonus_time <= 0:
                self.bonus_time = 0
                self.bonus_position = self.create_bonus()
                
        # Gestion de la fin du temps d un malus
        if self.malus_time > 0:
            self.malus_time -= timetowait
            if self.malus_time <= 0:
                self.malus_time = 0
                self.malus_position = self.create_malus()

        # Pour eviter que le serpent soit trop rapide / que le temps entre deux frames soit negatif
        if timetowait < 10:
            timetowait = 10
            
        # Gestion de la vitesse du serpent
        root.after(int(timetowait), self.move_snake)
        
        # Affichage du score
        self.canvas.create_text(WIDTH/2, 20, text=str(self.score), font=("Arial", 20, "bold"))

    def on_key_press(self, event):
        # Gestion des controles
        if event.keysym == "Up" and self.last_direction != "Down":
            if self.controls_inverted:
                self.direction = "Right"
            else:
                self.direction = "Up"
        elif event.keysym == "Down" and self.last_direction != "Up":
            if self.controls_inverted:
                self.direction = "Left"
            else:
                self.direction = "Down"
        elif event.keysym == "Left" and self.last_direction != "Right":
            if self.controls_inverted:
                self.direction = "Up"
            else:
                self.direction = "Left"
        elif event.keysym == "Right" and self.last_direction != "Left":
            if self.controls_inverted:
                self.direction = "Down"
            else:
                self.direction = "Right"

        if self.is_game_over:
            if event.keysym == "space":
                self.init_game()

    def game_over(self):
        # Ecran de game over
        self.canvas.create_text(WIDTH/2, HEIGHT/2, text="Game Over", font=("Arial", 20, "bold"))
        self.canvas.create_text(WIDTH/2, 20, text=str(self.score), font=("Arial", 20, "bold"))
        self.canvas.create_text(WIDTH/2, HEIGHT/2 + HEIGHT/4, text="Presser la barre espace pour recommencer une partie", font=("Arial", 15))
        self.snake_positions = []
        self.is_game_over = True


# Programme principal
root = tk.Tk()
root.title("Snake")
snake = Snake()
root.mainloop()