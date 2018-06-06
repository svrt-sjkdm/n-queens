# -*- coding: utf-8 -*-
"""
    queens class
"""

import chromosome
import numpy as np

class queens(object):
    
    def __init__(self):
        pass
    
    def crossover(self,population):
        
        crossed = []
        threshold = len(population)//2
        parentsA = population[:threshold]
        parentsB = population[threshold:]
        
        for k in range(threshold):
            cchild1 = parentsA[k][0].chrom[:]              # copy the childs
            cchild2 = parentsB[k][0].chrom[:]
            indx = np.random.randint(len(parentsA)) 
            cchild1[indx:] = parentsA[k][0].chrom[indx:]   # merge them in the selected index
            cchild2[indx:] = parentsB[k][0].chrom[indx:]
            
            child1 = chromosome.chromosome(population[0][0].size)
            child2 = chromosome.chromosome(population[0][0].size)
            
            child1.chrom = cchild1
            child2.chrom = cchild2
            
            crossed.append([child1,child1.Fitness()])                         # append the 2 childs into the crossed list
            crossed.append([child2,child2.Fitness()])
            
        return crossed
    
    """
        mutate every member of the population
    """
    def mutation(self,population):
        
        mutated = []
        for indv in population:
            indv[0].mutate()
            mutated.append([indv[0], indv[0].fitness])
        
        return mutated
        
    """
        selection using stochastic universal sampling
    """
    def selection2(self,population,n):
        
        survivors = []
        # compute the total fitness of the population to normalize
        F = sum([population[i][1] for i in range(len(population))])
        # number of childs to keep
        N = n
        # distance between the rulete's pointers
        P = F/N
        
        start = np.random.rand(0,int(P))
        pointers = [start+i*P for i in range(N+1)]
        fsum = 0 # sum of the fitness
        
        for point in pointers:
            i = 0
            while fsum < point:
                fsum += population[i][1]
                i += 1    
            survivors.append(population[i])
            
        return survivors

    """
        roulette wheel selection
    """
    def rwselection(self,population,n):
        p = population[:]
        survivors = []
        # compute the total fitness of the population to normalize
        F = sum([p[i][1] for i in range(len(p))])
        # normalize the fitness of each individual
        for k in range(len(p)):
            p[k][0].fitness /= F
            p[k][1] = p[k][0].fitness
        # sort the population by fitness (from highest to lowest)
        #population = sorted(population, key=lambda x: x[1], reverse=True)
        # generate a random number [0,1]
        x = np.random.rand()
        
        summ = 0
        # 
        for k in range(n):
            for indv in p:
                summ += indv[0].fitness
                if x < summ:
                    survivors.append(indv)
                    break

        return survivors        
    
    """
        solve the n-queen problem by using
        the given parameters
    """    
    def solve(self,size,n,gmax,pc,pm):
        
        solution = []
        population = []     
        g = 0             # current generation
        mutations = 0
        crossings = 0
        
        # generate the initial population
        for k in range(n):
            individual = chromosome.chromosome(size)
            population.append([individual,individual.Fitness()])
        
        # verify if the solution exists in the current population
        ########
        
        while True:
            
            # stop when the population's size is the same as the limit
            if g == gmax:
                break
            
            # increment the number of the generations
            g += 1
            
            # selecting the individuals
            population = self.rwselection(population, n//2) 
            
            # cross the survivors
            if np.random.rand() <= pc:
                population = self.crossover(population)
                crossings += 1
            
            # mutate the survivors
            if np.random.rand() <= pm:
                population = self.mutation(population)
                mutations += 1
            
            # verify if there is an individual wich is the solution
            
            for indv in population:
                if indv[0].fitness == 1.0:
                    solution.append(indv[0])
            
        return solution