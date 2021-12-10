class Raum:
    def __init__(self,v,w,a,s,d):
        self.value = v
        self.next = d
        self.before = a
        self.above = w
        self.under = s
    def toString(self):
        return self.value
    
class ZA_WARUDO:
    def __init__(self):
        self.__root = None
    def isEmpty(self):
        return self.__root==None
    def append(self,v):
        h = Node(v,None)
        if self.__root==None:
            self.__root = h
        else:
            hilfe = self.__root
            while hilfe.next!=None:
                hilfe = hilfe.next
            hilfe.next = h

    def show(self):
        s = ""
        hroot = self.__root
        if hroot!=None:
            while hroot.next!=None:
                s = s + str(hroot.value) + " , "
                hroot = hroot.next 
            s = s + str(hroot.value)                   
        print(s)

    def delRaum(self,i):
        element=self.__root
        for x in range(i-1):
            element=element.next
            nelement=element.next
        element=self.__root
        for x in range(i-2):
            element=element.next
        element.next=nelement