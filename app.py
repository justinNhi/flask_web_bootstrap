import json
from datetime import date
import flask
from flask import Flask, render_template, request, make_response
import pdfkit
app = Flask(__name__)
import data_product
import quan_ly_danh_sach_xe
import data_user

# from OpenSSL import SSL
# context = SSL.Context(SSL.PROTOCOL_TLSv1_2)
# context.use_privatekey_file('server.key')
# context.use_certificate_file('server.crt')

@app.route('/')
def login():
    return render_template('index.html')

@app.route('/user_login', methods=['POST'])
def user_login():
    print(request.form['data'])
    rs = data_user.user_login(json.loads(request.form['data']))
    print(rs)
    if rs == 0:
        return danh_sach_xe()
    else:
        return {}, 400, {'ContentType':'application/json'}

@app.route('/danh_sach_xe')
def danh_sach_xe():
    data_brand_model = data_product.brand_model_view()
    data_brand_model_json = json.dumps(data_brand_model)
    danh_sach_xe = quan_ly_danh_sach_xe.product_danh_sach_xe()
    return render_template('danh_sach_xe.html', danh_sach_xe=danh_sach_xe, data_brand_model_json = data_brand_model_json, data_brand_model = data_brand_model, max_id=data_product.product_get_max_id())


@app.route('/danh_sach_xe_add_xe', methods=['POST'])
def danh_sach_xe_add_xe():
    json_data = request.form['data']
    json_data_dic = json.loads(json_data)
    code_result, json_resut = data_product.product_add_new_short_5_para(json_data_dic)
    # print(code_result, json_resut)
    if code_result == 0:
        return json.dumps(json_resut), 200, {'ContentType':'application/json'}
    else:
        return {}, 400, {'ContentType':'application/json'}

@app.route('/quan_ly_xe', methods=['POST'])
def quan_ly_xe():
    data_type = data_product.type_view()
    data_color = data_product.color_view()
    data_brand_model = data_product.brand_model_view()
    data_brand_model_json = json.dumps(data_brand_model)
    try:
        PRODUCT_ID = request.form['PRODUCT_ID']
    except:
        PRODUCT_ID = 0
    data_xe = data_product.product_view_one(PRODUCT_ID)
    # danh_sach_xe = quan_ly_danh_sach_xe.product_danh_sach_xe()
    return render_template('quan_ly_xe.html', data_xe=data_xe, PRODUCT_ID = PRODUCT_ID, data_type = data_type, data_brand_model = data_brand_model, data_brand_model_json = data_brand_model_json, data_color=data_color)


@app.route('/quan_ly_xe_cap_nhat_all', methods=['POST'])
def quan_ly_xe_cap_nhat_all():
    json_data = request.form['data']
    json_data_dict = json.loads(json_data)
    error_code = data_product.product_update_all(json_data_dict)
    if error_code == 0:
        return json.dumps({"error_code": error_code}), 200, {'ContentType': 'application/json'}
    else:
        return {}, 400, {'ContentType': 'application/json'}

# @app.route('/quan_ly_xe_cap_nhat_chi_phi_nhap_va_gia_ban', methods=['POST'])
# def quan_ly_xe_cap_nhat_chi_phi_nhap_va_gia_ban():
#     json_data = request.form['data']
#     json_data_dict = json.loads(json_data)
#     error_code = data_product.product_cap_nhat_chi_phi_nhap_va_gia_ban(json_data_dict)
#     if error_code == 0:
#         return json.dumps({"error_code": error_code}), 200, {'ContentType': 'application/json'}
#     else:
#         return {}, 400, {'ContentType': 'application/json'}

@app.route('/quan_ly_xe_cap_nhat_chi_phi_ban_va_gia_ban_thuc_te', methods=['POST'])
def quan_ly_xe_cap_nhat_chi_phi_ban_va_gia_ban_thuc_te():
    json_data = request.form['data']
    json_data_dict = json.loads(json_data)
    error_code = data_product.product_cap_nhat_chi_phi_ban_va_gia_ban_thuc_te(json_data_dict)
    if error_code == 0:
        return json.dumps({"error_code": error_code}), 200, {'ContentType': 'application/json'}
    else:
        return {}, 400, {'ContentType': 'application/json'}


@app.route('/quan_ly_xe_cap_nhat_chi_tiet_xe_1', methods=['POST'])
def quan_ly_xe_cap_nhat_chi_tiet_xe_1():
    json_data = request.form['data']
    json_data_dict = json.loads(json_data)
    error_code = data_product.product_cap_nhat_chi_tiet_xe_1(json_data_dict)
    if error_code == 0:
        return json.dumps({"error_code": error_code}), 200, {'ContentType': 'application/json'}
    else:
        return {}, 400, {'ContentType': 'application/json'}

@app.route('/quan_ly_xe_cap_nhat_chi_tiet_xe_2', methods=['POST'])
def quan_ly_xe_cap_nhat_chi_tiet_xe_2():
    json_data = request.form['data']
    json_data_dict = json.loads(json_data)
    error_code = data_product.product_cap_nhat_chi_tiet_xe_2(json_data_dict)
    if error_code == 0:
        return json.dumps({"error_code": error_code}), 200, {'ContentType': 'application/json'}
    else:
        return {}, 400, {'ContentType': 'application/json'}

@app.route('/quan_ly_xe_cap_nhat_trang_thai_xe', methods=['POST'])
def quan_ly_xe_cap_nhat_trang_thai_xe():
    json_data = request.form['data']
    json_data_dict = json.loads(json_data)
    error_code = data_product.product_cap_nhat_trang_thai_xe(json_data_dict)
    if error_code == 0:
        return json.dumps({"error_code": error_code}), 200, {'ContentType': 'application/json'}
    else:
        return {}, 400, {'ContentType': 'application/json'}

@app.route('/quan_ly_xe_upload_hinh_anh', methods=['POST'])
def quan_ly_xe_upload_hinh_anh():
    json_data = request.form['data']
    error_code = data_product.product_upload_hinh_anh(json_data)
    if error_code == 0:
        return json.dumps({"error_code": error_code}), 200, {'ContentType': 'application/json'}
    else:
        return {}, 400, {'ContentType': 'application/json'}

@app.route('/danh_sach_xe_vo_hieu_hoa', methods=['POST'])
def danh_sach_xe_vo_hieu_hoa():
    json_data = request.form['data']
    error_code = data_product.product_deactive(json.loads(json_data))
    if error_code == 0:
        return json.dumps({"error_code": error_code}), 200, {'ContentType': 'application/json'}
    else:
        return {}, 400, {'ContentType': 'application/json'}


#DASHBOARD

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

# @app.route('/bang_bao_gia')
# @app.route('/pdf_bang_bao_gia', methods=['POST'])
# def pdf_bang_bao_gia():
#     danh_sach_xe = quan_ly_danh_sach_xe.product_pdf_danh_sach_xe()
#
#     return render_template('pdf_bang_bao_gia.html', danh_sach_xe=danh_sach_xe)


@app.route('/autocar_dunglam_bang_bao_gia')
def autocar_dunglam_bang_bao_gia():
    danh_sach_xe = quan_ly_danh_sach_xe.product_pdf_danh_sach_xe()
    return render_template('pdf_bang_bao_gia.html', danh_sach_xe=danh_sach_xe)



@app.route('/pdf_bang_bao_gia', methods=['POST'])
def pdf_bang_bao_gia():
    danh_sach_xe = quan_ly_danh_sach_xe.product_pdf_danh_sach_xe()
    render = render_template('pdf_bang_bao_gia.html', danh_sach_xe=danh_sach_xe)
    config = pdfkit.configuration(wkhtmltopdf="C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe")
    pdf = pdfkit.from_string(render, False, configuration=config)
    get_today= date.today().strftime('%d/%m/%Y')
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Dispositon'] = 'attachment; filename=Autocar_dunglam_bang_bao_gia_ngay' +str(get_today) +'.pdf'
    print(type(response))
    return response

if __name__ == '__main__':
    # app.run(host="0.0.0.0", port=7878, debug=True, ssl_context='adhoc')
    app.run(host="0.0.0.0", port=7878, debug=True)
