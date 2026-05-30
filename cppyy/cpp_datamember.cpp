import cppyy

cpp_code = """
class Person {
public:
    Person(const std::string& n) : name(n) {}

    std::string name;
};
"""

cppyy.cppdef(cpp_code)

p = cppyy.gbl.Person("Anubhav")
print(f"Person's first name is: {p.name}")

p.name = "Vahbuna"
print(f"Person's new name is: {p.name}")