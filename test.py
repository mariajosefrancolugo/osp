import base64
import urllib2

creds = base64.encodestring('test:test')[:-1]

data_types = [
    {
        'json': 'instructors.json',
        'url': '/instructors/import/',
    },
    {
        'json': 'students.json',
        'url': '/students/import/',
    },
    {
        'json': 'courses.json',
        'url': '/courses/import/',
    },
    {
        'json': 'sections.json',
        'url': '/sections/import/',
    },
]

for data_type in data_types:
    f = file('test_data/%s' % data_type['json'])
    data = f.read()
    f.close()

    req = urllib2.Request('http://localhost:8000/api%s' % data_type['url'])
    req.add_header('Authorization', 'Basic %s' % creds)
    req.add_header('Content-type', 'application/json')
    req.add_data(data)

    res = urllib2.urlopen(req)
    out = res.read()
    res.close()

    print out
