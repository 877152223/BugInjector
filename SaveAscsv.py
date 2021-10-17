

def cut(buggycode,location,deleted):
    before=location
    after=location+deleted
    backetCount=[0,0,0] # index 0 is [], two is (),three is {},positive means left more than right, negative means right more then left.
    scope=True
    for code in buggycode[before:after]:
        count(code,backetCount)
    while((backetCount[0]!=0 or backetCount[1]!=0 or backetCount[2]!=0) and scope):
        if(backetCount[0]>0 or backetCount[1]>0 or backetCount[2]>0):
            after+=1
            count(buggycode[after-1],backetCount)
        if(backetCount[0]<0 or backetCount[1]<0 or backetCount[2]<0):
            before-=1
            count(buggycode[before],backetCount)
        if(before<0):
            raise Exception('Out of Scope. Before')
        if(after>len(buggycode)):
            raise Exception('Out of Scope. After')

    return [before,after]





def count(code,backetCount):
    for char in code:
        if (char == '['):
            backetCount[0] += 1
        elif (char == ']'):
            backetCount[0] -= 1
        elif (char == '('):
            backetCount[1] += 1
        elif (char == ')'):
            backetCount[1] -= 1
        elif (char == '{'):
            backetCount[2] += 1
        elif (char == '}'):
            backetCount[2] -= 1

def main():
    file=open('/Users/zhipengzhang/testcode')
    lines=file.readlines()
    result=cut(lines,3,4)





if __name__=='__main__':
    main()

