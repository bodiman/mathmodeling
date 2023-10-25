import pandas as pd
from scipy.spatial import distance

df = pd.read_csv("uzips.csv")
df = df[["zip", "lat", "lng"]]

"""
Algorithm will take in a radius

1. Loop through ll zip codes
    2. for each zip code, track zip codes within r miles
"""

r_miles = 100
r = 1/69.1 * r_miles

def collect_info(startindex, stopindex):
    corresponding_zipcodes = {}
    for index1, row1 in df.iterrows():
        if index1 < startindex:
            continue
        if index1 > stopindex:
            break

        zipcodes = []
        for _, row2 in df.iterrows():
            if (row1["lat"] - row2["lat"])**2 + (row1["lng"] - row2["lng"])**2 < r**2:
                zipcodes.append(str(row2["zip"]))
        
        corresponding_zipcodes[row1["zip"]] = ",".join(zipcodes)
        print(index1)
    return corresponding_zipcodes

import threading
import multiprocessing

# print(multiprocessing.cpu_count())
if __name__ == "__main__":
    # Add this line to ensure proper execution on Windows
    multiprocessing.freeze_support()

    num_processes = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(processes=num_processes)


    # t1 = threading.Thread(target=collect_info, args=(0, 5))
    # t2 = threading.Thread(target=collect_info, args=(6, 10))
    results = pool.starmap(collect_info, [(0, 4223), (4223*1, 4223*2), (4223*2, 4223*3), (4223*3, 4223*4), (4223*4, 4223*5), (4223*5, 4223*6), (4223*6, 4223*7), (4223*7, 33788)])

    pool.close()
    pool.join()
    
    corresponding_zipcodes = {k: v for d in results for k, v in d.items()}
    
    exported = pd.DataFrame(corresponding_zipcodes.values(), index=corresponding_zipcodes.keys())
    exported.to_csv("radial_zipcodes.csv")