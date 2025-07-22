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


---

### rp2040 Setup
1. Flash rp2040 with CircuitPython or MicroPython
   **micropython is recommended**
    - install and open a nice interpreter.
        On windows:
        ```bash
        pip install thonny
        ```
        and then
        ```bash
        thonny
        ```
    - hold the RST button whilst plugging your rp2040 into your pc (over a data-capable cable) to put it in flash mode
    - in thonny, in the bottom right settings you can flash the rp2040 with circuitpython / micropython
    - when done, unplug the board, then plug it back in.


3. Upload this library
   
    - make a new file, paste code from this repo in [folder for the firmware you just flashed]/ServoRX.py
    - Save it (ctrl-s) as ServoRX.py

---

### Using the library
- Make a new file for your code (tip: name it boot.py to auto-run on boot, but only do that after testing your code by manually running it)
##### CircuitPython example
> limited to 1 channel! use micropython for multiple + more efficiency
```python
import time
import board

#   \\ Import the ServoRX library like so
from ServoRX import ServoRX

#   \\ set the pin on a variable
CH1 = board.GP21 

#   \\ PWM min - max \\ maps out which number correlates to 0% and 100% stick position
CH1_MAP = [1310,1705]

#  \\ wait x seconds after checking 
delay=0.2

#  \\  initiate the instance of ServoRX 
Instance_1 = ServoRX(pin=CH1, map=CH1_MAP)

while True:

    #  \\ get current stick position
    Input_1 = Instance_1.get_rx()

    #  \\ returns a list:
    # 0%-100% in Input_1[0] 
    # raw pwm pulses in Input_1[1]

    print('CH1: ', Input_1[0])

    time.sleep(delay)

```
##### MicroPython example (Recommended)
```python
import time

#   \\ Import the ServoRX library like so
from ServoRX import ServoRX

#   \\ set the pins on variables

# channel | GPIO pin on rp2040 | Notes on what it is for
CH1       =         21         # CH1  -  Right Joystick 
CH2       =         22         # CH2  -  Right Joystick  
CH3       =         29         # CH3  -  Left Joystick  
CH4       =         26         # CH4  -  Left Joystick  
CH5       =         27         # CH5  -  Right Knob
CH6       =         28         # CH6  -  Left Knob

#   \\ PWM min - max \\ used to interpret stick position
CH1_MAP = [1310,1705]
CH2_MAP = [1383,1684]  
CH3_MAP = [1281,1790]
CH4_MAP = [1285,1684]  
CH5_MAP = [1012,2000]
CH6_MAP = [1010,2035]

#  \\ wait x seconds after checking 
delay=0.2

#  \\ Initiate a ServoRX instance for each channel
Instance_1 = ServoRX(pin=CH1, map=CH1_MAP)
Instance_2 = ServoRX(pin=CH2, map=CH2_MAP)
Instance_3 = ServoRX(pin=CH3, map=CH3_MAP)
Instance_4 = ServoRX(pin=CH4, map=CH4_MAP)
Instance_5 = ServoRX(pin=CH5, map=CH5_MAP)
Instance_6 = ServoRX(pin=CH6, map=CH6_MAP)

while True:
    #  \\ get stick positions 
    Input_1 = Instance_1.get_rx()
    Input_2 = Instance_2.get_rx()
    Input_3 = Instance_3.get_rx()
    Input_4 = Instance_4.get_rx()
    Input_5 = Instance_5.get_rx()
    Input_6 = Instance_6.get_rx()

    #  \\ returns a list, 
    # 0%-100% in Input_1[0] 
    # raw pwm pulses in Input_1[1]

    print('CH1: ', Input_1[0],
          'CH2: ',Input_2[0],
          'CH3: ',Input_3[0],
          'CH4: ',Input_4[0],
          'CH5: ',Input_5[0],
          'CH6: ',Input_6[0])

    time.sleep(delay)

```

---

### Controller calibration / map

It is recommended to print out the raw PWM values, and find the lowest and highest point you can reach with your controller. Then hardcode those numbers in the map variable(s). 

##### Micropython mapping example
```python
import time
from ServoRX import ServoRX

Channel1 = ServoRX(pin=29) # will use default map for now

while True:
  stick = Channel1.get_rx()

  print(f"""
  clamped percentage: {stick[0]}
  raw PWM signals (limited to map): {stick[1]}
  """

  time.sleep(0.5)

# when youre done, 
# you can hardcode the lowest and highest value
map=[1298, 1765]

Channel1 = ServoRX(pin=board.GP29, map=map) # initiate with map

# then use like normal and you will 
# have it correctly interpret stick 
# positions and return a number 
# between 0 and 100


```

---

### Future update:
- add logic to mimick ELRS or other modern speedybee compatible RF protocols, over uart.
