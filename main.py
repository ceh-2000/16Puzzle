#16 Puzzle

#Name: Clare Heinbaugh
#Date: 10/2/2017

import random
import heapq
import sys
from timeit import default_timer
import cProfile

#Heap functions

#heapq.heapreplace(heap, item) <-- this is faster than popping then pushing
#heapq.heappushpop(heap, item) <-- push then pop faster
#heappush(heap, item)
#heappop(heap)

#Heuristic information:

#admissible: not overestimated for ANY node
#consistent: value for a node is never greater than heuristic value of neighbors
#Manhattan distance: takes into account what's out of order AND how far
#Hamming distance: takes only what's out of order into account

all_configs = """1,1 2 3 4 5 6 7 8 9 10 11 0 13 14 15 12
2,1 2 3 4 5 6 7 0 9 10 11 8 13 14 15 12
3,1 2 3 4 5 6 0 8 9 10 7 12 13 14 11 15
4,1 2 3 4 5 0 7 8 9 6 11 12 13 10 14 15
5,1 2 3 4 5 6 7 8 10 0 11 12 9 13 14 15
6,1 6 2 4 5 0 3 8 9 10 7 11 13 14 15 12
7,1 2 3 4 6 10 7 8 5 0 11 12 9 13 14 15
8,1 2 3 4 5 10 6 8 13 9 7 12 14 0 11 15
9,2 3 4 0 1 6 7 8 5 10 11 12 9 13 14 15
10,1 2 4 12 5 6 3 0 9 10 8 7 13 14 11 15
11,5 1 3 4 9 2 7 8 13 0 10 12 14 6 11 15
12,5 1 2 4 9 6 3 7 13 10 0 8 14 15 11 12
13,5 3 4 8 2 1 0 7 9 6 10 11 13 14 15 12
14,1 2 8 3 5 11 6 4 0 10 7 12 9 13 14 15
15,5 1 3 4 13 2 7 8 6 10 11 12 14 9 0 15
16,5 1 2 4 6 0 10 7 13 11 3 8 14 9 15 12
17,5 2 4 0 6 1 3 8 13 11 7 12 10 9 14 15
18,2 5 3 4 1 7 11 8 9 6 0 12 13 14 15 10
19,3 7 2 4 1 5 10 8 6 0 11 12 9 13 14 15
20,6 3 7 4 2 9 10 8 1 5 12 15 13 0 14 11
21,3 7 1 0 6 2 8 4 5 10 11 12 9 13 14 15
22,1 4 8 3 7 2 10 11 5 6 0 15 9 13 14 12
23,1 2 3 4 5 6 14 8 13 0 9 11 10 12 15 7
24,9 5 1 2 6 4 8 3 10 14 7 11 13 0 15 12
25,2 5 1 3 9 6 12 4 10 14 8 0 13 11 15 7
26,1 10 6 4 5 9 2 8 13 12 0 7 14 11 3 15
27,1 2 3 0 5 12 7 4 13 6 14 9 10 8 11 15
28,2 5 4 7 9 1 3 8 11 10 0 6 14 13 15 12
29,1 8 3 0 5 7 4 12 14 6 2 15 9 13 10 11
30,2 4 8 12 1 7 3 14 0 6 15 11 5 9 13 10
31,5 1 3 2 10 6 15 7 9 8 11 4 0 13 14 12
32,6 2 3 8 5 0 7 11 1 10 4 12 13 14 9 15
33,6 7 4 11 3 2 8 12 1 5 13 15 0 9 10 14
34,9 5 8 3 6 0 10 11 2 1 14 7 13 15 12 4
35,9 1 5 7 0 13 2 4 14 6 12 3 10 15 8 11
36,3 14 2 4 9 1 7 8 0 12 6 10 13 5 11 15
37,5 9 1 3 0 11 2 7 10 13 12 4 6 15 8 14
38,2 6 4 8 1 10 7 3 5 13 11 15 12 14 9 0
39,3 4 6 8 1 2 12 11 15 14 7 0 5 10 9 13
40,5 6 3 4 8 0 1 15 10 7 2 11 12 9 14 13
41,5 15 3 4 2 10 6 12 9 8 7 13 11 1 0 14
42,0 9 1 10 3 5 4 2 14 6 11 7 12 13 8 15
43,7 11 6 3 1 5 2 15 12 14 8 0 13 10 9 4
44,14 5 11 6 9 0 4 3 15 1 7 12 8 2 13 10
46,13 11 9 3 14 7 1 4 0 5 10 12 15 2 6 8
47,2 4 1 6 12 13 5 3 14 7 11 15 0 9 8 10
48,7 8 1 10 2 4 5 13 0 9 3 6 11 14 15 12
49,2 10 15 4 14 11 0 6 9 13 8 3 5 7 12 1
50,2 3 0 8 15 12 6 7 13 1 4 9 14 11 10 5"""




global puzzle_size
puzzle_size = 16
global overall
overall = 4
global goal_state
goal_state = "123456789ABCDEF0"




global raw_config
raw_config = {0: [1, 4],
              1: [0, 2, 5],
              2: [1, 3, 6],
              3: [2, 7],
              4: [0, 5, 8],
              5: [1, 4, 6, 9],
              6: [2, 5, 7, 10],
              7: [3, 6, 11],
              8: [4, 9, 12],
              9: [5, 8, 10, 13],
              10: [6, 9, 11, 14],
              11: [7, 10, 15],
              12: [8, 13],
              13: [9, 12, 14],
              14: [10, 13, 15],
              15: [11, 14]
              }


global table_of_h
table_of_h = {}

class Config_Node:
    def __init__(self, state, parent, depth, neighs, hval):
        self.state = state
        self.parent = parent
        self.depth = depth
        self.neighs = neighs
        self.fval = depth + hval
        self.hval = hval 
    def getDepth(self):
        return self.depth
    def iterateDepth(self):
        self.depth+=1
    def setNeighs(self):
        li_config = self.state
        sam = li_config.index("0")  # 0 represents a space in the puzzle
        self.neighs = raw_config[sam]

def gen_heur_hamming(s_config):

    #Hamming distance
    l_config = list(s_config)
    cur_num = 1
    count = 0
    for c in l_config:
        if(int(c) != cur_num):
            count+=1
        cur_num+=1

    return count

def get_row(config, val):
    pos = config.index(val)
    row = int(pos/4)
    return row

def get_col(config, val):
    pos = config.index(val)
    col = pos%4
    return col

#def gen_table_of_h():
#    for x in list(goal_state):
#        if(x!="0"):
            


def gen_heur(config):
    heur_num = 0
    for x in list(goal_state):
        if(x!="0"):
            r = get_row(config, x)
            c = get_col(config, x)
            gr = get_row(goal_state, x)
            gc = get_col(goal_state, x)
            row_dif = abs(r-gr)
            col_dif = abs(c-gc)
            heur_num += (row_dif + col_dif) 
    return heur_num
    

def make_init():
    s="123456789ABCDEF0" #"0" gets switched
    return ''.join(random.sample(s,len(s)))


def construct_path(goal_state, config):
    cur = goal_state
    lm = []
    while cur.state != config.state:
        lm.append(cur.state)
        cur = cur.parent
    lm.append(cur.state)
    
    print(lm[::-1])
    print("Steps: ", (len(lm)-1))


def switch_it(config, ch1, ch2):
    config = config.replace(ch2, '!')
    config = config.replace(ch1, ch2)
    config = config.replace('!', ch1)
    return config

def find_actual_neighs(config): #parameter is Config_Node object

    str_config = config.state
    neigh_indices = config.neighs
    ind_of_0 = str_config.index("0")
    li_neighs = [] #store as Config_Node object
    for c in neigh_indices:
        neigh_state = switch_it(str_config, "0", str_config[c])
        li_neighs.append(Config_Node(neigh_state, config, config.depth+1, set_neighs(neigh_state), 0)) #since it takes a while to generate heuristic, wait to generate until later

    return li_neighs

def set_neighs(str_config):
    ind_of_0 = str_config.index("0")
    neighs = raw_config[ind_of_0] #list of indices where 0 can move to in string
    return neighs

#get around issue of having unique tuple values
class PriorityEntry:

    def __init__(self, priority, data):
        self.data = data
        self.priority = priority

    def __lt__(self, other):
    
        if(self.priority == other.priority):
            if(self.data.depth > other.data.depth):
                return True
            else: 
              return False
        else:
            return self.priority < other.priority


def make_nice(s):
    sam = ""
    s = s.replace("0", "_")
    for x in list(s):
        if(s.index(x)==0):
            sam=x+" "
        elif(s.index(x)%overall==0):
            sam=sam + "\n" + x + " "
        else:
            sam+=x+" "
    sam += "\n------"
    return sam

def make_puz(f):
    s = all_puz_configs[f]
    li = s.split()
    new_s = ""
    for c in li:
        if(c=="10"):
            new_s+="A"
        elif(c=="11"):
            new_s+="B"
        elif(c=="12"):
            new_s+="C"
        elif(c=="13"):
            new_s+="D"
        elif(c=="14"):
            new_s+="E"
        elif(c=="15"):
            new_s+="F"
        else:
            new_s+=c
    return new_s
    
global all_puz_configs
all_puz_configs = {}

def make_all():
    #file = open(“puzzles.txt”, “r”) 
    lines = all_configs.split("\n")
    for c in lines:
      n = c.split(",")
      #print(n)
      steps = int(n[0])
      config = n[1]
      all_puz_configs[steps] = config 
      #print(config)

def main():

    make_all()
    #print(all_puz_configs)

    #user_steps = input("Enter the number of steps for a puzzle (1-50): ")
    #s_config = make_puz(user_steps)

    num_count = 1
    for do_it_now in range(len(all_puz_configs.keys())):
        s_config = make_puz(num_count) #make_init()
        start_time = default_timer()

        neighs = set_neighs(s_config)
        start = Config_Node(s_config, None, 0, neighs, gen_heur(s_config))
        openSet = [PriorityEntry(0, start)]
        heapq.heapify(openSet)
        closedSet = {}
        count_it = 0

        solved = False
        
        while(len(openSet)>0 and solved==False):
            current = heapq.heappop(openSet).data #Config_Node object
            if(current.state == goal_state):
    
                construct_path(current, start) #current is the goal state
                end_time = default_timer()
                elapsed_time = end_time - start_time
                print(num_count) 
                print("Time: ", elapsed_time)
                solved = True
            if(solved == False):                          
                closedSet[current.state] = current
                neighs = find_actual_neighs(current) #list of neighbor configurations
                for c in neighs:
                    if c.state in closedSet.keys():
                      llama = 0
                    else:
                        c.hval = gen_heur(c.state)
                        c.fval = c.hval + c.depth
                        if(c not in openSet):
                          heapq.heappush(openSet, PriorityEntry(c.fval, c)) #pushes Config_Node object onto heap
            count_it+=1
        #print("This puzzle is unsolveable.")
        num_count+=1
    
    
        
                
                
#if __name__ == "__main__":
    #cProfile.run('main()')
main()

