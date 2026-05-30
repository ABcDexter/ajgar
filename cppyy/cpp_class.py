import cppyy

cpp_code = """
class Calculator {
public:
    int multiply(int a, int b) {
        return a * b;
    }
};
"""

cppyy.cppdef(cpp_code)

calc = cppyy.gbl.Calculator()

print(f"Running the Cpp code, the answer is:  {calc.multiply(6, 7)=}")