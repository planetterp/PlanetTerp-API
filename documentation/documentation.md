---
title: PlanetTerp API v1.0.0
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

<h1 id="planetterp-api">PlanetTerp API v1.0.0</h1>

> Scroll down for code samples, example requests and responses. Select a language for code samples from the tabs above or the mobile navigation menu.

Welcome to the <strong>test</strong> api

Base URLs:

* <a href="https://api.planetterp.com">https://api.planetterp.com</a>

Email: <a href="mailto:admin@planetterp.com">Support</a> 

<h1 id="planetterp-api-courses">courses</h1>

Get courses

## get__courses

> Code samples

```shell
# You can also use wget
curl -X GET https://api.planetterp.com/courses \
  -H 'Accept: application/json'

```

```http
GET https://api.planetterp.com/courses HTTP/1.1
Host: api.planetterp.com
Accept: application/json

```

```javascript

const headers = {
  'Accept':'application/json'
};

fetch('https://api.planetterp.com/courses',
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

result = RestClient.get 'https://api.planetterp.com/courses',
  params: {
  }, headers: headers

p JSON.parse(result)

```

```python
import requests
headers = {
  'Accept': 'application/json'
}

r = requests.get('https://api.planetterp.com/courses', headers = headers)

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
    $response = $client->request('GET','https://api.planetterp.com/courses', array(
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
URL obj = new URL("https://api.planetterp.com/courses");
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
    req, err := http.NewRequest("GET", "https://api.planetterp.com/courses", data)
    req.Header = headers

    client := &http.Client{}
    resp, err := client.Do(req)
    // ...
}

```

`GET /courses`

*Get courses*

Get all courses, in alphabetical order

<h3 id="get__courses-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|dept|query|string|false|Pass an optional department. Must be four characters.|
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
    "credits": 3
  }
]
```

<h3 id="get__courses-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Returns courses matching query|Inline|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|bad input parameter|None|

<h3 id="get__courses-responseschema">Response Schema</h3>

Status Code **200**

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|*anonymous*|[[Course](#schemacourse)]|false|none|none|
|» department|string|true|none|none|
|» course_number|string|true|none|none|
|» title|string|true|none|none|
|» credits|integer|true|none|none|

<aside class="success">
This operation does not require authentication
</aside>

<h1 id="planetterp-api-professors">professors</h1>

Get grades

## get__professors

> Code samples

```shell
# You can also use wget
curl -X GET https://api.planetterp.com/professors \
  -H 'Accept: application/json'

```

```http
GET https://api.planetterp.com/professors HTTP/1.1
Host: api.planetterp.com
Accept: application/json

```

```javascript

const headers = {
  'Accept':'application/json'
};

fetch('https://api.planetterp.com/professors',
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

result = RestClient.get 'https://api.planetterp.com/professors',
  params: {
  }, headers: headers

p JSON.parse(result)

```

```python
import requests
headers = {
  'Accept': 'application/json'
}

r = requests.get('https://api.planetterp.com/professors', headers = headers)

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
    $response = $client->request('GET','https://api.planetterp.com/professors', array(
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
URL obj = new URL("https://api.planetterp.com/professors");
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
    req, err := http.NewRequest("GET", "https://api.planetterp.com/professors", data)
    req.Header = headers

    client := &http.Client{}
    resp, err := client.Do(req)
    // ...
}

```

`GET /professors`

*Get professors*

Get all professors, in alphabetical order

> Example responses

> 201 Response

```json
[
  {
    "name": "Jon Snow",
    "slug": "snow",
    "type": "ta",
    "courses": [
      "MATH140"
    ]
  }
]
```

<h3 id="get__professors-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|201|[Created](https://tools.ietf.org/html/rfc7231#section-6.3.2)|item created|Inline|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|invalid input, object invalid|None|
|409|[Conflict](https://tools.ietf.org/html/rfc7231#section-6.5.8)|an existing item already exists|None|

<h3 id="get__professors-responseschema">Response Schema</h3>

Status Code **201**

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
  "credits": 3
}

```

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|department|string|true|none|none|
|course_number|string|true|none|none|
|title|string|true|none|none|
|credits|integer|true|none|none|

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
  "type": "ta",
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

