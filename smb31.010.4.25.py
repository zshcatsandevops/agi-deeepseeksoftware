# program.py
import pygame
import math
import os
import random

# Initialize Pygame
pygame.init()

# Game constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
TILE_SIZE = 32

# Colors
SKY_BLUE = (92, 148, 252)
MARIO_RED = (255, 0, 0)
MARIO_BLUE = (0, 0, 255)
BRICK_RED = (205, 92, 92)
PIPE_GREEN = (0, 128, 0)
COIN_YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRASS_GREEN = (76, 175, 80)
SAND_YELLOW = (237, 212, 111)
WATER_BLUE = (64, 164, 223)
CASTLE_GRAY = (128, 128, 128)
HUD_BLUE = (0, 80, 160)
HUD_RED = (220, 0, 0)
HUD_GOLD = (255, 204, 0)

class OverworldMap:
    def __init__(self):
        self.tile_size = 40
        self.map_width = 20
        self.map_height = 15
        self.map_data = []
        self.player_map_pos = [2, 7]  # Starting position on map
        self.generate_map()
        
    def generate_map(self):
        # Generate a simple SMB3-style overworld map
        # 0 = empty, 1 = path, 2 = grass, 3 = water, 4 = castle, 5 = pipe
        self.map_data = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
            [0, 0, 1, 2, 2, 2, 1, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 0, 0],
            [0, 0, 1, 2, 2, 2, 1, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 0, 0],
            [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]
        
        # Add some special tiles (castles, pipes, etc.)
        self.map_data[7][15] = 4  # Castle
        self.map_data[7][5] = 5   # Pipe
        self.map_data[7][11] = 5  # Pipe
        
    def can_move_to(self, x, y):
        # Check if the position is within bounds and is a path or special tile
        if 0 <= x < self.map_width and 0 <= y < self.map_height:
            return self.map_data[y][x] in [1, 2, 4, 5]  # Can move on paths, grass, castles, and pipes
        return False
        
    def draw(self, screen):
        # Draw the overworld map
        for y in range(self.map_height):
            for x in range(self.map_width):
                rect = pygame.Rect(x * self.tile_size, y * self.tile_size, self.tile_size, self.tile_size)
                
                if self.map_data[y][x] == 0:  # Empty/background
                    pygame.draw.rect(screen, SKY_BLUE, rect)
                elif self.map_data[y][x] == 1:  # Path
                    pygame.draw.rect(screen, SAND_YELLOW, rect)
                elif self.map_data[y][x] == 2:  # Grass
                    pygame.draw.rect(screen, GRASS_GREEN, rect)
                elif self.map_data[y][x] == 3:  # Water
                    pygame.draw.rect(screen, WATER_BLUE, rect)
                elif self.map_data[y][x] == 4:  # Castle
                    pygame.draw.rect(screen, CASTLE_GRAY, rect)
                    # Draw castle details
                    pygame.draw.rect(screen, BLACK, (x * self.tile_size + 10, y * self.tile_size + 5, 20, 25))
                    pygame.draw.rect(screen, MARIO_RED, (x * self.tile_size + 15, y * self.tile_size, 10, 5))
                elif self.map_data[y][x] == 5:  # Pipe
                    pygame.draw.rect(screen, PIPE_GREEN, rect)
                
                # Draw grid lines
                pygame.draw.rect(screen, BLACK, rect, 1)
        
        # Draw player on map
        player_rect = pygame.Rect(
            self.player_map_pos[0] * self.tile_size + 10,
            self.player_map_pos[1] * self.tile_size + 10,
            20, 20
        )
        pygame.draw.rect(screen, MARIO_RED, player_rect)

class Mario:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 32
        self.height = 32
        self.vel_x = 0
        self.vel_y = 0
        self.speed = 5
        self.jump_power = 15
        self.on_ground = False
        self.facing_right = True
        self.power_up_state = 0  # 0 = small, 1 = super, 2 = fire
        
    def update(self, platforms, camera_x):
        # Handle input
        keys = pygame.key.get_pressed()
        self.vel_x = 0
        
        if keys[pygame.K_RIGHT]:
            self.vel_x = self.speed
            self.facing_right = True
        if keys[pygame.K_LEFT]:
            self.vel_x = -self.speed
            self.facing_right = False
        if keys[pygame.K_SPACE] and self.on_ground:
            self.vel_y = -self.jump_power
            self.on_ground = False
            
        # Apply gravity
        self.vel_y += 0.8  # Gravity strength
        if self.vel_y > 15:  # Terminal velocity
            self.vel_y = 15
            
        # Update position
        self.x += self.vel_x
        self.y += self.vel_y
        
        # Check platform collisions
        self.on_ground = False
        mario_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
        for platform in platforms:
            plat_rect = pygame.Rect(platform.x, platform.y, platform.width, platform.height)
            
            # Check if Mario is colliding with platform
            if mario_rect.colliderect(plat_rect):
                # Check collision from top
                if self.vel_y > 0 and mario_rect.bottom > plat_rect.top and mario_rect.top < plat_rect.top:
                    self.y = plat_rect.top - self.height
                    self.on_ground = True
                    self.vel_y = 0
                # Check collision from bottom
                elif self.vel_y < 0 and mario_rect.top < plat_rect.bottom and mario_rect.bottom > plat_rect.bottom:
                    self.y = plat_rect.bottom
                    self.vel_y = 0
                # Check collision from left
                elif self.vel_x > 0 and mario_rect.right > plat_rect.left and mario_rect.left < plat_rect.left:
                    self.x = plat_rect.left - self.width
                # Check collision from right
                elif self.vel_x < 0 and mario_rect.left < plat_rect.right and mario_rect.right > plat_rect.right:
                    self.x = plat_rect.right
        
        # Boundary checking - prevent falling through bottom
        if self.y > SCREEN_HEIGHT - self.height:
            self.y = SCREEN_HEIGHT - self.height
            self.on_ground = True
            self.vel_y = 0
            
        # Left boundary
        if self.x < 0:
            self.x = 0
            
    def draw(self, screen, camera_x):
        x = self.x - camera_x
        
        # Only draw if on screen
        if -self.width < x < SCREEN_WIDTH:
            # Draw Mario based on power-up state
            if self.power_up_state == 0:  # Small Mario
                pygame.draw.rect(screen, MARIO_RED, (x + 8, self.y + 12, 16, 12))  # Body
                pygame.draw.rect(screen, MARIO_BLUE, (x + 6, self.y + 16, 20, 16))  # Overalls
                pygame.draw.rect(screen, (255, 220, 177), (x + 4, self.y, 24, 16))  # Face
                pygame.draw.rect(screen, MARIO_RED, (x + 2, self.y - 4, 28, 8))     # Hat
            else:  # Super Mario (larger)
                pygame.draw.rect(screen, MARIO_RED, (x + 6, self.y + 20, 20, 16))  # Body
                pygame.draw.rect(screen, MARIO_BLUE, (x + 4, self.y + 24, 24, 20))  # Overalls
                pygame.draw.rect(screen, (255, 220, 177), (x + 2, self.y + 4, 28, 20))  # Face
                pygame.draw.rect(screen, MARIO_RED, (x, self.y, 32, 8))             # Hat

class Platform:
    def __init__(self, x, y, width, height, color=BRICK_RED, breakable=False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.breakable = breakable
        
    def draw(self, screen, camera_x):
        x = self.x - camera_x
        
        # Only draw if on screen
        if -self.width < x < SCREEN_WIDTH:
            pygame.draw.rect(screen, self.color, (x, self.y, self.width, self.height))
            
            # Add brick pattern if it's a breakable brick
            if self.breakable:
                for i in range(0, self.width, 4):
                    for j in range(0, self.height, 4):
                        pygame.draw.rect(screen, (min(self.color[0] + 20, 255), 
                                                min(self.color[1] + 20, 255), 
                                                min(self.color[2] + 20, 255)), 
                                        (x + i, self.y + j, 2, 2))

class Coin:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 16
        self.height = 16
        self.rotation = 0
        self.collected = False
        
    def update(self):
        if not self.collected:
            self.rotation += 0.2  # Animation speed
            
    def draw(self, screen, camera_x):
        if not self.collected:
            x = self.x - camera_x
            
            # Only draw if on screen
            if -self.width < x < SCREEN_WIDTH:
                # Create spinning effect using sine wave
                scale = abs(math.sin(self.rotation))
                width = int(self.width * scale)
                height = self.height
                coin_rect = pygame.Rect(x + (self.width - width) // 2, self.y, width, height)
                pygame.draw.ellipse(screen, COIN_YELLOW, coin_rect)

class Goomba:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 32
        self.height = 32
        self.vel_x = -1  # Move left initially
        self.alive = True
        
    def update(self, platforms, camera_x):
        if self.alive:
            self.x += self.vel_x
            
            # Simple edge detection and platform following
            on_ground = False
            goomba_rect = pygame.Rect(self.x, self.y, self.width, self.height)
            
            for platform in platforms:
                plat_rect = pygame.Rect(platform.x, platform.y, platform.width, platform.height)
                
                # Check if Goomba is on a platform
                if (goomba_rect.bottom == plat_rect.top and 
                    goomba_rect.right > plat_rect.left and 
                    goomba_rect.left < plat_rect.right):
                    on_ground = True
                    
                # Reverse direction if hitting a wall
                if goomba_rect.colliderect(plat_rect):
                    if self.vel_x > 0:  # Moving right
                        self.x = plat_rect.left - self.width
                        self.vel_x *= -1
                    elif self.vel_x < 0:  # Moving left
                        self.x = plat_rect.right
                        self.vel_x *= -1
            
            # If not on ground, fall
            if not on_ground and self.y < SCREEN_HEIGHT - self.height:
                self.y += 5
                    
    def draw(self, screen, camera_x):
        if self.alive:
            x = self.x - camera_x
            
            # Only draw if on screen
            if -self.width < x < SCREEN_WIDTH:
                # Draw a simple Goomba representation
                pygame.draw.rect(screen, (139, 69, 19), (x, self.y, self.width, self.height))  # Brown body
                pygame.draw.rect(screen, BLACK, (x + 8, self.y + 8, 6, 6))  # Left eye
                pygame.draw.rect(screen, BLACK, (x + 18, self.y + 8, 6, 6)) # Right eye

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Super Mario Bros 3-style Game")
        self.clock = pygame.time.Clock()
        self.running = True
        self.score = 0
        self.lives = 3
        self.coins = 0
        self.world = 1
        self.level = 1
        self.time_left = 300  # 5 minutes in seconds
        self.camera_x = 0
        self.game_state = "overworld"  # "overworld" or "level"
        self.overworld_map = OverworldMap()
        
        # Create game objects for level
        self.mario = Mario(100, 300)
        self.platforms = []
        self.level_coins = []
        self.goombas = []
        
        # Load fonts for SNES-style HUD
        self.hud_font_large = pygame.font.SysFont('Arial', 24, bold=True)
        self.hud_font_small = pygame.font.SysFont('Arial', 18, bold=True)
        self.hud_font_tiny = pygame.font.SysFont('Arial', 14, bold=True)
        
        self.setup_level()
        
    def setup_level(self):
        # Clear existing objects
        self.platforms.clear()
        self.level_coins.clear()
        self.goombas.clear()
        
        # Reset timer for new level
        self.time_left = 300
        
        # Ground platform - fixed to be at the bottom of the screen
        self.platforms.append(Platform(0, SCREEN_HEIGHT - 40, SCREEN_WIDTH * 3, 40, (94, 53, 15)))
        
        # Some floating platforms
        self.platforms.append(Platform(200, 400, 200, 20, BRICK_RED, True))
        self.platforms.append(Platform(500, 350, 150, 20))
        self.platforms.append(Platform(700, 300, 100, 20, BRICK_RED, True))
        self.platforms.append(Platform(900, 400, 200, 20))
        
        # Add some coins
        for i in range(10):
            self.level_coins.append(Coin(300 + i * 50, 350))
            
        # Add some enemies - properly placed on ground
        self.goombas.append(Goomba(400, SCREEN_HEIGHT - 40 - 32))
        self.goombas.append(Goomba(800, SCREEN_HEIGHT - 40 - 32))
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if self.game_state == "overworld":
                    # Overworld movement
                    if event.key == pygame.K_RIGHT:
                        new_x = self.overworld_map.player_map_pos[0] + 1
                        if self.overworld_map.can_move_to(new_x, self.overworld_map.player_map_pos[1]):
                            self.overworld_map.player_map_pos[0] = new_x
                    elif event.key == pygame.K_LEFT:
                        new_x = self.overworld_map.player_map_pos[0] - 1
                        if self.overworld_map.can_move_to(new_x, self.overworld_map.player_map_pos[1]):
                            self.overworld_map.player_map_pos[0] = new_x
                    elif event.key == pygame.K_UP:
                        new_y = self.overworld_map.player_map_pos[1] - 1
                        if self.overworld_map.can_move_to(self.overworld_map.player_map_pos[0], new_y):
                            self.overworld_map.player_map_pos[1] = new_y
                    elif event.key == pygame.K_DOWN:
                        new_y = self.overworld_map.player_map_pos[1] + 1
                        if self.overworld_map.can_move_to(self.overworld_map.player_map_pos[0], new_y):
                            self.overworld_map.player_map_pos[1] = new_y
                    elif event.key == pygame.K_RETURN:
                        # Enter level if on a special tile
                        tile_x, tile_y = self.overworld_map.player_map_pos
                        tile_type = self.overworld_map.map_data[tile_y][tile_x]
                        if tile_type in [2, 4, 5]:  # Grass, castle, or pipe
                            self.game_state = "level"
                            self.setup_level()
                
    def update(self):
        if self.game_state == "level":
            # Update Mario with camera position for proper collision detection
            self.mario.update(self.platforms, self.camera_x)
            
            for coin in self.level_coins:
                coin.update()
                
            for goomba in self.goombas:
                goomba.update(self.platforms, self.camera_x)
                
            self.handle_collisions()
            self.update_camera()
            
            # Update timer
            self.time_left -= 1/FPS
            if self.time_left <= 0:
                self.time_left = 0
                # Time's up - lose a life
                self.lives -= 1
                if self.lives <= 0:
                    self.game_state = "overworld"
                    self.lives = 3
                else:
                    # Reset level
                    self.setup_level()
                    self.mario.x = 100
                    self.mario.y = 300
                    self.camera_x = 0
            
            # Check if level is complete (simple condition: reach far right)
            if self.mario.x > SCREEN_WIDTH * 2.5:
                self.game_state = "overworld"
                # Reset Mario position on map
                self.overworld_map.player_map_pos[0] += 1
                self.score += 1000  # Bonus for completing level
        
    def handle_collisions(self):
        mario_rect = pygame.Rect(self.mario.x, self.mario.y, self.mario.width, self.mario.height)
        
        # Coin collisions
        for coin in self.level_coins:
            if not coin.collected:
                coin_rect = pygame.Rect(coin.x, coin.y, coin.width, coin.height)
                if mario_rect.colliderect(coin_rect):
                    coin.collected = True
                    self.score += 100
                    self.coins += 1
                    if self.coins >= 100:
                        self.coins = 0
                        self.lives += 1
                    
        # Goomba collisions
        for goomba in self.goombas:
            if goomba.alive:
                goomba_rect = pygame.Rect(goomba.x, goomba.y, goomba.width, goomba.height)
                if mario_rect.colliderect(goomba_rect):
                    if self.mario.vel_y > 0 and self.mario.y + self.mario.height - 10 < goomba.y:  # Mario is falling onto Goomba
                        goomba.alive = False
                        self.mario.vel_y = -8  # Bounce off
                        self.score += 200
                    else:
                        if self.mario.power_up_state > 0:
                            self.mario.power_up_state -= 1
                            # Brief invincibility would be good here
                        else:
                            self.lives -= 1
                            # Reset Mario position
                            self.mario.x = 100
                            self.mario.y = 300
                            self.camera_x = 0
                            if self.lives <= 0:
                                self.game_state = "overworld"
                                self.lives = 3  # Reset lives
                                self.score = max(0, self.score - 1000)  # Penalty for game over
        
    def update_camera(self):
        # Camera follows Mario but doesn't go beyond level boundaries
        target_x = self.mario.x - SCREEN_WIDTH // 2
        
        # Keep camera within level bounds
        if target_x < 0:
            self.camera_x = 0
        elif target_x > SCREEN_WIDTH * 2:  # Max camera position (level width is SCREEN_WIDTH * 3)
            self.camera_x = SCREEN_WIDTH * 2
        else:
            self.camera_x = target_x
            
    def draw_snes_hud(self, screen):
        # Draw SNES-style HUD background
        hud_height = 40
        pygame.draw.rect(screen, HUD_BLUE, (0, 0, SCREEN_WIDTH, hud_height))
        pygame.draw.rect(screen, BLACK, (0, hud_height-2, SCREEN_WIDTH, 2))  # Separator line
        
        # Draw world info
        world_text = self.hud_font_small.render(f"WORLD", True, WHITE)
        world_num = self.hud_font_large.render(f"{self.world}-{self.level}", True, HUD_GOLD)
        screen.blit(world_text, (20, 5))
        screen.blit(world_num, (25, 20))
        
        # Draw lives with Mario icon
        pygame.draw.rect(screen, MARIO_RED, (120, 15, 12, 12))  # Simple Mario icon
        lives_text = self.hud_font_large.render(f"×{self.lives}", True, WHITE)
        screen.blit(lives_text, (140, 18))
        
        # Draw coins with coin icon
        pygame.draw.ellipse(screen, COIN_YELLOW, (220, 18, 16, 16))
        coins_text = self.hud_font_large.render(f"×{self.coins}", True, WHITE)
        screen.blit(coins_text, (240, 18))
        
        # Draw score
        score_text = self.hud_font_small.render("SCORE", True, WHITE)
        score_num = self.hud_font_large.render(f"{self.score:06d}", True, HUD_GOLD)
        screen.blit(score_text, (SCREEN_WIDTH - 150, 5))
        screen.blit(score_num, (SCREEN_WIDTH - 150, 20))
        
        # Draw time
        time_text = self.hud_font_small.render("TIME", True, WHITE)
        time_num = self.hud_font_large.render(f"{int(self.time_left):03d}", True, HUD_RED if self.time_left < 100 else WHITE)
        screen.blit(time_text, (SCREEN_WIDTH - 80, 5))
        screen.blit(time_num, (SCREEN_WIDTH - 80, 20))
        
    def draw_overworld_hud(self, screen):
        # Draw SNES-style HUD for overworld
        hud_height = 40
        pygame.draw.rect(screen, HUD_BLUE, (0, 0, SCREEN_WIDTH, hud_height))
        pygame.draw.rect(screen, BLACK, (0, hud_height-2, SCREEN_WIDTH, 2))  # Separator line
        
        # Draw world map title
        title_text = self.hud_font_large.render("WORLD MAP", True, HUD_GOLD)
        screen.blit(title_text, (SCREEN_WIDTH // 2 - 60, 10))
        
        # Draw lives with Mario icon
        pygame.draw.rect(screen, MARIO_RED, (20, 15, 12, 12))  # Simple Mario icon
        lives_text = self.hud_font_large.render(f"×{self.lives}", True, WHITE)
        screen.blit(lives_text, (40, 18))
        
        # Draw coins with coin icon
        pygame.draw.ellipse(screen, COIN_YELLOW, (120, 18, 16, 16))
        coins_text = self.hud_font_large.render(f"×{self.coins}", True, WHITE)
        screen.blit(coins_text, (140, 18))
        
        # Draw score
        score_text = self.hud_font_small.render("SCORE", True, WHITE)
        score_num = self.hud_font_large.render(f"{self.score:06d}", True, HUD_GOLD)
        screen.blit(score_text, (SCREEN_WIDTH - 150, 5))
        screen.blit(score_num, (SCREEN_WIDTH - 150, 20))
        
    def draw(self):
        if self.game_state == "overworld":
            self.draw_overworld()
        else:
            self.draw_level()
        
        pygame.display.flip()
        
    def draw_overworld(self):
        self.screen.fill(SKY_BLUE)
        self.overworld_map.draw(self.screen)
        
        # Draw SNES-style HUD
        self.draw_overworld_hud(self.screen)
        
        # Draw instructions
        instruction_font = pygame.font.SysFont(None, 24)
        instruction_text = instruction_font.render("Use arrow keys to move, ENTER to enter level", True, WHITE)
        self.screen.blit(instruction_text, (SCREEN_WIDTH // 2 - 180, SCREEN_HEIGHT - 30))
        
    def draw_level(self):
        self.screen.fill(SKY_BLUE)
        
        # Draw all game objects
        for platform in self.platforms:
            platform.draw(self.screen, self.camera_x)
            
        for coin in self.level_coins:
            coin.draw(self.screen, self.camera_x)
            
        for goomba in self.goombas:
            goomba.draw(self.screen, self.camera_x)
            
        self.mario.draw(self.screen, self.camera_x)
        
        # Draw SNES-style HUD
        self.draw_snes_hud(self.screen)
        
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
            
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()
