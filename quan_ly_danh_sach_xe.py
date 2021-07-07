from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, and_, inspect, func
from datetime import datetime, time, timedelta, date
import config

Base = automap_base()
engine = config.get_config()
SessionSql = sessionmaker()
SessionSql.configure(bind=engine)
Base.prepare(engine, reflect=True)

COLOR = Base.classes.COLOR
TYPE = Base.classes.TYPE
BRAND_MODEL = Base.classes.BRAND_MODEL
BRAND = Base.classes.BRAND

PRODUCT = Base.classes.PRODUCT
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

PRODUCT_danh_sach_xe_all = ["PRODUCT_ID", "PRODUCT_ID_NUMBER", "PRODUCT_NAME", "PRODUCT_MODEL_NAME",
                            "PRODUCT_BRAND_ID", "PRODUCT_BRAND_NAME", "PRODUCT_GET_DATE", "PRODUCT_TYPE_NAME",
                            "PRODUCT_STATUS"]


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


def product_danh_sach_xe():
    session_sql = SessionSql()
    rs_product_view = session_sql.query(PRODUCT).filter(PRODUCT.PRODUCT_USING_STATUS == 1)
    data = []
    for row in rs_product_view.all():
        data_row = {}
        for name in PRODUCT_danh_sach_xe_all:
            try:
                if name == "PRODUCT_GET_DATE":
                    str_date = str(getattr(row, name)).split('-')
                    data_row[name] = str_date[2] + '/' + str_date[1] + '/' +str_date[0]
                else:
                    data_row[name] = str(getattr(row, name))
            except:
                data_row[name] = ""
        data.append(data_row)
    session_sql.close()
    return data
