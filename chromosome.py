# -*- coding: utf-8 -*-
"""
    chromosome class
"""

import numpy as np

class chromosome(object):
    
    """ chromosome object """
    def __init__(self, size):
        
        self.size = size
        self.chrom = np.random.permutation(size)
        self.board = self.chromToBoard()
        self.fitness = self.Fitness()
        
    """ mutation by interchange """
    def mutate(self):
        
        indx_1 = np.random.randint(0,self.size)
        indx_2 = np.random.randint(0,self.size)
        while indx_2 == indx_1:
            indx_2 = np.random.randint(0,self.size)
        a = self.chrom[indx_1]
        self.chrom[indx_1] = self.chrom[indx_2]
        self.chrom[indx_2] = a
        self.fitness = self.Fitness()           # update the chromosome's fitness
        self.board = self.chromToBoard()        # update the chromosome's board
    
    """
        compute the chromosome's aptitude by 
        finding how many queens are in conflict
    """
    def Fitness(self):
        visited = []
        hor_attacks = 0
        diag_attacks = 0
        c = self.chrom
        # search for attacks horizontally
        for i in range(len(c)):
            x1 = c[i]      # row of the queen
            y1 = i         # col of the queen
            for j in range(len(c)):
                x2 = c[j]
                y2 = j
                if (x1,y1) == (x2,y2):
                    continue
                if (x1,y1) in visited:
                    continue
                if x1 == x2:
                    visited.append((x1,y1))
                    hor_attacks += 1
    
        # search for attacks diagonally     
        visited = []       
        for i in range(len(c)):
            x1 = c[i]
            y1 = i
            for j in range(len(c)):
                x2 = c[j]
                y2 = j
                if (x1,y1) == (x2,y2):                      # if same queen, skip
                    continue
                if (x1,y1) in visited:                      # if already visited, skip
                    continue
                if abs(y2-y1) == abs(x2-x1):                # if same diagonal
                    visited.append((x1,y1))
                    diag_attacks +=1
                    
        return 1/(1+hor_attacks + diag_attacks)
        
    """
        the chromosome is turned into a matrix 
        representation (game board)
    """
    def chromToBoard(self):
        board = np.zeros((self.size,self.size), int)
        for i in range(self.size):
            board[self.chrom[i]][i] = 1
        return board