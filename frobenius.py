'''Frobenius primality test. See details in arXiv:1807.07249 [math.NT]:
       Evaluation of the Effectiveness of the Frobenius Primality Test.
       (c)Sergei Khashin khash2@gmail.com
   This is a probabilistic method.
   The numbers on which it is wrong are called Frobenius pseudoprimes (FPP).
   Have been proved:
   a) There are no FPP < 2^64.
   b) There are many other limitations on FPP.
   c) There is no known FPP at all.
   There is a hypothesis that FPP does not exist at all.

   Example of usage see at the end of the file.
'''
#---- Jacobi symbol -----------------------------------------------------------
def Jacobi(a,b):
    if b<=1 or (b%2)==0: return 0;
    res = 1
    if a<0:
        if b%4==3: res=-1; 
        a = -a
    if a>=b: a=a%b;
    while True:
        if a==0: return 0;
        # now 1 <=a < b, b odd, ---------------
        while a%4 ==0: a//=4;
        if a%4==2 :  
            b8 = b%8
            if b8==3 or b8==5: res = -res
            a = a//2
        if a==1: return res
        # now 1 < a < b, a,b odd, -------------
        # J(a,b) -> J(b,a) --------------------
        if a%4==3 and b%4==3 : res = -res;
        t=b; b=a; a=t%a;

#------------------------------------------------------------------------------
def Frobenius_test(n):
    '''Frobinius primality test. See details in arXiv:1807.07249 [math.NT]:
           Evaluation of the Effectiveness of the Frobenius Primality Test.
           Sergei Khashin.
    '''
    if n<2: return False;
    if n==2 or n==3: return True;
    if n%2==0 or n%3==0: return False;
    # now n%2 !=0, n%3 !=0, n >= 5

    #if is_square(n): return False; ---
    x = 1<<((n.bit_length()+1)//2)
    while True:
        delta = x*x-n
        if delta==0: return False
        if delta< 0: break
        x -= 1+delta//(2*x)
    # now n%2 !=0, n%3 !=0, n >= 5 and n is not a perfect square

    #c = Frob_minC(n);
    c = 0
    if   n%4 == 3    : c=-1
    elif n%8 == 5    : c=2
    elif n%24==17    : c=3
    else:
        c = 5
        while True:
            jcn = Jacobi(c,n)
            if jcn== 0: return False;
            if jcn==-1: break;
            c =c+2
    # c is ready

    a = 1; b=1;
    if c<3: a=2;  
    #a1,b1 = Frob_pow(a,b,c,n,n)
    a1=1; b1=0; a2=a; b2=b; k=n

    while k>0:       
        if k % 2 == 1:                                      # z1 *= z2
            tb = (a1*b2 + a2*b1)%n
            ta = (a1*a2 + b1*b2*c)%n
            a1 = ta
            b1 = tb

        # z2 *= z2
        ta = (a2*a2+c*b2*b2)%n
        b2 = (2*a2*b2)%n;
        a2 = ta

        k>>=1;                                  # k /= 2
    return (a1==a) and (b1==n-b)

#--main------------------------------------------------------------------------
for n in range (3,100,2):
   if Frobenius_test(n): print(n) 
K=10**113+1
for n in range (K,K+1000,2):
   if Frobenius_test(n): print(n) 
#100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000099
#100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000561
#100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000609
#100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000801
input('Press <CR>..')
