import sys
import random as r

class genMap:

    def __init__(self,original,namenf):

        self.original = original
        self.name = namenf

    def generateLayout(self):
        of = open(self.original,'r')
        of.readline()
        nc = int(of.readline().split(' ')[1][:-1])
        nr = int(of.readline().split(' ')[1][:-1])
        pacman_pos = (r.randint(1,nr-2),r.randint(1,nc-2))
        food_pos = (r.randint(1,nr-2),r.randint(1,nc-2))

        while pacman_pos == food_pos:
            food_pos = (r.randint(1,nr-2),r.randint(1,nc-2))
        
        wf = open(self.name,'w+')
        line = ''
        count = 3
        x = 0
        y = 0
        
        with open(self.original,'r') as of:
           for l in of:
                if count > 0:
                    count-=1
                else:
                    for i in range(0,len(l)):
                        if pacman_pos == (x,y): line+='P'
                        elif food_pos == (x,y): line+='.'
                        elif(l[i] == 'T' or l[i] == '@'): line+='%'
                        elif(l[i] == '.'): line+=' '
                        x+=1
                    wf.write(line+'\n')
                    line = ''
                    y+=1
                    x=0

if __name__ == "__main__":
    #First argument: Map you want to conver to lay, Second argument: name of the .lay file
    maps = genMap(sys.argv[1],sys.argv[2])    
    maps.generateLayout()             
