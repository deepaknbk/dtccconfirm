import os
import collections
import csv
import zipfile


sysid_ref={
        '46029': 'FAR',
        '46030' : 'COM',
        '26029': 'FAR',
        '26030' : 'COM'
    }


participant_ref={
        '1723' : 'United Bank',
        '0725' : 'Raymond James Insurance Group, Inc.',
        '0443' : 'Pershing',
        '6317'  : 'TD Wealth Management Services, Inc',
        '0122' : 'Test IBD',
        '0987' : 'Def'
    }

outbound_path= 'C:/Users/User/PycharmProjects/dtccconfirm/outbounds/'
confirm_path='C:/Users/User/PycharmProjects/dtccconfirm/confirms/'
output_path='C:/Users/User/PycharmProjects/dtccconfirm/output/'
zip_path='C:/Users/User/PycharmProjects/dtccconfirm/zipfiles/'

outbound_file_start_with = ('DTSUTF','DTSFTP')

def parse_hdr(hdr):
    sysid = hdr[5:10]
    submitter = hdr[15:20]
    sent_dt = hdr[26:34]
    seq= hdr[59:63]
    return sysid,submitter,sent_dt,seq

def parse_outbound_file(file):
    ORecord = collections.namedtuple(
        'ORecord',
        'sysid,submitter,sent_dt,participant,participant_name,seq,file_type,hdr'
    )

    sysid,submitter,sent_dt,participant,participant_name,file_type,hdr,temp_file_type=None,None,None,None,None,None,None,None

    with open(file, 'r') as reader:
        # Read and print the entire file line by line
        for line in reader:
            if line[:3]=='HDR':
                sysid,submitter,sent_dt,seq=parse_hdr(line)
                hdr=line[:63]

            elif line[:3]=='C12' :
                participant=line[3:7]
                temp_file_type=line[31:34]

            elif line[:3]=='C21' or line[:3]=='C42' :
                participant = line[3:7]
    #print(temp_file_type)

    file_type=sysid_ref.get(sysid,temp_file_type)

    participant_name=participant_ref.get(participant,participant)

    record=ORecord(
        sysid, submitter, sent_dt,  participant,participant_name, file_type ,seq,hdr
    )

    #print(record)
    return record

def parse_confirm_file(file):
    CRecord = collections.namedtuple(
        'CRecord',
        'status,hdr'
    )
    sysid,submitter,sent_dt,status,hdr = None, None, None, None, None

    with open(file, 'r') as reader:
        # Read and print the entire file line by line
        #print('processing file:',file)
        for line in reader:

            if line[5:8]=='HDR':
                #sysid,submitter,sent_dt,seq=parse_hdr(line[5:])
                hdr=line[5:68]
            elif line.find('ACCEPTED')>0:
                status='Accepted'
            elif line.find('REJECTED')>0:
                status='REJECTED'
    record = CRecord(
        status, hdr
    )
    #print(record)
    return record

def dtcc_confirm_status():

    #Reding input data files using command prompt

    outbound_files=os.listdir(outbound_path)

    confirm_files = os.listdir(confirm_path)
    #print(outbound_files,confirm_files)
    #Populating Participant ID,File Type Feilds in Output file from input data files
    outbound_data=[]
    confirm_data=[]

    dtcc_confirm_data = []
    Dtcc_Confirm = collections.namedtuple(
        'Dtcc_Confirm',
        'sysid,submitter,sent_dt,participant,participant_name,file_type,seq,status'
    )

    for file in outbound_files:
        #print(f'Processing outbound file:{outbound_path+file}')
        outbound_record = parse_outbound_file(outbound_path+file)
        outbound_data.append(outbound_record)

    for file in confirm_files:
        #print(f'Processing Confirm file:{confirm_path+file}')
        confirm_record=parse_confirm_file(confirm_path+file)
        confirm_data.append(confirm_record)

    with open(output_path+'dtcc_outbound_status.csv', mode='w',newline='') as output_file:
        output_writer = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        output_writer.writerow(['sysid','submitter','sent_dt','participant','participant_name','file_type','seq','status'])
        status=None
        #print(outbound_data)
        #print(confirm_data)
        for orecord in outbound_data:
             for crecord in confirm_data:
                 if orecord.hdr==crecord.hdr:
                        status=crecord.status
                        # frecord=orecord+(crecord.status,)
                 frecord = Dtcc_Confirm(
                    orecord.sysid,
                    orecord.submitter,
                    orecord.sent_dt,
                    orecord.participant,
                    orecord.participant_name,
                    orecord.file_type,
                    orecord.seq,
                    status
                 )
                 #print(frecord)
             dtcc_confirm_data.append(frecord)
             output_writer.writerow(frecord)

def clean_up_files():

    for file in os.listdir(confirm_path):
        os.remove(confirm_path+file)

    for file in os.listdir(outbound_path):
        os.remove(outbound_path+file)

def unzip_files():
    zip_files = os.listdir(zip_path)

    confirm_zips = [ zip for zip in zip_files if zip.startswith('CONFIRM')]
    outbound_zips = [ zip for zip in zip_files if zip.startswith(outbound_file_start_with)]
    for zip in confirm_zips:
        data_zip = zipfile.ZipFile(zip_path+zip, 'r')
        data_zip.extractall(path=confirm_path)

    for zip in outbound_zips:
        data_zip = zipfile.ZipFile(zip_path+zip, 'r')
        data_zip.extractall(path=outbound_path)
    #print(confirm_zips,outbound_zips)

    pass

def archive_files():
    pass

def send_status_email():
    pass
