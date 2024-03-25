import numpy as np

def time_per_side(regular_coor, usr_type):
    ASD_times = []
    TD_times = []
    NaN_times = []
    for i in range(len(regular_coor)):
        ASD_time = 0
        TD_time = 0
        NaN_time = 0
        coors = regular_coor[i]
        for j in range(1, len(coors)):
            dtime = coors[j][2] - coors[j-1][2]

            if not(np.isnan(coors[j][0]) or np.isnan(coors[j-1][0])):
                last_type = not((coors[j-1][1] < 2560/2) ^ usr_type[i]) # Last stimulu type
                curr_type = not((coors[j][1] < 2560/2) ^ usr_type[i])   # Current stimulu type
                if not(last_type ^ curr_type):  # The same type?
                    if last_type:
                        ASD_time += dtime
                    else:
                        TD_time += dtime
                else:
                    ASD_time += dtime / 2
                    TD_time += dtime / 2
            elif np.isnan(coors[j][0]) and np.isnan(coors[j-1][0]):
                NaN_time += dtime
            elif np.isnan(coors[j-1][0]):
                NaN_time += dtime / 2
                if not((coors[j][1] < 2560/2) ^ usr_type[i]):       # Current stimulu type
                    ASD_time += dtime / 2   # Half for each
                else:
                    TD_time += dtime / 2
            else:
                NaN_time += dtime / 2
                if not((coors[j-1][1] < 2560/2) ^ usr_type[i]):     # Current stimulu type
                    ASD_time += dtime / 2   # Half for each
                else:
                    TD_time += dtime / 2
        ASD_times.append(ASD_time)
        TD_times.append(TD_time)
        NaN_times.append(NaN_time)
    return ASD_times, TD_times, NaN_times