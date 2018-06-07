# -*- coding: utf-8 -*-
"""
    n-queen problem using genetic algorithm
"""

import numpy as np
import math
import time

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

def writeFile(f,p,header):
    f.write(header)
    for indv in p:
        f.write('\nChromosome => ' + str(indv.chrom))
        f.write('\nFitness => ' + str(indv.fitness))
        f.write('\nBoard => \n') 
        f.write(str(board(indv.chrom)))
        f.write('\n\n')
    f.write('\n\n')
            
def solve(n,gmax,pc,pm,size):
    
    solution = []                   # solution list
    g = 0                           # generation's number
    p = []                          # population list
    f = open('solution.txt','w')    # file to write the populations
    ng = n//2                       # half of population's size
    start_time = time.time()        # Start time of the program
    
    p = genPopulation(n, size)      # generate the population
    p = computeFitness(p)           # compute their fitness
    
    writeFile(f,p,'Initial population:\n')
    
    while True:
        
        if g == gmax:
            break
        
        if len(solution) > 0:
            break
    
        g += 1
        
        p = selection(p,ng,'rws')
        writeFile(f,p,'Generation ' + str(g) + '\n' + 'Selected population\n')
        
        if np.random.rand() <= pc:
            p = crossover(p)
            writeFile(f,p,'Generation ' + str(g) + '\n' + 'Crossed population\n')
            
        if np.random.rand() <= pm:
            p = mutation(p)
            writeFile(f,p,'Generation ' + str(g) + '\n' + 'Mutated population\n')
        
        for indv in p:
            if indv.fitness == 1.0:
                end_time = time.time()             # end time of the solution
                solution.append(indv)
                print('\nThe solution was found!')
                print('...at generation => ', g)
                print('...in ' + str(end_time-start_time) + ' seconds')
                break
            break
    
    f.close()
    
    return solution
    
def main():
    n = 10            # number of initial population
    gmax = 100000       # maximum number of generations
    pc = 0.7            # crossover probability
    pm = 0.3            # mutation probability
    size = 6            # board size
    
    solution = solve(n,gmax,pc,pm,size)
        
    while len(solution) == 0:
        solution = solve(n,gmax,pc,pm,size)
    print('\nChromosome: ', solution[0].chrom)
    print('Fitness: ', solution[0].fitness)
    print('Board: \n')
    print(board(solution[0].chrom))    
        
        
if __name__ == "__main__":
    main()
    
'''

    solutions for the 6-queens problem (4 in total):
        
        1.- [1,3,5,0,2,4]
        2.- [4,2,0,5,3,1]
        3.- [2,5,1,4,0,3]
        4.- [3,0,4,1,5,2]
        
    some solutions for the 7-queens problem (40 in total):
        
        1.- [4,6,1,3,5,0,2]
        2.- [5,0,2,4,6,1,3]
        3.- [5,2,6,3,0,4,1]
        4.- [1,3,5,0,2,4,6]
        
    some solutions for the 8-queens problem (92 in total):
        
        1.- [2,5,1,4,7,0,6,3]
        2.- [1,5,7,2,0,3,6,4]
        3.- [4,6,1,3,7,0,2,5]
        4.- [3,7,0,2,5,1,6,4]
        5.- [4,1,5,0,6,3,7,2]
        6.- [4,6,1,5,2,0,7,3]
        7.- [3,6,4,1,5,0,2,7]
        8.- [4,2,7,3,6,0,5,1]
        
    some solutions for the 9-queens problem (352 in total):
        
        1.- [4,0,7,3,1,6,8,5,2]
        2.- [3,1,8,2,5,7,0,4,6]
        3.- [4,6,3,0,2,7,5,1,8]
        
    one solution for the 15-queen problem ():
        
        1.- [6,3,9,14,1,8,10,12,4,0,5,11,2,7,13]
        2.- [9,11,1,5,10,0,7,14,12,2,6,8,3,13,4]
    
'''
