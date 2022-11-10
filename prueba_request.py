import requests

url = 'http://10.200.100.124/ftsltools/.test/INTRAWAY/scopes-domine.php'
r = requests.get(url, allow_redirects=True)
open('ccap_scopes.csv', 'wb').write(r.content)