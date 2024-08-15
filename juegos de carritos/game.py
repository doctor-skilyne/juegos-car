import pygame
import random
import sys

# Inicializar Pygame
pygame.init()

# Configuración de la ventana
WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Juego de Carreras con Obstáculos")

# Colores
WHITE = (255, 255, 255)

# FPS
 
CLOCK = pygame.time.Clock()
FPS = 80

# Cargar imagen de fondo
try:
    background_image = pygame.image.load('pista.jpg').convert()
    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))  # Ajustar tamaño del fondo
except Exception as e:
    print(f"Error al cargar la imagen de fondo: {e}")
    pygame.quit()
    sys.exit()

# Cargar imagen del obstáculo
try:
    obstacle_image = pygame.image.load('obstaculo.png').convert_alpha()
    obstacle_image = pygame.transform.scale(obstacle_image, (50, 50))  # Ajustar tamaño del obstáculo
except Exception as e:
    print(f"Error al cargar la imagen del obstáculo: {e}")
    pygame.quit()
    sys.exit()

# Clase para el Vehículo
class Vehicle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        try:
            self.image = pygame.image.load('carrit.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (90, 70))  # Ajustar tamaño
        except Exception as e:
            print(f"Error al cargar la imagen del carrito: {e}")
            pygame.quit()
            sys.exit()
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT - 50)
        self.speed = 5

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.speed

        # Limitar el movimiento del vehículo a la ventana
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

# Clase para los Obstáculos
class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = obstacle_image  # Usar la imagen del obstáculo
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = random.randint(-150, -self.rect.height)
        self.speed = 5

    def update(self):
        self.rect.y += self.speed
        if self.rect.y > HEIGHT:
            self.kill()

# Crear instancias y grupos de sprites
vehicle = Vehicle()
all_sprites = pygame.sprite.Group()
all_sprites.add(vehicle)

obstacles = pygame.sprite.Group()

def spawn_obstacle():
    if random.random() < 0.02:
        obstacle = Obstacle()
        all_sprites.add(obstacle)
        obstacles.add(obstacle)

# Función para verificar colisiones
def check_collisions():
    if pygame.sprite.spritecollideany(vehicle, obstacles):
        return True
    return False

# Función para dibujar la puntuación
score = 0

def draw_score():
    global score
    font = pygame.font.SysFont(None, 36)
    text = font.render(f'Score: {score}', True, WHITE)
    WIN.blit(text, (10, 10))

# Función para mostrar "Game Over" y la puntuación final
def draw_game_over():
    font = pygame.font.SysFont(None, 72)
    game_over_text = font.render("Game Over", True, WHITE)
    score_text = font.render(f'Final Score: {score}', True, WHITE)
    
    WIN.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - game_over_text.get_height() // 2 - 50))
    WIN.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 + 10))
    pygame.display.flip()
    pygame.time.wait(3000)  # Esperar 3 segundos antes de cerrar el juego

# Bucle principal del juego
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Dibujar el fondo
    WIN.blit(background_image, (0, 0))

    # Actualizar
    all_sprites.update()
    spawn_obstacle()

    # Verificar colisiones
    if check_collisions():
        draw_game_over()
        running = False

    # Incrementar puntuación
    score += 1

    # Dibujar los sprites y la puntuación
    all_sprites.draw(WIN)
    draw_score()

    pygame.display.flip()
    CLOCK.tick(FPS)

pygame.quit()
