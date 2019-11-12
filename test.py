import math
print(list (map(math.sqrt,[9,25,36])))

items=[1,2,3,4,5]
def inc(x):return x+1
print(list(map(inc,items)))

print(list(map((lambda x:x+1),items))) # inc by 1

print(list(filter((lambda x:x<4),items))) # filter anything less than 4

def odd(n):return n%2==1
print (list(filter (odd,range(10))))

def even(n):return n%2==0
print (list(filter (even,range(10))))

from functools import reduce
print (reduce(max, [34,32,99,67,10]))

data = [2,3,4,5,6]
print(reduce ((lambda x,y:x-y),items))

x=()
print(type(x))

for i in range (1,6,2): #3rd argument is for increment by +2:
	print(i)

S= [x**2 for x in range(5)]
print(S) 

names = ["name1","name2","name3"]
city = ["c1","c2","c3"]

dict1 = {'name':names, 'cities':city}
print(dict1["name"])
print(len(dict1))


mydata = [20,6,14]
mydata.append(15)
print(mydata)
mydata.insert(1,22)
print(mydata)
d= mydata.pop(2)
print(d)


print("---------------")

dict2 = {"b":20, "a":35}
dict2["b"]= -20
print(dict2)

dict2["c"]=40
dict2.pop("b")

print(dict2)

for k in dict2:
	print(k)