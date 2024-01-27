

# Get thresholds for beginner mode
def get_thresholds_beginner():

    _ANGLE_SHOULDER_ELBOW_VERT = {
                            'NORMAL' : (0,  35),
                            'TRANS'  : (40, 55),
                            'PASS'   : (60, 100)
                           }    

    #go low:s1-->s2 shoulder_elbow_vert in[0,35]
    #go deeper:s2-->s3    shoulder_elbow_vert in[40,80]
    #elbows_pointed_out: shoulder_elbow_vert<10 and knee_ankle_vert>60
    #hip_mistake:shoulder_hip_knee <170
    thresholds = {
                    'SHOUDER_ELBOW_VERT': _ANGLE_SHOULDER_ELBOW_VERT,
                    'KNEE_ANKLE_VERT':60,
                    'SHOULDER_HIP_KNEE':150,
                    'ELBOW_THRESH':10,
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

    _ANGLE_SHOULDER_ELBOW_VERT = {
                            'NORMAL' : (0,  35),
                            'TRANS'  : (40, 80),
                            'PASS'   : (90, 120)
                           }    

    #go low:s1-->s2 shoulder_elbow_vert in[0,35]
    #go deeper:s2-->s3    shoulder_elbow_vert in[40,80]
    #elbows_pointed_out: shoulder_elbow_vert<10 and knee_ankle_vert>60
    #hip_mistake:shoulder_hip_knee <170
    thresholds = {
                    'SHOUDER_ELBOW_VERT': _ANGLE_SHOULDER_ELBOW_VERT,
                    'KNEE_ANKLE_VERT':60,
                    'SHOULDER_HIP_KNEE':170,
                    'ELBOW_THRESH':10,
                    #'HIP_THRESH'   : [10, 50],
                    #'ANKLE_THRESH' : 45,
                    #'KNEE_THRESH'  : [50, 70, 95],

                    'OFFSET_THRESH'    : 35.0,
                    'INACTIVE_THRESH'  : 15.0,

                    
                    'CNT_FRAME_THRESH' : 50
                            
                }
                 
    return thresholds