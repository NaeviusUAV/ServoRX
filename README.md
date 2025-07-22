# ServoRX 
Made to use old school RC plane receivers that are made to drive servos, on a speedybee, by converting the signal over an rp2040.

---

### Wiring

            --------------------
            | BAT | PWM 5V GND |----------------------------      
            | CH1 | PWM 5V GND |                             |
            | CH2 | PWM 5V GND |                             |
            | CH..| PWM 5V GND |   1600 BC       receiver    |
            |                  |                             |
            |                  |                             |
            --------------------_____________________________|
            L------------------|-----------------------------=

              
We need 3.3V logic, so gotta underpower the receiver (warning: can break, its risky). 
            
            rp2040  |  receiver
           =========|===========
              3.3V  |  BAT 5v
               GND  |  BAT GND
        
              
Then pick a channel
            
            rp2040   |  receiver
            =========|===========
           GPIO pin  |  receiver PWM


  
### rp2040 Setup
1. Flash rp2040 with CircuitPython

    On windows:
    ```bash
    pip install thonny
    ```
    and then
    ```bash
    thonny
    ```
    to install and open a nice interpreter.
    in its settings you can flash the rp2040 with circuitpython (needs to be put in flash mode)

2. Upload this library
   
    - make a new file, paste code from ServoRX.py in this repo.
    - Save it (ctrl-s) as ServoRX.py.
    - Make a new file called main.py or boot.py (boot.py will auto-run on boot)


### Using the library
example:
```python
from ServoRX import ServoRX
import time
import board

# Receiver channel | GPIO pin on rp2040
CH1                 =       board.GP21                       # CH1  -  Right Joystick  -  Right/Left  -  Left is 0, Normal is 50, Right is 100
CH2                 =       board.GP22                       # CH2  -  Right Joystick  -  Up/Down  -  Right Switch  -  Down is 0, Normal is 50, Up is 100
CH3                 =       board.GP29                       # CH3  -  Left Joystick  -  Up/Down
CH4                 =       board.GP26                       # CH4  -  Left Joystick  -  Right/Left  -  Right Switch  -  Left is 0, Normal is 50, Right is 100
CH5                 =       board.GP27                       # CH5  -  Right Knob     -  0 to 100
CH6                 =       board.GP28                       # CH6  -  Left Knob      -  0 to 100

#   \\ PWM min - max \\ used to interpret stick position
CH1_MAP = [1310,1705]
CH2_MAP = [1383,1684]                                        # CH2  -  Right Switch lowers 2% to everything - Keep Right Switch towards you for this map.
CH3_MAP = [1281,1790]
CH4_MAP = [1285,1684]                                        # CH4  -  Right Switch adds 10% to everything - Keep Right Switch towards you for this map.
CH5_MAP = [1012,2000]
CH6_MAP = [1010,2035]

#  \\ wait x seconds after checking \\ avoids overloading rp2040
delay=0.2

#  \\ sets pin & map \\ inits pulse reading, class init (variables are now self)
Instance_1 = ServoRX(pin=CH1, map=CH1_MAP)
Instance_2 = ServoRX(pin=CH2, map=CH2_MAP)
Instance_3 = ServoRX(pin=CH3, map=CH3_MAP)
Instance_4 = ServoRX(pin=CH4, map=CH4_MAP)
Instance_5 = ServoRX(pin=CH5, map=CH5_MAP)
Instance_6 = ServoRX(pin=CH6, map=CH6_MAP)

while True:
    #  \\ get stick positions \\ returns list: % (0-100) in [0] and raw pwm pulses in [1]
    Input_1 = Instance_1.get_rx()
    print('CH1: ',Input_1[0])
    Input_2 = Instance_2.get_rx()
    print('CH2: ',Input_2[0])
    Input_3 = Instance_3.get_rx()
    print('CH3: ',Input_3[0])
    Input_4 = Instance_4.get_rx()
    print('CH4: ',Input_4[0])
    Input_5 = Instance_5.get_rx()
    print('CH5: ',Input_5[0])
    Input_6 = Instance_6.get_rx()
    print('CH6: ',Input_6[0])



    time.sleep(delay)



```
returns a list with index 0 being the percentage of throttle, index 1 being raw PWM values

### Controller calibration / map
```python         
            in get_rx(    map # <-- is the controller calibration map
```
its just a list of [min, max] values to clamp the PWM signals to.
it is recommended to print out the raw PWM values, and find the lowest and highest point you can reach with your controller.

example:
```python
import board
import time
from ServoRX import ServoRX

Channel1 = ServoRX(pin=board.GP29)         # initiate, will use default map for now

while True:
  stick = Channel1.get_rx()

  print(f"""
  clamped percentage with current map: {stick[0]}
  raw PWM signals (limited to map): {stick[1]}
  """

  time.sleep(0.5)

# when youre done, you can hardcode the lowest value you could reach, and the highest:
map=[1298, 1765]
Channel1 = ServoRX(pin=board.GP29, map=map)         # initiate, with the map for your controller

# the rest works the same


```

