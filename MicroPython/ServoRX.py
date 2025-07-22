# ServoRX.py  –  MicroPython version
# ---------------------------------------------------------------------------
# Measure one hobby‑RC PWM channel on an RP2040 (or any MCU with µs timer).
# Works with up to six (or more) simultaneous instances.
# ---------------------------------------------------------------------------

from machine import Pin, disable_irq, enable_irq
import time

class ServoRX:
    """
    Capture a PWM‑style RC receiver channel and convert it to 0‑100 %.
    
    get_rx()  -> [percent, smoothed_pulse_us, latest_pulse_us]
                 (percent is None until a valid pulse is seen)
    
    * pin        : GPIO number or Pin object (set as INPUT automatically)
    * map=(lo,hi): clamp range in µs (usually 1000–2000)
    * smoothing  : N‑sample moving average, 0/1 = off
    """

    def __init__(self, pin, map=(1000, 2000), smoothing=0):
        # user parameters
        self._low, self._high = map
        self._smooth_n        = max(1, int(smoothing))

        # internal state
        self._pulse_raw   = None       # last pulse width [µs]
        self._history     = []         # for moving average
        self._t_rise      = 0          # timestamp of rising edge
        self._last_good   = 0          # for spike filter
        self._hundred_cnt = 0

        # set up GPIO + IRQ
        self._pin = pin if isinstance(pin, Pin) else Pin(pin, Pin.IN)
        self._pin.irq(self._irq, Pin.IRQ_RISING | Pin.IRQ_FALLING)

    # ---------------------------------------------------------------------
    # Interrupt handler – runs on every edge (keep it *very* short!)
    # ---------------------------------------------------------------------
    def _irq(self, pin):
        now = time.ticks_us()

        if pin.value():                # rising edge
            self._t_rise = now
        else:                          # falling edge
            width = time.ticks_diff(now, self._t_rise)

            # accept widths in a generous 300‑3000 µs window
            if 300 <= width <= 3000:
                self._pulse_raw = width

                if self._smooth_n > 1:
                    self._history.append(width)
                    if len(self._history) > self._smooth_n:
                        self._history.pop(0)

    # ---------------------------------------------------------------------
    # Helper for suppressing a single 100 % spike
    # ---------------------------------------------------------------------
    def _spike_filter(self, pct):
        if pct != 100:
            self._hundred_cnt = 0
            self._last_good   = pct
            return pct
        self._hundred_cnt += 1
        if self._last_good < 90 and self._hundred_cnt == 1:
            return self._last_good
        self._last_good = 100
        return 100

    # ---------------------------------------------------------------------
    # Public API
    # ---------------------------------------------------------------------
    def get_rx(self):
        """
        Return [percent, smoothed_pulse, latest_pulse].
        Percent is None until the first valid pulse arrives.
        """
        # copy shared data atomically
        irq_state = disable_irq()
        raw = self._pulse_raw
        hist = tuple(self._history)    # small, safe copy
        enable_irq(irq_state)

        if raw is None:                # no pulse captured yet
            return [None, None, None]

        pulse_avg = raw
        if self._smooth_n > 1 and hist:
            pulse_avg = sum(hist) // len(hist)

        pct = (pulse_avg - self._low) * 100 / (self._high - self._low)
        pct = self._spike_filter(pct)

        return [pct, pulse_avg, raw]

