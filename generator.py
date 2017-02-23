import numpy
from numpy.random import choice

class Generator:
    videos = []
    video_count = 0
    cache_count = 0

    def __init__(self, videos, cache_count):
        self.videos = videos
        self.video_count = len(videos)
        self.cache_count = cache_count

    def New_Speciment(self):
        pass


    def New_Speciment(self, parentA, parentB):
        pass

    def Random_Generation(self, speciment_count):
        pass

    def New_Generation(self, speciment_count, previous_best):
        pass
    def Get_Generation(self, speciment_count, previous_best):
        if previous_best == []:
            return self.Random_Generation(speciment_count)
        else
            return self.New_Generation(speciment_count, previous_best)
