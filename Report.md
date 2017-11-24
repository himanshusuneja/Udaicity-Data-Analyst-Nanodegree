

```python

# Project 3: OpenStreetMap Data Wrangling with SQL

**Name:** Himanshu Suneja

**Map Area**: New Delhi as it's my Home town

* Location: New Delhi, India
* [MapZen URL](https://s3.amazonaws.com/metro-extracts.mapzen.com/new-delhi_india.osm.bz2)

# 1. Data Audit
### Unique Tags
In this file, i did iterate parsing through different tags in XML file and bundled all unique tags in thier respective tag named dictionaries

* `'bounds': 1`
* `'member': 28524,`
* `'nd': 4240871,`
* `'node': 3429725,`
* `'osm': 1,`
* `'relation': 6230,`
* `'tag': 830280,`
* `'way': 696006`

### Patterns in the Tags
Using 'tags.py' 4 expressions were created to check certain patterns in tags. Each tags categories was counted as below

*  `"lower" : 814008`, for tags that contain only lowercase letters and are valid,
*  `"lower_colon" : 15845`, for otherwise valid tags with a colon in their names,
*  `"problemchars" : 421`, for tags with problematic characters, and
*  `"other" : 421`, for other tags that do not fall into the other three categories.

# 2. Problems Encountered in the Map
###Street address inconsistencies
Theere were many inconsistencies with names in the file. Below is the old name corrected with the better name. Using `audit.py`, i updated the names.
 

* **Abbreviations** 
    * `Ln -> Lane`
* **LowerCase**
    * `state -> State`
* **Misspelling**
    * `Republik -> Republic`
* **Hindi names**
    * `rasta -> Road`
* **UPPER CASE words**
    * 'atm -> ATM'


### City name inconsistencies
Using `audit.py`, updated the names

* **LowerCase**
	* `New delhi -> New Delhi`


#3. Data Overview
### File sizes:

* `new-delhi_india.osm (1): 720.8 MB`
* `nodes_csv: 275.7 MB`
* `nodes_tags.csv: 1.56 MB`
* `ways_csv: 40.89 MB`
* `ways_nodes.csv: 101.4 MB`
* `ways_tags.csv: 25.2 MB`
* `new-delhi_india.osm (1)_db.sqlite: 78.5 MB`

###Number of nodes:
``` python
'SELECT COUNT(*) FROM nodes'
```
**Output:**
```
3429725
```
###Number of unique users:
```python
'SELECT COUNT(DISTINCT e.uid) FROM \
(SELECT uid FROM nodes UNION ALL SELECT uid FROM ways) e'
```
**Output:**
```
1564
```

### Number of ways:
```python
'SELECT COUNT(*) FROM ways'
```
**Output:**
```
696006
```

###Number of most contrubuting users:
```python
'SELECT e.user, COUNT(*) as num FROM \
(SELECT user FROM nodes UNION ALL SELECT user FROM ways) e\
GROUP BY e.user \
ORDER BY num DESC \
LIMIT 10'
```
**Output:**    
    
```
Oberaffe			270150
premkumar			164029
saikumar			159904
Naresh08			136219
anushap				133366
sdivya				129895
anthony1			125805
himabindhu			122724
sathishshetty		122238
Apreethi			113991
```

###Number of users contributing only once:
```python
'SELECT COUNT(*) FROM \
(SELECT e.user, COUNT(*) as num FROM \
(SELECT user FROM nodes UNION ALL SELECT user FROM ways) e\
GROUP BY e.user \
HAVING num = 1) u'
```
**Output:**
```
428
```

###Top 10 amenities:
```python
'SELECT value, COUNT(*) as num FROM nodes_tags\
WHERE key="amenity" \
GROUP BY value \
ORDER BY num DESC \
LIMIT 10'

```
**Output:**
```
restaurant			225
atm					229
fuel				228
place_of_worship	204
bank				189
school				165
fast_food			135
parking				93
cafe				88
hospital			88
```


# 4. Additional Data Exploration

###List of postalcodes
```python
'SELECT e.value, COUNT(*) as num FROM \
(SELECT value FROM nodes_tags WHERE key="postcode"\
UNION ALL SELECT value FROM ways_tags WHERE key="postcode") e \
GROUP BY e.value \
ORDER BY num DESC \
LIMIT 10'
```
**Output:**
```
110087		509
122001		101
110092		65
100006		59
110010		58
110075		58
201301		56
110085		37
110042		36
110021		31

```
###Top 5 cusines
```python
"SELECT nodes_tags.value, COUNT(*) as num \
FROM nodes_tags \
JOIN (SELECT DISTINCT(id) FROM nodes_tags WHERE value='restaurant') AS restaurants \
ON nodes_tags.id = restaurants.id \
WHERE nodes_tags.key = 'cuisine' \
GROUP BY nodes_tags.value \
ORDER BY num DESC \
LIMIT 5"
```
**Output:**
```
indian				25
regional			11
pizza				8
North_Indian		5
chinese				5
```

### Top 5 Banks
'''python
"SELECT nodes_tags.value, COUNT(*) as num \
                            FROM nodes_tags \
                            JOIN (SELECT DISTINCT(id) FROM nodes_tags WHERE value='bank') AS bank \
                            ON nodes_tags.id = bank.id \
                            WHERE nodes_tags.key = 'name' \
                            GROUP BY nodes_tags.value \
                            ORDER BY num DESC \
                            LIMIT 5
'''
**Output**
'''
State Bank of India		23
ICICI Bank				16
HDFC Bank				14
Punjab National Bank	11
Axis Bank				9

'''

# 5. Conclusion
'''
The openstreetmap data of New Delhi is quite big and was fun to work with as i am the resident of this place. Although the data was very aptly written with few typo errors.
I tried to address and clean the data to sum amount. There was very less additional information about tourist attractions, trending places,
and capital attraction places given that New Delhi is the capital of the country 
'''

### Anticipated Problems
'''
To do data wrangling in this project is very time-consuming as it is complicated due many inconsitencies in data.i have spotted few of them 
and perform data wrangling on them, but given so many inconsistencies this data has more errors.

Gamification is one of the methods which can help to motivating top contributing users to provide more accuracy and quality in data.
This gamification, though, needs to apply OpenStreetMap best practices so that the data submitted has less inconsistencies.
'''

#### More information
'''
* We can develope a mechanism or script so that tha Hindi language used in the data can match up the english language
* Although there will be few challenges in implementing it such as translation errors but same can be countered using google transaltion or by an interpreterer.
* There can be some neagtive impact on data as many hindi origin word does not have english write up.
'''
### Benifits
'''
* Developing such kind of word translation scripts will not only reduce cleaning but also becomes a time saving and provide more accurate data.                      
'''

# Files
* `Quiz/` : scripts completed in lesson Case Study OpenStreetMap
* `README.md` : this file
* `sample.osm`: sample data of the OSM file
* `audit.py` : audit street, city and update their names
* `data.py` : build CSV files from OSM and also parse, clean and shape data
* `database.py` : create database of the CSV files
* `Parsing.py` : find unique tags in the data
* `query.py` : different queries about the database using SQL
* 'Report.html' : HTML file of the report                      
* `tags.py` : count multiple patterns in the tags
* `Sample+OSM` : Sample code to create sample data    
```


```


    ---------------------------------------------------------------------------

    KeyboardInterrupt                         Traceback (most recent call last)

    <ipython-input-7-d403319321b6> in <module>()
         55     return street_types
         56 
    ---> 57 pprint.pprint(dict(audit(OSMFILE_sample))) # print the existing names
         58 
         59 def string_case(s): # change string into titleCase except for UpperCase
    

    <ipython-input-7-d403319321b6> in audit(osmfile)
         46     osm_file = open(osmfile, "r")
         47     street_types = defaultdict(set)
    ---> 48     for event, elem in ET.iterparse(osm_file, events=("start",)):
         49 
         50         if elem.tag == "node" or elem.tag == "way":
    

    <string> in next(self)
    

    KeyboardInterrupt: 

