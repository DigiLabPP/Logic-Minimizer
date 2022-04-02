import math
import numpy as np


def Transpose(l):
    l2=list(zip(*l))
    l1=[]
    for i in l2:
        l1.append(list(i))
    return l1


def binary(n,num):
    s=""
    while n>=2:
        s+=str((n%2))
        n//=2
    s+=str(n)
    while len(s)<num:
        s+='0'
    return s[::-1]


def decimal(s):
    d=0
    i=0
    while i in s:
        d*=2
        d+=int(i)
    return d


def adjacency(s1,s2):               #To check the adjacency of two implicants
    num=0
    n=len(s1)
    for i in range(n):          
        if s1[i]!=s2[i]:
            index=i
            num+=1
    adj=True if (num==1 and (s1[index]!="" and s2[index]!="")) else False
    return adj,index


def imp(l):
    n=len(l)
    c=[]
    for i in range(n):
        if l[i]:
            c.append(i)
    return set(c)


def Minimize(minterms,dontcares,num):
    tot=minterms[::]
    tot.extend(dontcares)
    implicants=[]
    mincover=[]
    l1=[]
    l2=[]
    l3=[]
    for i in tot:
        l1.append(binary(i,num))
        l2.append([i])
    n=len(l1)
    ch=1
    while ch:
        ch=0
        for i in range(n-1):
            if l1[i].count('1')>l1[i+1].count('1'):
                l1[i],l1[i+1]=l1[i+1],l1[i]
                l2[i],l2[i+1]=l2[i+1],l2[i]
                ch=1
    while True:
        m1=[]
        m2=[]
        n=len(l1)
        l3=[False]*n            
        i=0
        j=0
        while i<n:
            while j<n :
                if l1[j].count('1')==l1[i].count('1'):          #Constructing the Prime Implicant Table
                    j+=1
                    if j<n:
                        if l1[j].count('1')!=l1[i].count('1'):
                            if l1[j].count('1')==l1[i].count('1')+1:
                                num1=j
                            else:
                                num1=j
                                i=num1
                    else:
                        i=j
                        break
                elif l1[j].count('1')==l1[i].count('1')+1:
                    adj,ind=adjacency(l1[i],l1[j])
                    if adj:
                        l3[i]=True
                        l3[j]=True
                        p=l1[i][:ind:]+"_"+l1[i][ind+1::]
                        if p not in m1:
                            m1.append(p)
                            m=l2[i][::]
                            m.extend(l2[j])
                            m2.append(m)
                    if j+1<n:
                        j+=1
                    else:
                        j=num1
                        i+=1
                else:
                    j=num1
                    i+=1
        num1=0
        for i in range(n):
            if not(l3[i]):
                implicants.append(l1[i])
                mincover.append(l2[i])
                num1+=1
        if num1==n:
            break
        l1=m1[::]
        l2=m2[::]
    ok=False
    implicants.reverse()
    mincover.reverse()
    final=set(minterms)                             #Constructing the Cover Table
    lst=minterms[::]
    for i in range(len(implicants)):
        mincover[i]=list(set(mincover[i])&final)
    l1=[]
    for i in range(len(implicants)):                  
        l0=[]
        for j in range(len(lst)):
            l0.append(lst[j] in mincover[i])
        l1.append(l0)
    minimized=[]
    num1=1
    num2=1
    while num1:
        num1=0
        ch=len(implicants)
        n=len(lst)
        while num2:
            num2=0
            l2=Transpose(l1)
            j=0
            epi=[]
            for num in range(len(lst)):
                if l2[num].count(True)==1:
                    epi.append(lst[num])
            # print("Picking EPIs")
            while epi!=[]:
                # print(j)               #Picking the Essential Prime Implicants
                if epi[0] not in lst:
                    del epi[0]
                    continue
                ind1=lst.index(epi[0])
                i=l2[ind1].index(True)
                a=0
                while a<len(lst):
                    if lst[a] in mincover[i]:
                        del lst[a]
                        del l2[a]
                    else:
                        a+=1
                l1=Transpose(l2)
                minimized.append(implicants[i])
                del implicants[i]
                del mincover[i]
                del epi[0]
                if l1!=[]:
                    del l1[i]
                l2=Transpose(l1)
                j=0
                num2=1
            # print(minimized)
            final=set(lst)
            for i in range(len(implicants)):
                mincover[i]=list(set(mincover[i])&final)
            l2=Transpose(l1) 
            if final!=set():
                ch=1
                while ch:
                    ch=0 
                    for i in range(len(implicants)-1):
                        if l1[i].count(True)<l1[i+1].count(True):
                            l1[i],l1[i+1]=l1[i+1],l1[i]
                            implicants[i],implicants[i+1]=implicants[i+1],implicants[i]
                            mincover[i],mincover[i+1]=mincover[i+1],mincover[i]
                            ch=1
                ch=len(implicants)
                i=ch-1
                while i>0:
                    j=i-1
                    while j>=0:
                        if set(mincover[i])&set(mincover[j])==set(mincover[i]):    #Removing dominated rows
                            s1=set(mincover[j])-set(mincover[i])
                            x=0
                            for m1 in range(len(implicants)):
                                if s1&set(mincover[m1])==s1 and implicants[m1].count('')>=implicants[j].count(''):
                                    x+=1 
                            if x>1 and implicants[i].count('')>implicants[j].count('') and mincover[i]!=[]:
                                del implicants[j]
                                del mincover[j]
                                del l1[j]
                            else:
                                del implicants[i]
                                del mincover[i]
                                del l1[i]
                            num2=1
                            i-=1
                            j=i-1
                            continue
                        j-=1
                    if j==-1:
                        i-=1
                ch=1
                l2=Transpose(l1)
                while ch:
                    ch=0
                    for i in range(len(lst)-1):
                        if l2[i].count(True)>l2[i+1].count(True):
                            l2[i],l2[i+1]=l2[i+1],l2[i]
                            lst[i],lst[i+1]=lst[i+1],lst[i]
                            ch=1
                final=set(lst)
                ch=len(lst)
                i=ch-1
                while i>0:
                    j=i-1
                    while j>=0:
                        if imp(l2[i])&imp(l2[j])==imp(l2[j]):                   #Removing dominating columns
                            del l2[i]
                            del lst[i]
                            num2=1
                            i-=1
                            j=i-1
                            continue
                        j-=1
                    if j==-1:
                        i-=1
                l1=Transpose(l2)
                final=set(lst)
                for i in range(len(implicants)):
                    mincover[i]=list(set(mincover[i])&final)
        if final!=set():
            minimized.append(implicants[0])
            final=final-set(mincover[0])
            lst=list(final)
            del implicants[0]
            del mincover[0]
            del l1[0]
            l2=Transpose(l1)
            num1=1
    return minimized

def simplify(minterms,dontcares,minimal,num,var):
    lim = 2**num
    f_sop=""
    f_pos=""
    min_not=list(set(range(0,lim))-set(minterms)-set(dontcares))
    minimal1=Minimize(min_not,dontcares,num)
    ch=1 
    while ch:
        ch=0 
        for i in range(len(minimal1)-1):
            if minimal1[i].count('')<minimal1[i+1].count(''):
                minimal1[i],minimal1[i+1]=minimal1[i+1],minimal1[i]
                ch=1
    if minimal==[]:
        f_sop+="0"
        f_pos+="0"
    elif minimal[0]=="_"*num:
        f_sop+="1"
        f_pos+="1"
    else:
        num_terms=len(minimal)
        for i in range(num_terms):
            term=minimal[i]
            for j in range(len(term)):
                if term[j]=="_":
                    continue
                else:
                    f_sop+=var[j]
                    if term[j]=="0":
                        f_sop+="'"
            if i<num_terms-1:
                f_sop+=" + "
        for term in minimal1:
            if term.count("_")<num-1 and minimal1!=[term]:
                f_pos+="("
            for j in range(num):
                if term[j]=="_":
                    continue
                else:
                    f_pos+=var[j]
                    if term[j]=="1":
                        f_pos+="'"
                    if j<num-1 and term[j+1::]!=(num-j-1)*"_":
                        f_pos+=" + "
            if term.count("_")<num-1 and minimal1!=[term]:
                f_pos+=")"
    return f_sop,f_pos