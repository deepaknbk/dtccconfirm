import os
import pandas as pd 
import time
import psutil
import psutil
import mail
import json 

#Output file 
df = pd.DataFrame([], columns = ['Participant ID', 'Participant Name','File Type','Status'])

#Reding input data files using command prompt 
os.chdir('D:\Problem\Automation Effort\ConfirmEmail\Input Files')
cmd="dir"
d=os.popen(cmd)
inputFiles=d.read()
input_data=[]
for file_name in inputFiles.split("\n"):
    if file_name !='':
        if file_name[0] != ' ' and file_name.find("<DIR>") == -1:
            input_data.append(file_name)

#Populating Participant ID,File Type Feilds in Output file from input data files
data=[]
for i in input_data:
    temp=i.strip().split(" ")
    file_name=temp[len(temp)-1]
    cmd="type "+file_name
    d=os.popen(cmd)
    dd=d.read().split("\n")
    temp=file_name[14:19]
    
    if temp.strip() == '46027':
        df = df.append(pd.Series([dd[2].strip()[3:7],dd[0].strip(),dd[2].strip()[31:34],''], index=df.columns ), ignore_index=True)
    if temp.strip() == '46029':
        df = df.append(pd.Series([dd[2].strip()[3:7],dd[0].strip(),'COM',''], index=df.columns ), ignore_index=True)    
    if temp.strip() == '46030':
        df = df.append(pd.Series([dd[2].strip()[3:7],dd[0].strip(),'FAR',''], index=df.columns ), ignore_index=True)
    data.append(dd[0])
    
nrow_output = len(df)


#Reading Response Files of input files
os.chdir('D:\Problem\Automation Effort\ConfirmEmail\Result Files')
cmd="dir"
d=os.popen(cmd)
result_Files=d.read()
result_data=[]
for file_name in result_Files.split("\n"):
    if file_name !='':
        if file_name[0] != ' ' and file_name.find("<DIR>") == -1:
            result_data.append(file_name)

#Populating  Status Field in Output file from Response data files
for i in result_data:
    temp=i.strip().split(" ")
    file_name=temp[len(temp)-1]
    cmd="type "+file_name
    d=os.popen(cmd)
    dd=d.read()
    for j in data:
        if dd.find(j.strip()) != -1:
            temp_var=[val for val in dd.split("\n") if val.strip()!=""]
            temp_index=df.index[df['Participant Name'] == j.strip()]
            df.loc[temp_index, 'Status'] = temp_var[len(temp_var)-1].strip()


#Generating Temprory Participant Names and writing into participantNames.json file
participantNames = {}
for index in range(8):
    pName = 'Participant'+ str(index)
    participantNames[index] = pName
result = json.dumps(participantNames) 
os.chdir('D:\Problem\Automation Effort\ConfirmEmail\Output Files')
f= open("participantNames.json","w+")
f.write(result)
f.close()

#Populating Participant Names Field in output file from participantNames.json file
with open('participantNames.json') as json_file: 
    participantNames = json.load(json_file) 

for index in range(8):
    df.loc[index, 'Participant Name'] = participantNames.get(str(index))
    

#Converting Data Frame to output File
df.to_csv('D:\Problem\Automation Effort\ConfirmEmail\Output Files\output.csv')          
            
#Sending mail
os.chdir('D:\Problem\Automation Effort\ConfirmEmail\Solution')
mail.send_status()