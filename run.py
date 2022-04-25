import sys
import pandas as pd
import itertools
import numpy as np
from queue import PriorityQueue


def valid_args(args):
    # TODO
    return True


def first_iteration(df, num_trans, min_supp):
    L_1 = pd.DataFrame(columns=['Itemset', 'Support'])
    num_cols = df.shape[1]

    # create a table containing support count of each item in the dataset. This will be the candidate set
    c_1 = pd.DataFrame(columns=['Itemset', 'Count'])

    for i in range(0, num_cols):
        count = df.values[:, i].sum()
        c_1.loc[len(c_1.index)] = [{df.columns[i]}, count]
        L_1 = get_frequent_items_first_pass(L_1, count, num_trans, df, i, min_supp)

    return L_1

def get_frequent_items_first_pass(L_1, count, num_trans, df, i, min_supp):
    supp = check_support(count, num_trans)

    # compare each item in the candidate set to the min support. If less than min supp, remove the items.This gives the itemset L1
    if supp >= min_supp:
        L_1.loc[len(L_1.index)] = [{df.columns[i]}, supp * 100]

    return L_1

def generate_kth_candidate_set(df, L_k_1, num_trans, min_supp):  # create kth candidate set using join of Lk-1 and Lk-1.
    c_k = pd.DataFrame(columns=['Itemset', 'Count'])
    L_k = pd.DataFrame(columns=['Itemset', 'Support'])

    for itemset_k_1 in L_k_1['Itemset']:
        for new_item in df.columns:
            if new_item not in itemset_k_1:
                itemset = itemset_k_1.copy()
                itemset.add(new_item)

                meets_support = np.full(num_trans, True)
                for i in itemset:
                    meets_support = meets_support & df[i]

                count = (meets_support).sum()
                c_k.loc[len(c_k.index)] = [itemset, count] # append to dataframe the new itemset and the count
                L_k = generate_kth_frequent_itemset(itemset, L_k_1, count, L_k, num_trans, min_supp)

    return L_k

def generate_kth_frequent_itemset(itemset_k, L_k_1, count, L_k, num_trans, min_supp):
    subsets_k_1 = [set(i) for i in itertools.combinations(itemset_k, len(itemset_k)-1)]

    is_valid_k_set = True
    for i in subsets_k_1:
        is_valid_k_set = set(i) in L_k_1.values[:, 0]

    if is_valid_k_set:
        support = check_support(count, num_trans)
        if support >= min_supp: # if support is greater than min support, then add that itemset to the frequent itemset
            L_k.loc[len(L_k.index)] = [itemset_k, support * 100]  # append to dataframe the new itemset and the count

    return L_k

def check_support(count, num_of_transactions):
    return float(count)/float(num_of_transactions)

def add_frequent_itemset(frequent_itemsets, L_k):
    for i in L_k.values:
        item, supp = i
        item = sorted(list(item))
        frequent_itemsets.put((supp, item))

    return frequent_itemsets

def main():
    args = tuple(sys.argv[1:])
    # error message if the arguments are invalid
    if not valid_args(args): # TODO
        print("Invalid arguments.")
        print("Usage: python3 run.py INTEGRATED-DATASET.csv <min_sup> <min_conf>")
        return

    dataset_file, min_supp, min_conf = args
    min_supp = float(min_supp)
    min_conf = float(min_conf)
    df = pd.read_csv(dataset_file)
    k = 1

    frequent_itemsets = PriorityQueue()
    num_trans = df.shape[0] # get number of rows of dataframe which represents the transactions
    L_1 = first_iteration(df, num_trans, min_supp) # run the first iteration of the algo for itemsets of 1
    frequent_itemsets = add_frequent_itemset(frequent_itemsets, L_1)

    print("==Frequent {} itemsets(min_sup= {}%)".format(k, min_supp))
    #print(L_1)

    L_k = L_1 # initialize L_k
    L_k_1 = L_1
    k += 1

    while len(L_k_1) != 0:
        L_k = generate_kth_candidate_set(df, L_k_1 , num_trans, min_supp)
        frequent_itemsets = add_frequent_itemset(frequent_itemsets, L_k)

        print("==Frequent {} itemsets(min_sup= {}%)".format(k, min_supp))
        #print(L_k)


        L_k_1 = L_k
        k += 1

    confidence_rules = PriorityQueue() 
    
    # find all itemsets that are > 1 size
    # compute the sets like [x -> y] or [x -> y, z] or [x -> y, z, a]


    with open("output.txt", "w") as f:
        print("==Frequent itemsets (min_sup={0:.3g}%)".format(min_supp*100), file=f)
        frequent_itemsets_print = list()
        while not frequent_itemsets.empty():
            frequent_itemsets_print = [frequent_itemsets.get()] + frequent_itemsets_print

        for supp, itemset in frequent_itemsets_print:
            print("{itemset}, {supp:.3f}%".format(itemset=itemset, supp=supp), file=f)

if __name__ == "__main__":
    main()