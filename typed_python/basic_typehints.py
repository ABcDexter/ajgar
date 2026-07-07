############################
# Try with variadic function
############################

def add_n_numbers(*args: int, **kwargs: int) -> int:         
    # NOTE : Python internally bundles these to: args = tuple[int, ...] and kwargs = dict[str, int], further read https://peps.python.org/pep-0484/#arbitrary-argument-lists-and-default-argument-values
    '''
    Adds n numbers and return the sum
    '''
    print(f"{args=} {type(args)=} {kwargs} {type(kwargs)}")
    for _ in args:
        assert type(_) == int

    sum = 0 
    for i in range(len(args)):
        
        sum += args[i]
    return sum

print(add_n_numbers(1,2,3,4,5,6,7,8,9)) # works fine

print(add_n_numbers('0', '1')) #fails with Assertion Erorr