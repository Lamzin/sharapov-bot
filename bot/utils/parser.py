# -*- coding: utf-8

import re


class Parser(object):

    LEVEL = ur'<P ALIGN=CENTER>.*</P><BR>'
    FLOWER_IMG = ur'<IMG SRC="./\d.gif" BORDER=0>'
    FLOWER_EXIST = u'./1.gif'
    FLOWER_DOES_NOT_EXIST = u'./0.gif'

    def __init__(self):
        self.level = None
        self.flowers = None

    def parse(self, html):
        self.flowers = 0
        flower_images = re.findall(Parser.FLOWER_IMG, html)
        for flower_image in flower_images:
            self.flowers *= 2
            if Parser.FLOWER_EXIST in flower_image:
                self.flowers += 1

        level_tag = re.findall(Parser.LEVEL, html)[0]
        self.level = int(re.findall(ur'\d', level_tag)[-1])
