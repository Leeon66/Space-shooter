import pygame, random, sys

pygame.init()
W, H = 480, 640
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Space Shooter")
clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 24)
big_font = pygame.font.SysFont("arial", 48)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 30), pygame.SRCALPHA)
        pygame.draw.polygon(self.image, (0, 200, 255), [(20, 0), (0, 30), (40, 30)])
        self.rect = self.image.get_rect(midbottom=(W // 2, H - 20))
        self.last_shot = 0

    def update(self):
        keys = pygame.key.get_pressed()
        self.rect.x += 6 * ((keys[pygame.K_RIGHT] or keys[pygame.K_d]) - (keys[pygame.K_LEFT] or keys[pygame.K_a]))
        self.rect.clamp_ip(screen.get_rect())
        now = pygame.time.get_ticks()
        if keys[pygame.K_SPACE] and now - self.last_shot > 250:
            self.last_shot = now
            bullet = Bullet(self.rect.centerx, self.rect.top)
            all_sprites.add(bullet)
            bullets.add(bullet)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((4, 14))
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect(midbottom=(x, y))

    def update(self):
        self.rect.y -= 10
        if self.rect.bottom < 0:
            self.kill()


class Enemy(pygame.sprite.Sprite):
    def __init__(self, speed_bonus):
        super().__init__()
        self.image = pygame.Surface((34, 34))
        self.image.fill((255, 60, 60))
        self.rect = self.image.get_rect(x=random.randint(0, W - 34), y=-40)
        self.speed = random.randint(2, 4) + speed_bonus

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > H:
            self.kill()


def new_game():
    global all_sprites, bullets, enemies, player, score, lives, game_over
    all_sprites, bullets, enemies = (pygame.sprite.Group() for _ in range(3))
    player = Player()
    all_sprites.add(player)
    score, lives, game_over = 0, 3, False


new_game()
stars = [(random.randint(0, W), random.randint(0, H)) for _ in range(60)]
SPAWN = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN, 700)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); sys.exit()
        if event.type == SPAWN and not game_over:
            enemy = Enemy(score // 100)  # enemies get faster as score rises
            all_sprites.add(enemy)
            enemies.add(enemy)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r and game_over:
            new_game()

    if not game_over:
        all_sprites.update()
        score += 10 * len(pygame.sprite.groupcollide(enemies, bullets, True, True))
        lives -= len(pygame.sprite.spritecollide(player, enemies, True))
        game_over = lives <= 0

    screen.fill((10, 10, 30))
    for x, y in stars:
        pygame.draw.circle(screen, (200, 200, 200), (x, y), 1)
    all_sprites.draw(screen)
    screen.blit(font.render(f"Score: {score}   Lives: {lives}", True, (255, 255, 255)), (10, 10))
    if game_over:
        text = big_font.render("GAME OVER", True, (255, 80, 80))
        screen.blit(text, text.get_rect(center=(W // 2, H // 2 - 20)))
        hint = font.render("Press R to restart", True, (255, 255, 255))
        screen.blit(hint, hint.get_rect(center=(W // 2, H // 2 + 30)))
    pygame.display.flip()
    clock.tick(60)