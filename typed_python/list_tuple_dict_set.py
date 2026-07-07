##########################################
# Basic Type Hints in Python on containers
##########################################

# NOTE lists are mutable
def combine_two_lists(l1: list[int], l2:list[int]) -> list[int]: 
    '''
    Combined integers of two lists and return a single list
    '''
    print(f"{l1} at {hex(id(l1))}")
    l1.extend(l2) 
    print(f"returning a f{type(l1)} with address {hex(id(l1))}")
    return l1

print(combine_two_lists([3,1,4], [1,5,9,2,6,5,3,5,8,9,7,9])) 

print(f"{'#'*50}")
# NOTE Tuples are immutable
def combine_two_tuples(t1: tuple[int], t2:tuple[int]) -> tuple[int]:
    '''
    Combined integers of two tuples and return a single tuple
    '''
    new_tuple = t1 + t2
    print(f"returning a f{type(t1)}")
    return new_tuple

print(combine_two_tuples((3,1,4), (1,5,9,2,6,5,3,5,8,9,7,9))) 

print(f"{'#'*50}")
# NOTE Dictionaries are mutable
def combine_two_dicts(d1: dict[str, int], d2:dict[str, int]) -> dict[str, int]: 
    '''
    Combined integers of two dictionaries and return a single dictionary
    '''
    print(f"{d1} at {hex(id(d1))}")
    d1.update(d2) 
    print(f"returning a f{type(d1)} with address {hex(id(d1))}")
    return d1

print(combine_two_dicts({"a": 1, "b": 2}, {"c": 3, "d": 4}))    

print(f"{'#'*50}")
# NOTE Sets are mutable
def combine_two_sets(s1: set[int], s2:set[int]) -> set[int]:
    '''
    Combined integers of two sets and return a single set
    '''
    print(f"{s1} at {hex(id(s1))}")
    s1.update(s2) 
    print(f"returning a f{type(s1)} with address {hex(id(s1))}")
    return s1   

print(combine_two_sets({1, 2, 3}, {4, 5, 6}))