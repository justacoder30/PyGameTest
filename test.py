class Parent:
    def __init__(self, name):
        self.father = name

class Son(Parent):
    def __init__(self, name):
        super().__init__(name)

class Daughter(Parent):
    def __init__(self, daughter):
        self.father = daughter

human = Parent("Joe")
son = Son("Jack")
a = 2
a = son
print(a.father)