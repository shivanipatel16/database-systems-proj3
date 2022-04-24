import pandas as pd
from itertools import chain, combinations

# issubset function returns true if all elements in set are in another set
    # create a table containing support count of each item in the dataset. This will be the candidate set
    # compare each item in the candidate set to the min support. If less than min supp, remove the items. This gives the itemset L1.
    # create second candidate set using join of Lk-1 and Lk-1.
    # Check all subsets of an itemset to see if they are frequent. If not frequent, then remove the itemset.
    # Find support of the itemsets
    # compare each item in the second candidate set to the min support. If less than min supp, remove the items. This gives the itemset L2.
    # TODO: get frequent 1 itemsets

def first_iteration(df,num_trans):
    L1 = pd.DataFrame(columns=['Itemset', 'Support'])
    num_cols = df.shape[1]
    c1 = pd.DataFrame(columns=['Itemset', 'Count'])
    for i in range(0, num_cols):
        count = df.values[:, i].sum()
        c1.loc[len(c1.index)] = [[df.columns[i]], count]
        get_frequent_items_first_pass(L1, count, num_trans, df, i)
    return L1, c1

def get_frequent_items_first_pass(L1, count,num_trans, df, i):
    min_supp = 0.01
    supp = check_support(count, num_trans)
    if supp >= min_supp:
        L1.loc[len(L1.index)] = [df.columns[i], supp * 100]
    # if supp < min_supp:
    #     print("PRUNED")
    #     print([df.columns[i]], df.values[:, i].sum())
    return L1

def generate_kth_candidate_set(df,Lk_1,num_trans):
    num_cols = df.shape[1]
    cK = pd.DataFrame(columns=['Itemset', 'Count'])
    LK = pd.DataFrame(columns=['Itemset', 'Support'])
    for i in range(0, num_cols):
        for j in range(i + 1, num_cols):
            new_colname = [df.columns[i], df.columns[j]]
            count = (df.values[:, i] & df.values[:, j]).sum()
            cK.loc[len(cK.index)] = [new_colname, count] #append to dataframe the new itemset and the count
            LK = generate_kth_frequent_itemset(new_colname,Lk_1,count,LK,num_trans)
    return LK,cK

def generate_kth_frequent_itemset(colname,LK_1,count,LK,num_trans):
    min_supp = 0.01
    subset = set((chain.from_iterable(combinations(colname, r) for r in range(1,len(colname)))))
    is_subset_list = []
    LK_1_set = LK_1.values[:, 0]
    for i in subset:
        is_subset_list.append(set(i).issubset(LK_1_set))
    if all(is_subset_list) == True: #if all the subsets are in the previous frequent itemset list, then check support and continue
        support = check_support(count, num_trans)
        if support >= min_supp: #if support is greater than min support, then add that itemset to the frequent itemset
            LK.loc[len(LK.index)] = [colname, support * 100]  #append to dataframe the new itemset and the count
    return LK

def check_support(count, num_of_transactions):
    supp = count/num_of_transactions
    return supp

if __name__ == "__main__":
    # main()
    df = pd.read_csv("INTEGRATED-DATASET.csv")
    num_trans = df.shape[0] #get number of rows of dataframe which represents the transactions
    L1, C1 = first_iteration(df,num_trans) #run the first iteration of the algo for itemsets of 1
    empty_set = set()
    print("==Frequent itemsets(min_sup= 1%)")
    print(L1)
    LK = L1 #initialize LK
    Lk_1 = L1
    k = 2

    while len(LK) != 0:
        print("==Frequent", k, "itemsets(min_sup= 1%)")
        LK,CK = generate_kth_candidate_set(df, Lk_1 , num_trans)
        Lk_1 = LK
        print(LK)
        k += 1
