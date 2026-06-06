import cppyy

cpp_code = """
class Person {
public:
    Person(const std::string& n) : name(n) {}

    std::string getName() const { 
        return name; 
    }
    void setName(const std::string& n) { 
        name = n; 
    }
        
private:
    std::string name;
};
"""

cppyy.cppdef(cpp_code)

p = cppyy.gbl.Person("Anubhav")
print(f"Person's first name is: {p.getName()}")

p.setName("Vahbuna")
print(f"Person's new name is: {p.getName()}")