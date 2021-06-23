import json

import flask
from flask import Flask, render_template, request

app = Flask(__name__)
import data_product

@app.route('/main')
def main():
    return render_template('main.html')

@app.route('/quan_ly_xe')
def quan_ly_xe():
    return render_template('quan_ly_xe.html')
@app.route('/')
@app.route("/list_xe")
def list_xe():
    data_short = data_product.product_view_short()
    return render_template('list_xe.html', data_short = data_short)

@app.route("/them_xe")
def them_xe():
    data_color = data_product.color_view()
    data_type = data_product.type_view()
    data_brand_model = data_product.brand_model_view()
    data_brand_model = json.dumps(data_brand_model)
    print(data_brand_model)
    return render_template('them_xe.html', data_color=data_color, data_type=data_type,data_brand_model = data_brand_model)

@app.route("/xe", methods=['POST'])
def xe():
    return render_template('xe.html')

@app.route("/xe_gia", methods=['POST'])
def xe_gia():
    PRODUCT_ID = request.form['PRODUCT_ID']
    if PRODUCT_ID is not None:
        data_prices = data_product.product_view_prices(PRODUCT_ID)
        return render_template('xe_gia.html', data_prices=data_prices)
    else:
        return list_xe()



if __name__ == '__main__':
    app.run(debug=True)
