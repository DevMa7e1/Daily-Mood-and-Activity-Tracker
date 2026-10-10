from datetime import datetime

class Day:
    def __init__(self, date: datetime, rating: int = 5, word: str = 'no word', events: dict[str, datetime] = {}) -> None:
        self.date = datetime(date.year, date.month, date.day)
        self.rating = rating
        self.word = word
        self.events = events