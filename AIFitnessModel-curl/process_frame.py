import time
import cv2
import numpy as np
from utils import find_angle, get_landmark_features, draw_text, draw_dotted_line
class ProcessFrame:
    def __init__(self, thresholds, flip_frame = False):
        
        # Set if frame should be flipped or not.
        self.flip_frame = flip_frame

        # self.thresholds
        self.thresholds = thresholds

        # Font type.
        self.font = cv2.FONT_HERSHEY_SIMPLEX

        # line type
        self.linetype = cv2.LINE_AA

        # set radius to draw arc
        self.radius = 20

        # Colors in BGR format.
        self.COLORS = {
                        'blue'       : (0, 127, 255),
                        'red'        : (255, 50, 50),
                        'green'      : (0, 255, 127),
                        'light_green': (100, 233, 127),
                        'yellow'     : (255, 255, 0),
                        'magenta'    : (255, 0, 255),
                        'white'      : (255,255,255),
                        'cyan'       : (0, 255, 255),
                        'light_blue' : (102, 204, 255)
                      }


 
        # Dictionary to maintain the various landmark features.
        self.dict_features = {}
        self.left_features = {
                                'shoulder': 11,
                                'elbow'   : 13,
                                'wrist'   : 15,                    
                                'hip'     : 23,
                                'knee'    : 25,
                                'ankle'   : 27,
                                'foot'    : 31
                             }

        self.right_features = {
                                'shoulder': 12,
                                'elbow'   : 14,
                                'wrist'   : 16,
                                'hip'     : 24,
                                'knee'    : 26,
                                'ankle'   : 28,
                                'foot'    : 32
                              }

        self.dict_features['left'] = self.left_features
        self.dict_features['right'] = self.right_features
        self.dict_features['nose'] = 0

        
        # For tracking counters and sharing states in and out of callbacks.
        self.state_tracker = {
            'state_seq': [],

            'start_inactive_time': time.perf_counter(),
            'start_inactive_time_front': time.perf_counter(),
            'INACTIVE_TIME': 0.0,
            'INACTIVE_TIME_FRONT': 0.0,

            # 0 --> dont sway your elbow forward, 
            'DISPLAY_TEXT' : np.full((2,), False),
            'COUNT_FRAMES' : np.zeros((2,), dtype=np.int64),

            #'CURL': False,
            'HOLD_WEIGHT_AND_CURL': False,
            'SQUEEZE_BICEP': False,


            'DONT_SWAY_YOUR_ELBOW_FORWARD': False,
            ######'CORRECT_YOUR_HIPS': False,

            'prev_state': None,
            'curr_state':None,

            
            'CURL_COUNT':0,
            'IMPROPER_CURL':0,

            
        }
        
        self.FEEDBACK_ID_MAP = {
                                0: ("Don't sway your elbows forward", 215, (0, 153, 255)),
                                1: ('Hold Weight And Curl', 125, (255, 80, 80)),
                                #2: ('KNEE FALLING OVER TOE', 170, (255, 80, 80)),
                                #3: ('SQUAT TOO DEEP', 125, (255, 80, 80))
                               }
    def _get_state(self, elbow_angle):
        
        elbow = None        

        if self.thresholds['WRIST_ELBOW_VERT']['NORMAL'][0] <= elbow_angle <= self.thresholds['WRIST_ELBOW_VERT']['NORMAL'][1]:
            elbow = 1
        elif self.thresholds['WRIST_ELBOW_VERT']['TRANS'][0] <= elbow_angle <= self.thresholds['WRIST_ELBOW_VERT']['TRANS'][1]:
            elbow = 2
        elif self.thresholds['WRIST_ELBOW_VERT']['PASS'][0] <= elbow_angle <= self.thresholds['WRIST_ELBOW_VERT']['PASS'][1]:
            elbow = 3

        return f's{elbow}' if elbow else None
    

    def _update_state_sequence(self, state):

        if state == 's2':
            if (('s3' not in self.state_tracker['state_seq']) and (self.state_tracker['state_seq'].count('s2'))==0) or \
                    (('s3' in self.state_tracker['state_seq']) and (self.state_tracker['state_seq'].count('s2')==1)):
                        self.state_tracker['state_seq'].append(state)
            
        elif state == 's3':
            if (state not in self.state_tracker['state_seq']) and 's2' in self.state_tracker['state_seq']: 
                self.state_tracker['state_seq'].append(state)


    def _show_feedback(self, frame, c_frame, dict_maps, hold_weight, squeeze_bicep):


        if hold_weight:
            draw_text(
                frame, 
                'Hold the weight and curl slowly', 
                pos=(30, 80),
                text_color=(0, 0, 0),
                font_scale=0.6,  # Increase the font scale to make the text larger
                text_color_bg=(255, 255, 0)
            )
        if squeeze_bicep:
            draw_text(
                frame, 
                'Squeeze your bicep', 
                pos=(30, 100),
                text_color=(0, 0, 0),
                font_scale=0.6,  # Increase the font scale to make the text larger
                text_color_bg=(255, 255, 0)
                )

        for idx in np.where(c_frame)[0]:
            draw_text(
                    frame, 
                    dict_maps[idx][0], 
                    pos=(30, dict_maps[idx][1]),
                    text_color=(255, 255, 230),
                    font_scale=0.6,
                    text_color_bg=dict_maps[idx][2]
                )

        return frame
    



    def process(self, frame: np.array, pose):
        play_sound = None
       

        frame_height, frame_width, _ = frame.shape

        # Process the image.
        keypoints = pose.process(frame)
        
        if keypoints.pose_landmarks:
            ps_lm = keypoints.pose_landmarks

            nose_coord = get_landmark_features(ps_lm.landmark, self.dict_features, 'nose', frame_width, frame_height)
            left_shldr_coord, left_elbow_coord, left_wrist_coord, left_hip_coord, left_knee_coord, left_ankle_coord, left_foot_coord = \
                                get_landmark_features(ps_lm.landmark, self.dict_features, 'left', frame_width, frame_height)
            right_shldr_coord, right_elbow_coord, right_wrist_coord, right_hip_coord, right_knee_coord, right_ankle_coord, right_foot_coord = \
                                get_landmark_features(ps_lm.landmark, self.dict_features, 'right', frame_width, frame_height)

            offset_angle = find_angle(left_shldr_coord, right_shldr_coord, nose_coord)

            print(offset_angle)
            if offset_angle > self.thresholds['OFFSET_THRESH']:
                
                display_inactivity = False

                end_time = time.perf_counter()
                self.state_tracker['INACTIVE_TIME_FRONT'] += end_time - self.state_tracker['start_inactive_time_front']
                self.state_tracker['start_inactive_time_front'] = end_time

                if self.state_tracker['INACTIVE_TIME_FRONT'] >= self.thresholds['INACTIVE_THRESH']:
                    self.state_tracker['CURL_COUNT'] = 0
                    self.state_tracker['IMPROPER_CURL'] = 0
                    display_inactivity = True

                cv2.circle(frame, nose_coord, 7, self.COLORS['white'], -1)
                cv2.circle(frame, left_shldr_coord, 7, self.COLORS['yellow'], -1)
                cv2.circle(frame, right_shldr_coord, 7, self.COLORS['magenta'], -1)

                if self.flip_frame:
                    frame = cv2.flip(frame, 1)

                if display_inactivity:
                    # cv2.putText(frame, 'Resetting SQUAT_COUNT due to inactivity!!!', (10, frame_height - 90), 
                    #             self.font, 0.5, self.COLORS['blue'], 2, lineType=self.linetype)
                    play_sound = 'reset_counters'
                    self.state_tracker['INACTIVE_TIME_FRONT'] = 0.0
                    self.state_tracker['start_inactive_time_front'] = time.perf_counter()

                draw_text(
                    frame, 
                    "CORRECT: " + str(self.state_tracker['CURL_COUNT']), 
                    pos=(int(frame_width*0.68), 30),
                    text_color=(255, 255, 230),
                    font_scale=0.6,
                    text_color_bg=(18, 185, 0)
                )  
                

                draw_text(
                    frame, 
                    "INCORRECT: " + str(self.state_tracker['IMPROPER_CURL']), 
                    pos=(int(frame_width*0.68), 80),
                    text_color=(255, 255, 230),
                    font_scale=0.6,
                    text_color_bg=(221, 0, 0),
                    
                )  
                
                
                draw_text(
                    frame, 
                    'CAMERA NOT ALIGNED PROPERLY!!!', 
                    pos=(30, frame_height-60),
                    text_color=(255, 255, 230),
                    font_scale=0.6,
                    text_color_bg=(255, 153, 0),
                ) 
                
                
                draw_text(
                    frame, 
                    'OFFSET ANGLE: '+str(offset_angle), 
                    pos=(30, frame_height-30),
                    text_color=(255, 255, 230),
                    font_scale=0.6,
                    text_color_bg=(255, 153, 0),
                ) 

                # Reset inactive times for side view.
                self.state_tracker['start_inactive_time'] = time.perf_counter()
                self.state_tracker['INACTIVE_TIME'] = 0.0
                self.state_tracker['prev_state'] =  None
                self.state_tracker['curr_state'] = None
            
            # Camera is aligned properly.
            else:

                self.state_tracker['INACTIVE_TIME_FRONT'] = 0.0
                self.state_tracker['start_inactive_time_front'] = time.perf_counter()


                dist_l_sh_hip = abs(left_elbow_coord[1]- left_wrist_coord[1])
                dist_r_sh_hip = abs(right_elbow_coord[1] - right_wrist_coord)[1]

                shldr_coord = None
                elbow_coord = None
                wrist_coord = None
                hip_coord = None
                knee_coord = None
                ankle_coord = None
                foot_coord = None

                if dist_l_sh_hip > dist_r_sh_hip:
                    shldr_coord = left_shldr_coord
                    elbow_coord = left_elbow_coord
                    wrist_coord = left_wrist_coord
                    hip_coord = left_hip_coord
                    knee_coord = left_knee_coord
                    ankle_coord = left_ankle_coord
                    foot_coord = left_foot_coord

                    multiplier = -1
                                     
                
                else:
                    shldr_coord = right_shldr_coord
                    elbow_coord = right_elbow_coord
                    wrist_coord = right_wrist_coord
                    hip_coord = right_hip_coord
                    knee_coord = right_knee_coord
                    ankle_coord = right_ankle_coord
                    foot_coord = right_foot_coord

                    multiplier = 1
                    

                # ------------------- Verical Angle calculation --------------
                    
                #keep holding the weight and curl slowly : s1-->s2 WRIST_ELBOW_VERT in [160,180]
                #CURL your arm :s2-->s3    WRIST_ELBOW_VERT in [80,120]
                #dont sway your elbow forward: ELBOW_SHOULDER_HIP > 30
                
                elbow_wrist_vert = find_angle(wrist_coord, np.array([elbow_coord[0], 0]),elbow_coord)
                cv2.ellipse(frame, elbow_coord, (30, 30), 
                            angle = 0, startAngle = -90, endAngle = -90+multiplier*elbow_wrist_vert, 
                            color = self.COLORS['white'], thickness = 3, lineType = self.linetype)

                draw_dotted_line(frame, elbow_coord, start=elbow_coord[1]-80, end=elbow_coord[1]+20, line_color=self.COLORS['blue'])



                elbow_shoulder_vert = find_angle(elbow_coord, np.array([shldr_coord[0], frame.shape[0]-1]),shldr_coord)
                cv2.ellipse(frame, shldr_coord, (30, 30), 
                            angle = 0, startAngle = -90, endAngle = -90+multiplier*elbow_shoulder_vert, 
                            color = self.COLORS['white'], thickness = 3, lineType = self.linetype)

                draw_dotted_line(frame, shldr_coord, start=shldr_coord[1]-80, end=shldr_coord[1]+20, line_color=self.COLORS['blue'])

                # elbow_shoulder_hip = find_angle(elbow_coord,hip_coord, shldr_coord)
                # cv2.ellipse(frame, shldr_coord, (20, 20), 
                #             angle = 0, startAngle = -90-find_angle(elbow_coord,np.array([0,shldr_coord[1]]),shldr_coord),
                #             endAngle = -90-find_angle(elbow_coord,np.array([0,shldr_coord[1]]),shldr_coord)-multiplier*elbow_shoulder_hip, 
                #             color = self.COLORS['white'], thickness = 3,  lineType = self.linetype)
                

                # shoulder_hip_knee = find_angle(shldr_coord,knee_coord, hip_coord)
                # cv2.ellipse(frame, hip_coord, (20, 20), 
                #             angle = 0, startAngle = 180-find_angle(shldr_coord,np.array([0,hip_coord[1]]),hip_coord),
                #             endAngle = 180-find_angle(shldr_coord,np.array([0,hip_coord[1]]),hip_coord)-multiplier*shoulder_hip_knee, 
                #             color = self.COLORS['white'], thickness = 3,  lineType = self.linetype)

                #draw_dotted_line(frame, knee_coord, start=knee_coord[1]-50, end=knee_coord[1]+20, line_color=self.COLORS['blue'])



                # ankle_vertical_angle = find_angle(knee_coord, np.array([ankle_coord[0], 0]), ankle_coord)
                # cv2.ellipse(frame, ankle_coord, (30, 30),
                #             angle = 0, startAngle = -90, endAngle = -90 + multiplier*ankle_vertical_angle,
                #             color = self.COLORS['white'], thickness = 3,  lineType=self.linetype)

                # draw_dotted_line(frame, ankle_coord, start=ankle_coord[1]-50, end=ankle_coord[1]+20, line_color=self.COLORS['blue'])

                # ------------------------------------------------------------
        
                
                # Join landmarks.
                cv2.line(frame, shldr_coord, elbow_coord, self.COLORS['light_blue'], 4, lineType=self.linetype)
                cv2.line(frame, wrist_coord, elbow_coord, self.COLORS['light_blue'], 4, lineType=self.linetype)
                cv2.line(frame, shldr_coord, hip_coord, self.COLORS['light_blue'], 4, lineType=self.linetype)
                cv2.line(frame, knee_coord, hip_coord, self.COLORS['light_blue'], 4,  lineType=self.linetype)
                cv2.line(frame, ankle_coord, knee_coord,self.COLORS['light_blue'], 4,  lineType=self.linetype)
                cv2.line(frame, ankle_coord, foot_coord, self.COLORS['light_blue'], 4,  lineType=self.linetype)
                
                # Plot landmark points
                cv2.circle(frame, shldr_coord, 7, self.COLORS['yellow'], -1,  lineType=self.linetype)
                cv2.circle(frame, elbow_coord, 7, self.COLORS['yellow'], -1,  lineType=self.linetype)
                cv2.circle(frame, wrist_coord, 7, self.COLORS['yellow'], -1,  lineType=self.linetype)
                cv2.circle(frame, hip_coord, 7, self.COLORS['yellow'], -1,  lineType=self.linetype)
                cv2.circle(frame, knee_coord, 7, self.COLORS['yellow'], -1,  lineType=self.linetype)
                cv2.circle(frame, ankle_coord, 7, self.COLORS['yellow'], -1,  lineType=self.linetype)
                cv2.circle(frame, foot_coord, 7, self.COLORS['yellow'], -1,  lineType=self.linetype)

                

                current_state = self._get_state(int(elbow_wrist_vert))
                # print(f'current state {current_state}')
                self.state_tracker['curr_state'] = current_state
                self._update_state_sequence(current_state)



                # -------------------------------------- COMPUTE COUNTERS --------------------------------------
                # print(self.state_tracker['state_seq'])

                if current_state == 's1':
                    if len(self.state_tracker['state_seq']) == 3 and  not  self.state_tracker['DONT_SWAY_YOUR_ELBOW_FORWARD']:
                        self.state_tracker['CURL_COUNT']+=1
                        play_sound = str(self.state_tracker['CURL_COUNT'])
                        
                    elif 's2' in self.state_tracker['state_seq'] and len(self.state_tracker['state_seq'])==1:
                        self.state_tracker['IMPROPER_CURL']+=1
                        play_sound = 'incorrect'

                    elif self.state_tracker['DONT_SWAY_YOUR_ELBOW_FORWARD'] :
                        self.state_tracker['IMPROPER_CURL']+=1
                        play_sound = 'incorrect'
                        
                    
                    self.state_tracker['state_seq'] = []
                    #self.state_tracker['INCORRECT_POSTURE'] = False
                    self.state_tracker['DONT_SWAY_YOUR_ELBOW_FORWARD']=False
                    # self.state_tracker['CORRECT_YOUR_HIPS']=False
                    if  elbow_wrist_vert > self.thresholds['WRIST_ELBOW_VERT']['NORMAL'][0] :
                    #    self.state_tracker['state_seq'].count('s1')==0
                        self.state_tracker['HOLD_WEIGHT_AND_CURL'] = True  
                        self.state_tracker['DISPLAY_TEXT'][1] = True

                # ----------------------------------------------------------------------------------------------------


                # -------------------------------------- PERFORM FEEDBACK ACTIONS --------------------------------------
                else: 
                     #keep holding the weight and curl slowly : s1-->s2 WRIST_ELBOW_VERT in [160,180]                   
                    if  elbow_wrist_vert > self.thresholds['WRIST_ELBOW_VERT']['NORMAL'][0] :
                    #    self.state_tracker['state_seq'].count('s1')==0
                        self.state_tracker['HOLD_WEIGHT_AND_CURL'] = True  

                   #CURL your arm :s2-->s3    WRIST_ELBOW_VERT in [80,120]
                    elif  elbow_wrist_vert > self.thresholds['WRIST_ELBOW_VERT']['TRANS'][0] and \
                        elbow_wrist_vert <= self.thresholds['WRIST_ELBOW_VERT']['TRANS'][1] and \
                       self.state_tracker['state_seq'].count('s1')==1 :
                        self.state_tracker['SQUEEZE_BICEP'] = True  

                    #elbows_pointed_out: shoulder_elbow_vert<10 and knee_ankle_vert>60
                    # print(f'anklevert{ankle_vertical_angle} and thresh {self.thresholds["KNEE_ANKLE_VERT"]}')
                    # if elbow_vertical_angle < self.thresholds['ELBOW_THRESH'] and ankle_vertical_angle>self.thresholds['KNEE_ANKLE_VERT'] :
                    #     self.state_tracker['DISPLAY_TEXT'][0] = True
                    #     self.state_tracker['ELBOWS_POINTED_OUT'] = True

                    #hip_mistake:shoulder_hip_knee< 170
                    #dont sway your elbow forward: ELBOW_SHOULDER_HIP > 30   
                           
                    if (elbow_shoulder_vert > self.thresholds['SHOULDER_ELBOW_VERT_THRESH']) :
                        
                        self.state_tracker['DISPLAY_TEXT'][0] = True
                        self.state_tracker['DONT_SWAY_YOUR_ELBOW_FORWARD'] = True


                # ----------------------------------------------------------------------------------------------------


                
                
                # ----------------------------------- COMPUTE INACTIVITY ---------------------------------------------

                display_inactivity = False
                
                if self.state_tracker['curr_state'] == self.state_tracker['prev_state']:

                    end_time = time.perf_counter()
                    self.state_tracker['INACTIVE_TIME'] += end_time - self.state_tracker['start_inactive_time']
                    self.state_tracker['start_inactive_time'] = end_time

                    if self.state_tracker['INACTIVE_TIME'] >= self.thresholds['INACTIVE_THRESH']:
                        self.state_tracker['CURL_COUNT'] = 0
                        self.state_tracker['IMPROPER_CURL'] = 0
                        display_inactivity = True

                
                else:
                    
                    self.state_tracker['start_inactive_time'] = time.perf_counter()
                    self.state_tracker['INACTIVE_TIME'] = 0.0

                # -------------------------------------------------------------------------------------------------------
              


                elbow_text_coord_x = elbow_coord[0] + 10
                shoulder_text_coord_x = shldr_coord[0] + 15
                # wrist_text_coord_x = wrist_coord[0] + 10

                if self.flip_frame:
                    frame = cv2.flip(frame, 1)
                    elbow_text_coord_x = frame_width - elbow_coord[0] + 10
                    shldr_text_coord_x = frame_width - shldr_coord[0] + 15
                    # wrist_text_coord_x = frame_width - wrist_coord[0] + 10

                
                
                if ('s2' in self.state_tracker['state_seq'] ) or (current_state == 's1'and not 's2' in self.state_tracker['state_seq'] ):
                    self.state_tracker['HOLD_WEIGHT_AND_CURL'] = False

                if 's3' in self.state_tracker['state_seq'] or (current_state == 's2'  and not 's3' in self.state_tracker['state_seq']):
                    self.state_tracker['SQUEEZE_BICEP'] = False



                self.state_tracker['COUNT_FRAMES'][self.state_tracker['DISPLAY_TEXT']]+=1



                frame = self._show_feedback(frame, self.state_tracker['COUNT_FRAMES'], self.FEEDBACK_ID_MAP,self.state_tracker['HOLD_WEIGHT_AND_CURL'], self.state_tracker['SQUEEZE_BICEP'])




                if display_inactivity:
                    # cv2.putText(frame, 'Resetting COUNTERS due to inactivity!!!', (10, frame_height - 20), self.font, 0.5, self.COLORS['blue'], 2, lineType=self.linetype)
                    play_sound = 'reset_counters'
                    self.state_tracker['start_inactive_time'] = time.perf_counter()
                    self.state_tracker['INACTIVE_TIME'] = 0.0

                
                cv2.putText(frame, str(int(elbow_shoulder_vert)), (shoulder_text_coord_x, shldr_coord[1]), self.font, 1, self.COLORS['light_green'], 2, lineType=self.linetype)
                cv2.putText(frame, str(int(elbow_wrist_vert)), (elbow_text_coord_x, elbow_coord[1]+10), self.font, 1, self.COLORS['light_green'], 2, lineType=self.linetype)
                #cv2.putText(frame, str(int(ankle_vertical_angle)), (wrist_text_coord_x, ankle_coord[1]), self.font, 1, self.COLORS['light_green'], 2, lineType=self.linetype)

                 
                draw_text(
                    frame, 
                    "CORRECT: " + str(self.state_tracker['CURL_COUNT']), 
                    pos=(int(frame_width*0.68), 30),
                    text_color=(255, 255, 230),
                    font_scale=0.6,  # Increase the font scale to make the text larger
                    text_color_bg=(18, 185, 0)
                )

                draw_text(
                    frame, 
                    "INCORRECT: " + str(self.state_tracker['IMPROPER_CURL']), 
                    pos=(int(frame_width*0.68), 80),
                    text_color=(255, 255, 230),
                    font_scale=0.6,  # Increase the font scale to make the text larger
                    text_color_bg=(221, 0, 0),
                )
  
                
                
                self.state_tracker['DISPLAY_TEXT'][self.state_tracker['COUNT_FRAMES'] > self.thresholds['CNT_FRAME_THRESH']] = False
                self.state_tracker['COUNT_FRAMES'][self.state_tracker['COUNT_FRAMES'] > self.thresholds['CNT_FRAME_THRESH']] = 0    
                self.state_tracker['prev_state'] = current_state
                                  

       
        
        else:

            if self.flip_frame:
                frame = cv2.flip(frame, 1)

            end_time = time.perf_counter()
            self.state_tracker['INACTIVE_TIME'] += end_time - self.state_tracker['start_inactive_time']

            display_inactivity = False

            if self.state_tracker['INACTIVE_TIME'] >= self.thresholds['INACTIVE_THRESH']:
                self.state_tracker['CURL_COUN'] = 0
                self.state_tracker['IMPROPER_CURL'] = 0
                display_inactivity = True

            self.state_tracker['start_inactive_time'] = end_time

            draw_text(
                    frame, 
                    "CORRECT: " + str(self.state_tracker['CURL_COUNT']), 
                    pos=(int(frame_width*0.68), 30),
                    text_color=(255, 255, 230),
                    font_scale=0.6,
                    text_color_bg=(18, 185, 0)
                )  
                

            draw_text(
                    frame, 
                    "INCORRECT: " + str(self.state_tracker['IMPROPER_CURL']), 
                    pos=(int(frame_width*0.68), 80),
                    text_color=(255, 255, 230),
                    font_scale=0.6,
                    text_color_bg=(221, 0, 0),
                    
                )  

            if display_inactivity:
                play_sound = 'reset_counters'
                self.state_tracker['start_inactive_time'] = time.perf_counter()
                self.state_tracker['INACTIVE_TIME'] = 0.0
            
            
            # Reset all other state variables
            
            self.state_tracker['prev_state'] =  None
            self.state_tracker['curr_state'] = None
            self.state_tracker['INACTIVE_TIME_FRONT'] = 0.0
            self.state_tracker['DONT_SWAY_YOUR_ELBOW_FORWARD'] = False
            # self.state_tracker['CORRECT_YOUR_HIPS'] = False
            self.state_tracker['DISPLAY_TEXT'] = np.full((2,), False)
            self.state_tracker['COUNT_FRAMES'] = np.zeros((2,), dtype=np.int64)
            self.state_tracker['start_inactive_time_front'] = time.perf_counter()
            
            
            
        return frame, play_sound

      

 