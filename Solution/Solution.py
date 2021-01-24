import os
import collections
import pandas as pd 
import time
import psutil
import psutil
#import mail
import json
import csv

def parse_hdr(hdr):
    region = hdr[4:5]
    sysid = hdr[5:10]
    submitter = hdr[15:20]
    sent_dt = hdr[26:34]
    seq = hdr[59:63]
    return region,sysid,submitter,sent_dt,seq

def parse_outbound_file(file):
    ORecord = collections.namedtuple(
        'ORecord',
        'region,sysid,submitter,sent_dt,seq,participant,file_type,hdr'
    )
    sysid_ref={
        '46029': 'FAR',
        '46030' : 'COM'
    }
    region,sysid,submitter,sent_dt,seq,participant,file_type,hdr,temp_file_type=None,None,None,None,None,None,None,None,None
    with open(file, 'r') as reader:
        # Read and print the entire file line by line
        for line in reader:
            if line[:3]=='HDR':
                region,sysid,submitter,sent_dt,seq=parse_hdr(line)
                hdr=line[:63]

            elif line[:3]=='C12' :
                participant=line[3:7]
                temp_file_type=line[31:34]

            elif line[:3]=='C21' or line[:3]=='C42' :
                participant = line[3:7]
    #print(temp_file_type)

    file_type=sysid_ref.get(sysid,temp_file_type)

    record=ORecord(
        region, sysid, submitter, sent_dt, seq, participant, file_type ,hdr
    )
    return  record

def parse_confirm_file(file):
    CRecord = collections.namedtuple(
        'CRecord',
        'region,sysid,submitter,sent_dt,seq,status,hdr'
    )
    region,sysid,submitter,sent_dt,seq,status,hdr = None, None, None, None, None, None,None

    with open(file, 'r') as reader:
        # Read and print the entire file line by line
        for line in reader:
            if line[5:8]=='HDR':
                region,sysid,submitter,sent_dt,seq=parse_hdr(line[5:])
                hdr=line[5:68]
            elif line.find('ACCEPTED'):
                status='Accepted'
            elif  line.find('REJECTED'):
                status='REJECTED'
    record = CRecord(
        region, sysid, submitter, sent_dt, seq, status ,hdr
    )
    return record

def dtcc_confirm():

    #Reding input data files using command prompt
    outbound_path= 'C:/Users/User/PycharmProjects/dtccconfirm/Input Files/'
    outbound_files=os.listdir(outbound_path)
    confirm_path='C:/Users/User/PycharmProjects/dtccconfirm/Result Files/'
    confirm_files = os.listdir(confirm_path)
    print('Files:',outbound_files)
    print(os.getcwd(),__file__)
    #Populating Participant ID,File Type Feilds in Output file from input data files
    outbound_data=[]
    confirm_data=[]

    dtcc_confirm_data = []
    dtcc_confirm = collections.namedtuple(
        'Dtcc_Confirm',
        'region, file, sent_dt, participant, hdr'
    )

    for file in outbound_files:
        #print(f'Processing outbound file:{outbound_path+file}')
        outbound_record = parse_outbound_file(outbound_path+file)
        outbound_data.append(outbound_record)

    for file in confirm_files:
        #print(f'Processing Confirm file:{confirm_path+file}')
        confirm_record=parse_confirm_file(confirm_path+file)
        confirm_data.append(confirm_record)
    with open('output.csv', mode='w',newline='') as output_file:
        output_writer = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        output_writer.writerow(['region','sysid','submitter','sent_dt','seq','participant','file_type','hdr','status'])
        for orecord in outbound_data:
             for crecord in confirm_data:
                 if orecord.hdr==crecord.hdr:
                        frecord=orecord+(crecord.status,)
                        dtcc_confirm_data.append(frecord)
                        output_writer.writerow(frecord)

    print(dtcc_confirm_data)



