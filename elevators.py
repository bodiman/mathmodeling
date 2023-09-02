import torch
from torch.nn.functional import softmax
from torch import tensor

from itertools import permutations, combinations

torch.set_default_dtype(torch.float64)

floors = tensor([1, 2, 3, 4, 5, 6], dtype=torch.float64)
floor_employees = tensor([100, 120, 60, 120, 80, 20], dtype=torch.float64)

def sample_from_positive_ordered_list(tsr, capacity=10):
    #randomly draw from the list with probabilities proportional to the number of people in each category
    
    """
    Algorithm:
    1. softmax to get probabilities
    2. draw intagers proportional to the probabilities
    3. update list numbers based on what is drawn
    """

    cap = min(capacity, tsr.sum())


    probs = tsr / tsr.sum()
    unrounded = cap * probs
    rounded = torch.floor(cap * probs)
    
    missing = int((cap - sum(rounded)).item())
    residual = unrounded - rounded
    idxs = torch.topk(residual, missing).indices
    addlist = torch.tensor([1 if i in idxs else 0 for i in range(len(residual))])
    
    rounded += addlist
    tsr = tsr - rounded

    return tsr, rounded

def highest_non_zero_index(lst):
    highest_index = -1  # Initialize with a value that is not a valid index
    
    for i, value in enumerate(lst):
        if value != 0:
            highest_index = i
    
    return highest_index

def elevator_run_default(floor_employees, time=0):
    time += 15
    floor_employees, sample = sample_from_positive_ordered_list(floor_employees)
    nfloors = highest_non_zero_index(sample) + 1
    for i in range(nfloors):
        time += 5
        if sample[i] != 0:
            time += 10
    
    time += 5 * nfloors

    return floor_employees, time


#sample employees from thing
#stop for employees at each floor
#come down from the maximum floor
def simulation(floor_employees):
    time = 0
    while floor_employees.sum() != 0:
        floor_employees, time = elevator_run_default(floor_employees, time)
        # print(floor_employees, time)
    
    return(floor_employees, time)
    

def create_partial_copy(tensor, indices):
    new_tensor = torch.zeros_like(tensor)  # Create a tensor of zeros with the same shape as the original tensor
    new_tensor[indices] = tensor[indices]  # Set values at specified indices to original values
    return new_tensor

def get_max_index(lst):
    max_value = max(lst)
    max_index = lst.index(max_value)
    return max_index

def grouped_simulation(floor_employees, floors):
    results = []

    combinations = generate_combinations(floors.tolist())
    for combination in combinations:
        times = []
        for group in combination:
            indices = [element - 1 for element in group]
            copy = create_partial_copy(floor_employees, indices)
            times.append(simulation(copy)[1])
            
        if len(times) == 3:
            idx = get_max_index(times)
            times[idx] /= 2
        elif len(times) == 2:
            times[0] /= 2
            times[1] /= 2
        elif len(times) == 1:
            times[0] /= 4

        results.append((combination, max(times)))

    sorted_results = sorted(results, key=lambda x: x[1])
    print(sorted_results)
    """
    basically split up floor_employees into 4 different catagories, 
    run a simulation on each of the categories, and take the maximum time from all simulations.
    
    But wait, it's more complicated than that. You could split it in any way that adds up
    to less than 4.

    1 communal
    1 reserved 3 communal

    etc.

    for each of these possibilities, you need to check all permutations and combinations
    of which elevator is reserved for which group and in what place.

    """


def find_division_combinations(target_sum, max_number, current_sum=0, current_combination=[], combs = []):
    if current_sum == target_sum:
        combs.append(current_combination)
        return current_combination
    if current_sum > target_sum or max_number == 0:
        return
    
    find_division_combinations(target_sum, max_number - 1, current_sum, current_combination.copy(), combs)
    current_combination.append(max_number)
    find_division_combinations(target_sum, max_number, current_sum + max_number, current_combination.copy(), combs)

    return combs



def divide_into_buckets(numbers, bucket_lengths):
    # Check if the sum of bucket lengths is greater than the number of elements
    if sum(bucket_lengths) > len(numbers):
        raise ValueError("Total bucket lengths cannot exceed the number of elements.")

    buckets = []
    start_index = 0
    
    for length in bucket_lengths:
        end_index = start_index + length
        bucket = numbers[start_index:end_index]
        buckets.append(bucket)
        start_index = end_index
    
    return buckets


def generate_combinations(floors):
    collections = []
    arrangements = [list(perm) for perm in permutations(floors)]
    templates = find_division_combinations(6, 6)
    for template in templates:
        if len(template) > 4:
            continue

        for arrangement in arrangements:
            collections.append(divide_into_buckets(arrangement, template))
    
    return collections
                
                


    """
    For template 1, grab all possibilities of 3 and fill in the rest
    For template 2,
        Grab all possibilities of 2
        Then all other possibilities of 2, filtering out repeats
    
    """

    """
    For a list 1-6,

    it should return 

    [1], [2], [3], [4, 5, 6]
    [1], [2], [3, 4], [5, 6]

    etc.

    The basic frames are

    1, 1, 1, 3
    1, 1, 2, 2
    1, 1, 4
    1, 2, 3
    2, 2, 2
    1, 5
    2, 4
    3, 3

    Get all permutation and combinations of the numbers and then split them into these groupings
    But the permutations need to be in 4 buckets
    """

grouped_simulation(floor_employees, floors)

# g1 = tensor([100, 0, 0, 0, 0, 0], dtype=torch.float64)
# g2 = tensor([0, 120, 0, 0, 0, 0], dtype=torch.float64)
# g3 = tensor([0, 0, 60, 120, 0, 0], dtype=torch.float64)
# g4 = tensor([0, 0, 0, 0, 80, 20], dtype=torch.float64)

# print(simulation(g1))
# print(simulation(g2))
# print(simulation(floor_employees))
# print(simulation(g4))