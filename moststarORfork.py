 # https://api.github.com/search/repositories?l=C&q=stars%3A10000..12000&per_page=100&page=4

import urllib3
import json
import time
import csv
import time
def getList(start,end,language):  #Only first 1000 results will be returned. Limited to Github
    headers={'Authorization':'token ghp_756GkRIJZYT0oSbiGwwzTzarrGAcwE0kl6ec','User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0','Accept':'	text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'}

    http = urllib3.PoolManager(headers=headers)
    result=[]
    for i in range(10):
        if(end==None):
            url = 'https://api.github.com/search/repositories?q=language:'+language+'+stars%3A>' + str(start) + '&per_page=100&page=' + str(i)
        else:
            url='https://api.github.com/search/repositories?&q=language:'+language+'+stars%3A'+str(start)+'..'+str(end)+'&per_page=100&page='+str(i)
        r=http.request('GET',url)
        time.sleep(2.5)
        print(r.status)
        data = json.loads(r.data)
        if(r.status != 200):
            print(data['message'])

        #print(data.keys())
        list=data['items']
        if(len(list)==0):
            break
            return result
        for item in list:
            name=item['html_url']
            star=str(item['watchers'])
            #print(name[19:]+'  '+star)
            add = (name[19:], star)
            x=str(item['language'])
            print('language',x)
            if (add not in result):
                result.append((name[19:], star))
            else:
                break
    return result


def main():
    file=open('starlistc','w')
    writer=csv.writer(file)
    list=getList(12000,None,'C')
    print(list)
    writer.writerows(list)
    interval=100
    for i in range(12000,400,-1*interval):
        end=i
        start=i-interval
        print(start,' ',end)
        list=getList(start,end,'C')
        print(list)
        writer.writerows(list)
    file.close()


main()


