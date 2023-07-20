import sys
import math

filename = sys.argv[1]
num_features = 0
features = []

def get_decisiontree_and_featureslist(filename):              #returns [ vals, decision ]
    global num_features, features
    decision_tree = []
    features = open(filename).readlines()[0].strip().split(",")
    lines = open(filename).readlines()[1:]
    num_features = len(lines[0].strip().split(","))
    for line in lines:
        ls = line.strip().split(",")
        decision_tree.append(ls)
    return decision_tree

def find_featls(dectree):
    featls = []
    for i in range(num_features):
        featls.append([])
    for ftlist in dectree:
        for i in range(num_features):
            featls[i].append(ftlist[i])
    return featls

def calc_entropy(f):
    val_freq_dic, entropy, total = {}, 0, len(f)
    for val in (f):
        if(val not in val_freq_dic): val_freq_dic.update({ val : 1 })
        else: val_freq_dic[val] += 1

    for val in val_freq_dic:
        freq = val_freq_dic[val]
        entropy += (freq/total)*(math.log2(freq/total))
    return -1*entropy    

def calc_expectedentropy(f, starting_dataset):
    fval_outcome_dic, expected_entropy, total = {}, 0, len(f)           #val_outcome_dic = { feature_val<string> : [corresponding_outcome]<list of strings> }
    for i in range(total):
        fval, outcome = f[i], starting_dataset[i]
        if(fval not in fval_outcome_dic): fval_outcome_dic.update({ fval : [outcome] })
        else: fval_outcome_dic[fval].append(outcome)

    for fval in fval_outcome_dic:
        outcomels = fval_outcome_dic[fval]
        expected_entropy += (len(outcomels)/total) * calc_entropy(outcomels)    
    return expected_entropy

def find_infogain(featureslist):            #returns { (features) <tuple of strings> : infogain <float> }
    starting_dataset = featureslist[-1]
    starting_entropy = calc_entropy(starting_dataset)
    feat_infogain = {}
    for feature in featureslist[:-1]:
        expected_entropy = calc_expectedentropy(feature, starting_dataset)
        feat_infogain.update({tuple(feature) : starting_entropy - expected_entropy})
    return feat_infogain

def find_pos_values(featurelist):
    valuesls = []
    for value in featurelist:
        if value not in valuesls: valuesls.append(value)
    return valuesls

def split_dataset(ind, decisiontree, pos_vals):
    valuesls = []
    for val in pos_vals:
        valls = []
        for ls in decisiontree:
            if(ls[ind] == val): valls.append(ls)
        valuesls.append(valls)
    return valuesls

def getdepth(depth):
    s = ""
    for i in range(depth): s += "  "
    return s

def recur(decisiontree, featureslist, depth):
    global features, f
    f.write(getdepth(depth))
    feature_infogain = find_infogain(featureslist)
    max_infogain_feature = list(max(feature_infogain, key = feature_infogain.get))
    ind = featureslist.index(max_infogain_feature)
    f.write(f"* {features[ind]}?\n")
    depth += 1
    pos_vals = find_pos_values(max_infogain_feature)
    split_ls = split_dataset(ind, decisiontree, pos_vals)                      #[ [value1ls], [value2ls], ... ]
    for dataset in split_ls:
        ftlist = find_featls(dataset)
        feat, starting_dataset = ftlist[ind], ftlist[-1]
        if((expectedentropy:=calc_expectedentropy(feat, starting_dataset)) == 0):
            f.write(getdepth(depth))
            f.write(f"* {feat[0]} --> {starting_dataset[0]}\n")
        else: 
            f.write(getdepth(depth))
            f.write(f"* {feat[0]}\n")
            recur(dataset, ftlist, depth+1)

dectree = get_decisiontree_and_featureslist(filename)
ftslist = find_featls(dectree)
f = open("treeout.txt", "w")
recur(dectree, ftslist, 0)

'''
The recursive algorithm should:
1. Consider each feature in turn. Find the information gain from differentiating based on that feature.
2. Choose the feature with the highest information gain.
3. Split the dataset into smaller datasets based on the possible values of the chosen feature.
4. If any of the resulting datasets has an entropy of 0, then it is a leaf.
5. Otherwise, recur on any smaller dataset with an entropy > 0.
'''