import json

import flask
from flask import Flask, render_template, request

app = Flask(__name__)
import data_product
import quan_ly_danh_sach_xe

@app.route('/main')
def main():
    return render_template('main.html')


@app.route('/quan_ly_xe')
def quan_ly_xe():
    return render_template('quan_ly_xe.html')


@app.route('/')
def danh_sach_xe():
    return render_template('danh_sach_xe.html')


@app.route("/list_xe")
def list_xe():
    data_short = data_product.product_view_short()
    return render_template('list_xe.html', data_short=data_short)


@app.route("/them_xe")
def them_xe():
    data_color = data_product.color_view()
    data_type = data_product.type_view()
    data_brand_model = data_product.brand_model_view()
    print(data_brand_model)
    data_brand_model_json = json.dumps(data_brand_model)
    return render_template('them_xe.html', data_color=data_color, data_type=data_type,
                           data_brand_model=data_brand_model, data_brand_model_json=data_brand_model_json,
                           max_id=data_product.product_get_max_id())


@app.route("/xe", methods=['POST'])
def xe():
    return render_template('chi_tiet_xe.html')


@app.route("/gia_xe", methods=['POST'])
def xe_gia():
    PRODUCT_ID = request.form['PRODUCT_ID']
    if PRODUCT_ID is not None:
        data_prices = data_product.product_view_prices(PRODUCT_ID)
        print(data_prices)
        return render_template('gia_xe.html', data_prices=data_prices)
    else:
        return list_xe()


@app.route("/xe_gia_cap_nhat", methods=['POST'])
def xe_gia_cap_nhat():
    PRODUCT_ID = request.form['PRODUCT_ID']
    json_gia_xe_cap_nhat = {}
    for name in data_product.product_cols_small_cap_nhat_gia_no_val_6():
        json_gia_xe_cap_nhat[name] = request.form[name]
    print(json_gia_xe_cap_nhat)
    if PRODUCT_ID is not None:
        data_product.product_update_gia_xe(json_gia_xe_cap_nhat)
        data_prices = data_product.product_view_prices(PRODUCT_ID)
        return render_template('gia_xe.html', data_prices=data_prices)
    else:
        return list_xe()


@app.route('/them_moi_xe', methods=['POST'])
def them_moi_xe():
    product_cols = data_product.product_get_cols_small()
    json_add = {}
    for name_col in product_cols:
        try:
            json_add[name_col] = request.form[name_col]
        except:
            pass
    code, id = data_product.product_add(json_add)
    if code == 0:
        return list_xe()
    else:
        data_color = data_product.color_view()
        data_type = data_product.type_view()
        data_brand_model = data_product.brand_model_view()
        data_brand_model_json = json.dumps(data_brand_model)
        return render_template('them_xe.html', data_color=data_color, data_type=data_type,
                               data_brand_model=data_brand_model, data_brand_model_json=data_brand_model_json)

@app.route("/danh_sach_xe_post_danh_sanh_xe_all", methods=["POST"])
def danh_sach_xe_post_danh_sanh_xe_all():
    danh_sach_xe = quan_ly_danh_sach_xe.product_danh_sach_xe()
    print(danh_sach_xe)
    # danh_sach_xe_json = json.dumps(danh_sach_xe, ensure_ascii=False).encode('utf8')
    # print(danh_sach_xe_json)
    return json.dumps(danh_sach_xe), 200, {'ContentType':'application/json'}



if __name__ == '__main__':
    app.run(host="192.168.1.79", port=7877, debug=True)
