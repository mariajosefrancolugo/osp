import base64
import urllib2

creds = base64.encodestring('test:test')[:-1]

f = file('test_data/instructors.json')
data = f.read()
f.close()

req = urllib2.Request('http://localhost:8000/api/instructors/import/')
req.add_header('Authorization', 'Basic %s' % creds)
req.add_header('Content-type', 'application/json')
req.add_data(data)

res = urllib2.urlopen(req)
out = res.read()
res.close()

print out
