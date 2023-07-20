def categorize_cars(state):
    visited = []
    for i in range(len(state)):
        if((num:=state[i]) != "." and num not in visited):
            visited.append(num)
            if(num == state[i+1] == state[i+2]): h_cars.update({num : 3})
            elif(num == state[i+1]): h_cars.update({num : 2})
            elif((i <= 23) and num == state[i+6] == state[i+12]): v_cars.update({num : 3})
            elif(num == state[i+6]): v_cars.update({num : 2})

sample_board = "111..2..3..2003..26.3.446...5.777.5."
h_cars = {}                 #horizontal_cars = {num(str) : length(int)}
v_cars = {}                 #vertical_cars = {num(str) : length(int)}

def categorize_cars(state):
    visited = []
    for i in range(len(state)):
        if((num:=state[i]) != "." and num not in visited):
            visited.append(num)
            if(num == state[i+1] == state[i+2]): h_cars.update({num : 3})
            elif(num == state[i+1]): h_cars.update({num : 2})
            elif((i <= 23) and num == state[i+6] == state[i+12]): v_cars.update({num : 3})
            elif(num == state[i+6]): v_cars.update({num : 2})

def dicadd(dic, car, ind):
    if(car not in dic): dic.update({car : [ind]})
    else: dic[car].append(ind)

def current_indexes(state):
    temp, dic = list(state), {}
    for i in range(len(temp)):
        if(temp[i] != "."): dicadd(dic, temp[i], i)
    return dic

def get_possible_hindexes(parent, dic):                                                #parent is string
    car_leftpossibleindex, car_rightpossibleindex = {}, {}                        #{carnum(str) : [possibleindex(int)]}
    for car in h_cars.keys():
        state = list(parent)
        leftindex, length = dic[car][0], h_cars[car]
        rightindex = leftindex + length - 1
        while((leftindex%6!=0) and (state[leftindex-1] == ".")):                  #Checking indexes to the left of car
            dicadd(car_leftpossibleindex, car, leftindex-1)
            leftindex -= 1
        while(((rightindex+1)%6!=0) and (state[rightindex+1] == ".")):            #Checking indexes to the right of car
            dicadd(car_rightpossibleindex, car, rightindex+1)
            rightindex += 1
    return (car_leftpossibleindex, car_rightpossibleindex)

def get_possible_vindexes(parent, dic):                                                #parent is string
    car_toppossibleindex, car_bottompossibleindex = {}, {}                        #{carnum(str) : [possibleindex(int)]}
    for car in v_cars.keys():
        state = list(parent)
        topindex, length = dic[car][0], v_cars[car]
        bottomindex = ((length-1) * 6) + topindex
        while((topindex>5) and (state[topindex-6] == ".")):                       #Checking indexes above car
            dicadd(car_toppossibleindex, car, topindex-6)
            topindex -= 6
        while((bottomindex<30) and (state[bottomindex+6] == ".")):                #Checking indexes below car
            dicadd(car_bottompossibleindex, car, bottomindex+6)
            bottomindex += 6
    return (car_toppossibleindex, car_bottompossibleindex)

'''
categorize_cars(sample_board)
indexesdic = current_indexes(sample_board)
print(indexesdic)
print(get_possible_hindexes(sample_board, indexesdic))
print(get_possible_vindexes(sample_board, indexesdic))
'''

print(len("BCCCDEBFFFDEAAGHIJKKGHIJ...LMM...LNN"))