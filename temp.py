class A:
    i=0

class B:
    j=0

class C:
    k=0

class ABC(A,B,C):
    d=0

    def __init__(self,w,x,y,z):
        self.i=w
        self.j=x
        self.k=y
        self.d=z

    def __str__(self):
        return "{0} {1} {2} {3} ".format(self.i,self.j,self.k,self.d)

alpha=[]

for i in range (0,4):
    alpha.append(ABC(i,i,i,i))

for i in range (0,4):
    print alpha[i]
