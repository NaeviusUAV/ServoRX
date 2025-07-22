#Problem: only good for 1, when you ask it to read 6 channels or anything more than 1, it wont work.


# ServoRX.py


# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------
import board                         
import time                        
import pulseio

# -----------------------------------------------------------------------------
# Global Constants / Configuration
# -----------------------------------------------------------------------------
DEFAULT_GPIO_NR = 0
DEFAULT_MAP = [0, 2000]


# -----------------------------------------------------------------------------
# Class 
# -----------------------------------------------------------------------------
class ServoRX:
    """
    ServoRX - Made to use old school RC plane receivers that are made to drive servos, on a speedybee.
    """


    def __init__(self, pin=DEFAULT_GPIO_NR, map=DEFAULT_MAP, smoothing=0):
        """
        Initialize Servo_RX on the given pin and map

        Args:
            pin: board pin to which the device is connected.
        """
  
        # 'self' refers to this instance of ServoRX.
        self.MIN=map[0]
        self.MAX=map[1]
        self.PIN=pin


        self.SMOOTH_N    = smoothing     

        self.pulses = pulseio.PulseIn(pin, maxlen=8, idle_state=False)
        self.pulses.clear()
        self.pulses.resume()

        self.history = []

        self._last_good = 0
        self._hundred_count = 0




    def help(self):
        print('Made to use old school RC plane receivers that are made to drive servos, on a speedybee, by converting the signal over an rp2040.')
        print("""
    Wiring:

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

              
    Code:
            
        Now we interpret this GPIO
            
            def get_rx(gpio=int, 
                        map=[int, int])
            
                returns e.g. 100.0 for 100% throttle

            
        controller calibration
            
            in get_rx(    map       <-- is the controller calibration map
            
            its just a list of [min, max] values to clamp the PWM signals to.
            Its recommended to calibrate it by doing this:
                map = calibrate_controller(gpio=int)
            
            that will guide you through the process. and then you can use the variable in get_rx.
            
            Alternatively:
            you can use default values for map: [1000, 2000]
            or print(map) and then hardcode those values.
        
    """)
        return None

    def get_rx(self, gpio=None, map=None):

        # -----------------------------------------------------------------------------
        # prep vars
        # -----------------------------------------------------------------------------
        if gpio == None or map == None:
            gpio=self.PIN
            low=self.MIN
            high=self.MAX
        else:
            low=map[0]
            high=map[1]
                
        # -----------------------------------------------------------------------------
        # helpers
        # -----------------------------------------------------------------------------
        def Filtering(pulse):
            """
            Suppress an isolated 100% spike when the last good value was < 50%.
            Returns (bad_reading, value_to_use), always as (bool, int).
            """
            global _last_good, _hundred_count

            # pull globals into locals (one load each)
            last = self._last_good
            cnt  = self._hundred_count

            if pulse != 100:
                # non‑100 always accepted
                self._hundred_count = 0
                self._last_good     = pulse
                return False, pulse

            # pulse == 100 path
            cnt += 1
            self._hundred_count = cnt

            # only the very first 100% after a low (<50%) is rejected
            if last < 90 and cnt == 1:
                return True, last

            # otherwise accept
            self._last_good = 100
            return False, 100

        # -----------------------------------------------------------------------------
        # main
        # -----------------------------------------------------------------------------

        # pause and snapshot the buffer
        self.pulses.pause()
        count = len(self.pulses)
        durations = [self.pulses[i] for i in range(count)]
        self.pulses.clear()
        self.pulses.resume()

        # extract HIGH times (every 2nd entry: index 1,3,5,…)
        highs = durations[1::2]
        if not highs:
            return None, None, None, durations

        # take the most recent high pulse
        pulse = highs[-1]
        
        # clamp to valid range
        
        pulse = min(max(pulse, low), high)
        
        if self.SMOOTH_N > 1:
            # smoothing
            self.history.append(pulse)
            if len(self.history) > self.SMOOTH_N:
                self.history.pop(0)
            avg_pulse = sum(self.history) // len(self.history)
        else:
            avg_pulse = pulse
        # map to 0–100%
        received_value = (avg_pulse - low) * 100 / (high - low)
        
        bad_reading, correction=Filtering(received_value)
        
        received_value = correction

        return [received_value, avg_pulse, pulse, durations]


