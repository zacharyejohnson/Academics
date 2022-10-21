class intSet(): 
    def __init__(self):
        self.set = {}
        self.size = 0

    def insert(self, element):
        if element not in self.set: 
            self.set.update(element) 
        else: 
            print("Element is already in set!")

    def remove(self, element): 
        if element in self.set: 
            self.set.remove(element)

    def isMember(self, element): 
        return element in self.set

    def __str__(self): 
        string = "{" + [f"{item}, " for item in self.set()] + "}"
        return string

    def isSubset(self, subset):
        result = True
        for element in subset: 
            if element not in self.set: 
                result = False
            else: 
                continue

        return result 

    def intersect(self, set): 
        return self.set.intersect(set) 

    def union(self, set):
        return self.set.union(set)

    def diff(self, set): 
        return self.set.difference(set)



