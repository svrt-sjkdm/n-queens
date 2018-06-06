# -*- coding: utf-8 -*-
"""
    n-queen problem using genetic algorithm
"""

import numpy as np
import math

class chromosome(object):
    
    def __init__(self, chrom):
        self.chrom = chrom
        self.size = len(chrom)
        self.fitness = -1
        self.ps = -1

def cross(c1,c2):
    # index of the position to cross
    indx = np.random.randint(1,len(c1))
    ch1 = list(c1)
    ch2 = list(c2)
    ch1[indx:] = c2[indx:]
    ch2[indx:] = c1[indx:]
    
    return [ch1,ch2]
    

def crossover(p):
    crossed = []
    n = math.ceil(len(p)/2)
    parentsA = p[0:n]
    parentsB = p[n:]
    for parentA,parentB in zip(parentsA,parentsB):
        ch1,ch2 = cross(parentA.chrom,parentB.chrom)
        crossed.append(chromosome(ch1))
        crossed.append(chromosome(ch2))
    crossed = computeFitness(crossed)
    return crossed

def mutate(c):
    mutated = c[:]
    indx = np.random.randint(len(c))
    num = np.random.randint(len(c))
    while num == c[indx]:
        num = np.random.randint(len(c))
    mutated[indx] = num
    
    return mutated

def mutation(p):
    mutateds = []
    for indv in p:
        mutateds.append(chromosome(mutate(indv.chrom)))
    mutateds = computeFitness(mutateds)
    return mutateds

def selection(p,n,method):
    survivors = []
    if method == 'rws':
        # compute the total fitness of the population
        p = computeFitness(p)
        F = sum([p[i].fitness for i in range(len(p))])
        # normalize the fitness of each individual
        for k in range(len(p)):
            p[k].ps = p[k].fitness/F
        # sort the population by fitness (from highest to lowest)
        p = sorted(p, key=lambda x: x.fitness, reverse=True)
            
        for k in range(n):
            x = np.random.rand()
            tsum = 0
            for i in range(len(p)):
                tsum += p[i].ps
                if x < tsum:
                    survivors.append(p[i])
                    break
    if method == 'rank':
        p = computeFitness(p)
        p = sorted(p, key=lambda x: x.fitness, reverse=True)
        survivors = p[:n]
        
    return survivors

def fitness(c):
    visited = []
    hattacks = 0
    dattacks = 0
        
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
                hattacks += 1
    
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
                dattacks +=1
                    
    return 1/(1+hattacks+dattacks)      

def genPopulation(n, size):
    p = []
    for i in range(n):
        chrom = np.random.permutation(size)
        indv = chromosome(chrom)
        p.append(indv)
    return p

def computeFitness(p):
    for indv in p:
        indv.fitness = fitness(indv.chrom)
    return p

def board(c):
    board = np.zeros((len(c),len(c)), int)
    for i in range(len(c)):
        board[c[i]][i] = 1
    return board
    
    
def _main(): 
    
    n = 4
    gmax = 100000
    pc = 0.7
    pm = 0.3
    
    g = 0
    p = []
    
    
    p = genPopulation(n, 6)
    p = computeFitness(p)
    
    print('poblacion')
    print()
    for indv in p:
        print('cromosoma ==> ', indv.chrom)
        print('fitness ==> ,', indv.fitness)
        print(board(indv.chrom))
    print('------------------------------------')
    
    p = selection(p,len(p)//2,'rws')
    
    print('poblacion seleccionada')
    print()
    for indv in p:
        print('cromosoma ==> ', indv.chrom)
        print('fitness ==> ,', indv.fitness)
        print(board(indv.chrom))
    print('------------------------------------')
    
    p = crossover(p)
    
    print('poblacion cruzada')
    print()
    for indv in p:
        print('cromosoma ==> ', indv.chrom)
        print('fitness ==> ,', indv.fitness)
        print(board(indv.chrom))
    print('------------------------------------')
    
    p = mutation(p)
        
    print('poblacion mutada')
    print()
    for indv in p:
        print('cromosoma ==> ', indv.chrom)
        print('fitness ==> ,', indv.fitness)
        print(board(indv.chrom))
    print('------------------------------------')
    
    for indv in p:
        if indv.fitness == 1.0:
            print('solution found!')
            print(indv.chrom)
            
def solve(n,gmax,pc,pm,size):
    
    solution = []
    g = 0
    ncross = 0
    nmuts = 0
    p = []
    
    p = genPopulation(n, size)
    p = computeFitness(p)
    
    while g < gmax:
        
        g += 1
        
        p = selection(p,len(p)//2,'rws')
        
        if np.random.rand() <= pc:
            p = crossover(p)
            ncross += 1
            
        if np.random.rand() <= pm:
            p = mutation(p)
            nmuts += 1
        
        for indv in p:
            if indv.fitness == 1.0:
                solution.append(indv)
                break
            break
    
    return solution
    
def main():
    n = 1000            # number of initial population
    gmax = 100000       # maximum number of generations
    pc = 0.7            # crossover probability
    pm = 0.3            # mutation probability
    
    solution = solve(n,gmax,pc,pm,8)
    
    if len(solution) == 0:
        print('No solution was found')
    else:
        print('The solution was found!\n')
        print('Chromosome: ', solution[0].chrom)
        print('Fitness: ', solution[0].fitness)
        print('Board: \n')
        print(board(solution[0].chrom))
    
'''

    solutions for the 6-queen problem:
        
        1.- [1,3,5,0,2,4]
        2.- [4,2,0,5,3,1]
        3.- [2,5,1,4,0,3]
        4.- [3,0,4,1,5,2]
        
'''

if __name__ == "__main__":
    main()