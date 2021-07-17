from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, and_, inspect, func
from datetime import datetime, time, timedelta, date
import config
import base64
Base = automap_base()
engine = config.get_config()
SessionSql = sessionmaker()
SessionSql.configure(bind=engine)
Base.prepare(engine, reflect=True)

COLOR = Base.classes.COLOR
TYPE = Base.classes.TYPE
BRAND_MODEL = Base.classes.BRAND_MODEL
BRAND = Base.classes.BRAND

GUEST = Base.classes.GUEST
SHAR = Base.classes.PRODUCT_IMAGE

PRODUCT_cols = PRODUCT.__table__.columns.keys()
PRODUCT_cols_small = ["PRODUCT_ID", "PRODUCT_ID_NUMBER", "PRODUCT_NAME", "PRODUCT_DES", "PRODUCT_TYPE_ID",
                      "PRODUCT_BRAND_ID",
                      "PRODUCT_MODEL_ID", "PRODUCT_ORIGIN", "PRODUCT_RELEASE_YEAR", "PRODUCT_YEAR", "PRODUCT_SEAT",
                      "PRODUCT_FUEL_NAME", "PRODUCT_COLOR", "PRODUCT_ODO", "PRODUCT_ENGINE", "PRODUCT_GET_DATE",
                      "PRODUCT_SELL_DATE", "PRODUCT_VALUE_1", "PRODUCT_VALUE_2", "PRODUCT_VALUE_3", "PRODUCT_VALUE_4",
                      "PRODUCT_VALUE_5", "PRODUCT_VALUE_6", "PRODUCT_STATUS"]
PRODUCT_cols_small_cap_nhat_gia = ["PRODUCT_ID", "PRODUCT_NAME", "PRODUCT_SELL_DATE", "PRODUCT_VALUE_1",
                                   "PRODUCT_VALUE_2",
                                   "PRODUCT_VALUE_3", "PRODUCT_VALUE_4", "PRODUCT_VALUE_5", "PRODUCT_VALUE_6",
                                   "PRODUCT_STATUS"]
PRODUCT_cols_small_cap_nhat_gia_no_val_6 = ["PRODUCT_ID", "PRODUCT_NAME", "PRODUCT_SELL_DATE", "PRODUCT_VALUE_1",
                                            "PRODUCT_VALUE_2",
                                            "PRODUCT_VALUE_3", "PRODUCT_VALUE_4", "PRODUCT_VALUE_5", "PRODUCT_STATUS"]

PRODUCT_danh_sach_xe_aLL = ["PRODUCT_ID", "PRODUCT_ID_NUMBER", "PRODUCT_NAME", "PRODUCT_DES", "PRODUCT_TYPE_ID",
                            "PRODUCT_BRAND_ID",
                            "PRODUCT_MODEL_ID", "PRODUCT_ORIGIN", "PRODUCT_RELEASE_YEAR", "PRODUCT_YEAR",
                            "PRODUCT_SEAT",
                            "PRODUCT_FUEL_NAME", "PRODUCT_COLOR", "PRODUCT_ODO", "PRODUCT_ENGINE", "PRODUCT_GET_DATE",
                            "PRODUCT_SELL_DATE", "PRODUCT_VALUE_1", "PRODUCT_VALUE_2", "PRODUCT_VALUE_3",
                            "PRODUCT_VALUE_4",
                            "PRODUCT_VALUE_5", "PRODUCT_VALUE_6", "PRODUCT_STATUS"]







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


def color_add(color_name=None, color_name_en=None):
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
                'COLOR_NAME': color_name
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
            for name in ["PRODUCT_ID", "PRODUCT_GET_DATE", "PRODUCT_ID_NUMBER", 'PRODUCT_NAME', 'PRODUCT_BRAND_NAME',
                         'PRODUCT_GET_DATE', 'PRODUCT_STATUS']:
                data_row[name] = str(getattr(row, name))
            data.append(data_row)
    session_sql.close()
    return data


def product_view_prices(PRODUCT_ID):
    session_sql = SessionSql()
    rs_product_view = session_sql.query(PRODUCT).filter(PRODUCT.PRODUCT_ID == PRODUCT_ID).first()
    data = {}
    if rs_product_view is not None:
        for name in ["PRODUCT_ID", "PRODUCT_ID_NUMBER", 'PRODUCT_NAME', 'PRODUCT_GET_DATE', 'PRODUCT_SELL_DATE',
                     'PRODUCT_VALUE_1', 'PRODUCT_VALUE_2', 'PRODUCT_VALUE_3', 'PRODUCT_VALUE_4', 'PRODUCT_VALUE_5',
                     'PRODUCT_VALUE_6', "PRODUCT_STATUS"]:
            if name in ['PRODUCT_VALUE_1', 'PRODUCT_VALUE_2', 'PRODUCT_VALUE_3', 'PRODUCT_VALUE_4'
                , 'PRODUCT_VALUE_5', 'PRODUCT_VALUE_6']:
                if getattr(rs_product_view, name) is None or int(getattr(rs_product_view, name)) == 0:
                    data[name] = str(getattr(rs_product_view, name))
                else:
                    # data[name] = str(getattr(rs_product_view, name))
                    data[name + '_number'] = int(getattr(rs_product_view, name))
                    data[name] = "{:,}".format(getattr(rs_product_view, name))
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
        for row in rs_product_view.all():
            data_row = {}
            for ind_n, name in enumerate(
                    ['PRODUCT_ID_NUMBER', 'PRODUCT_NAME', 'PRODUCT_DES', 'PRODUCT_TYPE_NAME', 'PRODUCT_BRAND_NAME',
                     'PRODUCT_MODEL_NAME', 'PRODUCT_ORIGIN', 'PRODUCT_RELEASE_YEAR', 'PRODUCT_YEAR', 'PRODUCT_SEAT',
                     'PRODUCT_FUEL_NAME', 'PRODUCT_COLOR', 'PRODUCT_ODO', 'PRODUCT_ENGINE', 'PRODUCT_GET_DATE',
                     'PRODUCT_SELL_DATE', 'PRODUCT_VALUE_1', 'PRODUCT_VALUE_2', 'PRODUCT_VALUE_3', 'PRODUCT_VALUE_4'
                        , 'PRODUCT_VALUE_5', 'PRODUCT_VALUE_6']):
                if name in ['PRODUCT_VALUE_1', 'PRODUCT_VALUE_2', 'PRODUCT_VALUE_3', 'PRODUCT_VALUE_4'
                    , 'PRODUCT_VALUE_5', 'PRODUCT_VALUE_6']:
                    data_row[data_name[ind_n] + '_number'] = int(getattr(row, name))
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
            'BRAND_ID': str(getattr(row, 'BRAND_ID')),
            'BRAND_NAME': str(getattr(row, 'BRAND_NAME'))
        }
        rs_model = session_sql.query(BRAND_MODEL).filter(BRAND_MODEL.BRAND_ID == getattr(row, 'BRAND_ID'))
        data_mode_row = []
        for row_model in rs_model.all():
            data_model = {}
            data_model['MODEL_ID'] = str(getattr(row_model, 'MODEL_ID'))
            data_model['MODEL_NAME'] = str(getattr(row_model, 'MODEL_NAME'))
            data_mode_row.append(data_model)

        data_brand['MODEL'] = data_mode_row
        data.append(data_brand)
    session_sql.close()
    return data


def product_get_max_id():
    return get_max_id(PRODUCT.PRODUCT_ID)


def product_get_cols():
    return PRODUCT_cols


def product_get_cols_small():
    return PRODUCT_cols_small


def product_add(json_add):
    session_sql = SessionSql()
    print(json_add)
    json_insert = {}
    try:
        for name_cols in PRODUCT_cols_small:
            if name_cols == "PRODUCT_SELL_DATE":
                json_insert[name_cols] = None
            else:
                json_insert[name_cols] = json_add[name_cols]
                if name_cols == "PRODUCT_BRAND_ID":
                    json_insert["PRODUCT_BRAND_NAME"] = session_sql.query(BRAND.BRAND_NAME). \
                        filter(BRAND.BRAND_ID == json_add['PRODUCT_BRAND_ID']).first()[0]
                if name_cols == "PRODUCT_MODEL_ID":
                    json_insert["PRODUCT_MODEL_NAME"] = session_sql.query(BRAND_MODEL.MODEL_NAME). \
                        filter(BRAND_MODEL.MODEL_ID == json_add['PRODUCT_MODEL_ID']).first()[0]
                if name_cols == "PRODUCT_TYPE_ID":
                    json_insert["PRODUCT_TYPE_NAME"] = session_sql.query(TYPE.TYPE_NAME). \
                        filter(TYPE.TYPE_ID == json_add['PRODUCT_TYPE_ID']).first()[0]
        try:
            obj = PRODUCT(**json_insert)
            session_sql.add(obj)
            session_sql.commit()
            error_code = 0
            max_id = json_add['PRODUCT_ID']
        except Exception as e:
            print(e)
            error_code = 1
            max_id = 0
    except:
        error_code = 1
        max_id = 0
    print(json_insert)
    print(error_code, json_add['PRODUCT_ID'])
    session_sql.close()
    return error_code, max_id


def product_get_cols_small_cap_nhat_gia():
    return PRODUCT_cols_small_cap_nhat_gia


def product_cols_small_cap_nhat_gia_no_val_6():
    return PRODUCT_cols_small_cap_nhat_gia_no_val_6


def product_update_gia_xe(json_data):
    session_sql = SessionSql()
    json_data_update = {}
    PRODUCT_ID = json_data["PRODUCT_ID"]
    for name in PRODUCT_cols_small_cap_nhat_gia_no_val_6:
        if name != 'PRODUCT_ID':
            if json_data[name] != "":
                if name in ["PRODUCT_VALUE_1", "PRODUCT_VALUE_2",
                            "PRODUCT_VALUE_3", "PRODUCT_VALUE_4", "PRODUCT_VALUE_5"]:
                    change_name = json_data[name]
                    new_name = []
                    print(name, change_name)
                    for i in range(0, len(change_name)):
                        if change_name[i].isnumeric():
                            new_name.append(change_name[i])
                    new_name = int(''.join(new_name))
                    json_data_update[name] = new_name
                else:
                    json_data_update[name] = json_data[name]
    json_data_update['PRODUCT_VALUE_6'] = int(json_data_update['PRODUCT_VALUE_5']) - (
            int(json_data_update['PRODUCT_VALUE_1']) + int(json_data_update['PRODUCT_VALUE_2']) + int(
        json_data_update['PRODUCT_VALUE_4']))
    try:
        rs = session_sql.query(PRODUCT).filter(PRODUCT.PRODUCT_ID == PRODUCT_ID).update(json_data_update)
        if rs == 1:
            session_sql.commit()
    except:
        pass
    session_sql.close()


def product_add_new_short_5_para(json_data):
    session_sql = SessionSql()
    json_insert = {}
    json_return = {}
    for name in PRODUCT_cols:
        try:
            json_insert[name] = json_data[name]
        except:
            json_insert[name] = None

    try:
        json_insert["PRODUCT_ID"] = int(json_data["PRODUCT_ID"])
        json_insert["PRODUCT_ID_NUMBER"] = str(json_data['PRODUCT_ID_NUMBER'])
        json_insert["PRODUCT_NAME"] = str(json_data['PRODUCT_NAME'])
        json_insert["PRODUCT_LICENSE_PLATE"] = str(json_data['PRODUCT_LICENSE_PLATE'])

        json_insert["PRODUCT_BRAND_ID"] = int(json_data['PRODUCT_BRAND_ID'])
        json_insert["PRODUCT_BRAND_NAME"] = str(
            session_sql.query(BRAND.BRAND_NAME).filter(BRAND.BRAND_ID == int(json_data['PRODUCT_BRAND_ID'])).first()[0])

        json_insert["PRODUCT_MODEL_ID"] = int(json_data['PRODUCT_MODEL_ID'])
        json_insert["PRODUCT_MODEL_NAME"] = str(session_sql.query(BRAND_MODEL.MODEL_NAME).filter(
            BRAND_MODEL.MODEL_ID == int(json_data['PRODUCT_MODEL_ID'])).first()[0])
        value_3 = ''
        json_insert["PRODUCT_VALUE_1"] = 0
        json_insert["PRODUCT_VALUE_2"] = 0
        json_insert["PRODUCT_VALUE_3"] = int(value_3.join(json_data['PRODUCT_VALUE_3'].split(',')))
        json_insert["PRODUCT_VALUE_4"] = 0
        json_insert["PRODUCT_VALUE_5"] = 0
        json_insert["PRODUCT_VALUE_6"] = 0
        json_insert["PRODUCT_VALUE_7"] = 0
        json_insert["PRODUCT_ODO"] = 0
        json_insert["PRODUCT_STATUS"] = str(json_data['PRODUCT_STATUS'])
        json_insert["PRODUCT_USING_STATUS"] = 1
        # print("json_insert", json_insert)
        try:
            obj = PRODUCT(**json_insert)
            session_sql.add(obj)
            session_sql.commit()
            error_code = 0
            json_return = json_insert
        except Exception as e:
            print(e)
            error_code = 1
    except:
        error_code = 1
    session_sql.close()
    return error_code, json_return


def product_view_one(PRODUCT_ID):
    session_sql = SessionSql()
    rs = session_sql.query(PRODUCT).filter(PRODUCT.PRODUCT_ID == PRODUCT_ID).first()
    data_return = {}
    if rs is not None:
        for name in PRODUCT_cols:
            # if name in ['PRODUCT_VALUE_1','PRODUCT_VALUE_2','PRODUCT_VALUE3_','PRODUCT_VALUE_4','PRODUCT_VALUE_5',
            #             'PRODUCT_VALUE_6',]:
            #     data_return[name] = str(getattr(rs, name)) + " VNĐ"
            # else:
            data_return[name] = str(getattr(rs, name))
    session_sql.close()
    return data_return


# Quan Ly Xe
def product_cap_nhat_lai(PRODUCT_ID):
    session_sql = SessionSql()
    rs = session_sql.query(PRODUCT).filter(PRODUCT.PRODUCT_ID == PRODUCT_ID).first()
    gia_nhap = getattr(rs, "PRODUCT_VALUE_1")
    chi_phi_nhap = getattr(rs, "PRODUCT_VALUE_2")
    chi_phi_ban = getattr(rs, "PRODUCT_VALUE_4")
    gia_ban_thuc_te = getattr(rs, "PRODUCT_VALUE_5")
    lai_thu_duoc = int(gia_ban_thuc_te) - (int(gia_nhap) + int(chi_phi_nhap) + int(chi_phi_ban))
    session_sql.query(PRODUCT).filter(PRODUCT.PRODUCT_ID == PRODUCT_ID).update({"PRODUCT_VALUE_6": lai_thu_duoc})
    session_sql.commit()
    session_sql.close()


def product_cap_nhat_thong_tin_xe(json_data):
    session_sql = SessionSql()
    json_update = {}
    print(json_data)
    PRODUCT_ID = 0
    try:
        PRODUCT_ID = int(json_data['PRODUCT_ID'])
        try:
            BRAND_ID = int(json_data['PRODUCT_BRAND_ID'])
            BRAND_NAME = str(session_sql.query(BRAND.BRAND_NAME).filter(BRAND.BRAND_ID == BRAND_ID).first()[0])
            json_update['PRODUCT_BRAND_ID'] = BRAND_ID
            json_update['PRODUCT_BRAND_NAME'] = BRAND_NAME
        except:
            pass

        try:
            MODEL_ID = int(json_data['PRODUCT_MODEL_ID'])
            MODEL_NAME = str(
                session_sql.query(BRAND_MODEL.MODEL_NAME).filter(BRAND_MODEL.MODEL_ID == MODEL_ID).first()[0])
            json_update['PRODUCT_MODEL_ID'] = MODEL_ID
            json_update['PRODUCT_MODEL_NAME'] = MODEL_NAME
        except:
            pass

        try:
            TYPE_ID = int(json_data['PRODUCT_TYPE_ID'])
            TYPE_NAME = str(session_sql.query(TYPE.TYPE_NAME).filter(TYPE.TYPE_ID == TYPE_ID).first()[0])
            json_update['PRODUCT_TYPE_ID'] = TYPE_ID
            json_update['PRODUCT_TYPE_NAME'] = TYPE_NAME
        except:
            pass

        try:
            PRODUCT_NAME = str(json_data['PRODUCT_NAME'])
            if PRODUCT_NAME != "":
                json_update['PRODUCT_NAME'] = PRODUCT_NAME
        except:
            pass

        try:
            PRODUCT_NAME = str(json_data['PRODUCT_LICENSE_PLATE'])
            if PRODUCT_NAME != "":
                json_update['PRODUCT_LICENSE_PLATE'] = PRODUCT_NAME
        except:
            pass

        try:
            PRODUCT_NAME = str(json_data['PRODUCT_LICENSE_PLATE_PLACE'])
            if PRODUCT_NAME != "":
                json_update['PRODUCT_LICENSE_PLATE_PLACE'] = PRODUCT_NAME
        except:
            pass

        try:
            PRODUCT_NAME = str(json_data['PRODUCT_NAME'])
            if PRODUCT_NAME != "":
                json_update['PRODUCT_NAME'] = PRODUCT_NAME
        except:
            pass

        try:
            PRODUCT_NAME = str(json_data['PRODUCT_REGISTRY_DATE'])
            if PRODUCT_NAME != "":
                json_update['PRODUCT_REGISTRY_DATE'] = PRODUCT_NAME
        except:
            pass

        try:
            PRODUCT_NAME = str(json_data['PRODUCT_STATUS'])
            if PRODUCT_NAME != "":
                json_update['PRODUCT_STATUS'] = PRODUCT_NAME
        except:
            pass

        rs = session_sql.query(PRODUCT).filter(PRODUCT.PRODUCT_ID == PRODUCT_ID).update(json_update)
        if rs == 1:
            session_sql.commit()
            error_code = 0
        else:
            error_code = 1

    except:
        error_code = 1
    session_sql.close()
    return error_code, PRODUCT_ID


def product_cap_nhat_chi_phi_gia(json_data):
    session_sql = SessionSql()
    json_update = {}
    try:
        PRODUCT_ID = int(json_data['PRODUCT_ID'])

        try:
            PRODUCT_GET_DATE = str(json_data['PRODUCT_GET_DATE'])
            if PRODUCT_GET_DATE != "":
                json_update['PRODUCT_GET_DATE'] = PRODUCT_GET_DATE
        except:
            pass

        try:
            PRODUCT_VALUE_1 = str(json_data['PRODUCT_VALUE_1'])
            if PRODUCT_VALUE_1 != "":
                PRODUCT_VALUE_1 = str(PRODUCT_VALUE_1)
                VALUE = []
                for i in PRODUCT_VALUE_1:
                    if i.isnumeric():
                        VALUE.append(i)
                NUMBER_VALUE = ''
                NUMBER_VALUE = NUMBER_VALUE.join(VALUE)
                json_update['PRODUCT_VALUE_1'] = NUMBER_VALUE
        except:
            pass
        try:
            PRODUCT_VALUE_1 = str(json_data['PRODUCT_VALUE_2'])
            if PRODUCT_VALUE_1 != "":
                PRODUCT_VALUE_1 = str(PRODUCT_VALUE_1)
                VALUE = []
                for i in PRODUCT_VALUE_1:
                    if i.isnumeric():
                        VALUE.append(i)
                NUMBER_VALUE = ''
                NUMBER_VALUE = NUMBER_VALUE.join(VALUE)
                json_update['PRODUCT_VALUE_2'] = NUMBER_VALUE
        except:
            pass
        try:
            PRODUCT_VALUE_1 = str(json_data['PRODUCT_VALUE_3'])
            if PRODUCT_VALUE_1 != "":
                PRODUCT_VALUE_1 = str(PRODUCT_VALUE_1)
                VALUE = []
                for i in PRODUCT_VALUE_1:
                    if i.isnumeric():
                        VALUE.append(i)
                NUMBER_VALUE = ''
                NUMBER_VALUE = NUMBER_VALUE.join(VALUE)
                json_update['PRODUCT_VALUE_3'] = NUMBER_VALUE
        except:
            pass

        print(json_update)
        rs = session_sql.query(PRODUCT).filter(PRODUCT.PRODUCT_ID == PRODUCT_ID).update(json_update)
        if rs == 1:
            print(1, json_update)
            session_sql.commit()
            product_cap_nhat_lai(PRODUCT_ID)
            error_code = 0
        else:
            print(2, json_update)
            error_code = 1

    except:
        error_code = 1
    session_sql.close()
    return error_code


def product_cap_nhat_chi_phi_ban_va_gia_ban_thuc_te(json_data):
    session_sql = SessionSql()
    json_update = {}
    print(json_data)
    try:
        PRODUCT_ID = int(json_data['PRODUCT_ID'])

        try:
            PRODUCT_GET_DATE = str(json_data['PRODUCT_SELL_DATE'])
            if PRODUCT_GET_DATE != "":
                json_update['PRODUCT_SELL_DATE'] = PRODUCT_GET_DATE
        except:
            pass

        try:
            PRODUCT_VALUE_1 = str(json_data['PRODUCT_VALUE_4'])
            if PRODUCT_VALUE_1 != "":
                PRODUCT_VALUE_1 = str(PRODUCT_VALUE_1)
                VALUE = []
                for i in PRODUCT_VALUE_1:
                    if i.isnumeric():
                        VALUE.append(i)
                NUMBER_VALUE = ''
                NUMBER_VALUE = NUMBER_VALUE.join(VALUE)
                json_update['PRODUCT_VALUE_4'] = NUMBER_VALUE
        except:
            pass
        try:
            PRODUCT_VALUE_1 = str(json_data['PRODUCT_VALUE_5'])
            if PRODUCT_VALUE_1 != "":
                PRODUCT_VALUE_1 = str(PRODUCT_VALUE_1)
                VALUE = []
                for i in PRODUCT_VALUE_1:
                    if i.isnumeric():
                        VALUE.append(i)
                NUMBER_VALUE = ''
                NUMBER_VALUE = NUMBER_VALUE.join(VALUE)
                json_update['PRODUCT_VALUE_5'] = NUMBER_VALUE
        except:
            pass

        print(json_update)
        rs = session_sql.query(PRODUCT).filter(PRODUCT.PRODUCT_ID == PRODUCT_ID).update(json_update)
        if rs == 1:
            print(1, json_update)
            session_sql.commit()
            product_cap_nhat_lai(PRODUCT_ID)
            error_code = 0
        else:
            print(2, json_update)
            error_code = 1

    except:
        error_code = 1
    session_sql.close()
    return error_code


def product_cap_nhat_chi_tiet_xe_1(json_data):
    session_sql = SessionSql()
    json_update = {}
    print(json_data)
    try:
        PRODUCT_ID = int(json_data['PRODUCT_ID'])

        try:
            VALUE = str(json_data['PRODUCT_ORIGIN'])
            if VALUE != "":
                json_update['PRODUCT_ORIGIN'] = VALUE
        except:
            pass

        try:
            VALUE = str(json_data['PRODUCT_RELEASE_YEAR'])
            if VALUE != "":
                json_update['PRODUCT_RELEASE_YEAR'] = VALUE
        except:
            pass

        try:
            VALUE = str(json_data['PRODUCT_YEAR'])
            if VALUE != "":
                json_update['PRODUCT_YEAR'] = VALUE
        except:
            pass

        try:
            VALUE = str(json_data['PRODUCT_SEAT'])
            if VALUE != "":
                json_update['PRODUCT_SEAT'] = VALUE
        except:
            pass

        print(json_update)
        rs = session_sql.query(PRODUCT).filter(PRODUCT.PRODUCT_ID == PRODUCT_ID).update(json_update)
        if rs == 1:
            print(1, json_update)
            session_sql.commit()
            error_code = 0
        else:
            print(2, json_update)
            error_code = 1

    except:
        error_code = 1
    session_sql.close()
    return error_code

def product_cap_nhat_chi_tiet_xe_2(json_data):
    session_sql = SessionSql()
    json_update = {}
    print(json_data)
    try:
        PRODUCT_ID = int(json_data['PRODUCT_ID'])

        try:
            VALUE = str(json_data['PRODUCT_COLOR'])
            if VALUE != "":
                json_update['PRODUCT_COLOR'] = VALUE
        except:
            pass

        try:
            VALUE = str(json_data['PRODUCT_ODO'])
            if VALUE != "":
                json_update['PRODUCT_ODO'] = VALUE
        except:
            pass

        try:
            VALUE = str(json_data['PRODUCT_FUEL_NAME'])
            if VALUE != "":
                json_update['PRODUCT_FUEL_NAME'] = VALUE
        except:
            pass

        try:
            VALUE = str(json_data['PRODUCT_ENGINE'])
            if VALUE != "":
                json_update['PRODUCT_ENGINE'] = VALUE
        except:
            pass

        print(json_update)
        rs = session_sql.query(PRODUCT).filter(PRODUCT.PRODUCT_ID == PRODUCT_ID).update(json_update)
        if rs == 1:
            print(1, json_update)
            session_sql.commit()
            error_code = 0
        else:
            print(2, json_update)
            error_code = 1

    except:
        error_code = 1
    session_sql.close()
    return error_code

def product_cap_nhat_trang_thai_xe(json_data):
    session_sql = SessionSql()
    json_update = {}
    print(json_data)
    try:
        PRODUCT_ID = int(json_data['PRODUCT_ID'])

        try:
            VALUE = str(json_data['PRODUCT_STATUS'])
            if VALUE != "":
                json_update['PRODUCT_STATUS'] = VALUE
        except:
            pass


        rs = session_sql.query(PRODUCT).filter(PRODUCT.PRODUCT_ID == PRODUCT_ID).update(json_update)
        if rs == 1:
            print(1, json_update)
            session_sql.commit()
            error_code = 0
        else:
            print(2, json_update)
            error_code = 1

    except:
        error_code = 1
    session_sql.close()
    return error_code

def product_update_all(json_data):
    session_sql = SessionSql()
    json_update = {}
    try:
        PRODUCT_ID = int(json_data['PRODUCT_ID'])
        try:
            BRAND_ID = int(json_data['PRODUCT_BRAND_ID'])
            BRAND_NAME = str(session_sql.query(BRAND.BRAND_NAME).filter(BRAND.BRAND_ID == BRAND_ID).first()[0])
            json_update['PRODUCT_BRAND_ID'] = BRAND_ID
            json_update['PRODUCT_BRAND_NAME'] = BRAND_NAME
        except:
            pass

        try:
            MODEL_ID = int(json_data['PRODUCT_MODEL_ID'])
            MODEL_NAME = str(
                session_sql.query(BRAND_MODEL.MODEL_NAME).filter(BRAND_MODEL.MODEL_ID == MODEL_ID).first()[0])
            json_update['PRODUCT_MODEL_ID'] = MODEL_ID
            json_update['PRODUCT_MODEL_NAME'] = MODEL_NAME
        except:
            pass

        try:
            TYPE_ID = int(json_data['PRODUCT_TYPE_ID'])
            TYPE_NAME = str(session_sql.query(TYPE.TYPE_NAME).filter(TYPE.TYPE_ID == TYPE_ID).first()[0])
            json_update['PRODUCT_TYPE_ID'] = TYPE_ID
            json_update['PRODUCT_TYPE_NAME'] = TYPE_NAME
        except:
            pass

        try:
            PRODUCT_NAME = str(json_data['PRODUCT_NAME'])
            if PRODUCT_NAME != "":
                json_update['PRODUCT_NAME'] = PRODUCT_NAME
        except:
            pass

        try:
            PRODUCT_NAME = str(json_data['PRODUCT_LICENSE_PLATE'])
            if PRODUCT_NAME != "":
                json_update['PRODUCT_LICENSE_PLATE'] = PRODUCT_NAME
        except:
            pass

        try:
            PRODUCT_NAME = str(json_data['PRODUCT_LICENSE_PLATE_PLACE'])
            if PRODUCT_NAME != "":
                json_update['PRODUCT_LICENSE_PLATE_PLACE'] = PRODUCT_NAME
        except:
            pass

        try:
            PRODUCT_NAME = str(json_data['PRODUCT_NAME'])
            if PRODUCT_NAME != "":
                json_update['PRODUCT_NAME'] = PRODUCT_NAME
        except:
            pass

        try:
            PRODUCT_NAME = str(json_data['PRODUCT_REGISTRY_DATE'])
            if PRODUCT_NAME != "":
                json_update['PRODUCT_REGISTRY_DATE'] = PRODUCT_NAME
        except:
            pass

        try:
            PRODUCT_NAME = str(json_data['PRODUCT_STATUS'])
            if PRODUCT_NAME != "":
                json_update['PRODUCT_STATUS'] = PRODUCT_NAME
        except:
            pass

        try:
            PRODUCT_GET_DATE = str(json_data['PRODUCT_GET_DATE'])
            if PRODUCT_GET_DATE != "":
                json_update['PRODUCT_GET_DATE'] = PRODUCT_GET_DATE
        except:
            pass

        try:
            PRODUCT_VALUE_1 = str(json_data['PRODUCT_VALUE_1'])
            if PRODUCT_VALUE_1 != "":
                VALUE = PRODUCT_VALUE_1.split(',')
                NUMBER_VALUE = ''
                NUMBER_VALUE = NUMBER_VALUE.join(VALUE)
                json_update['PRODUCT_VALUE_1'] = NUMBER_VALUE
        except:
            pass
        try:
            PRODUCT_VALUE_1 = str(json_data['PRODUCT_VALUE_2'])
            if PRODUCT_VALUE_1 != "":
                VALUE = PRODUCT_VALUE_1.split(',')
                NUMBER_VALUE = ''
                NUMBER_VALUE = NUMBER_VALUE.join(VALUE)
                json_update['PRODUCT_VALUE_2'] = NUMBER_VALUE
        except:
            pass
        try:
            PRODUCT_VALUE_1 = str(json_data['PRODUCT_VALUE_3'])
            if PRODUCT_VALUE_1 != "":
                VALUE = PRODUCT_VALUE_1.split(',')
                NUMBER_VALUE = ''
                NUMBER_VALUE = NUMBER_VALUE.join(VALUE)
                json_update['PRODUCT_VALUE_3'] = NUMBER_VALUE
        except:
            pass
        try:
            PRODUCT_GET_DATE = str(json_data['PRODUCT_SELL_DATE'])
            if PRODUCT_GET_DATE != "":
                json_update['PRODUCT_SELL_DATE'] = PRODUCT_GET_DATE
        except:
            pass

        try:
            PRODUCT_VALUE_1 = str(json_data['PRODUCT_VALUE_4'])
            if PRODUCT_VALUE_1 != "":
                VALUE = PRODUCT_VALUE_1.split(',')
                NUMBER_VALUE = ''
                NUMBER_VALUE = NUMBER_VALUE.join(VALUE)
                json_update['PRODUCT_VALUE_4'] = NUMBER_VALUE
        except:
            pass
        try:
            PRODUCT_VALUE_1 = str(json_data['PRODUCT_VALUE_5'])
            if PRODUCT_VALUE_1 != "":
                VALUE = PRODUCT_VALUE_1.split(',')
                NUMBER_VALUE = ''
                NUMBER_VALUE = NUMBER_VALUE.join(VALUE)
                json_update['PRODUCT_VALUE_5'] = NUMBER_VALUE
        except:
            pass

        try:
            VALUE = str(json_data['PRODUCT_ORIGIN'])
            if VALUE != "":
                json_update['PRODUCT_ORIGIN'] = VALUE
        except:
            pass

        try:
            VALUE = str(json_data['PRODUCT_RELEASE_YEAR'])
            if VALUE != "":
                json_update['PRODUCT_RELEASE_YEAR'] = VALUE
        except:
            pass

        try:
            VALUE = str(json_data['PRODUCT_SEAT'])
            if VALUE != "":
                json_update['PRODUCT_SEAT'] = VALUE
        except:
            pass

        try:
            VALUE = str(json_data['PRODUCT_COLOR'])
            if VALUE != "":
                json_update['PRODUCT_COLOR'] = VALUE
        except:
            pass

        try:
            PRODUCT_VALUE_1 = str(json_data['PRODUCT_ODO'])
            if PRODUCT_VALUE_1 != "":
                VALUE = PRODUCT_VALUE_1.split(',')
                NUMBER_VALUE = ''
                NUMBER_VALUE = NUMBER_VALUE.join(VALUE)
                json_update['PRODUCT_ODO'] = NUMBER_VALUE
        except:
            pass

        try:
            VALUE = str(json_data['PRODUCT_FUEL_NAME'])
            if VALUE != "":
                json_update['PRODUCT_FUEL_NAME'] = VALUE
        except:
            pass

        try:
            VALUE = str(json_data['PRODUCT_ENGINE'])
            if VALUE != "":
                json_update['PRODUCT_ENGINE'] = VALUE
        except:
            pass
        print(json_update)
        print(len(json_update))
        if len(json_update) > 0:
            rs = session_sql.query(PRODUCT).filter(PRODUCT.PRODUCT_ID == PRODUCT_ID).update(json_update)
            if rs == 1:
                print(json_update)
                session_sql.commit()
                product_cap_nhat_lai(PRODUCT_ID)
                error_code = 0
            else:
                error_code = 1
        else:
            error_code = 1

    except:
        error_code = 1
    session_sql.close()
    return error_code

def product_upload_hinh_anh(data):
    # session_sql = SessionSql()
    print(len(data))
    # rs = session_sql.query(PRODUCT_IMAGE).filter(PRODUCT_IMAGE.PRODUCT_ID == 1).update({"PRODUCT_IMAGE_1": image_1})
    # print(rs)
    # session_sql.close()

    return 1


def product_deactive(json_data):
    session_sql = SessionSql()
    try:
        PRODUCT_ID = int(json_data['PRODUCT_ID'])
        rs = session_sql.query(PRODUCT).filter(PRODUCT.PRODUCT_ID == PRODUCT_ID).update({
            "PRODUCT_USING_STATUS" : 0
        })
        if rs == 1:
            session_sql.commit()
            error_code = 0
        else:
            error_code = 1
    except:
        error_code = 1
    session_sql.close()
    return error_code
