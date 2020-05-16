---
title: PlanetTerp API v1
language_tabs:
  - shell: Shell
  - http: HTTP
  - javascript: JavaScript
  - ruby: Ruby
  - python: Python
  - php: PHP
  - java: Java
  - go: Go
toc_footers: []
includes: []
search: true
highlight_theme: darkula
headingLevel: 2

---

<!-- Generator: Widdershins v4.0.1 -->

<h1 id="planetterp-api">PlanetTerp API v1</h1>

> Scroll down for code samples, example requests and responses. Select a language for code samples from the tabs above or the mobile navigation menu.

Welcome to <a href="https://planetterp.com">PlanetTerp</a>'s API. This API provides access to data relating to courses, professors, and grade data at the <a href="https://umd.edu">University of Maryland &mdash; College Park</a> (UMD).<br /><br /> The primary purpose of this API is to provide access to grade data. There is already a student-run API that provides access to professor and grade data: <a href="https://umd.io">umd.io</a>.<br /><br /> The course and professor data on this website was obtained using a combination of umd.io and <a href="https://app.testudo.umd.edu/soc/">UMD's Schedule of Classes</a>. The grade data is from the <a href="https://www.irpa.umd.edu"">UMD Office of Institutional Research, Planning &amp; Assessment</a> (IRPA) and obtained through <a href="https://www.umd.edu/administration/public-information-request">a request</a> under <a href="http://www.marylandattorneygeneral.gov/OpenGov%20Documents/PIA_manual_printable.pdf">the state of Maryland's Public Information Act</a> (PIA).<br /><br/> The base URL of the API is <a href="https://api.planetterp.com/v1">https://api.planetterp.com/v1</a>.<br /><br /> For support, please email <a href="mailto:admin@planetterp.com">admin@planetterp.com</a>.

Base URLs:

* <a href="https://api.planetterp.com/v1">https://api.planetterp.com/v1</a>

Email: <a href="mailto:admin@planetterp.com">Support</a> 

<h1 id="planetterp-api-courses">Courses</h1>

## Get courses

<a id="opIdGet courses"></a>

> Code samples

```shell
# You can also use wget
curl -X GET https://api.planetterp.com/v1/courses \
  -H 'Accept: application/json'

```

```http
GET https://api.planetterp.com/v1/courses HTTP/1.1
Host: api.planetterp.com
Accept: application/json

```

```javascript

const headers = {
  'Accept':'application/json'
};

fetch('https://api.planetterp.com/v1/courses',
{
  method: 'GET',

  headers: headers
})
.then(function(res) {
    return res.json();
}).then(function(body) {
    console.log(body);
});

```

```ruby
require 'rest-client'
require 'json'

headers = {
  'Accept' => 'application/json'
}

result = RestClient.get 'https://api.planetterp.com/v1/courses',
  params: {
  }, headers: headers

p JSON.parse(result)

```

```python
import requests
headers = {
  'Accept': 'application/json'
}

r = requests.get('https://api.planetterp.com/v1/courses', headers = headers)

print(r.json())

```

```php
<?php

require 'vendor/autoload.php';

$headers = array(
    'Accept' => 'application/json',
);

$client = new \GuzzleHttp\Client();

// Define array of request body.
$request_body = array();

try {
    $response = $client->request('GET','https://api.planetterp.com/v1/courses', array(
        'headers' => $headers,
        'json' => $request_body,
       )
    );
    print_r($response->getBody()->getContents());
 }
 catch (\GuzzleHttp\Exception\BadResponseException $e) {
    // handle exception or api errors.
    print_r($e->getMessage());
 }

 // ...

```

```java
URL obj = new URL("https://api.planetterp.com/v1/courses");
HttpURLConnection con = (HttpURLConnection) obj.openConnection();
con.setRequestMethod("GET");
int responseCode = con.getResponseCode();
BufferedReader in = new BufferedReader(
    new InputStreamReader(con.getInputStream()));
String inputLine;
StringBuffer response = new StringBuffer();
while ((inputLine = in.readLine()) != null) {
    response.append(inputLine);
}
in.close();
System.out.println(response.toString());

```

```go
package main

import (
       "bytes"
       "net/http"
)

func main() {

    headers := map[string][]string{
        "Accept": []string{"application/json"},
    }

    data := bytes.NewBuffer([]byte{jsonReq})
    req, err := http.NewRequest("GET", "https://api.planetterp.com/v1/courses", data)
    req.Header = headers

    client := &http.Client{}
    resp, err := client.Do(req)
    // ...
}

```

`GET /courses`

*Get courses*

Get all courses, in alphabetical order

<h3 id="get-courses-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|department|query|string|false|Only get courses in a department. Must be four characters.|
|reviews|query|boolean|false|Show reviews for the course (reviews for professors that taught the course and listed this course as the one being reviewed).|
|limit|query|integer|false|Maximum number of records to return. Must be between 1 and 1000. Default 100.|
|offset|query|integer|false|Number of records to skip for pagination. Default 0.|

> Example responses

> 200 Response

```json
[
  {
    "department": "MATH",
    "course_number": 140,
    "title": "Calculus I",
    "description": "Introduction to calculus, including functions, limits, continuity, derivatives and applications of the derivative, sketching of graphs of functions, definite and indefinite integrals, and calculation of area. The course is especially recommended for science, engineering and mathematics majors.",
    "credits": 3,
    "professors": [
      [
        "Jon Snow",
        "Tyrion Lannister"
      ]
    ]
  }
]
```

<h3 id="get-courses-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Returns courses matching query|Inline|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|bad input parameter|None|

<h3 id="get-courses-responseschema">Response Schema</h3>

Status Code **200**

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|*anonymous*|[[Course](#schemacourse)]|false|none|none|
|» department|string|true|none|none|
|» course_number|string|true|none|none|
|» title|string|true|none|none|
|» description|string|true|none|none|
|» credits|integer|true|none|none|
|» professors|[string]|true|none|none|

<aside class="success">
This operation does not require authentication
</aside>

<h1 id="planetterp-api-professors">Professors</h1>

## Get professors

<a id="opIdGet professors"></a>

> Code samples

```shell
# You can also use wget
curl -X GET https://api.planetterp.com/v1/professors \
  -H 'Accept: application/json'

```

```http
GET https://api.planetterp.com/v1/professors HTTP/1.1
Host: api.planetterp.com
Accept: application/json

```

```javascript

const headers = {
  'Accept':'application/json'
};

fetch('https://api.planetterp.com/v1/professors',
{
  method: 'GET',

  headers: headers
})
.then(function(res) {
    return res.json();
}).then(function(body) {
    console.log(body);
});

```

```ruby
require 'rest-client'
require 'json'

headers = {
  'Accept' => 'application/json'
}

result = RestClient.get 'https://api.planetterp.com/v1/professors',
  params: {
  }, headers: headers

p JSON.parse(result)

```

```python
import requests
headers = {
  'Accept': 'application/json'
}

r = requests.get('https://api.planetterp.com/v1/professors', headers = headers)

print(r.json())

```

```php
<?php

require 'vendor/autoload.php';

$headers = array(
    'Accept' => 'application/json',
);

$client = new \GuzzleHttp\Client();

// Define array of request body.
$request_body = array();

try {
    $response = $client->request('GET','https://api.planetterp.com/v1/professors', array(
        'headers' => $headers,
        'json' => $request_body,
       )
    );
    print_r($response->getBody()->getContents());
 }
 catch (\GuzzleHttp\Exception\BadResponseException $e) {
    // handle exception or api errors.
    print_r($e->getMessage());
 }

 // ...

```

```java
URL obj = new URL("https://api.planetterp.com/v1/professors");
HttpURLConnection con = (HttpURLConnection) obj.openConnection();
con.setRequestMethod("GET");
int responseCode = con.getResponseCode();
BufferedReader in = new BufferedReader(
    new InputStreamReader(con.getInputStream()));
String inputLine;
StringBuffer response = new StringBuffer();
while ((inputLine = in.readLine()) != null) {
    response.append(inputLine);
}
in.close();
System.out.println(response.toString());

```

```go
package main

import (
       "bytes"
       "net/http"
)

func main() {

    headers := map[string][]string{
        "Accept": []string{"application/json"},
    }

    data := bytes.NewBuffer([]byte{jsonReq})
    req, err := http.NewRequest("GET", "https://api.planetterp.com/v1/professors", data)
    req.Header = headers

    client := &http.Client{}
    resp, err := client.Do(req)
    // ...
}

```

`GET /professors`

*Get professors*

Get all professors, in alphabetical order

<h3 id="get-professors-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|type|query|string|false|Show only reviews for professors or teaching assistants. Default shows both.|
|reviews|query|boolean|false|Show reviews for the professor.|
|limit|query|integer|false|Maximum number of records to return. Must be between 1 and 1000. Default 100.|
|offset|query|integer|false|Number of records to skip for pagination. Default 0.|

#### Enumerated Values

|Parameter|Value|
|---|---|
|type|professor|
|type|ta|

> Example responses

> 200 Response

```json
[
  {
    "name": "Jon Snow",
    "slug": "snow",
    "type": "professor",
    "courses": [
      "MATH140"
    ]
  }
]
```

<h3 id="get-professors-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Returns professors matching query|Inline|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|bad input parameter|None|

<h3 id="get-professors-responseschema">Response Schema</h3>

Status Code **200**

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|*anonymous*|[[Professor](#schemaprofessor)]|false|none|none|
|» name|string|true|none|none|
|» slug|string|true|none|none|
|» type|string|true|none|none|
|» courses|[string]|true|none|none|

#### Enumerated Values

|Property|Value|
|---|---|
|type|professor|
|type|ta|

<aside class="success">
This operation does not require authentication
</aside>

<h1 id="planetterp-api-grades">Grades</h1>

## Get grades

<a id="opIdGet grades"></a>

> Code samples

```shell
# You can also use wget
curl -X GET https://api.planetterp.com/v1/grades \
  -H 'Accept: application/json'

```

```http
GET https://api.planetterp.com/v1/grades HTTP/1.1
Host: api.planetterp.com
Accept: application/json

```

```javascript

const headers = {
  'Accept':'application/json'
};

fetch('https://api.planetterp.com/v1/grades',
{
  method: 'GET',

  headers: headers
})
.then(function(res) {
    return res.json();
}).then(function(body) {
    console.log(body);
});

```

```ruby
require 'rest-client'
require 'json'

headers = {
  'Accept' => 'application/json'
}

result = RestClient.get 'https://api.planetterp.com/v1/grades',
  params: {
  }, headers: headers

p JSON.parse(result)

```

```python
import requests
headers = {
  'Accept': 'application/json'
}

r = requests.get('https://api.planetterp.com/v1/grades', headers = headers)

print(r.json())

```

```php
<?php

require 'vendor/autoload.php';

$headers = array(
    'Accept' => 'application/json',
);

$client = new \GuzzleHttp\Client();

// Define array of request body.
$request_body = array();

try {
    $response = $client->request('GET','https://api.planetterp.com/v1/grades', array(
        'headers' => $headers,
        'json' => $request_body,
       )
    );
    print_r($response->getBody()->getContents());
 }
 catch (\GuzzleHttp\Exception\BadResponseException $e) {
    // handle exception or api errors.
    print_r($e->getMessage());
 }

 // ...

```

```java
URL obj = new URL("https://api.planetterp.com/v1/grades");
HttpURLConnection con = (HttpURLConnection) obj.openConnection();
con.setRequestMethod("GET");
int responseCode = con.getResponseCode();
BufferedReader in = new BufferedReader(
    new InputStreamReader(con.getInputStream()));
String inputLine;
StringBuffer response = new StringBuffer();
while ((inputLine = in.readLine()) != null) {
    response.append(inputLine);
}
in.close();
System.out.println(response.toString());

```

```go
package main

import (
       "bytes"
       "net/http"
)

func main() {

    headers := map[string][]string{
        "Accept": []string{"application/json"},
    }

    data := bytes.NewBuffer([]byte{jsonReq})
    req, err := http.NewRequest("GET", "https://api.planetterp.com/v1/grades", data)
    req.Header = headers

    client := &http.Client{}
    resp, err := client.Do(req)
    // ...
}

```

`GET /grades`

*Get grades*

Get grades for a course, professor, or both.

<h3 id="get-grades-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|course|query|string|false|Show only grades for the given course.|
|professor|query|string|false|Show only grades for the given professor.|
|semester|query|string|false|Show only grades for the given semester. Semester should be provided as the year followed by the semester code. `01` means Spring and `08` means Fall. For example, `202001` means Spring 2020.|

> Example responses

> 200 Response

```json
[
  {
    "course": "MATH140",
    "professor": "Jon Snow",
    "semester": "202001",
    "section": "0101",
    "A+": 1,
    "A": 1,
    "A-": 1,
    "B+": 1,
    "B": 1,
    "B-": 1,
    "C+": 1,
    "C": 1,
    "C-": 1,
    "D+": 1,
    "D": 1,
    "D-": 1,
    "F": 1,
    "W": 1,
    "Other": 1
  }
]
```

<h3 id="get-grades-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Returns grades matching query|Inline|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|bad input parameter|None|

<h3 id="get-grades-responseschema">Response Schema</h3>

Status Code **200**

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|*anonymous*|[[Grades](#schemagrades)]|false|none|none|
|» course|string|true|none|none|
|» professor|string|true|none|none|
|» semester|string|true|none|none|
|» section|string|true|none|none|
|» A+|integer|true|none|none|
|» A|integer|true|none|none|
|» A-|integer|true|none|none|
|» B+|integer|true|none|none|
|» B|integer|true|none|none|
|» B-|integer|true|none|none|
|» C+|integer|true|none|none|
|» C|integer|true|none|none|
|» C-|integer|true|none|none|
|» D+|integer|true|none|none|
|» D|integer|true|none|none|
|» D-|integer|true|none|none|
|» F|integer|true|none|none|
|» W|integer|true|none|none|
|» Other|integer|true|none|none|

<aside class="success">
This operation does not require authentication
</aside>

# Schemas

<h2 id="tocS_Course">Course</h2>
<!-- backwards compatibility -->
<a id="schemacourse"></a>
<a id="schema_Course"></a>
<a id="tocScourse"></a>
<a id="tocscourse"></a>

```json
{
  "department": "MATH",
  "course_number": 140,
  "title": "Calculus I",
  "description": "Introduction to calculus, including functions, limits, continuity, derivatives and applications of the derivative, sketching of graphs of functions, definite and indefinite integrals, and calculation of area. The course is especially recommended for science, engineering and mathematics majors.",
  "credits": 3,
  "professors": [
    [
      "Jon Snow",
      "Tyrion Lannister"
    ]
  ]
}

```

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|department|string|true|none|none|
|course_number|string|true|none|none|
|title|string|true|none|none|
|description|string|true|none|none|
|credits|integer|true|none|none|
|professors|[string]|true|none|none|

<h2 id="tocS_Professor">Professor</h2>
<!-- backwards compatibility -->
<a id="schemaprofessor"></a>
<a id="schema_Professor"></a>
<a id="tocSprofessor"></a>
<a id="tocsprofessor"></a>

```json
{
  "name": "Jon Snow",
  "slug": "snow",
  "type": "professor",
  "courses": [
    "MATH140"
  ]
}

```

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|name|string|true|none|none|
|slug|string|true|none|none|
|type|string|true|none|none|
|courses|[string]|true|none|none|

#### Enumerated Values

|Property|Value|
|---|---|
|type|professor|
|type|ta|

<h2 id="tocS_Grades">Grades</h2>
<!-- backwards compatibility -->
<a id="schemagrades"></a>
<a id="schema_Grades"></a>
<a id="tocSgrades"></a>
<a id="tocsgrades"></a>

```json
{
  "course": "MATH140",
  "professor": "Jon Snow",
  "semester": "202001",
  "section": "0101",
  "A+": 1,
  "A": 1,
  "A-": 1,
  "B+": 1,
  "B": 1,
  "B-": 1,
  "C+": 1,
  "C": 1,
  "C-": 1,
  "D+": 1,
  "D": 1,
  "D-": 1,
  "F": 1,
  "W": 1,
  "Other": 1
}

```

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|course|string|true|none|none|
|professor|string|true|none|none|
|semester|string|true|none|none|
|section|string|true|none|none|
|A+|integer|true|none|none|
|A|integer|true|none|none|
|A-|integer|true|none|none|
|B+|integer|true|none|none|
|B|integer|true|none|none|
|B-|integer|true|none|none|
|C+|integer|true|none|none|
|C|integer|true|none|none|
|C-|integer|true|none|none|
|D+|integer|true|none|none|
|D|integer|true|none|none|
|D-|integer|true|none|none|
|F|integer|true|none|none|
|W|integer|true|none|none|
|Other|integer|true|none|none|

