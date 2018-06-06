# -*- coding: utf-8 -*-
"""
    6 queens problem     
    using genetic algorithms
"""

import queens


def main():
    n = 20                   # poblacion inicial
    g = 100000                # generaciones maximas
    pc = 0.7                 # probabilidad de cruza
    pm = 0.3                 # probabilidad de mutacion
    
    q = queens.queens()
    s = q.solve(6,n,g,pc,pm)
    
    if len(s) == 0:
        print('No solution was found...')
    else:
        print('The solution is:')
        print(s[0].chrom)
        print()
        s[0].chromToBoard()
        print(s[0].board)

if __name__ == "__main__":
    main()

# [1,3,5,0,2,4]
# [4,2,0,5,3,1]
# [2,5,1,4,0,3]

