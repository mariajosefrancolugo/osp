import base64
import urllib2

creds = base64.encodestring('test:test')[:-1]

data_types = [
    {
        'json': 'instructors.json',
        'url': '/instructor/import/',
    },
    {
        'json': 'students.json',
        'url': '/student/import/',
    },
    {
        'json': 'sections.json',
        'url': '/section/import/',
    },
    {
        'json': 'enrollments.json',
        'url': '/enrollment/import/',
    },
]

for data_type in data_types:
    f = file('test_data/%s' % data_type['json'])
    data = f.read()
    f.close()

    req = urllib2.Request('http://localhost:8001/api%s' % data_type['url'])
    req.add_header('Authorization', 'Basic %s' % creds)
    req.add_header('Content-type', 'application/json')
    req.add_data(data)

    res = urllib2.urlopen(req)
    out = res.read()
    res.close()

    print out
