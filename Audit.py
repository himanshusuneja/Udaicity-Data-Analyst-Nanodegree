
# coding: utf-8

# In[1]:


import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

FILE = "new-delhi_india.osm (1)"
regex = re.compile(r'\b\S+\.?', re.IGNORECASE)

expected = ["New Delhi", "Indian", "ATM", "Cinema", "Street", "State", "Country", "Land Use", "Society", "Feet", "Road", "Lane", "Republic", "Marg", "Jogabai"] #expected names in the dataset

mapping = {"New delhi": "New Delhi",
           "India Oil": "Indian Oil",
           "atm": "ATM",
           "cinames.": "Cinema",
           "cinema": "Cinema",
           "state": "State",
           "country": "Country",
           "landuse": "Land Use",
           "road": "Road",
           "Ft.": "Feet",
           "ft": "Feet",
           "rasta": "Road",
           "Roads": "Road",
           "society": "Society",
           "soc.": "Society",
           "Mg": "Marg",
           "Ln": "Lane",
           "Republik": "Republic",
           "JOgabai": "Jogabai"
            }

# Search string for the regex. If it is matched and not in the expected list then add this as a key to the set.
def audit_street(street_types, street_name): 
    m = regex.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)

def is_street_name(elem): # Check if it is a street name
    return (elem.attrib['k'] == "addr:street")

def audit(FILE): # return the list that satify the above two functions
    osm_file = open(FILE, "r")
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street(street_types, tag.attrib['v'])

    return street_types

pprint.pprint(dict(audit(FILE))) # print the existing names

def string_case(s): # change string into titleCase except for UpperCase
    if s.isupper():
        return s
    else:
        return s.title()

# return the updated names
def update_name(name, mapping):
    unlisted = {}
    m = street_type_re.search(name)
    if m:
        street_type = m.group()
        if street_type in mapping.keys():
            name = re.sub(street_type, mapping[street_type], name)
        else:
            unlisted[street_type] = name
    return name

update_street = audit(FILE) 

# print the updated names
for street_type, ways in update_street.iteritems():
    for name in ways:
        better_name = update_name(name, mapping)
        print name, "=>", better_name  

