"""
a={
    "data_1":{"id":1,"name":"roja","age":22},
    "data_2":{"id":2,"name":"ravi","age":25}
}

b=map(str,a.values())
b=list(b)
print(b)
"""
"""
a=["10","20","30"]
b=[]
for i in range(0,len(a)):
    b.append(int(a[i]))
print(b)

a=["10","20","30"]

b=map(int,a)
b=list(b)
print(b)

"""

a=[1,2,3,4]
b=map(lambda x: x*x,a)
b=list(b)
print(b)