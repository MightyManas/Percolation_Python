import matplotlib.pyplot as plt
import numpy as np

sheet_dict = {}

class cluster ():
    labels = np.array([])

    def __init__(self, i, j):
        self.i = i
        self.j = j  
        self.label = f"A{i}{j}" 
        self.left_change = self.leftmarker()
        self.topmarker(self.left_change)
        np.append(cluster.labels, self.label)

    def topmarker(self,left_change):
        top = sheet_dict[(self.i-1, self.j)]
        left = sheet_dict[(self.i, self.j-1)]
        if top.label in cluster.labels :
             self.label = top.label
             if left_change:
                 left.label = self.label

    def leftmarker(self):
        left = sheet_dict[(self.i, self.j-1)]
        if left.label in cluster.labels :
             self.label = left.label
             return True



k = 10
p = 0.8
sheet = np.ones(k**2)
index = int(k**2*p)
sheet[:index] = 0
np.random.shuffle(sheet)
sheet = sheet.reshape(k,k)
apple = cluster(1,1)
print(sheet)

i, j = 0, 0
while i < k:
    while j < k:
        if sheet[i][j] == 1:
                sheet_dict[(i,j)] = cluster(i,j)
                
        j += 1
    i += 1

print(cluster.labels)