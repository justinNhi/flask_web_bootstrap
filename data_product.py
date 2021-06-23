from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, and_, inspect, func
from datetime import datetime, time, timedelta
import config


Base = automap_base()
engine = config.get_config()
SessionSql = sessionmaker()
SessionSql.configure(bind=engine)
Base.prepare(engine, reflect=True)

COLOR = Base.classes.COLOR
PRODUCT = Base.classes.PRODUCT
TYPE = Base.classes.TYPE
BRAND_MODEL = Base.classes.BRAND_MODEL
BRAND = Base.classes.BRAND



PRODUCT_cols = PRODUCT.__table__.columns.keys()

def get_max_id(TABLE_NAME):
    session_sql = SessionSql()
    rs_user_id_max = session_sql.query(func.max(TABLE_NAME))
    get_id = rs_user_id_max.all()[0][0]
    if get_id == None:
        id_max = 1
    else:
        id_max = int(get_id) + 1
    session_sql.close()
    return id_max


def color_add(color_name=None, color_name_en = None):
    session_sql = SessionSql()
    error_code = 1
    if color_name is not None:
        rs_id_max = session_sql.query(func.max(COLOR.COLOR_ID))
        get_id = rs_id_max.all()[0][0]
        if get_id == None:
            color_id = 0
        else:
            color_id = int(get_id) + 1
        if color_name_en is None:
            json_insert = {
                'COLOR_ID': color_id,
                'COLOR_NAME':color_name
            }
        else:
            json_insert = {
                'COLOR_ID': color_id,
                'COLOR_NAME': color_name,
                'COLOR_NAME_EN': color_name_en
            }
        try:
            obj = COLOR(**json_insert)
            session_sql.add(obj)
            session_sql.commit()
            error_code = 0
        except:
            error_code = 1

    session_sql.close()
    return error_code

def product_view_short():
    session_sql = SessionSql()
    rs_product_view = session_sql.query(PRODUCT)
    data = []
    if len(rs_product_view.all()) > 0:
        for row in rs_product_view.all():
            data_row = {}
            for name in ["PRODUCT_ID", "PRODUCT_GET_DATE", "PRODUCT_ID_NUMBER", 'PRODUCT_NAME','PRODUCT_BRAND_NAME', 'PRODUCT_GET_DATE', 'PRODUCT_STATUS']:
                data_row[name] = str(getattr(row, name))
            data.append(data_row)
    session_sql.close()
    return data

def product_view_prices(PRODUCT_ID):
    session_sql = SessionSql()
    rs_product_view = session_sql.query(PRODUCT).filter(PRODUCT.PRODUCT_ID == PRODUCT_ID).first()
    data = {}
    if rs_product_view is not None:
        for name in ["PRODUCT_ID", "PRODUCT_ID_NUMBER", 'PRODUCT_NAME', 'PRODUCT_GET_DATE','PRODUCT_SELL_DATE',
                     'PRODUCT_VALUE_1', 'PRODUCT_VALUE_2', 'PRODUCT_VALUE_3', 'PRODUCT_VALUE_4', 'PRODUCT_VALUE_5', 'PRODUCT_VALUE_6']:
            if name in ['PRODUCT_VALUE_1', 'PRODUCT_VALUE_2', 'PRODUCT_VALUE_3', 'PRODUCT_VALUE_4'
                , 'PRODUCT_VALUE_5', 'PRODUCT_VALUE_6']:
                if getattr(rs_product_view, name) is not None:
                    data[name] = "{:,} VNĐ".format(getattr(rs_product_view, name))
                else:
                    data[name] = str(getattr(rs_product_view, name))
            else:
                data[name] = str(getattr(rs_product_view, name))
    session_sql.close()
    return data

def product_view_detail(product_id):
    session_sql = SessionSql()
    rs_product_view = session_sql.query(PRODUCT).filter(PRODUCT.PRODUCT_ID == product_id)
    data = []
    data_name = ['Mã xe', 'Tên xe', 'Mô tả', 'Loại xe', 'Nhà sản xuất', 'Mẫu xe', 'Xuất xứ', 'Năm sản xuất',
                 'Năm đăng ký',
                 'Số chỗ ngồi', 'Nhiên liệu  ', 'Màu', 'Odo', 'Động cơ', 'Ngày nhập', 'Ngày bán', 'Giá mua',
                 'Chi phí mua',
                 'Giá bán', 'Chi phí bán', 'Giá bán thực tế', 'Lãi']
    if len(rs_product_view.all()) > 0:
        print(rs_product_view.all())
        for row in rs_product_view.all():
            data_row = {}
            for ind_n, name in enumerate(['PRODUCT_ID_NUMBER', 'PRODUCT_NAME', 'PRODUCT_DES', 'PRODUCT_TYPE_NAME', 'PRODUCT_BRAND_NAME',
                         'PRODUCT_MODEL_NAME', 'PRODUCT_ORIGIN', 'PRODUCT_RELEASE_YEAR', 'PRODUCT_YEAR', 'PRODUCT_SEAT',
                         'PRODUCT_FUEL_NAME', 'PRODUCT_COLOR', 'PRODUCT_ODO', 'PRODUCT_ENGINE', 'PRODUCT_GET_DATE',
                         'PRODUCT_SELL_DATE', 'PRODUCT_VALUE_1', 'PRODUCT_VALUE_2', 'PRODUCT_VALUE_3', 'PRODUCT_VALUE_4'
                        , 'PRODUCT_VALUE_5', 'PRODUCT_VALUE_6']):
                if name in ['PRODUCT_VALUE_1', 'PRODUCT_VALUE_2', 'PRODUCT_VALUE_3', 'PRODUCT_VALUE_4'
                        , 'PRODUCT_VALUE_5', 'PRODUCT_VALUE_6']:

                    data_row[data_name[ind_n]] = "{:,} VNĐ".format(getattr(row, name))
                else:
                    data_row[data_name[ind_n]] = getattr(row, name)

            data.append(data_row)
    session_sql.close()
    return data, data_name

def color_view():
    session_sql = SessionSql()
    rs_color = session_sql.query(COLOR)
    data = []
    for row in rs_color.all():
        data_row = {}
        data_row['COLOR_ID'] = str(getattr(row, "COLOR_ID"))
        data_row['COLOR_NAME'] = str(getattr(row, "COLOR_NAME"))
        data.append(data_row)
    session_sql.close()
    return data

def type_view():
    session_sql = SessionSql()
    rs_color = session_sql.query(TYPE)
    data = []
    for row in rs_color.all():
        data_row = {}
        data_row['TYPE_ID'] = str(getattr(row, "TYPE_ID"))
        data_row['TYPE_NAME'] = str(getattr(row, "TYPE_NAME"))
        data.append(data_row)
    session_sql.close()

    return data

def brand_model_view():
    session_sql = SessionSql()
    data = []
    rs_brand = session_sql.query(BRAND)
    for row in rs_brand.all():
        data_brand = {
            'BRAND_ID': str(getattr(row,'BRAND_ID')),
            'BRAND_NAME': str(getattr(row, 'BRAND_NAME'))
        }
        rs_model = session_sql.query(BRAND_MODEL).filter(BRAND_MODEL.BRAND_ID == getattr(row, 'BRAND_ID'))
        data_mode_row = []
        for row_model in rs_model.all():
            data_model = {}
            data_model['MODEL_ID'] = str(getattr(row_model,'MODEL_ID'))
            data_model['MODEL_NAME'] = str(getattr(row_model,'MODEL_NAME'))
            data_mode_row.append(data_model)

        data_brand['MODEL'] = data_mode_row
        data.append(data_brand)
    session_sql.close()
    return data