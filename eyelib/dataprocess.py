import numpy as np
import copy

def regular_record(usr_coor, freq):
    """
    Delay the time for data with too high frequency and insert NaN for data with too low frequency
    Format the eye movement experiment record as equidistant time series
    """

    perms = 1000/freq
    perms4 = perms * 4

    # Delay time for data with too high frequency
    usr_coor = copy.deepcopy(usr_coor)
    for i in range(len(usr_coor)):
        accum = 0
        coor = np.array(usr_coor[i]).reshape(-1,3)
        if coor.shape[0] == 1:
            continue

        dtime = np.diff(coor[:,2])
        for j in range(dtime.shape[0]):
            if dtime[j] < perms:
                accum += perms - dtime[j]
            usr_coor[i][j+1] = (usr_coor[i][j+1][0], usr_coor[i][j+1][1], usr_coor[i][j+1][2]+accum)

    regular_coor = []
    for i in range(len(usr_coor)):  # Test number
        regular_coor.append([usr_coor[i][0]])
        coor = np.array(usr_coor[i]).reshape(-1,3)
        if coor.shape[0] == 1:
            regular_coor[i].append(coor[0])
            continue

        dtime = np.diff(coor[:,2])
        for j in range(dtime.shape[0]):
            if dtime[j] < perms:    # Filter out data with too high frequency
                continue
            if dtime[j] > perms4:
                for k in range(int(dtime[j]//perms)-1):
                    regular_coor[i].append((np.nan,np.nan,coor[j,2]+(k+1)*perms))    # Fill in the missing data as NaN
            regular_coor[i].append(coor[j+1])

    return regular_coor

def equi_record(regular_coor, freq):
    t_eps = 1e-4
    perms = 1000/freq

    linear_inter = lambda p1, p2, t: (p1[0]+(p2[0]-p1[0])*(t-p1[2])/(p2[2]-p1[2]), p1[1]+(p2[1]-p1[1])*(t-p1[2])/(p2[2]-p1[2]), t)
    equi_coor = []    # 60Hz time series
    for i in range(len(regular_coor)):
        equi_coor.append([])
        t_idx = 0
        for t in np.arange(regular_coor[i][0][2], regular_coor[i][-1][2], perms):
            while t > regular_coor[i][t_idx][2] + t_eps:
                t_idx += 1
            if np.abs(t - regular_coor[i][t_idx][2]) < t_eps:
                equi_coor[i].append((regular_coor[i][t_idx]))
            else:
                inter = linear_inter(regular_coor[i][t_idx-1], regular_coor[i][t_idx], t)
                equi_coor[i].append(inter)

    return equi_coor

def write_record(filepath, filename, format_coor):
    """
    Write the formatted eye movement experiment record to a file
    """
    for i in range(len(format_coor)):
        with open(filepath+filename+'_'+str(i)+'.tsv', 'w', encoding='utf-8') as f:
            for coor in format_coor[i]:
                f.write(str(coor[0])+'\t'+str(coor[1])+'\t'+str(coor[2])+'\n')