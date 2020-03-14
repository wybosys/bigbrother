# -*- coding:utf-8 -*-

import pyparsing as pp

def hex2dec(str):
    return int('0x' + str, 16)

def dec2hex(v):
    return '%04x' % v

def list_hex2dec(l):
    return [hex2dec(e) for e in l]

def list_dec2hex(l):
    return [dec2hex(e) for e in l]

class EventInfo:    
    TYPE_UNKNOWN = 0
    TYPE_KEY = 1
    TYPE_ABS = 2
    TYPE_SW = 3

    def __init__(self):
        super().__init__()
        self.type = EventInfo.TYPE_UNKNOWN
        self.type_value = 0

    def read(self, d):
        self.type_value = hex2dec(d[1])

    @staticmethod
    def Read(d):
        #print(d)
        typ = d[0]
        r = None
        if typ == 'KEY':
          r = EventInfoKey()
        if typ == 'SW':
          r = EventInfoSw()
        elif typ == 'ABS':
          r = EventInfoAbs()
        if r.read(d):
            return r
        return None

class EventInfoKey(EventInfo):
    def __init__(self):
        super().__init__()
        self.type = EventInfo.TYPE_KEY
        self.values = []

    def read(self, d):
        super().read(d)
        self.values = list_hex2dec(d[2])
        return True

    def __repr__(self):      
        print('KEY (%s):' % dec2hex(self.type_value))
        print(list_dec2hex(self.values))
        return ''
        
class EventInfoAbsValue:
    def __init__(self):
        super().__init__()
        self.key = ''
        self.value = 0
        self.min = 0
        self.max = 0
        self.fuzz = 0
        self.flat = 0
        self.resolution = 0

    def __repr__(self):
        print('key %s: value %d, min %d, max %d, fuzz %d, flat %d, resolution %d' % (self.key, self.value, self.min, self.max, self.fuzz, self.flat, self.resolution))
        return ''

    def read(self, d):
        #print(d)
        self.key = d[0]
        for e in d[1]:
          k = e[0]
          v = int(e[1])
          if hasattr(self, k):
            setattr(self, k, v)
        return True

class EventInfoAbs(EventInfo):
    def __init__(self):
        super().__init__()
        self.type = EventInfo.TYPE_ABS
        self.values = {}

    def __repr__(self):      
        print('ABS (%s):' % dec2hex(self.type_value))
        print(self.values)
        return ''

    def read(self, d):
        #print(d)
        super().read(d)
        for e in d[2]:
          r = EventInfoAbsValue()
          if r.read(e):
            self.values[r.key] = r
        return True

class EventInfoSw(EventInfo):
    def __init__(self):
        super().__init__()
        self.type = EventInfo.TYPE_SW
        self.values = []

    def __repr__(self):
        print('SW (%s):' % self.value)
        print(list_dec2hex(self.values))
        return ''

    def read(self, d):
        super().read(d)
        self.values = list_hex2dec(d[2])
        return True

class EventDevice:
    def __init__(self):
        super().__init__()
        self.clear()

    def __repr__(self):
        print('device %d: %s' % (self.index, self.path))
        print('name: %s' % self.name)
        print('events:')
        for k in self.events:
            print(self.events[k])
        return ''

    def clear(self):
        self.index = 0
        self.path = ''
        self.name = ''
        self.events = {}
        self.input_props = ''

    def read(self, d):
        self.index = int(d[0])
        self.path = d[1]
        self.name = d[2]
        for r in d[3]:
          e = EventInfo.Read(r)
          if e:
            self.events[e.type] = e
        self.input_props = d[4]   
        return True 

class EventDevices:
    def __init__(self):
        super().__init__()
        self.clear()

    def clear(self):
        self.devices = {}

    def parse(self, str):
        t = devices()        
        t.skipWhitespace = True                
        try:
          ret = t.parseString(str)
          #print(ret)
          # 转换list数据为结构数据          
          for rd in ret:
            d = EventDevice()
            if d.read(rd):
              self.devices[d.index] = d
        except:
          raise
          return False
        return True

    def __repr__(self):
        print(self.devices)
        return ''

# 构造ebnf解析器
integer = pp.Word(pp.nums)
hex = pp.Word(pp.nums + 'abcdef')
path = pp.Word(pp.alphanums + '/')
key = pp.Word(pp.alphanums)

info_name = pp.Suppress('name:') + pp.QuotedString('"')
info_value = pp.Suppress('(') + hex + pp.Suppress(')')

info_event_key = 'KEY' + info_value + pp.Suppress(':') + pp.Group(pp.OneOrMore(hex))
info_event_sw = 'SW' + info_value + pp.Suppress(':') + pp.OneOrMore(hex)
info_event_abs_value = key + integer + pp.Suppress(pp.Optional(','))
info_event_abs_values = hex + pp.Suppress(':') + pp.Group(pp.OneOrMore(pp.Group(info_event_abs_value)))
info_event_abs = 'ABS' + info_value + pp.Suppress(':') + pp.Group(pp.OneOrMore(pp.Group(info_event_abs_values)))
info_event = info_event_key | info_event_sw | info_event_abs
info_events = pp.Suppress('events:') + pp.Group(pp.OneOrMore(pp.Group(info_event)))

input_prop_value = '<none>' | pp.Word(pp.string.ascii_uppercase + '_')
input_props = pp.Suppress('input props:') + pp.OneOrMore(input_prop_value)

infos = info_name + info_events + pp.Group(input_props)
device = pp.Suppress('add device') + integer + pp.Suppress(':') + path + infos
devices = pp.OneOrMore(pp.Group(device))
