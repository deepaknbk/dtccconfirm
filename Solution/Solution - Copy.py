import os
import pandas as pd 
import time
import psutil
import psutil
#import mail
import json 

def dtcc_confirm():
    #Output file
    df = pd.DataFrame([], columns = ['Participant ID', 'Participant Name','File Type','Status'])

    #Reding input data files using command prompt
    path=r'C:\Users\User\PycharmProjects\dtccconfirm\Input Files'
    outbound_files=os.listdir(path)
    print('Files:',outbound_files)

    #Populating Participant ID,File Type Feilds in Output file from input data files
    data=[]
    for i in outbound_files:
        temp=i.strip().split(" ")
        file_name=temp[len(temp)-1]
        print('filename:',file_name)
        cmd="type "+file_name
        d=os.popen(cmd)
        dd=d.read().split("\n")
        temp=file_name[14:19]
        print('Temp:',temp)
        if temp.strip() == '46027':
            df = df.append(pd.Series([dd[2].strip()[3:7],dd[0].strip(),dd[2].strip()[31:34],''], index=df.columns ), ignore_index=True)
        if temp.strip() == '46029':
            df = df.append(pd.Series([dd[2].strip()[3:7],dd[0].strip(),'COM',''], index=df.columns ), ignore_index=True)
        if temp.strip() == '46030':
            df = df.append(pd.Series([dd[2].strip()[3:7],dd[0].strip(),'FAR',''], index=df.columns ), ignore_index=True)
        data.append(dd[0])
    print(dd)
    nrow_output = len(df)


    #Reading Response Files of input files
    os.chdir(r'C:\Users\User\PycharmProjects\dtccconfirm\Result Files')
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
    os.chdir(r'C:\Users\User\PycharmProjects\dtccconfirm\Output Files')
    f= open("participantNames.json","w+")
    f.write(result)
    f.close()

    #Populating Participant Names Field in output file from participantNames.json file
    with open('participantNames.json') as json_file:
        participantNames = json.load(json_file)

    for index in range(8):
        df.loc[index, 'Participant Name'] = participantNames.get(str(index))


    #Converting Data Frame to output File
    df.to_csv(r'C:\Users\User\PycharmProjects\dtccconfirm\Output Files\output.csv')

    #Sending mail
    os.chdir(r'C:\Users\User\PycharmProjects\dtccconfirm')
    #mail.send_status()