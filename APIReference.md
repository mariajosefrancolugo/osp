# Background #


The Online Student Profile API is a RESTful web service for pushing data from your ERP system to the OSP database. It is strictly a one-way street: data is pushed **from** your ERP system **to** the OSP API, never the other way around. The API accepts POST data sent to its entry points in JSON format. Access to the API is controlled by a list of authorized hosts in addition to a single authorization key.


# Data Structure #


The API expects the data submitted to it in a specific format. At the top level, it expects your authorization key, the entry point you are using, and the data associated with that entry point. Here is an example:

```json

[{
"api_key": "test_key_value",
"instructors": [
(data here)
]
}]
```

This tells the API what your authorization key is, that you're submitting instructor data, and then what that data is. In each of the entry point descriptions, there is a data sample which you can base your own data off of.


# Entry Points #


## Instructors ##


URL:

`/api/instructor/import/`

Fields:

  * **id\_number** (string): The instructor's ID number in your ERP system
  * **username** (string): The instructor's username that they would use to authenticate to LDAP/CAS
  * **first\_name** (string): The instructor's first name/given name
  * **last\_name** (string): The instructor's last name/surname
  * **email** (string): The instructor's email address
  * **phone\_number** (string): The instructor's primary phone number
  * **is\_active** (boolean): Determines whether the instructor's OSP account should be active or not

Data Sample:

```json

[{
"api_key": "test_key_value",
"instructors": [
{
"id_number": "0000001",
"username": "john.smith",
"first_name": "John",
"last_name": "Smith",
"email": "john.smith@example.edu",
"phone_number": "555-555-5555",
"is_active": true
},
{
"id_number": "0000002",
"username": "walter.raleigh",
"first_name": "Walter",
"last_name": "Raleigh",
"email": "walter.raleigh@example.edu",
"phone_number": "555-555-5555",
"is_active": true
},
{
"id_number": "0000003",
"username": "francis.drake",
"first_name": "Francis",
"last_name": "Drake",
"email": "francis.drake@example.edu",
"phone_number": "555-555-5555",
"is_active": true
}
]
}]
```


## Students ##


URL:

`/api/student/import/`

Fields:

  * **id\_number** (string): The student's ID number in your ERP system
  * **username** (string): The student's username that they would use to authenticate to LDAP/CAS
  * **first\_name** (string): The student's first name/given name
  * **last\_name** (string): The student's last name/surname
  * **email** (string): The student's email address
  * **phone\_number** (string): The student's primary phone number
  * **is\_active** (boolean): Determines whether the student's OSP account should be active or not

Data Sample:

```json

[{
"api_key": "test_key_value",
"students": [
{
"id_number": "0000004",
"username": "jason.bourne",
"first_name": "Jason",
"last_name": "Bourne",
"email": "jason.bourne@example.edu",
"phone_number": "555-555-5555",
"is_active": true
},
{
"id_number": "0000005",
"username": "harry.potter",
"first_name": "Harry",
"last_name": "Potter",
"email": "harry.potter@example.edu",
"phone_number": "555-555-5555",
"is_active": true
},
{
"id_number": "0000006",
"username": "peter.parker",
"first_name": "Peter",
"last_name": "Parker",
"email": "peter.parker@example.edu",
"phone_number": "555-555-5555",
"is_active": true
}
]
}]
```


## Sections ##


URL:

`/api/section/import/`

Fields:

  * **prefix** (string): The course prefix of the section
  * **number** (string): The course number of the section
  * **section** (string): The section number of the section
  * **instructors** (list of strings): The ERP ID numbers for instructors of the section
  * **term** (string): The abbreviation for the term the section belongs to. Possible choices are defined through the TERM\_CHOICES setting.
  * **year** (integer): The year the section belongs to
  * **title** (string): The course title of the section
  * **credit\_hours** (float): The number of credit hours of the section

Data Sample:

```json

[{
"api_key": "test_key_value",
"sections": [
{
"prefix": "ENG",
"number": "101",
"section": "01",
"instructors": ["0000001"],
"term": "fa",
"year": 2011,
"title": "Introduction to the English Language",
"credit_hours": 3.0
},
{
"prefix": "MAT",
"number": "101",
"section": "01",
"instructors": ["0000002"],
"term": "fa",
"year": 2011,
"title": "Introduction to Mathematics",
"credit_hours": 3.0
},
{
"prefix": "CIS",
"number": "101",
"section": "01",
"instructors": ["0000002", "0000003"],
"term": "fa",
"year": 2011,
"title": "Introduction to Computers",
"credit_hours": 3.0
}
]
}]
```


## Enrollments ##


URL:

`/api/enrollment/import/`

Fields:

  * **prefix** (string): The course prefix of the section of the enrollment
  * **number** (string): The course number of the section of the enrollment
  * **section** (string): The section number of the section of the enrollment
  * **term** (string): The abbreviation for the term the section of the enrollment belongs to. Possible choices are defined through the TERM\_CHOICES setting.
  * **year** (integer): The year the section of the enrollment belongs to
  * **student** (string): The ERP ID number of the student of the enrollment
  * **status** (string): The status of the enrollment. Possible choices are defined through the ENROLLMENT\_STATUS\_CHOICES setting.

Data Sample:

```json

[{
"api_key": "test_key_value",
"enrollments": [
{
"prefix": "ENG",
"number": "101",
"section": "01",
"term": "fa",
"year": 2011,
"student": "0000004",
"status": "N"
},
{
"prefix": "MAT",
"number": "101",
"section": "01",
"term": "fa",
"year": 2011,
"student": "0000004",
"status": "N"
},
{
"prefix": "ENG",
"number": "101",
"section": "01",
"term": "fa",
"year": 2011,
"student": "0000005",
"status": "N"
},
{
"prefix": "CIS",
"number": "101",
"section": "01",
"term": "fa",
"year": 2011,
"student": "0000006",
"status": "N"
}
]
}]
```