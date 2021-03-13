import urllib.request
import urllib.parse
import json
import random
# queryUrl = "http://127.0.0.1:5000/"
webHookURL = "https://b24-711w54.bitrix24.ru/rest/1/pf26w00qvw4fiqto//"
# queryUrl = 'https://postman-echo.com/post'
method = "crm.contact.add"

# method = "crm.contact.list"
params2 ={
"select": [ "ID","POST", "NAME", "LAST_NAME","BIRTHDATE", "TYPE_ID", "SOURCE_ID" ]
}
params = {
        "fields":
        { 
            "NAME": "Глеб", 
            "SECOND_NAME": "Егорович", 
            "LAST_NAME": "Титов", 
            "OPENED": "Y", 
            "ASSIGNED_BY_ID": 1, 
            "TYPE_ID": "CLIENT",
            "SOURCE_ID": "SELF",
            "PHONE": [ { "VALUE": "555888", "VALUE_TYPE": "WORK" } ] 	
        },    
        # "params": { "REGISTER_SONET_EVENT": "Y" }	
        }

def gen_name(first_letter=''):
    name = f"{first_letter}"
    for j in range(random.randrange(5, (10, 9)[bool(first_letter)])):
        l = chr(random.randrange(ord('а'), ord('я')))
        if not name:
            l = l.capitalize()
        name += l
    return name
def gen_phone(num=7):
    return random.randrange(1000000, 9999999)

def gen_birth():
    start_date = date(1970, 1, 1)
    end_date = date(2000, 1, 1)
    delta = end_date - start_date
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = random.randrange(int_delta)
    return start_date + timedelta(seconds=random_second)


def http_build_query(data):
    parents = list()
    pairs = dict()

    def renderKey(parents):
        depth, outStr = 0, ''
        for x in parents:
            s = "[%s]" if depth > 0 or isinstance(x, int) else "%s"
            outStr += s % str(x)
            depth += 1
        return outStr

    def r_urlencode(data):
        if isinstance(data, list) or isinstance(data, tuple):
            for i in range(len(data)):
                parents.append(i)
                r_urlencode(data[i])
                parents.pop()
        elif isinstance(data, dict):
            for key, value in data.items():
                parents.append(key)
                r_urlencode(value)
                parents.pop()
        else:
            pairs[renderKey(parents)] = str(data)

        return pairs
    return urllib.parse.urlencode(r_urlencode(data))


def sendPOST(url='https://postman-echo.com/post',method="",params={"key1":"value"}):
    data = json.dumps(params).encode('utf-8')
    req = urllib.request.Request(url+method, method="POST")
    req.add_header('Content-Type', 'application/json; charset=utf-8')
    req.add_header('Content-Length', len(data))
    res = {}
    with urllib.request.urlopen(req, data) as f:
        res = json.load(f)        
    return res

def sendGET(url='https://postman-echo.com/get/',method="",params={"key1":"value"}):
    with urllib.request.urlopen(url+method+"?"+http_build_query(params)) as f:
        res = json.load(f)        
    return res

# print(sendGET(webHookURL,"crm.contact.add", params=params))

# print(sendPOST(queryUrl,method,params))

batch = {"halt": 0, "cmd":{}}

for i in range(2):
    params = {
        "fields":{ 
            "NAME": gen_name(), 
            "SECOND_NAME": gen_name(), 
            "LAST_NAME": gen_name(), 
            "OPENED": "Y", 
            "ASSIGNED_BY_ID": 1, 
            "TYPE_ID": "CLIENT",
            "SOURCE_ID": "SELF",
            "PHONE": [ { "VALUE": str(gen_phone()), "VALUE_TYPE": "WORK" } ] 	
        }    
    }
    batch["cmd"][i] = "crm.contact.add?"+http_build_query(params)
# print(batch)

res = sendPOST(webHookURL,"batch",params=batch)
print(res)



