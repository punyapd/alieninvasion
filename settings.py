class Settings:
    def __init__(self):
        self.bg_color= (230 ,230,230)
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (0, 0 ,0)
        self.bullets_allowed = 5
        self.fleet_drop_speed = 10
        self.ship_limit = 3
        self.speedup_scale = 1.1
        self.alien_points = 50
        self.score_scale = 1.5
    def initalize_dynamic_settings(self):
        self.ship_speed  = 1
        self.bullet_speed = 5
        self.alien_speed = 1
        self.fleet_direction = 1
    def increase_speed(self):
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
    



    