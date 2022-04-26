# database-systems-proj3
Aditi Dam (ad3707) and Shivani Patel (svp2128)

**list of all files**
- README.md
- make-dataset.py
- run.py
- example-run.txt

## Install Requirements
```angular2html
sudo apt-get update
sudo apt install python3-pip
pip3 install pandas
```

## How to run the program:
```angular2html
python3 run.py INTEGRATED-DATASET.csv {min_sup} {min_conf}
```

## Detailed Description:

### NYC Open Data set we used: [Motor Vehicle Collisions - Crashed](https://data.cityofnewyork.us/Public-Safety/Motor-Vehicle-Collisions-Crashes/h9gi-nx95)
The Motor Vehicle Collisions crash table contains details on the crash event. Each row represents a crash event. The Motor Vehicle Collisions data tables contain information from all police reported motor vehicle collisions in NYC.

### High-level procedure to make INTEGRATED-DATASET.csv:
- First, we dropped columns that we did not think would make good basket items such as Latitude and Longitude.
- Since the dataset was over 1.8 million rows, we removed all rows that contained an NA, empty string, or Unspecified value. 
- Then, we took the columns that had numerical values such as Number of Persons Injuried, and we converted it to a boolean by making it True if the value was higher than 0 and False otherwise. 
- Then, the columns we were left with were Bourough, Contributing Factor Vehicle 1, and Contributing Factor Vehicle 2. Since, these strings were formattedly properly, we made each item in the set (such as all 5 boroughs), its own basket item. 
- Thus we were left with 166,434 rows x 133 columns: 
    - Some of the columns we have in our INTEGRATED-DATASET.csv: PERSONS INJURED,PERSONS KILLED,PEDESTRIANS INJURED,PEDESTRIANS KILLED,CYCLIST INJURED,CYCLIST KILLED,MOTORIST INJURED,MOTORIST KILLED,QUEENS - BOROUGH,BROOKLYN - BOROUGH,...,Failure to Yield Right-of-Way - CONTRIBUTING FACTOR VEHICLE 2

Note: make-dataset.py is the script we ran to make our INTEGRATED-DATASET.csv.

### Justification of Choice of Dataset:
We believe that this dataset of Motor Vehicle Collisions crash table provided interesting information as to whether collisions in NYC are as reckless as people may think. Where do these collosions usually happen? Is there a link between the reason why crash collosions happen with its location? What about injury rates? Is there an association with the injury rates with the reason why an accident occured? These were all questions that we decided we wanted to invest and learn more about about.

## Internal Design of Project:
**make-dataset.py** creates the INTEGRATED-DATASET.csvfile as specified in section earlier.

**run.py**
1. valid_args(): check input to make sure all inputs are valid and return usage if there is incorrect usage
2. main(): Convert INTEGRATED-DATASET.csv into pandas df
3. first_iteration() & get_frequent_items_first_pass(): Find all itemset of size 1 that meet the minimum support and call this L_1.
4. generate_kth_candidate_set( & generate_kth_frequent_itemset(): Iterate on L_k-1 to find L_k by finding the itemsets of size k using a join from L_k-1 and the original columns from INTEGRATED-DATASET.csv. Prune all itemsets of size k that contains subsets of size k-1 that are not in L_1. Prune all itemsets of size k that do not meet the minimum support.
5. main(): Repeat step 6 until L_k-1 is the empty set.
6. main(): Join all L_1, L_2, ..., L_k-1 , and let's call it frequent-itemsets
7. calculate_conf(): Form the association rules of all frequent-itemsets such that there is 1 item on the left side and 1 or more on the right side. The item on the left side must not be on the right side as well.
8. calculate_conf(): For every association rule, compute the confidence by computing the support of the the left side union right side divided by the support of the left side. Keep all rules that need the confidence threshold. 
9. print_output_file(): Generate output.txt file. 

## Compelling Run: 
```angular2html
run.py INTEGRATED-DATASET.csv 0.05 0.70
```

### Compelling Result:
These results are compelling because we can see that most motor collisions occur because of drivers being distracted, and we can see that many collosions occur in Mahattan. Furthermore, we can see that many injuries are due to a motorists. For example if a person is injuried, there is 76% confidence rate that they a motorist is injured. We can use this information to try to get better regulations for traffic violations and try to keep collisions rates low given that we know the target location and target vehicles that are associated with collisions. 
