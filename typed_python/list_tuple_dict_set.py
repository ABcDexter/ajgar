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