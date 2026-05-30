import cppyy

cpp_code = """
class A {
    public:
        A(int i=42) : m_int(i) {}
        int m_int;
        
};
"""

cppyy.cppdef(cpp_code)

from cppyy.gbl.std import cout, endl, vector
from cppyy.gbl import A

v = vector(A)(10)

print(f"Running the Cpp code, the answer is:  {v[0].m_int}")