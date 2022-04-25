import sys
import pandas as pd
import itertools
import numpy as np
from queue import PriorityQueue


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
        # if not os.path.isfile(dataset_file):
        #     return False
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
            L_k.loc[len(L_k.index)] = [itemset_k, support * 100]  # append to dataframe the new itemset and the count

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

def get_support(right_side,L_all):
    print("L_all IS")
    print(L_all)
    support = L_all.loc[L_all['Itemset'] == right_side]['Support'].values
    print(support)
    return support

def calculate_conf(support,items,L_all):
        #Get the support of left and right side of association rule
        #TODO: Get support of left side
        conf = 1
        if len(items) != 1:
            for i in itertools.combinations(items, len(items) - 1):  # gets all combos of items with length - 1.
                  right_side = set(items) - set(i) # subset subtraction. To get the single item that is not on the left side
                  left_side = set(i)
                  sup_left_side = support
                  sup_right_side = get_support(right_side,L_all)
                  #print(sup_right_side)
                  conf = sup_right_side / sup_left_side
                  print(left_side, "=>", right_side, "Conf:", conf, "Support:", support)
        return conf

def main(frequent_itemsets_=None):
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
    confidence_rules = PriorityQueue()
    num_trans = df.shape[0] # get number of rows of dataframe which represents the transactions
    L_1 = first_iteration(df, num_trans, min_supp) # run the first iteration of the algo for itemsets of 1
    frequent_itemsets = add_frequent_itemset(frequent_itemsets, L_1)
    frequent_itemsets_copy = frequent_itemsets

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

    frequent_itemsets_copy2 = frequent_itemsets
    L_all = pd.DataFrame(columns=['Itemset', 'Support'])
    while not frequent_itemsets_copy2.empty():
        support, items = frequent_itemsets_copy2.get()
        L_all.loc[len(L_all.index)] = [items, support]  # append to dataframe the new itemset and the count

    while not frequent_itemsets_copy.empty():
        support, items = frequent_itemsets_copy.get()
        conf1 = calculate_conf(support, items, L_all)
        print(conf1)

    
    # find all itemsets that are > 1 size


    with open("output.txt", "w") as f:
        print("==Frequent itemsets (min_sup={0:.3g}%)".format(min_supp*100), file=f)
        frequent_itemsets_print = list()
        confidence_rules_print = list()
        while not frequent_itemsets.empty():
             frequent_itemsets_print = [frequent_itemsets.get()] + frequent_itemsets_print
             #confidence_rules_print = [calculate_conf(support,items)] + confidence_rules_print

        for supp, itemset in frequent_itemsets_print:
            print("{itemset}, {supp:.3f}%".format(itemset=itemset, supp=supp), file=f)
        # for supp, itemset in confidence_rules_print:
        #     print("{itemset}, {conf:.3f}%".format(itemset=itemset, conf=conf), file=f)




if __name__ == "__main__":
    main()
