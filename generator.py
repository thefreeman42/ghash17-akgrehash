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
        #print(self.prob_dist)

    def random_cache(self):
        cache = np.zeros(shape = (1, self.video_count), dtype=np.int)
        available_size = self.cache_size
        valid = True
        vids = []
        while valid:
            vid = choice(range(self.video_count), 1, p=self.prob_dist)[0]
            #print(vid)
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
        #print(specimenA)
        #print(specimenB)
        specimenA[r.randrange(self.cache_count - 1)] = self.random_cache()
        return specimenA

    def recombine(self, specimenA, specimenB):
        #print(specimenA)
        #print(specimenB)
        rn = r.randrange(self.cache_count - 1)
        specimenA[rn] = specimenB[rn]
        return specimenA

    def cross_recombine(self, specimenA, specimenB):
        #print(specimenA)
        #print(specimenB)
        specimenA[r.randrange(self.cache_count - 1)] = specimenB[r.randrange(self.cache_count - 1)]
        return specimenA

    def new_specimen(self, parentA, parentB):      # genetic specimen
        actions = [self.mutate, self.recombine, self.cross_recombine]
        costs = [0.1, 0.08, 0.15]
        prob = [c/sum(costs) for c in costs]
        budget = 1.0
        #print(parentA)
        new_specimen = np.asmatrix(np.array(parentA).copy(), dtype = int)
        #print(new_specimen)
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
        prev_n = len(previous_best)

        prob_un = [math.exp(-float(x) / float(prev_n)) for x in range(prev_n)]
        prob = [x / sum(prob_un) for x in prob_un]

        # print(len(range(prev_n)))
        # print(len(prob))

        new_gen = previous_best
        for i in range(speciment_count - len(previous_best)):
            selected = choice(range(prev_n), 2, replace=False, p=prob)
            # print(selected[0])
            # print(selected[1])
            # print(previous_best[selected[0]])
            # print(previous_best[selected[1]])
            # print('foo')
            new_gen.append(self.new_specimen(previous_best[selected[0]], previous_best[selected[1]]))
        return new_gen

    def get_generation(self, speciment_count, previous_best):   # get new generation
        if previous_best == []:
            return self.random_generation(speciment_count)
        else:
            return self.new_generation(speciment_count, previous_best)

    def print_speciment(self, speciment):
        output = {}
        for n, i in np.transpose(np.nonzero(speciment)):
            if n not in output.keys():
                output[n] = []
            output[n].append(str(i))
        #print(output)
        #print(len(output))
        data = []
        data.append(str(len(output)))
        for key in output:
            st = str(key) + ' ' + ' '.join(output[key])
            data.append(st)
        fin = '\n'.join(data)
        return fin

# vids = [[50, 1000], [50, 1000], [80, 0], [30, 1500]]
#
# gen = Generator(vids, 3, 100)
# generation = gen.get_generation(5, [])
# for s in generation:
#     print(gen.print_speciment(s))
# print('\n\n')
# generation2 = gen.get_generation(5, generation[0:2])
# for s in generation2:
#     print(gen.print_speciment(s))
