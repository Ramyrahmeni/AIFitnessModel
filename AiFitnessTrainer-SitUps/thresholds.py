

# Get thresholds for beginner mode
def get_thresholds_beginner():

    _ANGLE_HIP_CHEST_VERT = {
                            'NORMAL' : (80,  95),
                            'TRANS'  : (35, 65),
                            'PASS'   : (0, 30)
                           }    

        
    thresholds = {
                    'HIP_CHEST_VERT': _ANGLE_HIP_CHEST_VERT,

                    #'HIP_THRESH'   : [10, 50],
                    #'ANKLE_THRESH' : 45,
                    #'KNEE_THRESH'  : [50, 70, 95],
                    'SHOULDER_THRESH'  : 30, #vert_shoulder_nose<30

                    'OFFSET_THRESH'    : 35.0,
                    'INACTIVE_THRESH'  : 15.0,

                    'CNT_FRAME_THRESH' : 50
                            
                }

    return thresholds



# Get thresholds for beginner mode
def get_thresholds_pro():

    _ANGLE_HIP_CHEST_VERT = {
                            'NORMAL' : (80,  95),
                            'TRANS'  : (35, 65),
                            'PASS'   : (0, 30)
                           }    

        
    thresholds = {
                    'HIP_KNEE_VERT': _ANGLE_HIP_CHEST_VERT,

                    #'HIP_THRESH'   : [10, 50],
                    #'ANKLE_THRESH' : 45,
                    #'KNEE_THRESH'  : [50, 70, 95],
                    'SHOULDER_THRESH'  : 30, #vert_shoulder_nose<30

                    'OFFSET_THRESH'    : 35.0,
                    'INACTIVE_THRESH'  : 15.0,

                    'CNT_FRAME_THRESH' : 50
                            
                }
                 
    return thresholds