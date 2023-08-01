from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# dic_list = {2:{1:90,2:30},3:{1:91,4:30},37:{1:90,9:0}}

def recommend(dic_list, id):
    results = []
    keys = [i for i in dic_list.keys()]

    i = id
    b = dic_list.get(i)
    for j in keys:
        if i == j:
            continue
        similar = [[], []]
        c = dic_list.get(j)
        for data in b.keys():
            if data in c.keys():
                similar[0].append(b.get(data))
                similar[1].append(c.get(data))

        a = cosine_similarity(similar)
        if a[0][1] >= 0.95:
            for data in c.keys():
                if data not in b.keys():
                    if data not in results:
                        results.append(data)

    if len(results)<10:
        count = 10
        probr = [i for i in b.values()]
        probr.sort(reverse=True)
        for i in probr:
            if count==0:
                    break
            for j in b.keys():
                if b[j] == i:
                    if j not in results:
                        results.append(j)
                        count -= 1
                if count==0:
                    break

    return results


# print(recommend(dic_list,2))
