"""
Example: override C++ virtual methods in Python using cppyy.

Run with: python3 cpp_override_example.py

If cppyy is not installed: pip install cppyy
"""
import time
import cppyy

cpp_code = '''
#include <iostream>
#include <string>

class Base {
public:
    Base() {}
    virtual ~Base() {}
    // a non-pure virtual method with default implementation
    virtual void greet() {
        std::cout << "C++ Base::greet()" << std::endl;
    }
    // a pure virtual method that Python must override
    virtual std::string who() const = 0;
};

// A small concrete C++ subclass so we can instantiate from C++ side
// and demonstrate dispatch to a C++ implementation.
class CppDerived : public Base {
public:
    CppDerived(const std::string &name) : _name(name) {}
    virtual ~CppDerived() {}
    void greet() override {
        std::cout << "C++ CppDerived::greet() from " << _name << std::endl;
    }
    std::string who() const override {
        return _name;
    }
private:
    std::string _name;
};

// helper functions to call from Python/C++ to demonstrate dispatch
void call_greet(Base* b) {
    if (b) b->greet();
}

std::string call_who(Base* b) {
    if (b) return b->who();
    return std::string("<null>");
}
'''

# Use cppdef to provide the C++ definitions to cppyy
cppyy.cppdef(cpp_code)

# Grab references to the C++ symbols
Base = cppyy.gbl.Base
call_greet = cppyy.gbl.call_greet
call_who = cppyy.gbl.call_who
CppDerived = cppyy.gbl.CppDerived

class PyDerived(Base):
    """Python subclass of the C++ Base class.

    Overriding greet (non-pure) and who (pure virtual).
    When passed into C++ functions that call virtual methods, these
    Python overrides will be dispatched.
    """
    def __init__(self, name: str):
        super().__init__()
        self._name = name

    def greet(self):
        # This will be called if C++ calls b->greet() when b points to this object
        print(f"Python override: Hello from {self._name}!")

    def who(self) -> str:
        return self._name


def main():
    def separator():
        print(f"{'#'*70}")
    
    def half_second_pause():
        time.sleep(0.5)

    def one_second_pause():
        time.sleep(1)

    print("Creating a concrete C++ derived object and calling greet() and who():")
    # Base is abstract (has a pure virtual who()), so we cannot instantiate it from Python.
    # Use the concrete C++ subclass CppDerived instead.
    b_cpp = CppDerived("Bob")
    b_cpp.greet()  # calls C++ CppDerived::greet()
    print('CppDerived::who() returns:', call_who(b_cpp))
    separator()
    one_second_pause()
    

    print("Creating Python-derived object...")
    d = PyDerived("Alice")
    print("Calling greet() from Python:")
    half_second_pause()  # just to separate output visually
    d.greet()
    
    separator()
    one_second_pause()
    print("Calling call_greet(d) from C++ (should dispatch to Python override):")
    half_second_pause()
    call_greet(d)
    separator()
    one_second_pause()

    print("Calling call_who(d) from C++ (returns string from Python override):")
    half_second_pause()
    print('call_who returned:', call_who(d))


if __name__ == '__main__':
    main()
