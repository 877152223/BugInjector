import csv
import os
import re
def isEnglish(line):
    words=re.split(r'[,.?\s]\s*', line.strip())
    if(len(words)<4):
        return False
    for word in words[:-1]:
        if(not word.isalnum()):
            return False
    return True


def main2():
    projectlist=os.listdir('/home/ubuntu/MLDATA/SPLITTED_PREPROCESS')
    csvfile=open('result1000+context250.csv','w')
    writer=csv.writer(csvfile,delimiter='@')
    writer.writerow(['id','buggy_code','patched_code','index'])
    x=0
    for project in projectlist:
        print(project)
        filelist = os.listdir('/home/ubuntu/MLDATA/SPLITTED_PREPROCESS/'+project)
        print(len(filelist))
        for filename in filelist:
            x+=1
            if(x>100000000000):
                #csvfile.close()
                #exit()
                pass
            try:
                    bug=list()
                    header=filename.split('_')[0]
                    bug.append(bug)
                    #Before
                    path='/home/ubuntu/MLDATA/SPLITTED_PREPROCESS/'+project+'/'+header+'_before.c'
                    f=open(path)
                    lines=f.readlines()
                    beforecodelist=list()
                    for line in lines:
                        if(not(line.strip().startswith('#') or line.strip().startswith('*') or line.strip()=='')):
                            beforecodelist.append(line)
                    f.close()


                    #After
                    path='/home/ubuntu/MLDATA/SPLITTED_PREPROCESS/'+project+'/'+header+'_after.c'
                    f=open(path)
                    lines=f.readlines()
                    aftercodelist=list()
                    for line in lines:
                        if (not (line.strip().startswith('#') or line.strip().startswith('*') or line.strip() == '')):
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
                        raise Exception


                    #find bug location
                    length1=len(beforecodelist)
                    length2=len(aftercodelist)
                    length=length1
                    index=0
                    SURROUNDING=10

                    if(length2<length1):
                        length=length1
                    for i in range(length):
                        if(beforecodelist[i].strip()!=aftercodelist[i].strip()):
                            index=i
                            break

                    #write into csv file
                    '''
                    if(index>=SURROUNDING):
                        beforecodelist=beforecodelist[index-SURROUNDING:]
                        aftercodelist=aftercodelist[index-SURROUNDING:]
                    beforecode = ''
                    aftercode = ''
                    beforebug=''
                    count1=0
                    count2 = 0
                    for i in range(len(beforecodelist)):
                        if(i<index):
                            beforebug+=beforecodelist[i]
                        else:
                            count1+=1
                            beforecode+=beforecodelist[i]
                    for i in range(len(aftercodelist)):
                        if(i<index):
                            pass
                        else:
                            count2+=1
                            aftercode+=aftercodelist[i]
                    '''
                    beforecode = ''
                    aftercode = ''
                    index=0
                    length1 = len(beforecodelist)
                    length2 = len(aftercodelist)
                    length = length1
                    if (length2 < length1):
                        length = length1
                    for i in range(length):
                        if(beforecodelist[i].strip()!=aftercodelist[i].strip()):
                            index=i
                            break
                    for i in range(len(beforecodelist)):
                        beforecode+=beforecodelist[i]
                    for i in range(len(aftercodelist)):
                        aftercode+=aftercodelist[i]
                    if (beforecode.strip() == ''):
                        continue
                    if (aftercode.strip() == ''):
                        continue
                    if(count2>3):
                        continue
                    if(count1>3):
                        continue
                    if(len(beforebug)<250):
                        continue

                    writer.writerow([id,beforecode,aftercode,str(index)])
                    print(id)
            except:
                pass

    csvfile.close()



print(33)
main2()