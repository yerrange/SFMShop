_dict = {1: 1000, 3:500, 2: 250, 4: 80000, 5: 1}


print(sorted(_dict.items(), key=lambda x: x[1]))