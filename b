fn add(a, b)     
   return a + b     
end     
     
a = 10 * add(3,add(2,add(1,1)))     
     
b = add(1,1)     
c = add(2,b)     
d = add(3,c)     
e = 10 * d     
     
out("a ", a)     
out("e ", e)     
out("x ", 10 * add(3,add(2,add(1,1))))

Z = add(1,1) + add(2,3)
out("Z ", Z)
