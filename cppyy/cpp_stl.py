import cppyy

std = cppyy.gbl.std

v = std.vector[int]()

for i in range(10):
    v.push_back(i)

print(f"Vector type is  : {type(v)=}")
print(f"Vector contents : {list(v)=}")
print(f"Vector size.    : {v.size()=}")
print(f"Vector capacity : {v.capacity()=}")
print(f"Vector dir      : {[i for i in dir(v) if not i.startswith('_')]}")