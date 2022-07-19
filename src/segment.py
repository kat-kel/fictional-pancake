from collections import namedtuple
from lxml import etree
import re

NS = {'t':'http://www.tei-c.org/ns/1.0'}
    
class Text:
    def __init__(self, file):
        self.root = etree.parse(file).getroot()
        self.lines = self.line_data()
        self.segments = self.make_segments()

    def line_data(self):
        LineData = namedtuple('LineData', ['xmlid', 'text'])
        data = []
        for line in self.root.findall('.//t:ab//t:lb', namespaces=NS):
            data.append(LineData(line.attrib['corresp'][1:], line.tail))
        return data

    def make_segments(self):
        s = "%%".join([line.text for line in self.line_data()])
        s = re.sub(r"⁊", "et", s)
        s = re.sub(r"[¬|\-]%%", "", s)
        s = re.sub(r"%%", " ", s)
        # break up the string into segments small enough for the segmentation model
        # capture a period and space (group 1) before capital letter or ⁋ (group 2)
        s = re.sub(r"(\.\s)([A-ZÉÀ])", r"\g<1>\n\g<2>", s)
        # capture "Et " if it is not preceded by string beginning
        s = re.sub(r"(?<!\n)Et\s|(?<!\n)⁋|(?<!\n)¶",r"\n\g<0>",s)
        s = re.sub(r"(?<!\n);|(?<!\n)\?|(?<!\n)\!|(?<!\n):",r"\g<0>\n", s)
        string = s.split('\n')
        return string
