import pygame, sys
from utils import load_image, WIDTH, HEIGHT
from entities import Player, Pipe
from random import randint, choice
from debug import debug

BG_HEIGHT = 512
    
class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()

        pygame.display.set_caption('Flappy Bird')
        pygame.display.set_icon(pygame.image.load('assets/favicon.ico'))

        #Assets
        self.background = load_image('background-day2.png')
        self.ground = load_image('base.png')      
        self.message = load_image('message.png')
        self.game_over = load_image('gameover.png')
        self.dying_sound = pygame.mixer.Sound('assets/audio/die.wav')
        self.hit_sound = pygame.mixer.Sound('assets/audio/hit.wav')

        self.point_sound = pygame.mixer.Sound('assets/audio/point.wav')
        self.font = pygame.font.Font('assets/sprites/flappy-bird-font.ttf', 30)
        self.font2 = pygame.font.Font('assets/FlappyBirdy.ttf', 60)
        
        self.ground_rect = self.ground.get_rect(topleft=(0, 512))
   
        self.game_active = False
        self.show_start_screen = True

        self.score = 0

        # Sprites
        self.player = Player(self, choice(['blue', 'yellow', 'red']))
        self.player_sprite = pygame.sprite.GroupSingle()
        self.player_sprite.add(self.player) 
        self.pipes = pygame.sprite.Group()
        
        # Timers
        self.pipe_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.pipe_timer, 1500)

    def pipe_maker(self, allowance_area):
        pipe_color = choice(['green', 'red'])
        down_pipe = Pipe(self, pipe_color)
        up_pipe = Pipe(self, pipe_color, True)

        center_point = randint(int(0.25*BG_HEIGHT), int(0.75*BG_HEIGHT))
        if center_point + allowance_area > BG_HEIGHT or center_point - allowance_area < BG_HEIGHT:
            center_point = randint(int(0.35*BG_HEIGHT), int(0.65*BG_HEIGHT))
        # x position stays the same, only y value changes (bottom or top)
        up_pipe.rect.bottom = center_point - allowance_area
        down_pipe.rect.top = center_point + allowance_area
        self.pipes.add(down_pipe)
        self.pipes.add(up_pipe)

    def score_tracker(self):
        for pipe in self.pipes:
            if self.player.rect.topleft[0] > pipe.rect.topleft[0]:
                self.point_sound.play()
                self.score += 0.5
    
    def score_display(self):
        score = self.font.render(f'{int(self.score)}', False, (0, 0, 0))
        score_rect = score.get_rect(center=(WIDTH // 2, HEIGHT // 6))
        self.screen.blit(score, score_rect)
    
    def game_over_score_display(self):
        score_over = self.font2.render('Score', False, 'blue')
        score_over_value = self.font.render(f'{int(self.score)}', False, 'blue')
        
        score_over_rect = score_over.get_rect(center=(WIDTH // 2, 420))
        score_over_value_rect = score_over_value.get_rect(center=(WIDTH // 2, 470))
        
        self.screen.blit(score_over, score_over_rect)
        self.screen.blit(score_over_value, score_over_value_rect)

    def start_screen(self):
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.ground, (0, 512)) 
        self.screen.blit(self.message, (WIDTH // 4, HEIGHT // 4))

    def run(self):
        while True:
            # Event Loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if self.show_start_screen:
                    self.start_screen()
                    if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYUP:
                        self.show_start_screen = False
                        self.game_active = True
                if self.game_active:
                    if event.type == self.pipe_timer:
                        self.pipe_maker(100)    
                        self.score_tracker()
                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                            self.player.press = True
                else:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.pipes.empty()
                        self.score = 0
                        self.game_active = True

            if self.game_active:  
                self.screen.blit(self.background, (0, 0))
                self.pipes.draw(self.screen)
                self.pipes.update()

                self.screen.blit(self.ground, (0, 512)) 

                self.player_sprite.draw(self.screen)
                self.player_sprite.update()
                self.score_display()

            elif self.show_start_screen == False and self.game_active == False:
                self.screen.blit(self.background, (0, 0))
                self.screen.blit(self.ground, (0, 512)) 
                self.screen.blit(self.game_over, (WIDTH // 4, HEIGHT // 2))
                self.game_over_score_display()

            # Debugging Information
            # debug(pygame.mouse.get_pos())
            # debug(pygame.mouse.get_pressed()[0], 0, 40)

            pygame.display.update()
            self.clock.tick(60)

if __name__ == '__main__':
    game = Game()
    game.run()