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

def generate_kth_candidate_set(df,L1,num_trans):
    num_cols = df.shape[1]
    c2 = pd.DataFrame(columns=['Itemset', 'Count'])
    L2 = pd.DataFrame(columns=['Itemset', 'Support'])
    for i in range(0, num_cols):
        for j in range(i + 1, num_cols):
            new_colname = [df.columns[i], df.columns[j]]
            count = (df.values[:, i] & df.values[:, j]).sum()
            c2.loc[len(c2.index)] = [new_colname, count] #append to dataframe the new itemset and the count
            L2 = generate_kth_frequent_itemset(new_colname,L1,count,L2,num_trans)
    return L2,c2

def generate_kth_frequent_itemset(colname,L1,count,L2,num_trans):
    min_supp = 0.01
    subset = set((chain.from_iterable(combinations(colname, r) for r in range(1,len(colname)))))
    is_subset_list = []
    L1_set = L1.values[:, 0]
    for i in subset:
        is_subset_list.append(set(i).issubset(L1_set))
    if all(is_subset_list) == True:
        support = check_support(count, num_trans)
        if support >= min_supp:
            L2.loc[len(L2.index)] = [colname, support  * 100]  #append to dataframe the new itemset and the count
    return L2

def check_support(count, num_of_transactions):
    supp = count/num_of_transactions
    return supp

if __name__ == "__main__":
    # main()
    df = pd.read_csv("INTEGRATED-DATASET.csv")
    num_trans = df.shape[0]
    L1, C1 = first_iteration(df,num_trans)
    print("==Frequent itemsets(min_sup= 1%)")
    print(L1)
    L2,C2 = generate_kth_candidate_set(df, L1,num_trans)
    print(L2)
