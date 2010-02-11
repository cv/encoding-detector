#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os
import chardet.universaldetector

def detect(filename):
    detector = chardet.universaldetector.UniversalDetector()
    for line in file(filename, 'rb'):
        detector.feed(line)
        if detector.done: break
    detector.close()
    result = detector.result
    result['filename'] = filename
    return result

def main(argv):
    if len(argv) < 2:
        print "Usage %s path1 [path2] [path3] ..." % argv[0]
        return -2

    results = []
    for d in argv[1:]:
        for root, dirs, files in os.walk(d):
            for e in dirs:
                if e[0] == '.':
                    dirs.remove(e)
            for f in files:
                if f[0] == '.':
                    files.remove(f)
            for name in files:
                results.append(detect(os.path.join(root, name)))

    errors = 0
    for result in results:
        if (not result['encoding'] in ('ascii', 'utf-8')) or result['confidence'] < 0.85: 
            errors = -1
            print "File %(filename)s is reporting as %(encoding)s with confidence %(confidence)f" % result

    if errors != 0:
        print "FAILED Encoding Detection. Perhaps you need to add the following to your template to help the detector:"
        print u"$! hêlp UTF-8 dætæctiõñ: ãå∫ß !$"

    print "Checked %d files" % len(results)
    return errors

if __name__ == "__main__":
    sys.exit(main(sys.argv))
