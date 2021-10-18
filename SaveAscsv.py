import csv
import os
import re
from difflib import Differ


def isEnglish(line):
    words = re.split(r'[,.?\s]\s*', line.strip())
    if (len(words) < 4):
        return False
    for word in words[:-1]:
        if (not word.isalnum()):
            return False
    return True


def diff(list1, list2):
    d = Differ()
    differlist = list(d.compare(list1, list2))
    index = []
    deleted = []
    added = []
    i = 0
    del_tmp_len = 0
    add_tmp_len = 0
    print(differlist)
    state = 0  # 0 is nothing different  1 is nothing to different 2 is in different 3 is different to after

    for line in differlist:
        if (state == 0):
            if (line.startswith(' ')):
                i += 1
            if (line.startswith('-')):
                index.append(i)
                i += 1
                state = 1
                del_tmp_len = 1
                add_tmp_len = 0
            if (line.startswith('+')):
                index.append(i)
                state = 1
                del_tmp_len = 0
                add_tmp_len = 1
        elif (state == 1):
            if (line.startswith('-')):
                del_tmp_len += 1
                i += 1
            if (line.startswith('+')):
                add_tmp_len += 1
            if (line.startswith(' ')):
                i += 1
                state = 0
                deleted.append(del_tmp_len)
                added.append(add_tmp_len)
    if (state == 1):
        deleted.append(del_tmp_len)
        added.append(add_tmp_len)
    return [index, deleted, added]


def main2():
    projectlist = os.listdir('/home/opc/MLDATA/SPLITTED_PREPROCESS')
    csvfile = open('result1000new.csv', 'w')
    writer = csv.writer(csvfile, delimiter='@')
    writer.writerow(['id', 'buggy_code', 'patched_code', 'index', 'removed', 'added'])
    x = 0
    for project in projectlist:
        print(project)
        filelist = os.listdir('/home/opc/MLDATA/SPLITTED_PREPROCESS/' + project)
        print(len(filelist))
        for filename in filelist:
            x += 1
            if (x > 10000):
                # csvfile.close()
                exit()
                pass
            try:
                bug = list()
                header = filename.split('_')[0]
                id = filename.split('#')[0]
                bug.append(bug)
                # Before
                path = '/home/opc/MLDATA/SPLITTED_PREPROCESS/' + project + '/' + header + '_before.c'
                f = open(path)
                lines = f.readlines()
                beforecodelist = list()
                for line in lines:
                    if (not (line.strip().startswith('#') or line.strip().startswith('*') or
                             line.strip() == '')):
                        beforecodelist.append(line)
                f.close()

                # After
                path = '/home/opc/MLDATA/SPLITTED_PREPROCESS/' + project + '/' + header + '_after.c'
                f = open(path)
                lines = f.readlines()
                aftercodelist = list()
                for line in lines:
                    if (not (line.strip().startswith('#') or line.strip().startswith('*') or line.strip() == '')):
                        aftercodelist.append(line)
                f.close()
                throw1 = False
                throw2 = False
                for line in beforecodelist:
                    isEng = isEnglish(line)
                    if (isEng):
                        throw1 = True
                        break
                if (not throw1):
                    for line in aftercodelist:
                        isEng = isEnglish(line)
                        if (isEng):
                            throw2 = True
                            break
                if (throw1 | throw2):
                    # pass
                    raise Exception

                # find bug location
                buglocation = diff(beforecodelist, aftercodelist)

                # write into csv file
                beforecode = ''
                aftercode = ''

                for i in range(len(beforecodelist)):
                    beforecode += beforecodelist[i]
                for i in range(len(aftercodelist)):
                    aftercode += aftercodelist[i]
                if (beforecode.strip() == ''):
                    continue
                if (aftercode.strip() == ''):
                    continue
                if (len(buglocation[0]) == 0):
                    continue
                """
                    if(downcode<3):
                        continue
                    if(upcode<3):
                        continue
                    """

                writer.writerow(
                    [id, beforecode, aftercode, str(buglocation[0]), str(buglocation[1]), str(buglocation[2])])
                print(id)
            except:
                pass

    csvfile.close()


if __name__ == "__main__":
    main2()
