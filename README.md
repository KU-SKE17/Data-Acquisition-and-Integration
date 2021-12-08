# DAQ Summary

![img](https://i.ibb.co/NrXdkBt/Screen-Shot-2564-12-08-at-12-57-50.png)

# (slide7) Data Collection

## Add primary data to database

### 1. create database

- add `id` [INT] -> Index/Key: `Primary`, Extra: `AUTO_INCREMENT`

- add `ts` [TIMESTAMP] -> Default: `CURRENT_TIMESTAMP`

- add other fields (data, lat, lot [Float])

### 2. create node-red

1. subscribe mqtt - set `mqtt in` node

   - `Server` = mqtt-broker: Server = iot.cpe.ku.ac.th
   - `Topic` = ku/daq2021/6210545505/xxx (whatever)
   - `QoS` = 0
   - `Output` = a parsed JSON object

2. map data to database - use template to insert data (sql)

   ```sql
   INSERT INTO <table_name> (lat, lon, temp)
   VALUES (
      {{payload.temperature}},
      {{payload.lat}},
      {{payload.lon}},
   )
   ```

3. connect database - set `Database` in `mysql` nod

   - `Host` = iot.cpe.ku.ac.th
   - `User` = b62xxxxxxxx
   - `Password` = email@ku.th
   - `Database` = b62xxxxxxxx (database name)

### 3. publish mqtt data from kidbright

```py
import json

 data = {
   "temperature": kb.temperature(),
   "lat": 13.7751376,
   "lon": 100.6119336
 }

 mqtt.publish(UNIQUE_ID, json.dumps(data))
```

## Add secondary data to database

### 1. create database (same as `primary source`)

- maybe set `ts` without default

### 2. create node-red

1. start with `inject` node

2. set `http request` node

   - `URL` = http://xxxxxxx (some-api)
   - if URL return JSON:
     - `Output` = a parsed JSON object
   - if URL return XML:
     - `Output` = a UTF-8 string
     - then add `xml` node after

3. set `delay` node

   - looping around `http request` node

4. map data to database (same as `primary source`)

5. connect database (same as `primary source`)

### 3. start node-red looping

## Add web scraping to database

### Web Scraper extension Usage

1. Open Chrome’s Developer Tools, select `Web Scraper`
2. `Create new Sitemap`, set `Sitemap name`, paste the `Start URL`
3. `Add new selector`, add
   - id: name of that indices (\*`column` or `row`)
   - Type = Text (default)
4. Click `Select` btn, click 2 indices on the website
5. make sure `Multiple` checked
6. check `Data preview`, copy Selector code
7. save!

### Web Scraper using Python

```python
values = soup.select(".col-md-8 td:nth-of-type(2)")
print(values)
# [<td>1,616.82</td>, <td>962.16</td>, <td>2,202.34</td>, <td>1,062.27</td>, <td>1,019.87</td>, <td>1,128.36</td>, <td>1,012.94</td>, <td>943.35</td>, <td>567.99</td>]

values = [
   # get only text, remove ',', and cast to float
   float(s.text.replace(",", ""))
   for s in soup.select(".col-md-8 td:nth-of-type(2)")
]
print(values)
# [1616.85, 962.34, 2202.54, 1062.17, 1020.04, 1128.39, 1013.19, 943.52, 567.29]
```

#### ex. settrade (using chrome's Web Scraper extension)

```python
import requests
from bs4 import BeautifulSoup

response = requests.get("https://www.settrade.com/C13_MarketSummary.jsp")
soup = BeautifulSoup(response.text, "html.parser")

# extract indices; also strip out wrapping whitespaces
indices = [s.text.strip() for s in soup.select(".col-md-8 a")]

# extract values; get rid of ',' and convert to numbers
values = [
    float(s.text.replace(",", ""))
    for s in soup.select(".col-md-8 td:nth-of-type(2)")
]

for idx, val in zip(indices, values):
    print(f"{idx} : {val}")
```

#### ex. carbonster (raw)

```python
import requests
from bs4 import BeautifulSoup
import pymysql as mysql
from config import DB_HOST, DB_USER, DB_PASSWD, DB_NAME

# set up html
URL = "https://www.worldometers.info/world-population/population-by-country/"
page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser")

# find scraping
results = soup.find("tbody")
row = results.find_all("tr")

insert_arr = []
for element in row:
   row_list = []
   country = element.find("a")
   country = country.text
   pop = element.find_all("td")[2]
   pop = pop.text
   pop = pop.replace(",", "")
   row_list.insert(0, country)
   row_list.insert(1, int(pop))
   row_list.insert(2, 2020)
   insert_arr.append(tuple(row_list))

print(insert_arr)

# set up database connect
connect = mysql.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWD, db=DB_NAME)
cursor = connect.cursor()

# execute database sql
cursor.execute("DELETE FROM population")
sql_q = """insert into population (country, population, year)
             values(%s, %s, %s)"""
cursor.executemany(sql_q, insert_arr)

# save
connect.commit()
```

### Web Scraper using Node-RED

1. start with `inject` node

2. set `http request` node

   - `URL` = Start URL

3. set `html` node

   - `Selector` = Selector code (from Web Scraper)

4. add `debug` node

## OpenRefine

- Data Transformation
  - Pivoting/unpivoting (transposition)
  - Mapping
  - Joining
  - Aggregating
- (เจอ) Messy Data
  - contains inconsistency
- (แก้ด้วย) Data Cleaning
  - มี tool ชื่อ `OpenRefine`

### OpenRefine Usage

- `Faceting` -> grouping and sorting text in that column (find misspell, case sensitive)
- `Clustering` -> from Faceting click Cluster btn(top right) (auto suggest for editing)
- `Transposition` -> switch position of row and column
- `Cells Transforming` -> update value using programming language
- Other:
  - Convert Type: using transform
  - Find and fix anomalies in the income values: using numeric facet
  - `Export` data to a csv file
  - `Import` data into a database (normalize as needed)

# (slide8) Data Integration

- Exchanging Data
- Copying Data
- Moving & Transforming Data

### 3 Data Integration Types

- `A2A`/`B2B` (Application to Application)
  - ATM Transactions
  - Hotel/Flight Booking
- `Database Replication/Mirroring`
  - DB Backup
  - DB Migration
  - Disaster Recovery Backup
- `ETL` (Extract-Transform-Load)
  - Data Warehouse
  - Data Analysis
  - Archiving
  - Purging

Each of them demands:

- different `Requirements`
- different `Architecture`
- different `Design Patterns`
- different `set of Challenges`
- different `Skill Sets`

So the `tools` are usually `specific only to one` type

## Data Integration Architectures

There are variety of possible architectures between `Warehousing` and `Virtual Integration`

- (from) `Data Sources`

  - SQL capabilities
  - XML databases with an XQuery interface
  - HTML

- (using) `Wrappers` - Communicate with the data sources

  - `Send` queries to a data source
  - `Receive` answers
  - possibly apply some basic transformations on the answer

- (and using) `Source Descriptions`

  - Connects the `mediated schema` and the `schemas of the sources`
  - Specify how attributes in the sources correspond to attributes in the mediated schema

- (to store data at) `Mediated Schema` or `Warehouse`

  - Interacts with the data integration system through `a single schema`
  - Contains `only the aspects of the domain` that are relevant to the application

## Query Processing

### Query Reformulation

- Reformulate the query into queries that refer to the
  schemas of the data sources
- Result: a set of queries (`logical query plan`)

### Query Optimization

- Takes as input a logical query plan and produces a `physical query` plan
- (decide which join algorithm to use)

### Query Execution

- Responsible for the `actual executio`n of the physical query plan
- Dispatches the queries to the individual sources through the wrappers
- Combines the results as specified by the query plan

```sql
-- sum every 6 hours
SELECT avg(pm25) as value, CONCAT(DATE(ts),' 00:00:00') as time, 'pm25' as sensor
FROM aqi
WHERE
  TIME(ts) BETWEEN '00:00' AND '05:59'
GROUP BY time

-- need 4 UNION a day
UNION

SELECT avg(pm25) as value, CONCAT(DATE(ts),' 06:00:00') as time, 'pm25' as sensor
FROM aqi
WHERE
  TIME(ts) BETWEEN '06:00' AND '11:59'
GROUP BY time
```

```sql
-- sum every 6 hours, without UNION
SELECT avg(pm25) as value, TIMESTAMP(DATE(ts), CONCAT(floor(hour(ts)/6)*6, ':00:00')) as time,'pm25' as type, 'aqi' as source, lat, lon
FROM aqi
GROUP BY time, lat, lon
```

```sql
-- create view
create view my_data as
-- TODO: add some SELECT (สักอันในข้างบน)

-- add view to warehouse
INSERT INTO warehouse.weather (ts, lat, lon, sensor, source, value, user)
SELECT ts, lat, lon, sensor, source, value, user FROM my_data;
```

# (slide9-11) Data Report

Web Application

- Provides service directly to `user`

Web Service/Web API

- Provides service to `other programs`

## API

### API Lifecycle

- Planning and Designing
  - modeling
  - specification
  - documentation
- Developing
  - client SDK
  - server implementation
- Testing
  - quality assurance
  - performance monitor
- Deploying
  - hosting
  - security
  - analytics
- Retiring
  - migration plan
  - deprecation
- (loop)

### REST

- REST: `RE`presentational `S`tate `T`ransfer
- REST is:
  - a style, `not` a standard
  - `Stateless`
  - `Cacheable`
- Service requests are done via generic HTTP methods:
  - GET
  - POST
  - PUT
  - DELETE
- Response Status Codes
  - 1xx: Informational (transfer protocol-level information)
  - 2xx: Success
  - 3xx: Redirection
  - 4xx: Client Error
  - 5xx: Server Error

Note.

- `Standards`:
  - HTTP/TLS for resource addressing and data transfer
  - JSON, XML, YAML, etc. for data representation

### REST Architecture

- Nouns (aka `resources`) -> URL
- Verbs (aka `requests`) -> HTTP Methods
- Data `representation` -> JSON, XML, etc.

## (slide9) OpenAPI

- Formerly known as `Swagger Specification`
- Language-agnostic, document-driven development
- Allows code generation for both developers and clients
- Allows both humans and computers to discover and understand your API’s capabilities

![img](https://i.ibb.co/p2vqPrf/Screen-Shot-2564-12-08-at-13-52-26.png)

ex. rain-api [github here!](https://github.com/KU-SKE17/rain-api)

1. after clone, and finish installation

2. edit [controller.py](https://github.com/KU-SKE17/rain-api/blob/main/controller.py)

   - update function(query) for endpoints

     ```python
     # start with
     import sys
     from flask import abort
     import pymysql as mysql
     from config import OPENAPI_AUTOGEN_DIR, DB_HOST, DB_USER, DB_PASSWD, DB_NAME

     sys.path.append(OPENAPI_AUTOGEN_DIR)
     from openapi_server import models

     db = mysql.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWD, db=DB_NAME)

     # add
     def get_basins():
        cs = db.cursor()
        cs.execute("SELECT basin_id,ename FROM basin")
        result = [
           models.BasinShort(basin_id, name) for basin_id, name in cs.fetchall()
        ]
        cs.close()
        return result
     ```

3. edit [openapi/rain-api.yaml](https://github.com/KU-SKE17/rain-api/blob/main/openapi/rain-api.yaml)

   - update endpoints

     ```yaml
     # start with
     openapi: 3.0.0
     info:
       title: Chaopraya Rainfalls API
       description: This API provides historical rainfall data over upper Chaopraya river basin between 1987 and 2021.  Raw data provided by Thai Meteorological Department (TMD).
       version: 1.0.0
     servers:
       - url: /rain-api/v1
     paths:
       /basins: # add since this line
         get:
           summary: Returns a list of basins.
           operationId: controller.get_basins
           responses:
             200:
               description: Success
               content:
                 application/json:
                   schema:
                     type: array
                     items:
                       $ref: "#/components/schemas/BasinShort"
     ```

   - update components schemas

     ```yaml
     # start with
     components:
       schemas:
         BasinShort: # add since this line
           type: object
           properties:
             basinId:
               type: integer
             name:
               type: string
     ```

## (slide10) GraphQL and Links

- `Graph` `Q`uery `L`anguage, developed by Facebook
- Data are modeled as a graph
- APIs are organized around types and fields, `not` endpoints
- Clients see APIs similar to OOP

ex. rain-graphql [github here!](https://github.com/KU-SKE17/rain-graphql)

1. after clone, and finish installation
2. Start GraphQL IDE, and try

   ```bash
   {
      basin(basinId:3) {
         name
         area
      }
   }
   ```

### Links

- to create `Nested Data Structures`

1. edit [openapi/rain-api-with-links.yaml](https://github.com/KU-SKE17/rain-graphql/blob/main/openapi/rain-api-with-links.yaml)

   ```yaml
   # ...
   /basins/{basinId}:
      parameters:
      - name: basinId
         in: path
         required: true
         schema:
         type : integer
      get:
         summary: Returns complete details of the specified basin
         operationId: controller.get_basin_details
         responses:
         200:
            description: Success
            content:
               application/json:
               schema:
                  $ref: '#/components/schemas/Basin'
            links: # add since this line
               stations:
                  operationId: controller.get_stations_in_basin
                  parameters:
                     basinId: $response.body#/basinId
               annualRainfall:
                  operationId: controller.get_basin_annual_rainfall
                  parameters:
                     basinId: $response.body#/basinId
               allAnnualRainfalls:
                  operationId: controller.get_basin_all_annual_rainfall
                  parameters:
                     basinId: $response.body#/basinId
   ```

2. Start GraphQL IDE, and try

   ```bash
   {
      basin(basinId: 3) {
         name
         area
         # add
         stations {
            name
            lat
            lon
         }
      }
   }
   ```

## (slide11) Data Visualization

- It is difficult for human brains to interpret large numbers
- Visualization helps communicate quantitive contents more effectively by means of abstraction and visual representation

ex. rain-visualization [github here!](https://github.com/KU-SKE17/rain-visualization) - everything are on README

ex. carbonster-api [github here!](https://github.com/SKE-survivors/carbonster-api)

### Good data visualization

- should be:
  - Telling a story
  - Answering certain questions
  - Visually appealing
  - Never misleading

### 2 Generation Types

- Server-Side Generation

  - The server generates visualizations in forms of `images` (PNG, PDF, SVG, ...)
  - The client (web browser) displays images on screen
  - Lots of server-side libraries and languages
  - Pro
    - Suitable for statically generated and cached images
    - Images can be generated in advance
  - Con
    - Computationally expensive for the server
    - Difficult to add interactivity

- Client-Side Generation

  - The server only provides data for generating visualizations, preferably via `API`
  - The client generates visualizations from the data using some client-side visualization libraries, mostly written in JavaScript
  - Pro
    - Less load on the server
    - Also many (free) JavaScript libraries readily available
    - Flexible and responsive user interaction
