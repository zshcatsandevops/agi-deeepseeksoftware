# program.py
import pygame
import math
import os

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
        
    def update(self, platforms):
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
            
            # Horizontal collision
            if mario_rect.colliderect(plat_rect):
                if self.vel_x > 0:  # Moving right
                    self.x = plat_rect.left - self.width
                elif self.vel_x < 0:  # Moving left
                    self.x = plat_rect.right
            
            # Vertical collision
            mario_rect = pygame.Rect(self.x, self.y, self.width, self.height)
            if mario_rect.colliderect(plat_rect):
                if self.vel_y > 0:  # Falling
                    self.y = plat_rect.top - self.height
                    self.on_ground = True
                    self.vel_y = 0
                elif self.vel_y < 0:  # Jumping
                    self.y = plat_rect.bottom
                    self.vel_y = 0
        
        # Boundary checking
        if self.y > SCREEN_HEIGHT - self.height:
            self.y = SCREEN_HEIGHT - self.height
            self.on_ground = True
            self.vel_y = 0
            
    def draw(self, screen, camera_x):
        x = self.x - camera_x
        # Draw a simple Mario representation
        pygame.draw.rect(screen, MARIO_RED, (x + 8, self.y + 12, 16, 12))  # Body
        pygame.draw.rect(screen, MARIO_BLUE, (x + 6, self.y + 16, 20, 16))  # Overalls
        pygame.draw.rect(screen, (255, 220, 177), (x + 4, self.y, 24, 16))  # Face
        pygame.draw.rect(screen, MARIO_RED, (x + 2, self.y - 4, 28, 8))     # Hat

class Platform:
    def __init__(self, x, y, width, height, color=BRICK_RED):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        
    def draw(self, screen, camera_x):
        x = self.x - camera_x
        pygame.draw.rect(screen, self.color, (x, self.y, self.width, self.height))

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
        
    def update(self, platforms):
        if self.alive:
            self.x += self.vel_x
            
            # Simple edge detection (would need improvement for actual platform edges)
            for platform in platforms:
                if (self.x < platform.x or 
                    self.x + self.width > platform.x + platform.width):
                    self.vel_x *= -1  # Reverse direction
                    break
                    
    def draw(self, screen, camera_x):
        if self.alive:
            x = self.x - camera_x
            # Draw a simple Goomba representation
            pygame.draw.rect(screen, (139, 69, 19), (x, self.y, self.width, self.height))  # Brown body
            pygame.draw.rect(screen, BLACK, (x + 8, self.y + 8, 6, 6))  # Left eye
            pygame.draw.rect(screen, BLACK, (x + 18, self.y + 8, 6, 6)) # Right eye

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Mario-like Game")
        self.clock = pygame.time.Clock()
        self.running = True
        self.score = 0
        self.lives = 3
        self.camera_x = 0
        
        # Create game objects
        self.mario = Mario(100, 300)
        self.platforms = []
        self.coins = []
        self.goombas = []
        
        self.setup_level()
        
    def setup_level(self):
        # Ground platform
        self.platforms.append(Platform(0, SCREEN_HEIGHT - 40, SCREEN_WIDTH * 3, 40))
        
        # Some floating platforms
        self.platforms.append(Platform(200, 400, 200, 20))
        self.platforms.append(Platform(500, 350, 150, 20))
        self.platforms.append(Platform(700, 300, 100, 20))
        self.platforms.append(Platform(900, 400, 200, 20))
        
        # Add some coins
        for i in range(10):
            self.coins.append(Coin(300 + i * 50, 350))
            
        # Add some enemies
        self.goombas.append(Goomba(400, 368))
        self.goombas.append(Goomba(800, 368))
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                
    def update(self):
        self.mario.update(self.platforms)
        
        for coin in self.coins:
            coin.update()
            
        for goomba in self.goombas:
            goomba.update(self.platforms)
            
        self.handle_collisions()
        self.update_camera()
        
    def handle_collisions(self):
        mario_rect = pygame.Rect(self.mario.x, self.mario.y, self.mario.width, self.mario.height)
        
        # Coin collisions
        for coin in self.coins:
            if not coin.collected:
                coin_rect = pygame.Rect(coin.x, coin.y, coin.width, coin.height)
                if mario_rect.colliderect(coin_rect):
                    coin.collected = True
                    self.score += 100
                    
        # Goomba collisions
        for goomba in self.goombas:
            if goomba.alive:
                goomba_rect = pygame.Rect(goomba.x, goomba.y, goomba.width, goomba.height)
                if mario_rect.colliderect(goomba_rect):
                    if self.mario.vel_y > 0 and self.mario.y < goomba.y:  # Mario is falling onto Goomba
                        goomba.alive = False
                        self.mario.vel_y = -8  # Bounce off
                        self.score += 200
                    else:
                        self.lives -= 1
                        # Reset Mario position
                        self.mario.x = 100
                        self.mario.y = 300
                        if self.lives <= 0:
                            self.running = False
        
    def update_camera(self):
        # Camera follows Mario but doesn't go beyond level start
        self.camera_x = self.mario.x - SCREEN_WIDTH // 2
        if self.camera_x < 0:
            self.camera_x = 0
        # Maximum camera position would be set based on level width in a full game
            
    def draw(self):
        self.screen.fill(SKY_BLUE)
        
        # Draw all game objects
        for platform in self.platforms:
            platform.draw(self.screen, self.camera_x)
            
        for coin in self.coins:
            coin.draw(self.screen, self.camera_x)
            
        for goomba in self.goombas:
            goomba.draw(self.screen, self.camera_x)
            
        self.mario.draw(self.screen, self.camera_x)
        
        # Draw UI
        font = pygame.font.SysFont(None, 36)
        score_text = font.render(f"Score: {self.score}", True, WHITE)
        lives_text = font.render(f"Lives: {self.lives}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(lives_text, (SCREEN_WIDTH - 120, 10))
        
        pygame.display.flip()
        
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)  # Control game speed :cite[4]
            
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()
