import pandas as pd

radial_data = pd.read_csv("radial_zipcodes.csv")
radial_data.rename(columns={'Unnamed: 0': 'zip', "0": "neighbors"}, inplace=True)

uzips = pd.read_csv("uzips.csv")

#meta functions

import copy
import numpy as np
import bisect

"""
Parameters
ordered_list int[]: an ordered list of integers
element int: an integer

Returns
true if element is contained by ordered_list, false if it does not
"""
def ordered_contains(ordered_list, element):
    index = bisect.bisect_left(ordered_list, element)
    return index < len(ordered_list) and ordered_list[index] == element


#helper functions

"""
Parameters
df DataFrame: a dataframe with a zip and neighbors column
zips int[]: a list of zipcodes to be removed 


Returns
updated_dataframe DataFrame: a copy of the dataframe with specified zip codes omitted
"""

def omit_zips(df, zips):
    new_zips = []
    new_neighbors = []
    
    for idx, row in df.iterrows():
        if row['zip'] in zips:
            continue

        new_zips.append(row['zip'])
        new_neighbors.append(",".join([x for x in row['neighbors'].split(",") if not ordered_contains(zips, float(x))]))

    updated_dataframe = pd.DataFrame({"zip": np.array(new_zips), "neighbors": np.array(new_neighbors)})

    return updated_dataframe


#Data Preprocessing

#Remove all Alaska, Hawaii, and Puerto Rico Zip codes

print("Filtering Data...")

exclude_ids = ['HI', 'PR', 'AK', 'VI']
filtered_df = uzips[uzips['state_id'].isin(exclude_ids)]
non_continental_zips = filtered_df['zip'].tolist()

radial_data = omit_zips(radial_data, non_continental_zips)

print("Data Filtered.")


def get_neighbors(zip):
    return [float(x) for x in radial_data[radial_data["zip"] == zip]["neighbors"].to_list()[0].split(",")]

def total_population(zips):
    return uzips[uzips['zip'].isin(zips)]["population"].sum()

def total_new_population(zip):
    neighbors = get_neighbors(zip)
    intersection = [neighbor for neighbor in neighbors if neighbor in radial_data["zip"].to_list()]
    return total_population(intersection)
    


def get_populations(startidx, endidx):
    radial_populations = {}
    
    for idx, zip in radial_data.iterrows():
        if idx < startidx:
            continue
        if idx > endidx:
            break
        print(idx, zip["zip"])
        radial_populations[zip["zip"]] = total_new_population(zip["zip"])
    
    return radial_populations


import multiprocessing
if __name__ == "__main__":
    # Add this line to ensure proper execution on Windows
    multiprocessing.freeze_support()
    
    num_processes = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(processes=num_processes)
    
    
    # t1 = threading.Thread(target=collect_info, args=(0, 5))
    # t2 = threading.Thread(target=collect_info, args=(6, 10))
    results = pool.starmap(get_populations, [(0, 4223), (4223*1, 4223*2), (4223*2, 4223*3), (4223*3, 4223*4), (4223*4, 4223*5), (4223*5, 4223*6), (4223*6, 4223*7), (4223*7, 33788)])
    
    pool.close()
    pool.join()
    
    corresponding_zipcodes = {k: v for d in results for k, v in d.items()}
    
    exported = pd.DataFrame(corresponding_zipcodes.values(), index=corresponding_zipcodes.keys())
    exported.to_csv("radial_populations.csv")