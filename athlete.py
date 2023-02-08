from scraper import Scraper
from typing import Dict

class Athlete(Scraper):
    def __init__(self, completed_goals: int, uncompleted_goals: int, rewards: int, total_goals: int, measurements: Dict[str, float]):
        self.completed_goals = completed_goals
        self.uncompleted_goals = uncompleted_goals
        self.rewards = rewards
        self.total_goals = total_goals
        self.measurements = measurements
