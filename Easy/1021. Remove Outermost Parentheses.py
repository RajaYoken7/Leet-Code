class Solution(object):
    def removeOuterParentheses(self, s):
        op=0
        cl=0
        arr=[]
        hashmap={"(":0 , ")":0}
        ind=1
        i=0
        while(i < len(s)):
            if(s[i]=="("):
                hashmap["("]+=1
            if(s[i]==")"):
                if(hashmap["("]>0):
                    hashmap["("]-=1
            if(hashmap["("]==0 and hashmap[")"]==0):
                arr.append(s[ind:i])
                ind=i+2
            i+=1

        return "".join(arr)
    
