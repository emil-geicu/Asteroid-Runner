import pygame, os, random
from design import levels

pygame.init()

# The size of the game window
screen_width, screen_height = 1280, 720
screen_size = screen_width, screen_height

window = pygame.display.set_mode(screen_size)
fade = pygame.Surface((screen_width, screen_height))
fade.fill((0,0,0))


# We make the name of the game window Asteroid Runner
pygame.display.set_caption("Asteroid Runner")

# We create an object to keep track of time
clock = pygame.time.Clock()

# We will consider 60 frames per second
fps = 60


# In the upcoming classes we wil make use of the inheritance
# We keep in mind that pygame.sprite.Sprite is the base class for visible game objects

# Class character is used for the player and the enemy in order to demonstrate polymorphism on function overwriting
class Character:
    def __init__(self):
        self.speed = 4
    def walkAnimation(self):
        print("walk")

# Player class refers to the ship that we are controlling a
class Player(pygame.sprite.Sprite,Character):
    # set image to be 32 x 32
    def __init__(self):

        # The super function allows the use of pygame.Rect object
        super().__init__()
        Character.__init__(self)

        # We set the image of the ship
        self.image = pygame.image.load("images/Spaceship/spaceship_east.png")

        # We fetch the rectangle dimenstion which has the same dimension as the ship's image
        self.rect = self.image.get_rect()

        self.hSpeed = 0
        self.vSpeed = 0
        self.speed=8
        self.isNextStage = False
        self.walkCount = 0
        self.hasFlashlight = False
        self.direction = 'S'
        self.portalNot = False
        self.ghostWalkCount = 0
        self.invulnerable = False
        self.invulnerable_count = 0

        self.live = 3
        self.score = 0

    def set_position(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def set_absolute_position(self, x, y):
        self.abs_x = x
        self.abs_y = y

    # We use the update function in order to make updates in relation of the player with other objects
    def update(self, collidable = pygame.sprite.Group(), treasures = pygame.sprite.Group(), hearts = pygame.sprite.Group(),portal = pygame.sprite.Group(), enemies = pygame.sprite.Group(), suns = pygame.sprite.Group(), flashlights = pygame.sprite.Group()):
        self.move(collidable)
        self.isCollided_with_treasures(treasures)
        self.isCollided_with_hearts(hearts)
        self.isCollided_with_flashlight(flashlights)
        self.isNextStage = self.isCollided_with_portal(portal)
        if self.invulnerable:
            if self.invulnerable_count >= 90:
                self.invulnerable_count = 0
                self.invulnerable = False
            else:
                self.invulnerable_count += 1

        else:
            self.isCollided_with_damage_source(enemies)
            self.isCollided_with_damage_source(suns)

        # We implement the animation of the player
        self.walkAnimation()

# Move function is used in order to take the input from the keyboard and determine the direction of the player
    def move(self, collidable):
        # We get the key pressed by user
        keys = pygame.key.get_pressed()

        # If we press any direction key:
        if(not self.isNextStage and (keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_UP] or keys[pygame.K_DOWN])):

            # We consider for horizontal movement if pressed left key
            if(keys[pygame.K_LEFT]):
                self.hSpeed = -self.speed

            elif (keys[pygame.K_RIGHT]):
                self.hSpeed = self.speed

            else:
                self.hSpeed = 0

            # We consider for vertical movement
            if (keys[pygame.K_UP]):
                self.vSpeed = -self.speed

            elif (keys[pygame.K_DOWN]):
                self.vSpeed = self.speed

            else:
                self.vSpeed = 0

            # We redefine the direction of the player
            if self.hSpeed > 0:
                if self.vSpeed > 0:
                    self.direction = 'SE'
                elif self.vSpeed < 0:
                    self.direction = 'NE'
                else:
                    self.direction = 'E'

            elif self.hSpeed < 0:
                if self.vSpeed > 0:
                    self.direction = 'SW'
                elif self.vSpeed < 0:
                    self.direction = 'NW'
                else:
                    self.direction = 'W'
            else:
                if self.vSpeed > 0:
                    self.direction = 'S'
                elif self.vSpeed < 0:
                    self.direction = 'N'
        # If all direction keys are not pressed the direction doesn't change
        else:
            self.hSpeed = 0
            self.vSpeed = 0

        # After determining the direction of player, we check if there is any collision
        self.isCollided(collidable)

    # We determine the direction and for each direction
    def walkAnimation(self):
        # If the ship isn't damage we load the images according to the direction
        if self.invulnerable == False:
            if self.direction == 'E':
                self.image = pygame.image.load('images/Spaceship/spaceship_east.png')
            elif self.direction == 'N':
                self.image = pygame.image.load('images/Spaceship/spaceship_north.png')
            elif self.direction == 'NE':
                self.image = pygame.image.load('images/Spaceship/spaceship_east.png')
            elif self.direction == 'NW':
                self.image = pygame.image.load('images/Spaceship/spaceship_west.png')
            elif self.direction == 'S':
                self.image = pygame.image.load('images/Spaceship/spaceship_south.png')
            elif self.direction == 'SE':
                self.image = pygame.image.load('images/Spaceship/spaceship_east.png')
            elif self.direction == 'SW':
                self.image = pygame.image.load('images/Spaceship/spaceship_west.png')
            elif self.direction == 'W':
                self.image = pygame.image.load('images/Spaceship/spaceship_west.png')

        else:
            # If the ship is damaged it becomes invulnerable so we have different pictures for each direction
            if self.direction == 'E':
                self.image = pygame.image.load('images/ghost/damaged_ship_east.png')
            elif self.direction == 'N':
                self.image = pygame.image.load('images/ghost/damaged_ship_north.png')
            elif self.direction == 'NE':
                self.image = pygame.image.load('images/ghost/damaged_ship_east.png')
            elif self.direction == 'NW':
                self.image = pygame.image.load('images/ghost/damaged_ship_west.png')
            elif self.direction == 'S':
                self.image = pygame.image.load('images/ghost/damaged_ship_south.png')
            elif self.direction == 'SE':
                self.image = pygame.image.load('images/ghost/damaged_ship_east.png')
            elif self.direction == 'SW':
                self.image = pygame.image.load('images/ghost/damaged_ship_west.png')
            elif self.direction == 'W':
                self.image = pygame.image.load('images/ghost/damaged_ship_west.png')

    def isCollided(self, collidable):
        # We find sprites in a group that intersect another sprite.
        # Intersection is determined by comparing the Sprite.rect attribute of each Sprite

        self.rect.x += self.hSpeed
        self.abs_x += self.hSpeed

        collision_list = pygame.sprite.spritecollide(self, collidable, False)

        # If intersection with collidable object in collision_list ( horizontal x direction )
        for collided_object in collision_list:
            if (self.hSpeed > 0):
                # We update the Absoulte position
                hDiff = collided_object.rect.left - self.rect.right
                self.abs_x += hDiff
                # We update the relative position
                self.rect.right = collided_object.rect.left
                self.hSpeed = 0

            elif (self.hSpeed < 0):
                # We update the Absoulte position
                hDiff = collided_object.rect.right - self.rect.left
                self.abs_x += hDiff
                # W update the relative position
                self.rect.left = collided_object.rect.right
                self.hSpeed = 0

        self.rect.y += self.vSpeed
        self.abs_y += self.vSpeed
        # If intersection is with collidable object in y direction
        collision_list = pygame.sprite.spritecollide(self, collidable, False)
        for collided_object in collision_list:
            # Moving down
            if (self. vSpeed > 0):
                # We update the Absoulte position
                vDiff = collided_object.rect.top - self.rect.bottom
                self.abs_y += vDiff

                # We update the relative position
                self.rect.bottom= collided_object.rect.top
                self.vSpeed = 0
            # Moving up
            elif (self. vSpeed < 0):
                # We update the Absoulte position
                vDiff = collided_object.rect.bottom - self.rect.top
                self.abs_y += vDiff

                # We update the relative position
                self.rect.top = collided_object.rect.bottom
                self.vSpeed = 0


    # The next part is represented by methods that describe the behaviour of the player with the collision with every other object

    def isCollided_with_treasures(self, treasures):
        if (pygame.sprite.spritecollide(self, treasures, True)):
            self.score += 100
            star_collision.play()


    def isCollided_with_hearts(self, hearts):
        if (pygame.sprite.spritecollide(self, hearts, True)):
            self.live += 1
            star_collision.play()

    def isCollided_with_portal(self, portals):

        collision_list = pygame.sprite.spritecollide(self, portals, False)
        for portal in collision_list:
            if (self.rect.collidepoint(portal.rect.centerx, portal.rect.centery)):
                if(self.hasFlashlight == True):
                    portal_collision.play()
                    self.portalNot = False
                    return True
                else:
                    self.portalNot = True



    def isCollided_with_damage_source(self, damage_source):
        collision_list = pygame.sprite.spritecollide(self, damage_source, False)
        for item in collision_list:
            if (item.rect.collidepoint(self.rect.centerx, self.rect.centery)):
                enemy_collision.play()
                self.invulnerable = True
                self.live -= 1
                return True

    def isCollided_with_flashlight(self, flashlights):
        if (pygame.sprite.spritecollide(self, flashlights, True)):
            self.hasFlashlight = True

# Enemy class refers to the enemy ships of the game
class Enemy(pygame.sprite.Sprite,Character):
    def __init__(self, x, y):

        super().__init__()
        Character.__init__(self)
        self.image = pygame.image.load('images/Enemy/enemy_east.png')
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y


        self.direction = random.choice(["up", "down", "left", "right"])


    def set_position(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def update(self, collidable = pygame.sprite.Group(), collidable_2 = pygame.sprite.Group()):
        self.move()
        self.isCollided(collidable)
        self.isCollided(collidable_2)

# For the move function we use directions in order to make the direction more clear
    def move(self):
        if self.direction == "up":
            self.dx = 0
            self.dy = -self.speed

        elif self.direction == "down":
            self.dx = 0
            self.dy = self.speed

        elif self.direction == "left":
            self.dx = -self.speed
            self.dy = 0

        elif self.direction == "right":
            self.dx = self.speed
            self.dy = 0

        else:
            self.dx = 0
            self.dy = 0

        self.walkAnimation()

        self.rect.x += self.dx
        self.rect.y += self.dy

# The walk animation is make checking the direction of the enemy ship and loading the image corresponding to that direction
    def walkAnimation(self):
        if self.direction == 'up':
            self.image = pygame.image.load('images/Enemy/enemy_north.png')
        elif self.direction == 'down':
            self.image = pygame.image.load('images/Enemy/enemy_south.png')
        elif self.direction == 'left':
            self.image = pygame.image.load('images/Enemy/enemy_west.png')
        elif self.direction == 'right':
            self.image = pygame.image.load('images/Enemy/enemy_east.png')

# We use this function in order to see if we collide with something
    def isCollided(self, collidable):
        # We check for any enemy collision with walls_Group, if there is a collision, we set the enemy ship to move in a random direction
        collision_list = pygame.sprite.spritecollide(self, collidable, False)
        for collided_object in collision_list:
            # If the ship is moving right
            if (self.dx > 0):
                self.rect.right = collided_object.rect.left
                self.dx = 0
                self.direction = random.choice(["up", "down", "left"])

            # If the ship is moving  Left
            if (self.dx < 0):
                self.rect.left = collided_object.rect.right
                self.dx = 0
                self.direction = random.choice(["up", "down", "right"])

            # If the ship is moving  down
            if (self.dy > 0):
                self.rect.bottom= collided_object.rect.top
                self.dy = 0
                self.direction = random.choice(["up", "left", "right"])
            # If the ship is moving  up
            if (self.dy < 0):
                self.dx = 0
                self.rect.top = collided_object.rect.bottom
                self.direction = random.choice(["down", "left", "right"])

    def shift_world(self, shift_x, shift_y):
        self.rect.x += shift_x
        self.rect.y += shift_y

# Wall class refers to the walls of the maze which in our case are some asteroids
class Wall(pygame.sprite.Sprite):

    def __init__(self, x, y):

        super().__init__()
        self.image = pygame.image.load('images/others/wall.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def shift_world(self, shift_x, shift_y):
        self.rect.x += shift_x
        self.rect.y += shift_y

    def draw(self, window):

        window.blit(self.image,(self.rect.x, self.rect.y))

# Flashlight class refers to the flashlight that lets us advance to the levels that are in the dark
class Flashlight(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('images/Flashlight/Flashlight.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def shift_world(self, shift_x, shift_y):
        self.rect.x += shift_x
        self.rect.y += shift_y

# Treasure class refers to little stars that are made as collectable objects. If we pe pick them out our score increases
class Treasure(pygame.sprite.Sprite):

    def __init__(self, x, y):

        super().__init__()
        self.image = pygame.image.load('images/others/foodA.png').convert_alpha()

        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y

    def shift_world(self, shift_x, shift_y):
        self.rect.x += shift_x
        self.rect.y += shift_y

# Heart class refers to our energy or lives of the ship
class Heart(pygame.sprite.Sprite):

    def __init__(self, x, y):

        super().__init__()
        self.image = pygame.image.load('images/features/heart.png').convert_alpha()

        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y

    def shift_world(self, shift_x, shift_y):
        self.rect.x += shift_x
        self.rect.y += shift_y

# Sun class makes dangerous objects for our ship. If we collide with a sun on heart is depleted
class Sun(pygame.sprite.Sprite):

    def __init__(self, x, y):

        super().__init__()


        self.image = pygame.image.load('images/Sun/star.png')

        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y

        self.count = 0

    def shift_world(self, shift_x, shift_y):
        self.rect.x += shift_x
        self.rect.y += shift_y


# Portal class is use for making portals that help us advance to the next levels
class Portal(pygame.sprite.Sprite):

    def __init__(self, x, y):

        super().__init__()
        self.image = pygame.image.load('images/portal/portal.png').convert_alpha()


        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.count = 0



    def shift_world(self, shift_x, shift_y):
        self.rect.x += shift_x
        self.rect.y += shift_y


# Darkness class is used to make the ilusion of a lantern in the dark from level 2 onwards
class Darkness(pygame.sprite.Sprite):
    def __init__(self):

        super().__init__()
        self.image = pygame.image.load('images/others/fog.png').convert_alpha()

        self.rect = self.image.get_rect()

    def update(self, player_x, player_y):
        self.rect.centerx = player_x + 16
        self.rect.centery = player_y + 16

# Here we initialize all the objects relevant to the game.
def create_instances():
    global current_level, running, player, player_group, darkness_group, flashlight_group
    global walls_group, enemies_group, treasures_group, hearts_group, portal_group, suns_group
    global screen_width, screen_height
    global winGame

    winGame = False
    current_level = 0

    # We make our player instance
    player = Player()
    player_group = pygame.sprite.Group()
    player_group.add(player)

    # We make groups for the other objects aswell
    walls_group = pygame.sprite.Group()
    enemies_group = pygame.sprite.Group()
    treasures_group = pygame.sprite.Group()
    portal_group = pygame.sprite.Group()
    suns_group = pygame.sprite.Group()
    hearts_group = pygame.sprite.Group()
    flashlight_group = pygame.sprite.Group()
    darkness_group = pygame.sprite.Group()
    darkness_group.add(Darkness())


# Here we do the managing of our camera
def run_viewbox(player_x, player_y):

    left_viewbox = screen_width / 2 - screen_width / 8
    right_viewbox = screen_width / 2 + screen_width / 8
    top_viewbox = screen_height / 2 - screen_height / 8
    bottom_viewbox = screen_height / 2 + screen_height / 8
    dx, dy = 0, 0

    if(player_x <= left_viewbox):
        dx = left_viewbox - player_x
        player.set_position(left_viewbox, player.rect.y)

    elif(player_x >= right_viewbox):
        dx = right_viewbox - player_x
        player.set_position(right_viewbox, player.rect.y)

    if(player_y <= top_viewbox):
        dy = top_viewbox - player_y
        player.set_position(player.rect.x, top_viewbox)

    elif(player_y >= bottom_viewbox):
        dy = bottom_viewbox - player_y
        player.set_position(player.rect.x, bottom_viewbox)

    if (dx != 0 or dy != 0):
        for wall in walls_group:
            wall.shift_world(dx, dy)

        for enemy in enemies_group:
            enemy.shift_world(dx, dy)

        for treasure in treasures_group:
            treasure.shift_world(dx, dy)

        for heart in hearts_group:
            heart.shift_world(dx, dy)

        for portal in portal_group:
            portal.shift_world(dx, dy)

        for sun in suns_group:
            sun.shift_world(dx, dy)

        for flashlight in flashlight_group:
            flashlight.shift_world(dx,dy)

# Here we setup our maze
def setup_maze(current_level):

    # We take every character of the matrix and we decode it
    for y in range(len(levels[current_level])):
        for x in range(len(levels[current_level][y])):
            character = levels[current_level][y][x]
            pos_x = (x*64)
            pos_y = (y*64)

            if character == "X":
                # We update wall coordinates
                walls_group.add(Wall(pos_x, pos_y))

            elif character == "F":
                # We update flashlight coordinates
                flashlight_group.add(Flashlight(pos_x, pos_y))

            elif character == "P":
                # We update player coordinates
                player.set_position(pos_x, pos_y)
                player.set_absolute_position(pos_x, pos_y)

            elif character == "E":
                # We update  enemy coordinates
                enemies_group.add(Enemy(pos_x, pos_y))

            elif character == "T":
                # We update  treasure coordinates
                treasures_group.add(Treasure(pos_x, pos_y))

            elif character == "H":
                # We update hearts coordinates
                hearts_group.add(Heart(pos_x, pos_y))

            elif character == "U":
                # We update  portal coordinates
                portal_group.add(Portal(pos_x, pos_y))

            elif character == "S":
                #Update suns coordinates
                suns_group.add(Sun(pos_x, pos_y))

# Here we clear our current level
def clear_maze():
    walls_group.empty()
    enemies_group.empty()
    treasures_group.empty()
    hearts_group.empty()
    suns_group.empty()
    portal_group.empty()
    flashlight_group.empty()
    player.isNextStage = False


# Here we make the transition between levels
def nextStage(isNextStage):
    global current_level, isGameOver
    global winGame
    # If we got to a new level we have 2 possibilities
    if isNextStage:
        current_level += 1

        # The first possibiliy is that we conquered all the levels and escaped the maze
        # In this case we will display the message YOU ESCAPED along with the score and lives of the player
        if current_level >= 4:
            winGame = True
            window.blit(background,(0,0))
            gameovertext = font1.render("YOU ESCAPED!", 1, (255, 17, 0))
            tip = font1.render("Press Q in order to exit.", 1, (255, 250, 250))
            gameoverScore = font1.render("Score= " + str(player.score), 1, (21, 0, 255))
            window.blit(gameovertext, (screen_width // 2 - 160, screen_height // 2 - 50))
            window.blit(tip, (screen_width // 2 - 320, screen_height // 2))
            run_viewbox(screen_width // 2 - 200, screen_height // 2)

        # The second possibilty is that we still have levels to escape so we clear the current level and we setup the next one
        elif winGame == False:
            clear_maze()
            setup_maze(current_level)



# We load the background and the loading screen of the game

background = pygame.image.load('images/others/background.jpg')
loadingScreen = pygame.image.load('images/others/loadingscreen.png')
heartShape = pygame.image.load('images/features/heart.png')

# We load the audio of each interaction of the player with the objects
# We adjust the volume also, because the default one is too loud

music = pygame.mixer.music.load(os.path.join('audios','Background_Music.mp3'))
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.1)
star_collision = pygame.mixer.Sound(os.path.join('audios', 'Star_Collision.wav'))
star_collision.set_volume(0.1)
enemy_collision = pygame.mixer.Sound(os.path.join('audios','Enemy_Collision.wav'))
enemy_collision.set_volume(0.1)
portal_collision = pygame.mixer.Sound(os.path.join('audios','Portal_Collision.wav'))
portal_collision.set_volume(0.1)

# We load the same custom font but with different dimensions

font1 = pygame.font.Font('images/Font/retrofont.ttf',35)
font2 = pygame.font.Font('images/Font/retrofont.ttf',20)

# Here in main(), we manage the states of the game

def main():

# We initialize the states of the game (loading state, game is over state, running state)
    loading = True
    isGameOver = False
    running = True

# We create the instances of the game and we make the correspondence between every character of each level matrix with its coresponding object
    create_instances()
    setup_maze(current_level)


# We initialize i with 0 and we will need it when we will make the transition between levels
    i = 0

# We make updates while the game is running
    while running:

        # While the game is running and we press the exit button of the window or the key q we terminate and exit the game
        for event in pygame.event.get():
            if(event.type == pygame.QUIT) or (event.type == pygame.KEYDOWN and (event.key == pygame.K_ESCAPE or event.key == pygame.K_q )):
             running = False



        # The first state is the loading state where we see the title screen and at the bottom the main objective of the game
        if loading:
            breakLoop = True
            while breakLoop:
                window.blit(loadingScreen, (0,0))
                tip = font2.render("Escape from the asteroid maze and watch out for tips!", 1, (255, 250, 250))
                window.blit(tip, (250, screen_height - 30))
                pygame.display.flip()

                # If we press the space key down we will end the loading screen and we will move to the actual playing state of the game
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        breakLoop = False
                        loading = False

        # If we run out of lives (hearts, energy, etc.) The program will display the message game over along with the current score
        elif isGameOver:
            window.blit(background,(0,0))
            gameovertext = font1.render("GAME OVER",1,(255, 17, 0))
            tip = font1.render("Press Q in order to exit.",1,(255,250,250))
            gameoverScore = font1.render("Score= " + str(player.score),1,(21, 0, 255))
            window.blit(gameovertext, (screen_width // 2 - 130, screen_height // 2 - 50))
            window.blit(gameoverScore, (screen_width // 2 - 110, screen_height // 2 - 10))
            window.blit(tip, (screen_width // 2 - 320, screen_height // 2 + 30))

        # If the player is still in the current level (stage) we make updates for every object that we see on our screen
        else:
            if (player.isNextStage != True):

                player_group.update(walls_group, treasures_group, hearts_group, portal_group, enemies_group, suns_group, flashlight_group)
                enemies_group.update(walls_group)
                darkness_group.update(player.rect.x, player.rect.y)


                # We update out view camera
                run_viewbox(player.rect.x, player.rect.y)

                # We make the background of the level to an environement simlar to space (The background is an image with a lot of stars)
                window.blit(background,(0,0))

                # We draw the walls
                for wall in walls_group:
                    if (wall.rect.x < screen_width) and (wall.rect.y < screen_height):
                        wall.draw(window)

            # We draw the remaining objects

            if player.isNextStage != True:
                player_group.draw(window)

            flashlight_group.draw(window)
            portal_group.draw(window)
            treasures_group.draw(window)
            hearts_group.draw(window)
            enemies_group.draw(window)

            suns_group.draw(window)

            # Implement fog from level 2 onwards
            if current_level >= 1 and winGame == False:
                darkness_group.draw(window)

            if player.portalNot == True:
                text = font2.render("Find the flashlight in order to advance into the portal!",1,(255,250,250))
                window.blit(text,(250,650))

            lifeLeftText = font1.render(' X '+ str(player.live),1,(255,250,250))
            scoreText = font1.render('Score: ' + str(player.score), 1, (255,250,250))
            window.blit(heartShape,(530,50))
            window.blit(lifeLeftText,(610,40))
            window.blit(scoreText, (610, 70))

            # If we advance to the next stage and we have not yet won the game we make a fading animation in order to make a
            #smooth transition between the completed level and the new level

            if player.isNextStage ==  True and winGame == False:
                fade.set_alpha(i)
                window.blit(fade, (0,0))
                pygame.display.update()
                pygame.time.delay(2)
                i += 15
                if i == 255:
                    i = 0
                    nextStage(player.isNextStage)
                    continue

            # If all the lives (energy, hearts) of the player run out the game is over
            if player.live == 0:
                isGameOver = True

        # We delay and update out screen
        pygame.display.flip()
        clock.tick_busy_loop(fps)
    pygame.quit()


# We run the main
main()
