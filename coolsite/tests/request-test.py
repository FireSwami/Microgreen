
datas = {
 'username':'def',
 'password':'def'
}
login = '12345678'
passwd = 'Testpassword1'
datas['username']  = login
datas['password'] = passwd
url = 'https://microgreen.ferumflex.com/login'
s = requests.Session()
loging = s.post(url, data = datas)
f = open('result.txt','w+')
f.write(loging.text)
f.close()