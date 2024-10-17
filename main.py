from flask import Flask,render_template,url_for,request,redirect
from json import load

app = Flask(__name__)

def decrypt(text):
    key = 12
    ref = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ/.:+-%&'
    length = len(ref)
    retur = ''
    for char in text:
        ind = ref.find(char)  
        result = ind - key%length if ind != -1 else None
        retur += char if result is None else ref[result] 
    return retur

@app.route('/wish/<wish_id>')
def wish(wish_id):
    with open(f'./data/{wish_id}.txt','r') as info:
        data = decrypt(info.read())

    aut,fst,img = data.split('|')
    return render_template('wish.html', aut=aut,img=img,msg=f'Happy {fst}')

@app.route('/create')
def create():
    return render_template('create.html')

@app.route('/create/preview')
def review():
    data = decrypt(request.args.get('d'))
    with open('./data/currentID.txt','r') as c:
        cID = c.read()
    auth,fst,img = data.split('|')
    return render_template('preview.html',aut=auth,msg=f'Happy {fst}',img=img)

@app.route('/create/save')
def save():
    data = request.args.get('d')
    with open('./data/currentID.txt','r') as c:
        cID = c.read()
    with open(f'./data/{cID}.txt','w') as file:
        file.write(data)
    with open('./data/currentID.txt','w') as c:
        c.write(('0'*(6-len(str(int(cID)+1))))+str(int(cID)+1))
    return redirect(url_for('wish',wish_id=cID))

app.run(debug=True)