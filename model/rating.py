from dataclasses import dataclass


@dataclass
class Rating:
    movie_id: str
    avg_rating : float
    total_votes : int
    median_rating : int

    def __hash__(self):
        return hash(self.movie_id)

    def __eq__(self, other):
        return self.movie_id == other.movie_id

    def __str__(self):
        return str(self.avg_rating)