import numpy as np
import random

# https://arxiv.org/abs/1703.02702


### Essentially, a wrap around a discrete ball-picker with interactions built in (inverting, racking, re-racking, etc.)
### Once actually tied into the game, this class becomes obsolete because the feedback is coming from observing the game.
### Don't spend too much time on this!
### Still, could be useful for real-time Monte Carlo, assuming game isn't easily solved. Or, perhaps adapt into an explicit
### player model of the shotgun rack. You do need a way to encode the phone and magnifying glass info, after all
class Shotgun:

    ### Perhaps can model Shotgun as a shifting Bernoulli distribution. Phone and magnifying glass info fix p=1 for
    ### certain samples
    def __init__(self, blanks, lives):
        # Rack the shotgun in a random order
        self.mag = [0]*blanks + [1]*lives
        random.shuffle(self.mag)

    def rack(self):
        # Remove the first shell and reveal its state
        return self.mag.pop(0)
    
    def invert(self):
        self.mag[0] = 1-self.mag[0]  # simple math

### Table class, defines players, shotgun rack and (hidden) order, and acts as the "game master"
### maybe gives rewards to the agents?
class Table:
    
    def __init__(self):
        self.shotgun = Shotgun()  # <- no need for a shotgun model if we just observe?