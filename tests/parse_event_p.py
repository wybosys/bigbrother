#!/usr/bin/env python3

import pyparsing as pp
import json

test = """
add device 1: /dev/input/event7
  name:     "sdm660-snd-card-cdp Button Jack"
  events:
    KEY (0001): 0072  0073  00e2 
        SW  (0005): 0002  0004  0006  0007  000f  0010  0012 
    ABS (0003): 0000  : value 0, min 0, max 1079, fuzz 0, flat 0, resolution 0
                0001  : value 0, min 0, max 2279, fuzz 0, flat 0, resolution 0
                0019  : value 0, min 0, max 255, fuzz 0, flat 0, resolution 0  
  input props:
    <none>
"""

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

class EventInfo:    
    TYPE_UNKNOWN = 0
    TYPE_KEY = 1
    TYPE_ABS = 2
    TYPE_SW = 3
    def __init__(self):
        super().__init__()
        self.type = EventInfo.TYPE_UNKNOWN
        self.type_value = 0

class EventInfoKey(EventInfo):
    def __init__(self):
        super().__init__()
        self.values = []

class EventInfoAbsValue:
    def __init__(self):
        super().__init__()
        self.value = 0
        self.min = 0
        self.max = 0
        self.fuzz = 0
        self.flat = 0
        self.resolution = 0

    def __repr__(self):
        print('value %d, min %d, max %d, fuzz %d, flat %d, resolution $d' % (self.value, self.min, self.max, self.fuzz, self.flat, self.resolution))
        return ''

class EventInfoAbs(EventInfo):
    def __init__(self):
        super().__init__()
        self.value = ''
        self.values = {}

    def __repr__(self):      
        print('ABS (%s):' % self.value)
        print(self.values)
        return ''

class EventInfoSw(EventInfo):
    def __init__(self):
        super().__init__()
        self.value = ''
        self.values = []

    def __repr__(self):
        print('SW (%s):' % self.value)
        print(self.values)
        return ''

class EventInfoInputProps:    
    INPUT_PROP_DIRECT = 1

class EventDevice:
    def __init__(self):
        super().__init__()
        self.index = 0
        self.path = ''
        self.name = ''
        self.events = {}
        self.input_props = None

    def __repr__(self):
        print('device %d: %s' % (self.index, self.path))
        print('name: %s' % self.name)
        print('events:')
        for k in self.events:
            print(self.events[k])
        print('input props:')
        print(self.input_props)        
        return ''

    def parse(self, str):
        t = devices()        
        t.skipWhitespace = True                
        try:
          ret = t.parseString(str)
          print(ret)
        except:
          raise
          return False
        return True

# 构造ebnf解析器
integer = pp.Word(pp.nums)
hex = pp.Word(pp.nums + 'abcdef')
path = pp.Word(pp.alphanums + '/')
key = pp.Word(pp.alphanums)

info_name = 'name:' + pp.QuotedString('"')
info_value = pp.Suppress('(') + hex + pp.Suppress(')')

info_event_key = 'KEY' + info_value + pp.Suppress(':') + pp.Group(pp.OneOrMore(hex))
info_event_sw = 'SW' + info_value + pp.Suppress(':') + pp.OneOrMore(hex)
info_event_abs_value = key + integer + pp.Suppress(pp.Optional(','))
info_event_abs_values = hex + pp.Suppress(':') + pp.Group(pp.OneOrMore(pp.Group(info_event_abs_value)))
info_event_abs = 'ABS' + info_value + pp.Suppress(':') + pp.OneOrMore(pp.Group(info_event_abs_values))
info_event = info_event_key | info_event_sw | info_event_abs
info_events = pp.Suppress('events:') + pp.Group(pp.ZeroOrMore(pp.Group(info_event)))

input_prop_value = '<none>' | pp.Word(pp.string.ascii_uppercase + '_')
input_props = 'input props:' + input_prop_value

infos = pp.Suppress(info_name) + pp.Group(info_events) + input_props
device = pp.Suppress('add device') + integer + pp.Suppress(':') + path + infos
devices = pp.OneOrMore(pp.Group(device))

ed = EventDevice()
if ed.parse(data):
    print(ed)
else:
    print("解析失败")
