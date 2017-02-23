import numpy as np
from numpy.random import choice

class Generator:
    videos = []
    video_count = 0
    cache_count = 0
    cache_size = 0

    prob_dist = []                                  # video selection probability distribution

    size_consideration_ratio = 0.2

    def __init__(self, videos, cache_count, cache_size):
        self.videos = videos
        self.video_count = len(videos)
        self.cache_count = cache_count
        self.cache_size = cache_size
        sum_r = float(sum(requests for size, requests in videos))
        sum_s = float(sum(size for size, requests in videos))
        for size, requests in videos:
            self.prob_dist.append(float(size) / sum_s * self.size_consideration_ratio + float(requests) / sum_r  * (1.0 - self.size_consideration_ratio) )

    def new_specimen(self):                        # random specimen
        spec = np.zeros(shape = (self.cache_count, self.video_count), dtype=np.int)
        for i in range(self.cache_count):
            available_size = self.cache_size
            valid = True
            vids = []
            while valid:
                vid = choice(range(self.video_count), 1, self.prob_dist)
                if vid in vids:
                    valid = False
                elif self.videos[vid][0] > available_size:
                    valid = False
                else:
                    available_size -= self.videos[vid][0]
                    vids.append(vid)
                    spec[i, vid] = 1
        return spec

    def new_specimen(self, parentA, parentB):      # genetic specimen
        pass

    def random_generation(self, speciment_count):   # randomised generation of specimens
        generation = []
        for i in range(speciment_count):
            generation.append(self.new_specimen())
        return generation

    def new_generation(self, speciment_count, previous_best):   # genetic generation of specimens
        pass

    def get_generation(self, speciment_count, previous_best):   # get new generation
        if previous_best == []:
            return self.Random_Generation(speciment_count)
        else:
            return self.New_Generation(speciment_count, previous_best)
