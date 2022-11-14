class MyMatrix(): 
    def __init__(self, data, dim): 
        self.data = data 
        self.dim = dim 

        self.rows = dim[0]
        self.cols = dim[1]

        if(self.rows*self.cols != len(data)): 
            print("invalid dimensions")

        self.matrix = []

        i = 0

        for row in range(self.rows):
            row_vector = []
            for col in range(self.cols):
                row_vector.append(data[i])
                i += 1
            self.matrix.append(row_vector)


    def __str__(self): 
        for row in self.matrix: 
            print(row)

    def __add__(self, other): 
        if self.dim == other.dim: 
            # we can take advantage of the fact that a and b both have data vectors for addition
            sum_vector = []
            for j in range(len(self.data)): 
                sum_vector.append( self.data[j] + other.data[j] )

            # then we convert the sum vector into a matrix with same dimensions as a and b 
            sum_matrix = MyMatrix(sum_vector, self.dim)
            return sum_matrix
        else: 
            print("Cannot add matrices whose dimensions do not match")

    def __mult__(self, other): 
        a = self.matrix
        b = other.matrix
        # using list comprehension and zip() function to perform multiplication
        result = [[sum(a*b for a,b in zip(X_row,Y_col)) for Y_col in zip(*b)] for X_row in a]
        #format for repurposing into MyMatrix Object using extend() method 
        return_val = []
        for ele in result: 
            return_val.extend(ele)

        res_mat = MyMatrix(return_val, (self.rows, other.cols))

        return res_mat
        






# tests
mat = MyMatrix([0,1,2,3,4,5,6,7,8], (3,3))
a = MyMatrix([0,1,2,3,4,5,6,7,8], (3,3))
sums = mat.__add__(a)
mults = mat.__mult__(a)
mults.__str__()
sums.__str__()
mat.__str__()