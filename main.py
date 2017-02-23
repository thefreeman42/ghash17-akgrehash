# AKG ReHash @ Google Hash Code 2017
from Endpoint import Endpoint
import numpy as np
from generator import Generator

def main():

    filename = 'me_at_the_zoo.in'
    P = input('Population size: ')
    S = input('Selection size: ')

    def setup(f):
        with open(f) as file:
            lines = file.readlines()

        n_video, n_endpoint, n_request, n_cache, cache_size = (int(param) for param in lines[0].strip().split(' '))
        video_sizes = [int(size) for size in lines[1].strip().split(' ')]
        idx = 2
        endpoints = []
        for i in range(n_endpoint):
            datacenter_latency, cache_count = (int(p) for p in lines[idx].strip().split(' '))
            caches = []
            for j in range(cache_count):
                idx += 1
                caches.append((int(x) for x in lines[idx].strip().split(' ')))
            endpoints.append(Endpoint(i, datacenter_latency, caches))
            idx += 1

        REQ_array = [[0 for _ in range(n_endpoint)] for _ in range(n_video)]
        for i in range(idx, len(lines)):
            req_line = [int(x) for x in lines[i].strip().split(' ')]
            if video_sizes[req_line[4]] <= cache_size:
                REQ_array[req_line[4]][req_line[8]] = req_line[0]
        REQ_matrix = np.array(REQ_array)

        VLAT_array = []
        for i in range(n_endpoint):
            VLAT_array.append([endpoints[i].base_latency for _ in range(n_video)])
        VLAT_matrix = np.array(VLAT_array).T

        CLAT_array = [[0 for _ in range(n_endpoint)] for _ in range(n_cache)]
        for i in range(n_endpoint):
            for key in endpoints[i].cache_list:
                CLAT_array[i][key] = endpoints[i].cache_list[key]
        CLAT_matrix = np.array(CLAT_array).T

        video_stats = []
        for i in range(n_video):
            video_stats.append([video_sizes[i], sum(REQ_array[i])])

        return REQ_matrix, VLAT_matrix, CLAT_matrix, video_stats, n_cache, cache_size

    def init(g, P, vstats, n_cache, cache_size):
        return g.get_generation(P, [])

    def eval(GEN):
        pass

    def select(GEN, scores, n_select):
        sorted_gen = [z[0] for z in sorted(zip(GEN, scores), key=lambda pair: pair[1])]
        best_score = sorted(scores)
        return sorted_gen[:n_select], best_score


    def breed(selection):
        return g.get_generation(P, selection)

    REQ_mx, VLAT_mx, CLAT_mx, vstats, n_cache, cache_size = setup(filename)

    g = Generator(vstats, n_cache, cache_size)
    GEN = init(g, P, vstats, n_cache, cache_size)

    for i in range(150):
        score_list = eval(GEN)

        selection, best_score = select(GEN, score_list, S)

        if i <= 148:
            print("Gen #{0} - {1}".format(i, best_score))
            GEN = breed(g, P, selection)
        else: print(best_score)

if __name__ == "__main__":
    main()
