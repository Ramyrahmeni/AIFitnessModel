

# Get thresholds for beginner mode
def get_thresholds_beginner():

    _ANGLE_SHOULDER_ELBOW_WRIST = {
                            'NORMAL' : (160,  180),
                            'TRANS'  : (110, 155),
                            'PASS'   : (70, 108)
                           }    

        
    thresholds = {
                    'SHOULDER_ELBOW_WRIST': _ANGLE_SHOULDER_ELBOW_WRIST,

                    'ELBOW_THRESH'   : 20,#this angle<20---->dont flare your elbows out
                    'DEEP_THRESH':[40,80],
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
                            'TRANS'  : (110, 155),
                            'PASS'   : (80, 108)
                           }    

        
    thresholds = {
                    'SHOULDER_ELBOW_WRIST': _ANGLE_SHOULDER_ELBOW_WRIST,

                    'ELBOW_THRESH'   : 20,#this angle<20---->dont flare your elbows out
                    'DEEP_THRESH':[40,80],
                    #'ANKLE_THRESH' : 45,
                    #'KNEE_THRESH'  : [50, 70, 95],

                    'OFFSET_THRESH'    : 35.0,
                    'INACTIVE_THRESH'  : 15.0,

                    'CNT_FRAME_THRESH' : 50
                            
                }
                 
    return thresholds