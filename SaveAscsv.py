import csv
import os
import re
from difflib import Differ
def isEnglish(line):
    words=re.split(r'[,.?\s]\s*', line.strip())
    if(len(words)<4):
        return False
    for word in words[:-1]:
        if(not word.isalnum()):
            return False
    return True


def main2():
    projectlist=os.listdir('/home/opc/MLDATA/SPLITTED_PREPROCESS')
    csvfile=open('result1000new.csv','w')
    writer=csv.writer(csvfile,delimiter='@')
    writer.writerow(['id','buggy_code','patched_code','index','removed','added'])
    x=0
    for project in projectlist:
        print(project)
        filelist = os.listdir('/home/opc/MLDATA/SPLITTED_PREPROCESS/'+project)
        print(len(filelist))
        for filename in filelist:
            x+=1
            if(x>10000):
                #csvfile.close()
                exit()
                pass
            try:
                    bug=list()
                    header=filename.split('_')[0]
                    id = filename.split('#')[0]
                    bug.append(bug)
                    #Before
                    path='/home/opc/MLDATA/SPLITTED_PREPROCESS/'+project+'/'+header+'_before.c'
                    f=open(path)
                    lines=f.readlines()
                    beforecodelist=list()
                    for line in lines:
                        if(not(line.strip().startswith('#') or line.strip().startswith('*') or 
line.strip()=='')):
                            beforecodelist.append(line)
                    f.close()


                    #After
                    path='/home/opc/MLDATA/SPLITTED_PREPROCESS/'+project+'/'+header+'_after.c'
                    f=open(path)
                    lines=f.readlines()
                    aftercodelist=list()
                    for line in lines:
                        if (not (line.strip().startswith('#') or line.strip().startswith('*') or line.strip() 
== '')):
                            aftercodelist.append(line)
                    f.close()
                    throw1=False
                    throw2=False
                    for line in beforecodelist:
                        isEng=isEnglish(line)
                        if(isEng):
                            throw1=True
                            break
                    if(not throw1):
                        for line in aftercodelist:
                            isEng=isEnglish(line)
                            if(isEng):
                                throw2=True
                                break
                    if(throw1|throw2):
                        #pass
                        raise Exception


                    #find bug location
                    length1=len(beforecodelist)
                    length2=len(aftercodelist)
                    length=length1
                    index=0

                    if(length2<length1):
                        length=length1
                    for i in range(length):
                        if(beforecodelist[i].strip()!=aftercodelist[i].strip()):
                            index=i
                            break

                    #find the length of bug
                    d = Differ()
                    differlist=list(d.compare(beforecodelist,aftercodelist))
                    downcode=0
                    upcode=0
                    for s in differlist:
                        if(s.strip().startswith('-')):
                            downcode+=1
                        elif(s.strip().startswith('+')):
                            upcode+=1
                    #write into csv file
                    beforecode = ''
                    aftercode = ''

                    for i in range(len(beforecodelist)):
                        beforecode+=beforecodelist[i]
                    for i in range(len(aftercodelist)):
                        aftercode+=aftercodelist[i]
                    if (beforecode.strip() == ''):
                        continue
                    if (aftercode.strip() == ''):
                        continue
                    if(index==0):
                        continue
                    if(downcode<3):
                        continue
                    if(upcode<3):
                        continue



                    writer.writerow([id,beforecode,aftercode,str(index),str(downcode),str(upcode)])
                    print(id)
            except:
                pass

    csvfile.close()




main2()
