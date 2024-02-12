

# Get thresholds for beginner mode
def get_thresholds_beginner():

    _ANGLE_WRIST_ELBOW_VERT = {
                            'NORMAL' : (150,  180),
                            'TRANS'  : (80, 140),
                            'PASS'   : (30, 79)
                           }    

    #keep holding the weight and curl slowly : s1-->s2 WRIST_ELBOW_VERT in [160,180]
    #CURL your arm :s2-->s3    WRIST_ELBOW_VERT in [80,120]
    #dont sway your elbow forward: ELBOW_SHOULDER_HIP > 30
    thresholds = {
                    'WRIST_ELBOW_VERT': _ANGLE_WRIST_ELBOW_VERT,
                    #'KNEE_ANKLE_VERT':60,
                    'ELBOW_SHOULDER_HIP_THRESH':10, 
                    #'ELBOW_THRESH':10,
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

    _ANGLE_WRIST_ELBOW_VERT = {
                            'NORMAL' : (150,  180),
                            'TRANS'  : (80, 140),
                            'PASS'   : (30, 79)
                           }    

    #keep holding the weight and curl slowly : s1-->s2 WRIST_ELBOW_VERT in [160,180]
    #CURL your arm :s2-->s3    WRIST_ELBOW_VERT in [80,120]
    #dont sway your elbow forward: ELBOW_SHOULDER_HIP > 40
    thresholds = {
                    'WRIST_ELBOW_VERT': _ANGLE_WRIST_ELBOW_VERT,
                    #'KNEE_ANKLE_VERT':60,
                    'ELBOW_SHOULDER_HIP_THRESH':10, 
                    #'ELBOW_THRESH':10,
                    #'HIP_THRESH'   : [10, 50],
                    #'ANKLE_THRESH' : 45,
                    #'KNEE_THRESH'  : [50, 70, 95],

                    'OFFSET_THRESH'    : 35.0,
                    'INACTIVE_THRESH'  : 15.0,

                    
                    'CNT_FRAME_THRESH' : 50
                            
                }
                 
    return thresholds