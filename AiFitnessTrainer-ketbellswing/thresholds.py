

# Get thresholds for beginner mode
def get_thresholds_beginner():

    _ANGLE_ELBOW_SHOULDER_VERT= {
                            'NORMAL' : (0,  45),
                            'TRANS'  : (50, 110),
                            'PASS'   : (120, 180)
                           }    


    #ANKLE_KNEE_THRESH>170(knees inline with toes)
    #straight arms:shoulder_elbow_wrist>175
    thresholds = {
                    'ELBOW_SHOULDER_VERT': _ANGLE_ELBOW_SHOULDER_VERT,
                    'ANKLE_THRESH' : 45,
                    'ELBOW_THERESH':175,
                    #'HIP_THRESH'   : [10, 50],
                    #'ANKLE_THRESH' : 45,
                    #'KNEE_THRESH'  : [50, 70, 95],

                    'OFFSET_THRESH'    : 35.0,
                    'INACTIVE_THRESH'  : 15.0,

                    
                    'CNT_FRAME_THRESH' : 50
                            
                }

    return thresholds



# Get thresholds for beginner mode
def get_thresholds_pro():

    _ANGLE_ELBOW_SHOULDER_VERT= {
                            'NORMAL' : (0,  45),
                            'TRANS'  : (50, 110),
                            'PASS'   : (120, 180)
                           }    


    #hip_mistake:shoulder_hip_knee <170
    #ANKLE_KNEE_THRESH>170(knees inline with toes)
    #straight arms:shoulder_elbow_wrist>175
    thresholds = {
                    'WRIST_SHOULDER_VERT': _ANGLE_ELBOW_SHOULDER_VERT,
                    'ANKLE_KNEE_THRESH':170,
                    'ELBOW_THERESH':175,
                    #'HIP_THRESH'   : [10, 50],
                    #'ANKLE_THRESH' : 45,
                    #'KNEE_THRESH'  : [50, 70, 95],

                    'OFFSET_THRESH'    : 35.0,
                    'INACTIVE_THRESH'  : 15.0,

                    
                    'CNT_FRAME_THRESH' : 50
                            
                }

    return thresholds