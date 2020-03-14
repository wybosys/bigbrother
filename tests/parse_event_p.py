#!/usr/bin/env python3

import pyparser

data = """
add device 1: /dev/input/event7
  name:     "sdm660-snd-card-cdp Button Jack"
  events:
    KEY (0001): 0072  0073  00e2 
  input props:
    INPUT_PROP_ACCELEROMETER
add device 2: /dev/input/event6
  name:     "sdm660-snd-card-cdp Headset Jack"
  events:
    SW  (0005): 0002  0004  0006  0007  000f  0010  0012 
  input props:
    <none>
add device 3: /dev/input/event4
  name:     "goodixfp"
  events:
    KEY (0001): 0066  0073  0074  008b  009e  00d4  00d8  00d9 
                00fe  0253  0254  0255  0256  0257 
  input props:
    <none>
add device 4: /dev/input/event5
  name:     "gpio-keys"
  events:
    KEY (0001): 0073 
  input props:
    <none>
add device 5: /dev/input/event3
  name:     "synaptics_dsx_proximity_3706"
  events:
    KEY (0001): 0145  014a 
    ABS (0003): 0000  : value 0, min 0, max 1079, fuzz 0, flat 0, resolution 0
                0001  : value 0, min 0, max 2279, fuzz 0, flat 0, resolution 0
                0019  : value 0, min 0, max 255, fuzz 0, flat 0, resolution 0
  input props:
    INPUT_PROP_DIRECT
add device 6: /dev/input/event0
  name:     "qpnp_pon"
  events:
    KEY (0001): 0072  0074 
  input props:
    <none>
add device 7: /dev/input/event1
  name:     "vivo_ts"
  events:
    KEY (0001): 0011  0012  0018  001e  0021  002e  0032  0067 
                0069  006a  008b  008f  009e  00ac  00f9  00fa 
                00fc  00fe  0145  014a  02ea 
    ABS (0003): 002f  : value 0, min 0, max 9, fuzz 0, flat 0, resolution 0
                0030  : value 0, min 0, max 255, fuzz 0, flat 0, resolution 0
                0035  : value 0, min 0, max 1079, fuzz 0, flat 0, resolution 0
                0036  : value 0, min 0, max 2279, fuzz 0, flat 0, resolution 0
                0039  : value 0, min 0, max 10, fuzz 0, flat 0, resolution 0
                003a  : value 0, min 0, max 255, fuzz 0, flat 0, resolution 0
  input props:
    INPUT_PROP_DIRECT
add device 8: /dev/input/event2
  name:     "synaptics_3706"
  events:
    KEY (0001): 008f  0145  014a 
    ABS (0003): 0000  : value 0, min 0, max 1079, fuzz 0, flat 0, resolution 0
                0001  : value 0, min 0, max 2279, fuzz 0, flat 0, resolution 0
                002f  : value 0, min 0, max 9, fuzz 0, flat 0, resolution 0
                0030  : value 0, min 0, max 255, fuzz 0, flat 0, resolution 0
                0031  : value 0, min 0, max 255, fuzz 0, flat 0, resolution 0
                0035  : value 0, min 0, max 1079, fuzz 0, flat 0, resolution 0
                0036  : value 0, min 0, max 2279, fuzz 0, flat 0, resolution 0
                0039  : value 0, min 0, max 65535, fuzz 0, flat 0, resolution 0
  input props:
    INPUT_PROP_DIRECT
could not get driver version for /dev/input/mouse0, Not a typewriter
could not get driver version for /dev/input/mice, Not a typewriter
could not get driver version for /dev/input/mouse1, Not a typewriter
"""

