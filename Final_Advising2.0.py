import pandas as pd
import itertools as it
import requests
from bs4 import BeautifulSoup
import sys
sys.stdin = open("inputf.txt", 'r')
sys.stdout = open("outputf.txt",'w')

dict= {
    "Time" : ["08:00", "09:30", "11:00", "12:30","02:00","03:30", "05:00"],
    "saturday" : ["","","","","","",""],
    "sunday" : ["","","","","","",""],
    "monday" : ["","","","","","",""],
    "tuesday" : ["","","","","","",""],
    "wednesday" : ["","","","","","",""],
    "thursday" : ["","","","","","",""]
}
df=pd.DataFrame(dict)

def all_clear():
    for i in range(7):
        df["saturday"][i]=""
        df["sunday"][i]=""
        df["monday"][i]=""
        df["tuesday"][i]=""
        df["wednesday"][i]=""
        df["thursday"][i]=""


def add(li,sec=''):
        # print(li)
        if df[li[1]][li[2]]=="":
            df[li[1]][li[2]]=li[0]+" "+sec
        else:
            clash=True
            return clash

def cle(li):
    if li[1]=="sa": li[1]="saturday"
    elif li[1]=="su": li[1]="sunday"
    elif li[1]=="mo": li[1]="monday"
    elif li[1]=="tu": li[1]="tuesday"
    elif li[1]=="we": li[1]="wednesday"
    elif li[1]=="th": li[1]="thursday"

    if li[2]=="08:00": li[2]=0
    elif li[2]=="09:30": li[2]=1
    elif li[2]=="11:00": li[2]=2
    elif li[2]=="12:30": li[2]=3
    elif li[2]=="02:00": li[2]=4
    elif li[2]=="03:30": li[2]=5
    elif li[2]=="05:00": li[2]=6

def cls_ck_day(day):
    for i in range(7):
        if df[day][i]!="":
            return False
        
def total_c_count():
    c=0
    for i in range(7):
        if df["saturday"][i]!="":
            c+=1
        if df["sunday"][i]!="":
            c+=1
        if df["monday"][i]!="":
            c+=1
        if df["tuesday"][i]!="":
            c+=1
        if df["wednesday"][i]!="":
            c+=1
        
        if df["thursday"][i]!="":
            c+=1
            
    return c
    

    
    
    


url = "https://admissions.bracu.ac.bd/academia/admissionRequirement/getAvailableSeatStatus"
content=requests.get(url)
html=content.content
soup=BeautifulSoup(html,"html.parser")


cl,sl,tl=[],[],[]
course_name=soup.find_all(["td"],style="text-align: center; width: 100px")
for i in course_name: cl.append(i.get_text())

course_sec=soup.find_all(["td"],style="text-align: center; width: 69px;")
for i in course_sec: sl.append(i.get_text())

course_time=soup.find_all(["td"],style="text-align: center; width: 290px;")
for i in course_time: tl.append(i.get_text())


s_course,s_sec,s_time=[],[],[]
course_number=input()
for b in range(int(course_number)):
    course=input()
    for i in range(len(cl)):
        if cl[i]==course:
            s_course.append(cl[i])
            s_sec.append(sl[i])
            s_time.append(tl[i])
        
#------ Making Dict from the list ------------
# aikhane akta cource er against ee list akare time deya ase.. 4 ta time hoole 4 ta time ee list akare deya ase.




dic={}
for i in s_course:
    if i not in dic:
        dic[i]=[]
for i in range(len(s_course)):
    dic[s_course[i]].append(s_time[i])

# print(dic)
# -------- Clear the dict time ---------
# aikhane time gula k just thik kore hoise jeno easyly oi gula dora jay.
new_dic={}
for k,v in dic.items():
    new_dic[k]=[]
    for i in v:
        new=i.split(") ")
        s=""
        for h in new:
            day=h[:2].lower()
            time=h[3:8]
            s+=day+time+" "
        new_dic[k].append(s)

# print("New Dict : ",new_dic)
#--------- Make all the combination ---------
# 4 ta couse taple hisebe just time gulo ase
allNames=[]
for k in new_dic.keys(): allNames.append(k)

# print("All Names : ",allNames)
combinations = it.product(*[new_dic[Name] for Name in allNames])
sor=list(combinations)
# for i in range(len(sor)):
#     print(sor[i])
# print(sor)


noClash = True

comb = 0
for p in range(len(sor)):

    
    # if p==10000: break
    c=0
    sec_list=[]
    for j in range(len(sor[p])):
        section=str(new_dic[allNames[j]].index(sor[p][j])+1)
        
        if int(section)<10: section="0"+section
        course=allNames[j]
        sec_list.append(section)
        
        # print(course,section)

        c+=1
        for i in range(len(cl)):
            status=False
            
            if cl[i]==course:
                
                if sl[i]==section:
                    # print(cl[i],sl[i])
                    new=tl[i].split(') ')
                    for r in new:
                        day=r[:2].lower()
                        time=r[3:8]
                        fl=[course,day,time]
                        # print(fl)
                        cle(fl)
                        status=add(fl)
                        # print("--------->",status)
                        if status==True:
                            
                            noClash = False
                            # print("----- XXXXXXX ------ There is a clash ----- XXXXXX-----")
                            break
                        else:
                            noClash = True
                            
                    if (noClash == False):
                        # all_clear()
                        break          
            
        
        if c==int(course_number):   
            if (noClash == True):
                
                # print("Check Class : ",cls_ck_day("saturday"))
                # if cls_ck_day("saturday")==None and cls_ck_day("thursday")==None:
                if total_c_count()==12:
                    
                    if cls_ck_day("saturday")==None and cls_ck_day("thursday")==None:
                        comb+=1
                        print("\nCombination : ",comb)
                        for g in range(4):
                            print(allNames[g], sec_list[g])
                        print()
                        print(df)
                        # print("---------->  ",total_c_count(),"   <------------")
            all_clear()
            break
    
# else:
#     print("------------------------")
#     print("| No Combination Found |")
#     print("------------------------")