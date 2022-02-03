import math
import pytweening
import pyxel


class TimedValue():
    def __init__(self, v=0, duration=30, f='easeOutElastic', offset=0, delay=0, autoreset=False, inverted=False, bounce=False, clock=None):
        """
        duration: duration (in frames).
        f: easing function name. Look them up at http://easings.net.
        offset: start from a non-zero value.
        delay: start after this many frames
        autoreset: reset automatically once duration has elpased
        inverted: start at target value and decrease to 0 (+ offset)
        bounce: goes back and forth between start and target value
        clock: function returning the date as an integer number of ticks
               (default: pyxel.frame_count)
        """

        self.v = math.ceil(v)
        self.duration = duration
        self.function = getattr(pytweening, f)
        self.offset = offset
        self.autoreset = autoreset
        self.inverted = inverted
        self.bounce = bounce
        self.delay = delay
        if clock:
            self.clock = clock
        else:
            self.clock = self.pyxelClock

        self.debug = True

        self.reset()

    def value(self, integer=False):
        if integer:
            if self.lastValueTime == self.clock():
                return math.floor(self.lastValue)
            newValue = math.floor(self.floatValue())
        else:
            if self.lastValueTime == self.clock():
                return self.lastValue
            newValue = self.floatValue()

        if self.crossingCheck(self.v, self.lastValue, newValue):
            self.catRecentlyDied = True
            if self.targetReachedTime < self.birthTime:
                self.targetReachedTime = self.clock()
            if self.debug:
                True

        if self.debug:
            crossed = self.crossingCheck(50, self.lastValue, newValue)

        self.lastValueTime = self.clock()
        self.penultimateValue = self.lastValue
        self.lastValue = newValue
        return newValue

    def floatValue(self):
        if self.clock() < self.delayedBirthTime:
            return self.offset

        progress = (self.clock() - self.delayedBirthTime) / self.duration

        if self.bounce:
            p = self.bouncingProgress(progress)
        else:
            p = self.normalProgress(progress)

        return self.offset + (self.v - self.offset) * self.function(p)

    def normalProgress(self, p):
        if p >= 1:
            if self.autoreset:
                self.reset()
                p = 0
            else:
                p = 1

        if self.inverted:
            p = 1 - p

        return p

    def bouncingProgress(self, p):
        if p < 1: return p
        pp = math.floor(p)
        if pp % 2 == 1:
            r = 1 - (p - pp)
        else:
            r = p - pp
        return r

    def setValue(self, newVal):
        """
        Change the target value. Can be called at any time.
        """
        self.v = newVal

    def reset(self):
        """
        Reset the birth time, effectively restarting the interpolation.
        """
        self.lastValue = self.offset
        self.birthTime = self.clock()
        self.lastValueTime = self.birthTime
        self.targetReachedTime = self.birthTime - 1
        self.delayedBirthTime = self.birthTime + self.delay
        self.catRecentlyDied = False
        self.catDeathNotified = False
        self.penultimateValue = self.lastValue

    def crossed(self, threshold):
        """
        Returns True if the current value is greater than the threshold argument but last queried value was not.
        threshold: numeric value for the threshold
        """
        if self.debug:
            True
        if self.lastValueTime == self.clock():
            r = self.crossingCheck(threshold, self.penultimateValue, self.lastValue)
        else:
            r = self.crossingCheck(threshold, self.lastValue, self.value())
        return r

    def crossingCheck(self, threshold, lastValue, value):
        """
        Returns True if the value argument is greater than threshold argument but last queried value was not.
        threshold: numeric value for the threshold
        lastValue: value to treat as previously known value
        value: value to check
        NOTE: Not intended for external use as value must be kept in sync with value() calls
        """
        return lastValue < threshold and value >= threshold

    def finished(self):
        if self.bounce: return False
        if self.targetReachedTime <= self.clock() and self.targetReachedTime > 0:
            return True
        return False

    def justFinished(self):
        if self.bounce: return False
        return self.targetReachedTime == self.clock()

    def pyxelClock(self):
        return pyxel.frame_count

#################################################################################

class TimedBool():
    def __init__(self, delay=30, autoreset=False, clock=None):
        """
        delay: delay before which the value becomes True (in frames).
        """
        if clock:
            self.clock = clock
        else:
            self.clock = self.pyxelClock
        self.birthTime = self.clock()
        self.delay = delay
        self.autoreset = autoreset
    def reset(self, delay=0):
        """
        Reset the birth time, effectively restarting the countdown.
        delay: new delay
        """
        if delay > 0:
            self.delay = delay
        self.birthTime = self.clock()

    def value(self):
        if self.clock() > self.birthTime + self.delay:
            if self.autoreset: self.reset()
            return True
        return False

    def true(self):
        return self.value()

    def false(self):
        return not self.value()

    def elapsed(self):
        return self.value()

    def up(self):
        return self.value()

    def pyxelClock(self):
        return pyxel.frame_count
