

# Get thresholds for beginner mode
def get_thresholds_beginner():

    _ANGLE_SHOULDER_ELBOW_WRIST = {
                            'NORMAL' : (160,  180),
                            'TRANS'  : (90, 150),
                            'PASS'   : (0, 70)
                           }    

        
    thresholds = {
                    'SHOULDER_ELBOW_WRIST': _ANGLE_SHOULDER_ELBOW_WRIST,

                    'HIP_THRESH'   : 170, #shoulder_hip_ankle<170
                    
                    #'ANKLE_THRESH' : 45,
                    
                    #'KNEE_THRESH'  : [50, 70, 95],

                    'OFFSET_THRESH'    : 35.0,
                    'INACTIVE_THRESH'  : 15.0,

                    'CNT_FRAME_THRESH' : 50
                            
                }

    return thresholds



# Get thresholds for beginner mode
def get_thresholds_pro():

    _ANGLE_SHOULDER_ELBOW_WRIST = {
                            'NORMAL' : (160,  180),
                            'TRANS'  : (90, 150),
                            'PASS'   : (0, 70)
                           }    

        
    thresholds = {
                    'SHOULDER_ELBOW_WRIST': _ANGLE_SHOULDER_ELBOW_WRIST,

                    'HIP_THRESH'   : 170, #shoulder_hip_ankle<170
                    
                    #'ANKLE_THRESH' : 45,
                    
                    #'KNEE_THRESH'  : [50, 70, 95],

                    'OFFSET_THRESH'    : 35.0,
                    'INACTIVE_THRESH'  : 15.0,

                    'CNT_FRAME_THRESH' : 50
                            
                }
                 
    return thresholds