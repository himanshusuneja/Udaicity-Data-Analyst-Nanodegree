
# coding: utf-8

# In[1]:


#!/usr/bin/env python

import xml.etree.cElementTree as ET
import pprint
import re


lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

MAP = "new-delhi_india.osm (1)"

def key_type(element, keys):
    if element.tag == "tag":
        if lower.search(element.attrib['k']):
            keys['lower'] = keys['lower'] + 1
        elif lower_colon.search(element.attrib['k']):
            keys['lower_colon'] = keys['lower_colon'] + 1
        elif problemchars.search(element.attrib['k']):
            print element.attrib['k']
            keys['problemchars'] = keys['problemchars'] + 1
        else:
            keys['other'] = keys['other'] + 1
        pass
        
    return keys



def process_map(filename):
    keys = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0}
    for _, element in ET.iterparse(filename):
        keys = key_type(element, keys)

    return keys

pprint.pprint(process_map(MAP))

