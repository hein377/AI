def find_indexes_to_check(start, goal):         #start and goal are lists
    inds_to_check = []
    for i in range(len(start)):
        if(start[i] != goal[i]): inds_to_check.append(i)
    return inds_to_check

def get_children(parent, itc):
    children = []
    for index in itc:
        for letter in alphabet:
            temp = list(parent)
            temp[index] = letter
            if((st:=''.join(temp)) in words and st!=parent): children.append(st)
    return children