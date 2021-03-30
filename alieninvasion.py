import sys
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stat import GameStats
from time import sleep

class AlienInvasion:
    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((0, 0) , pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.stats= GameStats(self)

        self.create_fleet()
        


        
    def run_game(self):
        while True:
           
            self.check_events()
            self.ship.update()
            self.bullets.update()
            self.update_bullets()
            self.check_fleet_edges()
            self._update_aliens()
            self.update_screen()
        
            
    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self.check_keydown_events(event)  
            elif event.type == pygame.KEYUP:
                self.check_keyup_events(event)
            
    def check_keydown_events(self,event):
        if event.key == pygame.K_RIGHT:
                self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
                self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
    def check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
    def _fire_bullet(self):
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
    def update_bullets(self):
        for bullet in self.bullets.copy():
            if bullet.rect.bottom < 0 :
                self.bullets.remove(bullet)
        collision = pygame.sprite.groupcollide(self.bullets , self.aliens, True , True)
        
        # bringing back the aliens
        if not self.aliens:
            self.bullets.empty()
            self.create_fleet()
            
    def create_fleet(self):
        alien = Alien(self)
        alien_width , alien_height = alien.rect.size
        available_space_x = self.settings.screen_width  - (2 * alien_width)
        no_of_alien_x = int((available_space_x) / (2 * alien_width))
        ship_height = self.ship.rect.height
        available_space_y = self.settings.screen_height - (3* alien_height)- ship_height
        number_rows = available_space_y // (2*alien_height)
        for row_number in range(number_rows):
            for alien_number in range(no_of_alien_x):
                self._create_alien(row_number, alien_number)
    def _create_alien(self, row_number, alien_number):
        alien = Alien(self)
        alien_width  = alien.rect.width
        alien_height = alien.rect.height
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)
    def _update_aliens(self):
        self.aliens.update()
        if pygame.sprite.collideany(self.ship , self.aliens):
            self.ship_hit()

        
    def update_screen(self):
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        pygame.display.flip()
    def check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self.change_fleet_direction()
                break
    def change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1
    def ship_hit(self):
        """respond to ship hit"""
        self.stats.ship_left -= 1
        self.aliens.empty()
        self.bullets.empty()
        self.create_fleet()
        self.center_ship()
          #pause
        sleep(0.5)


    
        

    
        
        

if __name__ == '__main__':
    A = AlienInvasion()
    A.run_game()
