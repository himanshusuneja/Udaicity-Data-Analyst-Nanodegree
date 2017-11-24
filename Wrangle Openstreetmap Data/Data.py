
# coding: utf-8

# In[5]:


import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint
import csv
import codecs
import pprint
import re
import xml.etree.cElementTree as ET

import cerberus

import schema

OSM_PATH = "new-delhi_india.osm (1)"

street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

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


NODES_PATH = "nodes.csv"
NODE_TAGS_PATH = "nodes_tags.csv"
WAYS_PATH = "ways.csv"
WAY_NODES_PATH = "ways_nodes.csv"
WAY_TAGS_PATH = "ways_tags.csv"

LOWER_COLON = re.compile(r'^([a-z]|_)+:([a-z]|_)+')
PROBLEMCHARS = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

SCHEMA = schema.schema

# Make sure the fields order in the csvs matches the column order in the sql table schema
NODE_FIELDS = ['id', 'lat', 'lon', 'user', 'uid', 'version', 'changeset', 'timestamp']
NODE_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_FIELDS = ['id', 'user', 'uid', 'version', 'changeset', 'timestamp']
WAY_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_NODES_FIELDS = ['id', 'node_id', 'position']


def shape_element(element, node_attr_fields=NODE_FIELDS, way_attr_fields=WAY_FIELDS,
                  problem_chars=PROBLEMCHARS, default_tag_type='regular'):
    
    """Clean and shape node or way XML element to Python dict"""

    node_attribs = {}
    way_attribs = {}
    way_nodes = []
    tags = []  # Handle secondary tags the same way for both node and way elements

    # YOUR CODE HERE
    if element.tag == 'node':

            for node_field in node_attr_fields:
                node_attribs[node_field] =element.attrib[node_field]

            for tag in element.iter('tag'):
                k = tag.attrib['k']

                # ignores tags containing problem characters in the k tag attribute:

                if re.search(PROBLEMCHARS,k):
                    continue
                else:
                    pass

                tag_dict = {}

                tag_dict['id'] = node_attribs['id']

                colon_find = re.split('[:]', k)

                if len(colon_find) == 1:

                    tag_dict['key'] = k
                    tag_dict['type'] = 'regular'  
                    
                elif len(colon_find) == 2:

                    tag_dict['key'] = colon_find[1]
                    tag_dict['type'] = colon_find[0]

                elif len(colon_find) > 2:

                    tag_dict['key'] = ':'.join(colon_find[1:])
                    tag_dict['type'] = colon_find[0]

                tag_dict['value'] = tag.attrib['v']

                tags.append(tag_dict)

            return {'node': node_attribs, 'node_tags': tags}

    elif element.tag == 'way':

        for way_field in way_attr_fields:
            way_attribs[way_field] =element.attrib[way_field]

        for tag in element.iter('tag'):
            k = tag.attrib['k']

            # ignores tags containing problem characters in the k tag attribute:

            if re.search(PROBLEMCHARS,k):
                print "Problem character found - skipping element"
                continue
            else:
                pass

            tag_dict = {}

            tag_dict['id'] = way_attribs['id']

            colon_find = re.split('[:]', k)

            if len(colon_find) == 1:

                tag_dict['key'] = k
                tag_dict['type'] = 'regular'

            elif len(colon_find) == 2:

                tag_dict['key'] = colon_find[1]
                tag_dict['type'] = colon_find[0]

            elif len(colon_find) > 2:

                tag_dict['key'] = ':'.join(colon_find[1:])
                tag_dict['type'] = colon_find[0]

            tag_dict['value'] = tag.attrib['v']
            
            if tag.attrib["k"] == 'addr:street':
                    tag_dict["value"] = update_name(tag.attrib["v"], mapping) 

            tags.append(tag_dict)

        n = 0
        for nd in element.iter('nd'):

            nd_dict = {}

            nd_dict['id'] = way_attribs['id']
            nd_dict['node_id'] = nd.attrib['ref']
            nd_dict['position'] = n
            way_nodes.append(nd_dict)
            n+=1

        return {'way': way_attribs, 'way_nodes': way_nodes, 'way_tags': tags}

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

    
    
def get_element(osm_file, tags=('node', 'way', 'relation')):
    """Yield element if it is the right type of tag"""

    context = ET.iterparse(osm_file, events=('start', 'end'))
    _, root = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            root.clear()


def validate_element(element, validator, schema=SCHEMA):
    """Raise ValidationError if element does not match schema"""
    if validator.validate(element, schema) is not True:
        field, errors = next(validator.errors.iteritems())
        message_string = "\nElement of type '{0}' has the following errors:\n{1}"
        error_string = pprint.pformat(errors)
        
        raise Exception(message_string.format(field, error_string))


class UnicodeDictWriter(csv.DictWriter, object):
    """Extend csv.DictWriter to handle Unicode input"""

    def writerow(self, row):
        super(UnicodeDictWriter, self).writerow({
            k: (v.encode('utf-8') if isinstance(v, unicode) else v) for k, v in row.iteritems()
        })

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)


# ================================================== #
#               Main Function                        #
# ================================================== #
def process_map(file_in, validate):
    """Iteratively process each XML element and write to csv(s)"""

    with codecs.open(NODES_PATH, 'w') as nodes_file,          codecs.open(NODE_TAGS_PATH, 'w') as nodes_tags_file,          codecs.open(WAYS_PATH, 'w') as ways_file,          codecs.open(WAY_NODES_PATH, 'w') as way_nodes_file,          codecs.open(WAY_TAGS_PATH, 'w') as way_tags_file:

        nodes_writer = UnicodeDictWriter(nodes_file, NODE_FIELDS)
        node_tags_writer = UnicodeDictWriter(nodes_tags_file, NODE_TAGS_FIELDS)
        ways_writer = UnicodeDictWriter(ways_file, WAY_FIELDS)
        way_nodes_writer = UnicodeDictWriter(way_nodes_file, WAY_NODES_FIELDS)
        way_tags_writer = UnicodeDictWriter(way_tags_file, WAY_TAGS_FIELDS)

        nodes_writer.writeheader()
        node_tags_writer.writeheader()
        ways_writer.writeheader()
        way_nodes_writer.writeheader()
        way_tags_writer.writeheader()

        validator = cerberus.Validator()

        for element in get_element(file_in, tags=('node', 'way')):
            el = shape_element(element)
            if el:
                if validate is True:
                    validate_element(el, validator)

                if element.tag == 'node':
                    nodes_writer.writerow(el['node'])
                    node_tags_writer.writerows(el['node_tags'])
                elif element.tag == 'way':
                    ways_writer.writerow(el['way'])
                    way_nodes_writer.writerows(el['way_nodes'])
                    way_tags_writer.writerows(el['way_tags'])
 

if __name__ == '__main__':
    # Note: Validation is ~ 10X slower. Thus if Validation is set True then the process will take longer time. Thus it is set False
    process_map(OSM_PATH, validate=False)

