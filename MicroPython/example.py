from ServoRX import ServoRX
import time


# Receiver channel | GPIO pin on rp2040
CH1                 =       21                       # CH1  -  Right Joystick  -  Right/Left  -  Left is 0, Normal is 50, Right is 100
CH2                 =       22                       # CH2  -  Right Joystick  -  Up/Down  -  Right Switch  -  Down is 0, Normal is 50, Up is 100
CH3                 =       29                       # CH3  -  Left Joystick  -  Up/Down
CH4                 =       26                       # CH4  -  Left Joystick  -  Right/Left  -  Right Switch  -  Left is 0, Normal is 50, Right is 100
CH5                 =       27                       # CH5  -  Right Knob     -  0 to 100
CH6                 =       28                       # CH6  -  Left Knob      -  0 to 100

#   \\ PWM min - max \\ used to interpret stick position
CH1_MAP = [1310,1705]
CH2_MAP = [1383,1684]                                        # CH2  -  Right Switch lowers 2% to everything - Keep Right Switch towards you for this map.
CH3_MAP = [1281,1790]
CH4_MAP = [1285,1684]                                        # CH4  -  Right Switch adds 10% to everything - Keep Right Switch towards you for this map.
CH5_MAP = [1012,2000]
CH6_MAP = [1010,2035]

#  \\ wait x seconds after checking \\ avoids overloading rp2040
delay=0.3

#  \\ sets pin & map \\ inits pulse reading, class init (variables are now self)
Instance_1 = ServoRX(pin=CH1, map=CH1_MAP)
time.sleep(delay)
Instance_2 = ServoRX(pin=CH2, map=CH2_MAP)
time.sleep(delay)
Instance_3 = ServoRX(pin=CH3, map=CH3_MAP)
time.sleep(delay)
Instance_4 = ServoRX(pin=CH4, map=CH4_MAP)
time.sleep(delay)


while True:

    #  \\ get stick positions \\ returns list: % (0-100) in [0] and raw pwm pulses in [1]

    Input_1 = Instance_1.get_rx()
    
    Input_2 = Instance_2.get_rx()
    
    Input_3 = Instance_3.get_rx()

    Input_4 = Instance_4.get_rx()
    
    print('CH1: ',Input_1[0],' CH2: ',Input_2[0],' CH3: ',Input_3[0],' CH4: ',Input_4[0])

    time.sleep(delay)


