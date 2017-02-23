import numpy as np
from numpy.random import choice
import random as r
import math

class Generator:
    videos = []
    video_count = 0
    cache_count = 0
    cache_size = 0

    prob_dist = []                                  # video selection probability distribution

    size_consideration_ratio = 0

    def __init__(self, videos, cache_count, cache_size):
        self.videos = videos
        self.video_count = len(videos)
        self.cache_count = cache_count
        self.cache_size = cache_size
#        print(self.video_count)
        sum_r = float(sum(requests for size, requests in videos))
        sum_s = float(sum(size for size, requests in videos))
        for size, requests in videos:
            self.prob_dist.append(float(size) / sum_s * self.size_consideration_ratio + float(requests) / sum_r  * (1.0 - self.size_consideration_ratio) )
        print(self.prob_dist)

    def random_cache(self):
        cache = np.zeros(shape = (1, self.video_count), dtype=np.int)
        available_size = self.cache_size
        valid = True
        vids = []
        while valid:
            vid = choice(range(self.video_count), 1, p=self.prob_dist)[0]
            print(vid)
            if vid in vids:
                valid = False
            elif self.videos[vid][0] > available_size:
                valid = False
            else:
                available_size -= self.videos[vid][0]
                vids.append(vid)
                cache[0, vid] = 1
        return np.array([cache])

    def random_specimen(self):                        # random specimen
        spec = np.zeros(shape = (self.cache_count, self.video_count), dtype=np.int)
        for i in range(self.cache_count):
            spec[i] = self.random_cache()
        return spec

    def mutate(self, specimenA, specimenB):
        specimenA[r.randrange(self.cache_count)] = self.random_cache()
        return specimenA

    def recombine(self, specimenA, specimenB):
        rn = r.randrange(self.cache_count)
        specimenA[rn] = specimenB[rn]
        return specimenA

    def cross_recombine(self, specimenA, specimenB):
        specimenA[r.randrange(self.cache_count)] = specimenB[r.randrange(self.cache_count)]
        return specimenA

    def new_specimen(self, parentA, parentB):      # genetic specimen
        actions = [self.mutate, self.recombine, self.cross_recombine]
        costs = [0.1, 0.08, 0.15]
        prob = [c/sum(costs) for c in costs]
        budget = 1.0

        new_specimen = np.asmatrix(np.array(parentA).copy(), dtype = int)
        while r.random() < budget:
            c = choice(range(len(actions)), 1, p=prob)[0]
            budget -= costs[c]
            new_specimen = actions[c](new_specimen, parentB)
        return new_specimen

    def random_generation(self, speciment_count):   # randomised generation of specimens
        generation = []
        for i in range(speciment_count):
            generation.append(self.random_specimen())
        return generation

    def new_generation(self, speciment_count, previous_best):   # genetic generation of specimens
        prob_un = [math.exp(-float(x) / float(speciment_count)) for x in range(speciment_count)]
        prob = [x / sum(prob_un) for x in prob_un]
        new_gen = previous_best
        for i in range(speciment_count - len(previous_best)):
            selected = choice(range(speciment_count), 2, p = prob, replace=False)
            new_gen.append(self.new_speciment(previous_best[selected[0]], previous_best[selected[1]]))
        return new_gen


    def get_generation(self, speciment_count, previous_best):   # get new generation
        if previous_best == []:
            return self.random_generation(speciment_count)
        else:
            return self.new_specimen(speciment_count, previous_best)

    def print_speciment(self, speciment):
        print(np.transpose(np.nonzero(speciment)))

vids = [[50, 1000], [50, 1000], [80, 0], [30, 1500]]

gen = Generator(vids, 3, 100)
generation = gen.get_generation(10, [])
print(generation)
print_speciment(generation[0])
#generation2 = gen.get_generation(10, generation[:3])
