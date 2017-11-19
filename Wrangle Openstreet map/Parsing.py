
# coding: utf-8

# In[2]:


import xml.etree.cElementTree as ET
import pprint


OSMFILE = "new-delhi_india.osm (1)"

def count_tags(filename):
    tags = {}
    for event, elem in ET.iterparse(filename):
        if elem.tag in tags: 
            tags[elem.tag] += 1
        else:
            tags[elem.tag] = 1
    return tags
    
pprint.pprint(count_tags(OSMFILE))

