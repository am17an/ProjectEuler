a = [0 for i in range(11)]
b = [0 for i in range(11)]

dx = [0,1,0,-1]
dy = [1,0,-1,0]

d = {}

#this returns a transform tuple of the kind (x,y,z,t) where we transform our current direction by x,y,z 
def calculate(n, who, D):
    global d
    res = [0,0,D,0]
    if n == 0:
        return res
    if (n,who,D) in d:
        return d[(n,who,D)]
    if who == 0:
        fr = calculate(n-1,who,D)
        res[0],res[1],res[2],res[3] = (res[0]+fr[0]),(res[1]+fr[1]),fr[2],res[3]+fr[3]
        res[2] = (res[2]+1)%4
        fr = calculate(n-1,1-who,res[2])
        res[0],res[1],res[2],res[3] = (res[0]+fr[0]),(res[1]+fr[1]),fr[2],res[3]+fr[3]
        res[0] = res[0] + dx[res[2]]
        res[1] = res[1] + dy[res[2]]
        res[3] += 1
        res[2] = (res[2]+1)%4
    else:
        res[2] = (res[2] +3)%4
        res[0],res[1] = res[0] + dx[res[2]],res[1] + dy[res[2]]
        res[3] +=1 
        fr = calculate(n-1,1-who,res[2])
        res[0],res[1],res[2],res[3] = (res[0]+fr[0]),(res[1]+fr[1]),fr[2],res[3] + fr[3]
        res[2] = (res[2] + 3)%4
        fr = calculate(n-1,who,res[2])
        res[0],res[1],res[2],res[3] = (res[0]+fr[0]),(res[1]+fr[1]),fr[2],res[3] + fr[3]
    
    d[(n,who,D)] = res
    return res

#this solves for (x,y) direction d, steps 
astr = "aRbFR"
bstr = "LFaLb"
def solve(x,y,di,steps,st,pos,wht):
    print x,y,di,steps,st,pos,wht
    if steps == 0:
        return (x,y,di)
    if wht[pos] == "a":
        r = calculate(st,0,di)
        if r[3] <= steps:
            return solve(x+r[0],y+r[1],r[2],steps-r[3],st,pos+1,wht)
        else:
            return solve(x,y,di,steps,st-1,0,astr)
    elif wht[pos] == "b":
        r = calculate(st,1,di)
        if r[3] <= steps:
            return solve(x+r[0],y+r[1],r[2],steps-r[3],st,pos+1,wht)
        else:
            return solve(x,y,di,steps,st-1,0,bstr)
    elif wht[pos] == 'R':
        di = (di+1)%4
    elif wht[pos] == 'L':
        di = (di+3)%4
    elif wht[pos] == 'F':
        x += dx[di]
        y += dy[di]
        steps -=1
    return solve(x,y,di,steps,st,pos+1,wht)

print solve(0,1,0,10**12 -1,50,0,"a")
