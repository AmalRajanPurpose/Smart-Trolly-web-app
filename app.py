import pyrebase
from flask import *
import pandas as pd

app = Flask(__name__)

config = {
    "apiKey": "AIzaSyB4Y5Z0Y3BbQPm_U-uWlv3oJPhkq4F4QSY",
    "authDomain": "smarttrolly-3f9fe.firebaseapp.com",
    "projectId": "smarttrolly-3f9fe",
    "storageBucket": "smarttrolly-3f9fe.appspot.com",
    "messagingSenderId": "745912954349",
    "appId": "1:745912954349:web:92b81522e8cd4d80b08be4",
    "measurementId": "G-KKZVGC7T0X",
    "databaseURL": "https://smarttrolly-3f9fe-default-rtdb.firebaseio.com/",
    'serviceAccountId': "https://smarttrolly-3f9fe-default-rtdb.firebaseio.com/"
}

uid = 'some-uid'

firebase = pyrebase.initialize_app(config)

db = firebase.database()


@app.route('/', methods=['GET', 'POST'])
def index():
    products = db.child().get()
    product = products.val()
    last_product = product.values()
    itemName = []
    Quantity = []
    for i in last_product:
        item_name = i.keys()
        quantity = i.values()
        itemName.append(item_name)
        Quantity.append(quantity)

    return render_template('smartTrolly.html', name=list(itemName[0]), que=list(Quantity[0]))


@app.route('/create_invoice', methods=['GET', 'POST'])
def invoice():
    products = db.child().get()
    product = products.val()
    last_product = product.values()
    itemName = []
    Quantity = []
    for i in last_product:
        item_name = i.keys()
        quantity = i.values()
        itemName.append(item_name)
        Quantity.append(quantity)

    amounts = []
    qu = []
    single = []
    for elem in last_product:
        item = elem.keys()
        for single_item in item:
            single.append(single_item)
            excel_data = pd.read_excel('amount.xlsx')
            data = pd.DataFrame(excel_data, columns=['ItemId', 'ItemName', 'Quantity', 'Price'])
            d = data.loc[(data["ItemName"] == single_item)]

            amount = d['Price']
            amounts.append(amount)

    for val in last_product:
        quant = val.values()
        for i in quant:
            qu.append(i)

    res_list = []
    for i in range(0, len(amounts)):
        res_list.append(amounts[i] * qu[i])
    print(single)
    li = []
    for i in res_list:
        a = sum(i)
        li.append(a)
    total_amount = sum(li)
    posts_ref = db.child('rfid').update(
        {"Total Amount": total_amount}, token='custom_token')
    print(posts_ref)
    return render_template('smartTrolly.html', name=list(itemName[0]), que=list(Quantity[0]), total_amount=total_amount)


from datetime import date

if __name__ == '__main__':
    app.run(debug=True)
