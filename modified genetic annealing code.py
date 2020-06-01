import numpy as np
import matplotlib.pyplot as plt
import random
import time

# at first to make this code simple and can be understood, we will consider the blocks pins at the half
# also the blocks of different sizes from 1 and 3 only for simplicity and also with different orientations which is vertical and horizontal
#please take care, if you want to work with different sizes, pick a suitable grid size to afford them

#you can also make all of the blocks equal in length by setting the differ in initialize by false

# we will start our initializations for the code with the following
INF = 100000
alpha = 0.99
threshold = 0.01

#for small inputs in order not to printing error messages
# INF = 10
# alpha = 0.9
# threshold = 0.01


#take care L (number of populations) must be even number as this algo takes 2 blocks with each other from population and do mutation

# initialization by random choosing different blocks with different sizes and different orientation and put them inside the grid
def initialize(k, N, grid,differ=True):
    if differ==False:
        return initialize2(k,N,grid)

    orientation_arr = {}
    for element in range(1, k + 1):
        # element number
        assigned = False
        while (not assigned):
            i = np.random.randint(2, N - 3)
            j = np.random.randint(2, N - 3)
            orientation = np.random.randint(2)  # 0 is vertical, 1 is horizontal
            length = random.randrange(1, 4, 2)  # length of block either 1 or 3 (odd to get center is real grid)
            # length=1
            # all of these checkings to ensure that there's at least 1 space between each 2 blocks
            if (grid[i, j] == 0 and grid[i + 1, j] == 0 and grid[i - 1, j] == 0 and grid[
                i, j + 1] == 0 and grid[i, j - 1] == 0):
                if (length == 1):
                    grid[i, j] = element
                    assigned = True
                    orientation_arr[element] = orientation
                else:
                    if (orientation==0 and i + 2 < N):
                        grid[i, j] = element
                        grid[i - 1, j] = element
                        grid[i + 1, j] = element
                        assigned = True
                        orientation_arr[element] = orientation
                    elif(orientation==1 and j+2<N):
                        grid[i, j] = element
                        grid[i , j-1] = element
                        grid[i , j+1] = element
                        assigned = True
                        orientation_arr[element] = orientation
    return grid, orientation_arr


def initialize2(k, N, grid):

    orientation_arr={}
    for element in range(1,k+1):
        assigned = False
        while(not assigned):
            i = np.random.randint(N)
            j = np.random.randint(N)
            if(grid[i,j]==0):
                grid[i,j] = element
                orientation_arr[element]=np.random.randint(2);
                assigned = True
    return grid,orientation_arr



# plotting the grid to see the shape of each block
def printgrid(grid):
    plt.imshow(grid, interpolation='None', aspect="auto")
    for (j, i), label in np.ndenumerate(grid):
        plt.text(i, j, label, ha='center', va='center')
    plt.show()

# choose the L population among the blocks then return it back
def make_population(L,k):
    pop=[]
    if(L>k):
        print("error pop > the number of blocks")
        exit()

    for i in range(L):
        temp = np.random.randint(1, k + 1)
        while(temp in pop):
            temp = np.random.randint(1, k + 1)
        pop.append(temp)
    return pop

# move random function will be executed when the propability in process is less than 0.5 or the 2 chosen blocks
# can't be mutated due to different sizes
# it will move you to a random place and also it can be chaing its orientation
def move_random(tempGrid, N, k, orientation_arr,element1):
    len_first_element = len(np.where(tempGrid == element1)[0])
    if (len_first_element == 1):
        (x1, y1) = list(zip(*np.where(tempGrid == element1)))[0]
        # find an empty place
        temp = list(zip(*np.where(tempGrid == 0)))
        (x2, y2) = temp[np.random.randint(len(temp))]
    else:
        a=None
        b = None
        c = None
        d = None
        e = None
        f = None
        try:
            ((a, b), (c, d), (e, f)) = zip(*np.where(tempGrid == element1))
        except:
            print("overlapped may be due to your bad inputs or the bad random first initialization, run again or choose your parameters correctly")
            exit()
        temp = list(zip(*np.where(tempGrid == 0)))
        for i, j in temp:
            if 2 <= i <= N - 3 and 2 <= j <= N - 3 and tempGrid[i, j] == 0:
                orientation = np.random.randint(2)
                if (orientation == 0):
                    if tempGrid[i, j] == 0 and tempGrid[i + 1, j] == 0 and tempGrid[i + 2, j] == 0:
                        tempGrid[i, j] = element1
                        tempGrid[i + 1, j] = element1
                        tempGrid[i + 2, j] = element1
                        tempGrid[a, b] = 0
                        tempGrid[c, d] = 0
                        tempGrid[e, f] = 0
                        orientation_arr[element1] = 0
                        break
                else:
                    if (tempGrid[i, j] == 0 and tempGrid[i, j + 1] == 0 and tempGrid[i, j + 2] == 0):
                        tempGrid[i, j] = element1
                        tempGrid[i, j + 1] = element1
                        tempGrid[i, j + 2] = element1
                        tempGrid[a, b] = 0
                        tempGrid[c, d] = 0
                        tempGrid[e, f] = 0
                        orientation_arr[element1] = 1
                        break
    return tempGrid, orientation_arr

# Suppose you are in any state say S, then you can go to
# some other state S'

def process(N, k, grid, orientation_arr,L):
    # each 50% of time
    # 1. swap positions of any two elements
    # 2. Move any element to a new position in the grid

    tempGrid = np.array(grid)
    # inorder if the 2 chosen are not the same length and if random is less < 0.5, enter the same (if) to do the same job
    if (np.random.random() < 0.5):


        # to ensure element2 != element1
        #make population
        pop=make_population(L,k)
        taken_members_dict = {}
        for i in pop:
            taken_members_dict[i]=0
        element1 = random.choice(pop)
        while(taken_members_dict[element1]==1):
            element1= random.choice(pop)
        element2 = random.choice(pop)
        while (element2 == element1 or taken_members_dict[element2]==1):
            element2  = random.choice(pop)

        taken_members_dict[element1]=1
        taken_members_dict[element2] = 1
        # after getting random 2 blocks from populations, make the MUTATION

        # get length of block
        len_first_element = len(np.where(tempGrid == element1)[0])
        len_second_element = len(np.where(tempGrid == element2)[0])

        # if they have the same length , then try to exchange them if they also have same orientation at (len = 3)
        if (len_first_element == len_second_element):
            if (len_first_element == 3):
                ((a, b), (c, d), (e, f)) = zip(*np.where(tempGrid == element1))
                ((g, h), (i, j), (k, l)) = zip(*np.where(tempGrid == element2))
                if (orientation_arr[element1] == orientation_arr[element2]):
                    tempGrid[a, b] = element2
                    tempGrid[c, d] = element2
                    tempGrid[e, f] = element2
                    tempGrid[g, h] = element1
                    tempGrid[i, j] = element1
                    tempGrid[k, l] = element1
                else:
                    if (orientation_arr[element1] == 0):
                        if (tempGrid[g + 1, h] == 0 and tempGrid[g + 2, h] == 0 and tempGrid[a, b + 1] == 0 and
                                tempGrid[a, b + 2] == 0):
                            tempGrid[g, h] = element1
                            tempGrid[g + 1, h] = element1
                            tempGrid[g + 2, h] = element1
                            tempGrid[i, j] = 0
                            tempGrid[k, l] = 0
                            tempGrid[a, b] = element2
                            tempGrid[a, b + 1] = element2
                            tempGrid[a, b + 2] = element2
                            tempGrid[c, d] = 0
                            tempGrid[e, f] = 0
                        elif (tempGrid[i + 1, j] == 0 and tempGrid[i + 2, j] == 0 and tempGrid[a, b + 1] == 0 and
                              tempGrid[a, b + 2] == 0):
                            tempGrid[i, j] = element1
                            tempGrid[i + 1, j] = element1
                            tempGrid[i + 2, j] = element1
                            tempGrid[g, h] = 0
                            tempGrid[k, l] = 0
                            tempGrid[a, b] = element2
                            tempGrid[a, b + 1] = element2
                            tempGrid[a, b + 2] = element2
                            tempGrid[c, d] = 0
                            tempGrid[e, f] = 0
                        elif (tempGrid[i + 1, j] == 0 and tempGrid[i + 2, j] == 0 and tempGrid[c, d + 1] == 0 and
                              tempGrid[c, d + 2] == 0):
                            tempGrid[i, j] = element1
                            tempGrid[i + 1, j] = element1
                            tempGrid[i + 2, j] = element1
                            tempGrid[g, h] = 0
                            tempGrid[k, l] = 0
                            tempGrid[c, d] = element2
                            tempGrid[c, d + 1] = element2
                            tempGrid[c, d + 2] = element2
                            tempGrid[a, b] = 0
                            tempGrid[e, f] = 0
                        elif (tempGrid[g + 1, h] == 0 and tempGrid[g + 2, h] == 0 and tempGrid[c, d + 1] == 0 and
                              tempGrid[c, d + 2] == 0):
                            tempGrid[g, h] = element1
                            tempGrid[g + 1, h] = element1
                            tempGrid[g + 2, h] = element1
                            tempGrid[i, j] = 0
                            tempGrid[k, l] = 0
                            tempGrid[c, d] = element2
                            tempGrid[c, d + 1] = element2
                            tempGrid[c, d + 2] = element2
                            tempGrid[a, b] = 0
                            tempGrid[e, f] = 0

                    else:
                        if (tempGrid[a + 1, b] == 0 and tempGrid[a + 2, b] == 0 and tempGrid[g, h + 1] == 0 and
                                tempGrid[g, h + 2] == 0):
                            tempGrid[a, b] = element2
                            tempGrid[a + 1, b] = element2
                            tempGrid[a + 2, b] = element2
                            tempGrid[c, d] = 0
                            tempGrid[e, f] = 0
                            tempGrid[g, h] = element1
                            tempGrid[g, h + 1] = element1
                            tempGrid[g, h + 2] = element1
                            tempGrid[i, j] = 0
                            tempGrid[k, l] = 0
                        elif (tempGrid[c + 1, d] == 0 and tempGrid[c + 2, d] == 0 and tempGrid[g, h + 1] == 0 and
                              tempGrid[g, h + 2] == 0):
                            tempGrid[c, d] = element2
                            tempGrid[c + 1, d] = element2
                            tempGrid[c + 2, d] = element2
                            tempGrid[a, b] = 0
                            tempGrid[e, f] = 0
                            tempGrid[g, h] = element1
                            tempGrid[g, h + 1] = element1
                            tempGrid[g, h + 2] = element1
                            tempGrid[i, j] = 0
                            tempGrid[k, l] = 0
                        elif (tempGrid[c + 1, d] == 0 and tempGrid[c + 2, d] == 0 and tempGrid[i, j + 1] == 0 and
                              tempGrid[i, j + 2] == 0):
                            tempGrid[c, d] = element2
                            tempGrid[c + 1, d] = element2
                            tempGrid[c + 2, d] = element2
                            tempGrid[a, b] = 0
                            tempGrid[e, f] = 0
                            tempGrid[i, j] = element1
                            tempGrid[i, j + 1] = element1
                            tempGrid[i, j + 2] = element1
                            tempGrid[g, h] = 0
                            tempGrid[k, l] = 0
                        elif (tempGrid[a + 1, b] == 0 and tempGrid[a + 2, b] == 0 and tempGrid[i, j + 1] == 0 and
                              tempGrid[i, j + 2] == 0):
                            tempGrid[a, b] = element2
                            tempGrid[a + 1, b] = element2
                            tempGrid[a + 2, b] = element2
                            tempGrid[c, d] = 0
                            tempGrid[e, f] = 0
                            tempGrid[i, j] = element1
                            tempGrid[i, j + 1] = element1
                            tempGrid[i, j + 2] = element1
                            tempGrid[g, h] = 0
                            tempGrid[k, l] = 0


            else:
                (a, b) = list(zip(*np.where(tempGrid == element1)))[0]
                (g, h) = list(zip(*np.where(tempGrid == element2)))[0]
                tempGrid[a, b] = element2
                tempGrid[g, h] = element1
        else:

            # if not the same length, then move each random
            tempgrid,orientation_arr = move_random(tempGrid,N,k,orientation_arr,element1)
            tempgrid, orientation_arr = move_random(tempGrid, N, k, orientation_arr, element2)
    else:
        # choose random block and try to change its place and orientation
        element1 = np.random.randint(1, k + 1)
        tempgrid,orientation_arr = move_random(tempGrid,N,k,orientation_arr,element1)

    #return after crossover to re-enter in the main list
    return tempGrid,orientation_arr

def updateTemp(T):
    return alpha*T



def create(k,weight=1):
    # Assuming that each element can have two input and one output.
    # Initially we only know who is connected with whom. We use 2-d
    # array 1 will represent there is connection between i and j,
    # 0 otherwise
    # filling the values in only upper triangular matrix

    connections = np.zeros([k + 1, k + 1])
    ii = 0
    while ii < k + 1:
        i = int(random.randint(1, k))
        j = int(random.randint(1, k))
        if (i > j) & (connections[j, i] == 0):
            connections[j, i] = weight
            ii = ii + 1
            print(j, i)
        if (i < j) & (connections[i, j] == 0):
            connections[i, j] = weight
            ii = ii + 1
            print(i, j)

    return connections



# This function finds the total wirelength
# find if the block is 3 length then take its half as we consider that the point itself is on the middle
# else continue as if it's square length 1 and the pin in its middle
def cost(k, grid, connections):
    distance = 0
    for element in range(1, k + 1):
        len_element = len(np.where(grid == element)[0])
        x1 = None
        y1 = None
        x2 = None
        y2 = None
        if (len_element == 3):
            (x1, y1) = list(zip(*np.where(grid == element)))[1]
        else:
            (x1, y1) = list(zip(*np.where(grid == element)))[0]

        for nextElement in range(element + 1, k + 1):
            if (connections[element, nextElement]):
                len_next_element = len(np.where(grid == nextElement)[0])
                if (len_next_element == 3):
                    (x2, y2) = list(zip(*np.where(grid == nextElement)))[1]
                else:
                    (x2, y2) = list(zip(*np.where(grid == nextElement)))[0]
                distance += connections[element,nextElement]* np.sqrt(np.absolute(x2 - x1)*np.absolute(x2 - x1) + np.absolute(y2 - y1)*np.absolute(y2 - y1))
    return distance


def annealing(N, k, grid, connections):
    T = INF
    # We initialize the grid
    #if false, this means that it will generate blocks of same size 1
    #true, it will generate random sizes blocks of 1 and 3
    grid,orientation_arr = initialize(k, N, grid,False)
    minCost = cost(k, grid, connections)

    print ("Initial Cost",minCost)
    print ("Initial Grid")
    print (grid)
    printgrid(grid)
    tic = time.clock()

    # No. of interation at each temperature
    # No. of temperature points to try
    while(T > threshold):
        # 4 os the number of population taken
        tempGrid,temp_orientation_arr = process(N, k, grid,orientation_arr,4)
        tempCost = cost(k, tempGrid, connections)
        delta = tempCost - minCost
        if (delta<0):
            grid = tempGrid
            orientation_arr=temp_orientation_arr
            minCost = tempCost
        else:
            p = np.exp(-delta / T)
            if(np.random.random()<p):
                grid = tempGrid
                orientation_arr=temp_orientation_arr
                minCost = tempCost
        T = updateTemp(T)

    return grid,minCost, tic

def mainrun(N,k):

    # We will store the positions of the elements in the N X N grid
    grid = np.zeros([N,N])
    connections = create(k,1)
    print(len(connections))
    finalGrid,cost,tic = annealing(N, k, grid, connections)
    toc = time.clock()
    tim = toc - tic
    print ("time taken ", tim)

    print ("Final Cost", cost)
    print ("Final Grid")
    print (finalGrid)
    printgrid(finalGrid)

mainrun(30,480)

# mainrun(16,8)


