import re
import json
import numpy as np

def read_record(filepath):
    '''
    Read eye movement experiment record file
    '''
    sti_type = []   # Left stimulus type: ASD/TD 
    eye_coor = []
    with open(filepath, 'r', encoding='utf-8') as f:
        file_content = f.read()
    file_content = re.split('[|^]', file_content)
    
    # Handle the user info
    exp_info = json.loads(file_content[0])
    if exp_info['deviceName'] == 'HWBAH4':
        freq = 30
    else:
        freq = 60
    
    # Handle the fixation coordinates
    for i in range((len(file_content)-1)//3):
        eye_coor.append([])
        sti_info = json.loads(file_content[3*i+1])
        sti_type.append(sti_info['autisticResource'])
        coors = re.split('[(,)]',file_content[3*(i+1)])
        coors = [coors[j:j+4] for j in range(0,len(coors),4)]
        for k, coor in enumerate(coors):   
            if len(coor) < 4:    # Filter out error data
                if k == len(coors) - 1:
                   eye_coor[i].append((np.nan, np.nan, t+1000/freq)) 
                continue
            x = float(coor[1]); y = float(coor[2]); t = float(coor[3]) 
            if x < 0 or y < 0:
                if k == 0 or k == len(coors) - 1:
                    eye_coor[i].append((np.nan, np.nan, t))
                continue
            eye_coor[i].append((x,y,t))
    
    usr_info_pattern = r'record_(\d{14})_([一-龥]{2,4}).txt'
    usr_info_match = re.search(usr_info_pattern, filepath)
    usr_info = {'expDate':usr_info_match.group(1), 'userName':usr_info_match.group(2)}

    return eye_coor, sti_type, exp_info, usr_info