#!/usr/bin/env python3

import sys, os
import cv2 as cv

class Case:

    def __init__(self):
        super().__init__()
        self.processed = None
        self.passed = False

    def process(self):
        return self

    def show(self):
        if self.processed is None:
            print('没有设置处理结果')
            return
        winnm = 'result'        
        if type(self.processed) == list:
            l = len(self.processed)
            if l == 0:
                print('没有设置处理结果')
                return
            for i in range(l):
                nm = '%s_%d' % (winnm, i)
                cv.namedWindow(nm, cv.WINDOW_AUTOSIZE) 
                cv.imshow(nm, self.processed[i])
        else:
            cv.namedWindow(winnm, cv.WINDOW_AUTOSIZE) 
            cv.imshow(winnm, self.processed)
        cv.waitKey(0)
        cv.destroyAllWindows()

class FindPattern(Case):

    def __init__(self, pat, src):
        super().__init__()
        self._pat = pat
        self._src = src
        # 判定相关系数
        self.factor = 0.1

    def process(self):
        src = cv.imread(self._src, 0)
        pat = cv.imread(self._pat, 0)
        th,tw = pat.shape[:2]

        src = 255 - src
        pat = 255 - pat
        
        mth = cv.TM_CCOEFF_NORMED
        res = cv.matchTemplate(src, pat, mth)

        mv, xv, ml, xl = cv.minMaxLoc(res)
        if mth == cv.TM_SQDIFF_NORMED:
            tl = ml
        else:
            tl = xl        

        self.passed = (1 - xv) < self.factor        
        if self.passed:            
            self.region = (tl[0], tl[1], tw, th)        
        else:
            self.region = None        
        return self

    def show(self):
        tmp = cv.imread(self._src)
        if self.passed:        
            tl = (self.region[0], self.region[1])
            br = (self.region[0] + self.region[2], self.region[1] + self.region[3])
            tmp = cv.rectangle(tmp, tl, br, (0,0,255), 2)
        tmp = cv.resize(tmp, (600, 800))
        self.processed = tmp
        super().show()        

if __name__ == "__main__":
    pat = sys.argv[1]
    src = sys.argv[2]
    if not os.path.exists(pat):
        print('找不到文件 %s' % pat)        
    if not os.path.exists(src):
        print('找不到文件 %s' % src)

    c = FindPattern(pat, src)
    c.process()
    print(c.region)
    c.show()
