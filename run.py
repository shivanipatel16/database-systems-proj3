import sys
import pandas as pd
import itertools
import numpy as np
from queue import PriorityQueue
import copy
import os


def valid_args(args):
    """
    validates input arguments to make sure exists and min_sup and min_conf are both between 0-1
    """
    if len(args) != 3:
        return False
    try:
        dataset_file, min_supp, min_conf = args
        min_supp = float(min_supp)
        min_conf = float(min_conf)
        if min_supp > 1 or min_supp < 0 or min_conf > 1 or min_conf < 0:
            return False
        if not os.path.isfile(dataset_file):
            print(os.path.isfile(dataset_file))
            return False
        return True
    except Exception as e:
        print(e)
        return False


def first_iteration(df, num_trans, min_supp):
    """
        creates L_1 which is the valid candidate sets of size 1

        df: pandas dataframe that represents the rows as market baskets and each column is an item in the basket
        num_trans: the number of transactions (row) in the df
        min_supp: the minimum support specified at runtime as command-line argument
        """
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
    """
    helper function to first_iteration that checks the current item to see if meets the minimum support and it adds to L_1 if it does

    L_1: pandas df that represents the valid itemsets with its support of size 1
    count: number of transactions that meet the criteria (in this case its the number of transactions that contain that item)
    num_trans: the number of transactions (row) in the df
    df: pandas dataframe that represents the rows as market baskets and each column is an item in the basket
    i: integer value that represents the index of the item in the df
    min_supp: the minimum support specified at runtime as command-line argument
    """
    supp = check_support(count, num_trans)

    # compare each item in the candidate set to the min support. If less than min supp, remove the items.This gives the itemset L1
    if supp >= min_supp:
        L_1.loc[len(L_1.index)] = [{df.columns[i]}, supp * 100]

    return L_1

def generate_kth_candidate_set(df, L_k_1, num_trans, min_supp):  # create kth candidate set using join of Lk-1 and Lk-1.
    """
        creates kth candidate set using join of Lk-1 and Lk-1 and then prunes the new candidate set by checking the subsets of size k-1 and then its support

        df: pandas dataframe that represents the rows as market baskets and each column is an item in the basket
        L_k_1: pandas df that represents the valid itemsets with its support of size k-1
        num_trans: the number of transactions (row) in the df
        min_supp: the minimum support specified at runtime as command-line argument
        """
    c_k = pd.DataFrame(columns=['Itemset', 'Count'])
    L_k = pd.DataFrame(columns=['Itemset', 'Support'])

    for itemset_k_1 in L_k_1['Itemset']:
        for new_item in df.columns:
            if new_item not in itemset_k_1:
                itemset = set(itemset_k_1.copy())
                itemset.add(new_item)

                meets_support = np.full(num_trans, True)
                for i in itemset:
                    meets_support = meets_support & df[i]

                count = (meets_support).sum()
                c_k.loc[len(c_k.index)] = [frozenset(itemset), count] # append to dataframe the new itemset and the count
                L_k = generate_kth_frequent_itemset(itemset, L_k_1, count, L_k, num_trans, min_supp)

    L_k.drop_duplicates(subset='Itemset', inplace=True)


    return L_k

def generate_kth_frequent_itemset(itemset_k, L_k_1, count, L_k, num_trans, min_supp):
    """
        performs pruning step by checking all subsets of size k-1 of itemset of size k and making sure it is in L_k_1
        then checks to make sure the itemset meets the minimum support threshold

        count: number of transactions that meet the criteria (in this case its the number of transactions that contain that item)
        num_trans: the number of transactions (row) in the df
        min_supp: the minimum support specified at runtime as command-line argument
        """

    subsets_k_1 = [set(i) for i in itertools.combinations(itemset_k, len(itemset_k)-1)]

    is_valid_k_set = True
    for i in subsets_k_1:
        is_valid_k_set = set(i) in L_k_1.values[:, 0]

    if is_valid_k_set:
        support = check_support(count, num_trans)
        if support >= min_supp: # if support is greater than min support, then add that itemset to the frequent itemset
            L_k.loc[len(L_k.index)] = [frozenset(itemset_k), support * 100]  # append to dataframe the new itemset and the count

    return L_k

def check_support(count, num_of_transactions):
    """
        simply returns the support given the count of transactions that met the criteria over the total num_of_transactions
        """
    return float(count)/float(num_of_transactions)

def add_frequent_itemset(frequent_itemsets, L_k):
    """
        add frequent itemsets to priority queue for final output.txt file

        frequent_items: priority queue where each itemset is ordered by the support
        L_k: pandas df that represents the valid itemsets with its support of size k
        """

    for i in L_k.values:
        item, supp = i
        item = sorted(list(item))
        frequent_itemsets.put((supp, item))

    return frequent_itemsets

def add_confident_itemset(confident_itemsets, L_conf):
    """
        add confident itemsets to priority queue for final output.txt file

        confident_items: priority queue where each itemset is ordered by the confident
        L_k: pandas df that represents the valid itemsets with its confident of size k
        """

    for i in L_conf.values:
        left, right, conf, supp = i
        left = sorted(list(left))
        right = list(right)
        my_tuple = (left, right, supp)
        confident_itemsets.put((conf, my_tuple))

    return confident_itemsets

def get_support(left_side, L_all):
    left_side = list(left_side)
    left_side = sorted(left_side)
    support = 0
    index = 0
    for i in L_all['Itemset']:
        if (i == left_side):
            support = L_all['Support'][index]
        index += 1

    return support

def calculate_conf(support, items, L_all, L_conf, min_conf):
        # Get the support of left and right side of association rule
        conf = 1
        if len(items) != 1:
            for i in itertools.combinations(items, len(items) - 1):  # gets all combos of items with length - 1.
                  right_side = set(items) - set(i) # subset subtraction. To get the single item that is not on the left side
                  left_side = set(i)
                  sup_union = support
                  sup_left_side = get_support(left_side, L_all)
                  conf = sup_union / sup_left_side
                  if conf >= min_conf:
                    L_conf.loc[len(L_conf.index)] = [left_side, right_side, conf * 100, support]  # append to dataframe the new itemset and the count
        return L_conf,support


def print_output_file(frequent_itemsets, confidence_rules, min_supp, min_conf):
    """
    prints out the output file using the frequent itemsets and confidence association rules
    """
    with open("output.txt", "w") as f:

        frequent_itemsets_print = list()
        while not frequent_itemsets.empty():
             frequent_itemsets_print = [frequent_itemsets.get()] + frequent_itemsets_print

        confidence_rules_print = list()
        while not confidence_rules.empty():
            confidence_rules_print = [confidence_rules.get()] + confidence_rules_print

        print("==Frequent itemsets (min_sup={0:.3g}%)".format(min_supp*100), file=f)
        for supp, itemset in frequent_itemsets_print:
            print("{itemset}, {supp:.3f}%".format(itemset=itemset, supp=supp), file=f)

        print("==High-confidence association rules (min_conf={0:.3g}%)".format(min_conf*100), file=f)
        for conf, my_tuple in confidence_rules_print:
            print("{left} => {right} (Conf: {conf:.3f}%, Supp:{supp: .3f}%)".format(left=my_tuple[0], right=my_tuple[1], conf=conf, supp=my_tuple[2]), file=f)

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
    frequent_itemsets_copy = PriorityQueue()
    frequent_itemsets_copy2 = PriorityQueue()
    confidence_rules = PriorityQueue()

    num_trans = df.shape[0] # get number of rows of dataframe which represents the transactions
    L_1 = first_iteration(df, num_trans, min_supp) # run the first iteration of the algo for itemsets of 1
    frequent_itemsets = add_frequent_itemset(frequent_itemsets, L_1)

    print("==Frequent {} itemsets(min_sup={}%)".format(k, min_supp))
    # print(L_1)

    L_k = L_1 # initialize L_k
    L_k_1 = L_1
    k += 1


    while len(L_k_1) != 0:
        L_k = generate_kth_candidate_set(df, L_k_1 , num_trans, min_supp)
        frequent_itemsets = add_frequent_itemset(frequent_itemsets, L_k)

        print("==Frequent {} itemsets(min_sup={}%)".format(k, min_supp))
        #print(L_k)
        L_k_1 = L_k
        k += 1

    frequent_itemsets_copy.queue = copy.deepcopy(frequent_itemsets.queue)
    frequent_itemsets_copy2.queue = copy.deepcopy(frequent_itemsets.queue)

    L_all = pd.DataFrame(columns=['Itemset', 'Support'])
    L_conf = pd.DataFrame(columns=['Left', 'Right', 'Confidence', 'Support'])

    while not frequent_itemsets_copy2.empty():
        support, items = frequent_itemsets_copy2.get()
        L_all.loc[len(L_all.index)] = [items, support]  # append to dataframe the new itemset and the count

    while not frequent_itemsets_copy.empty():
        support, items = frequent_itemsets_copy.get()
        L_conf, confidence = calculate_conf(support, items, L_all, L_conf, min_conf)

    confidence_rules = add_confident_itemset(confidence_rules, L_conf)

    print_output_file(frequent_itemsets, confidence_rules, min_supp, min_conf)

if __name__ == "__main__":
    main()
