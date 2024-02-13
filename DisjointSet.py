import numpy as np

class DisjointSet:
    def __init__(self, size):
        self.vertex = [i for i in range(size)]
        self.rank = [1] * size
        self.weight = [1] * size

    #check if v1 is a valid index
    def validate(self,v1) -> bool: 
        return 0 <= v1 < len(self.vertex)

    #return size of set of v1, using find based on rank
    def size(self, v1): 
        if not self.validate(v1):
            return 0
        root = self.findRank(v1)
        return self.rank[root]
    
    #returns v1's parent
    def parent(self, v1): 
        if not self.validate(v1):
            return -1
        return self.vertex[v1]
   
    #check if v1 and v2 are in the same set
    def isConnected(self, v1, v2) -> bool:
        return self.findWeight(v1) == self.findWeight(v2)
    
    #when using weighted quick union   
    def findWeight(self, v1):
        if not self.validate(v1):
            return -1
        while v1 != self.vertex[v1]:
            v1 = self.vertex[v1]
        return v1
    
    #find root when using union by rank, uses path compression
    #updates subtree's root for faster future access time 
    def findRank(self, v1):
        if not self.validate(v1):
            return -1
        if v1 != self.vertex[v1]:
            self.vertex[v1] = self.findRank(self.vertex[v1])
        return self.vertex[v1]
    
    def unionByWeight(self, v1, v2):
        root1 = self.findWeight(v1)
        root2 = self.findWeight(v2)
        root1_weight = self.size(v1)
        root2_weight = self.size(v2)

        if root1 == root2:
            return
            
        #does not preserve parent-child relationship
        if root1_weight < root2_weight:
            self.vertex[root1] = root2
            self.weight[root2] += root1_weight
        else: #root1_weight > root2_weight or they are equal
            self.vertex[root2] = root1
            self.weight[root1] += root2_weight
    
    def unionByRank(self, v1, v2):
        root1 = self.findRank(v1)
        root2 = self.findRank(v2)

        if root1 == root2:
            return

        if self.rank[root1] < self.rank[root2]:
            self.vertex[root1] = root2
        elif self.rank[root1] > self.rank[root2]:
            self.vertex[root2] = root1
        else:
            self.vertex[root2] = root1
            self.rank[root1] += 1


    #Given the DisjointSet data structure you have, and Connected matrix showing the connectivity among blocks, write a method to construct a DisjointSet at one time.

    def joinBlocks(self, Connected):
        if not Connected:
            return
        
        '''
        i = n -> blocks
        j = n -> rows
        '''
        n = len(Connected)

        for i in range(n):
            for j in range(n):
                if i != j and Connected[i][j] == 1:
                    self.unionByWeight(i, j)

    #Return number of connected block sets avaialble in the grid.
    def findBlocks(self):
        root = [] #unique roots
        n = len(self.vertex)
        
        for i in range(n):
            temp = self.findWeight(i)
            if temp not in root: #only append unique roots that are found for each item
                root.append(temp)

        return len(root)

    #Return number of bolcks in block set where the inquiry blockid belongs to. if the blockid is not connected to any, then return 1.
    def findBlockCount(self, blockid):
        if not self.validate(blockid):
            return -1

        root = self.findWeight(blockid)
        connected = 0

        #check if the root of given block is the same as others
        for i in range(len(self.vertex)):
            if self.findWeight(i) == root:
                connected += 1

        return connected
        


if __name__ == '__main__':
    # Tasks A
    uf = DisjointSet(10)
    # 0 1-2-5-6-7 3-8-9 4
    uf.unionByRank(1, 2)
    uf.unionByRank(2, 5)
    uf.unionByRank(5, 6)
    uf.unionByWeight(6, 7)
    uf.unionByRank(3, 8)
    uf.unionByWeight(8, 9)
    print(uf.isConnected(1, 5))  # true
    print(uf.isConnected(5, 7))  # true
    print(uf.isConnected(4, 9))  # false
    # 0 1-2-5-6-7 3-8-9-4
    uf.unionByWeight(9, 4)
    print(uf.isConnected(4, 9))  # true

    # Tasks B
    Connected = [[1,1,0,1], [1,1,0,0], [0,0,1,1], [1,0,1,1]]
    uf = DisjointSet(4)
    uf.joinBlocks(Connected)
    uf.findBlockCount(1)
