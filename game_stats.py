class GameStats():
    """track the stats of the game"""
    def __init__(self, ai_settings):
        self.ai_settings = ai_settings
        self.reset_stats()
        # inactive at first
        self.game_active = False

        # the highest score should not be reset in any case
        self.high_score = 0

    def reset_stats(self):
        """the information which maybe change in game"""
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1
