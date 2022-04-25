# database-systems-proj3
Aditi Dam (ad3707) and Shivani Patel (svp2128)

**list of all files**
- README.md
- make-dataset.py
- run.py

## Install Requirements
```angular2html
sudo apt-get update
sudo apt install python3-pip
```

## How to run the program:
```angular2html
python3 run.py INTEGRATED-DATASET.csv {min_sup} {min_conf}
```

## Detailed Description:

### NYC Open Data set we used:
[Motor Vehicle Collisions - Crashed](https://data.cityofnewyork.us/Public-Safety/Motor-Vehicle-Collisions-Crashes/h9gi-nx95)

The Motor Vehicle Collisions crash table contains details on the crash event. Each row represents a crash event. The Motor Vehicle Collisions data tables contain information from all police reported motor vehicle collisions in NYC.

### High-level procedure to make INTEGRATED-DATASET.csv:
- First, we dropped columns that we did not think would make good basket items such as Latitude and Longitude.
- Since the dataset was over 1.8 million rows, we removed all rows that contained an NA, empty string, or Unspecified value. 
- Then, we took the columns that had numerical values such as Number of Persons Injuried, and we converted it to a boolean by making it True if the value was higher than 0 and False otherwise. 
- Then, the columns we were left with were Bourough, Contributing Factor Vehicle 1, and Contributing Factor Vehicle 2. Since, these strings were formattedly properly, we made each item in the set (such as all 5 boroughs), its own basket item. 
- Thus we were left with 166,434 rows x 133 columns: 
    - Some of the columns we have in our INTEGRATED-DATASET.csv: PERSONS INJURED,PERSONS KILLED,PEDESTRIANS INJURED,PEDESTRIANS KILLED,CYCLIST INJURED,CYCLIST KILLED,MOTORIST INJURED,MOTORIST KILLED,QUEENS - BOROUGH,BROOKLYN - BOROUGH,...,Failure to Yield Right-of-Way - CONTRIBUTING FACTOR VEHICLE 2

Note: make-dataset.py is the script we run to make our INTEGRATED-DATASET.csv.

### Justification of Choice of Dataset:
We believe that this dataset of Motor Vehicle Collisions crash table provided interesting information as to whether collisions in NYC are as reckless as people may think. Where do these collosions usually happen? Is there a link between the reason why crash collosions happen with its location? What about injury rates? Is there an association with the injury rates with the reason why an accident occured? These were all questions that we decided we wanted to invest and learn more about about.

## Internal Design of Project:
**make-dataset.py** creates the INTEGRATED-DATASET.csvfile as specified in section earlier.

**run.py**
1. 

## Compelling Run:

### Compelling Result:
