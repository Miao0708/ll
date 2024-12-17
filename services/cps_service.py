# app/services/cps_order_generate.py

import pymysql
from random import randint, uniform, choice
from allpairspy import AllPairs
from loguru import logger
import math
from .base_service import BaseService
from ..config.cps_config import *


class CpsOrderGenerate:
    def __init__(self, creative_unit_ids):
        self.db_order = pymysql.connect(
            host='10.103.46.184',
            port=8066,
            user='ai_dsp_test',
            passwd='imsp_vcloud',
            db='iflytek_overseas_dsp'
        )
        self.db_report = pymysql.connect(
            host='10.103.46.184',
            port=8066,
            user='ai_dsp_test',
            passwd='imsp_vcloud',
            db='iflytek_overseas_report'
        )
        self.cursor_order = self.db_order.cursor()
        self.cursor_report = self.db_report.cursor()
        self.creative_unit_ids = creative_unit_ids
        self.insert_cps_order_sql = InsertCpsOrderSql
        self.insert_cps_plan_hour_sql = InsertCpsPlanHourSql

    def _insert_data(self, order_data):
        product_title = self._get_product_title(order_data['product_id'])
        order_time = order_data["order_date"] + randint(0, 86400 - 1)
        data = {
            'creative_unit_id': self.creative_unit_id,
            'project_id': self.project_id,
            'master_id': self.master_id,
            'plan_id': self.plan_id,
            'event_id': '',
            'order_id': "3031500351559471",
            'parent_order_id': "3031486135613943",
            'product_count': randint(1, 10),
            'product_title': product_title,
            'bid_id': '4480f70d-78b7-4192-938d-0f77a9a2c1e2',
            'ifly_uid': 'unique_sign_for_delete',
            'info': 'info_value',
            'order_time': order_time,
            'pay_time': order_time,
            'finished_time': 0,
            'settlement_time': 0,
            'estimate_amount': randint,
            'estimate_commission': round(uniform(1, 10), 2),
            'actual_amount': round(uniform(1, 10), 2),
            'actual_commission': round(uniform(0, 3), 2),
            'new_buyer_commission': round(uniform(2, 8), 2),
            'is_hot_product': choice([0, 1]),
            'is_affiliate_product': choice([0, 1]),
            'is_new_buyer': choice([0, 1]),
            'is_sync': 1,
            'category': choice(self.order_category),
            'product_status': 2,
            'bid_time': order_time,
            'adx_id': 107,
            'bundle': '',
            'action_type': 1,
            'account_type': 1,
            'currency': choice(['USD', 'CNY', 'EUR', 'GBP', 'VND']),
            'country': choice(CountryList),
        }
        data.update(order_data)
        logger.debug(order_data)  # 日志
        self.cursor_order.execute(self.insert_cps_order_sql, data)
        self.db_order.commit()

    def _init_info(self):
        sql = """
            SELECT master_id, campaign_id, plan_id, creative_id 
            FROM m_creative_unit 
            WHERE id = %s and is_del = 0
        """
        self.cursor_order.execute(sql, (self.creative_unit_id,))
        data = self.cursor_order.fetchall()[0]
        self.master_id, self.campaign_id, self.plan_id, self.creative_id = data

        sql = """
            SELECT user_id FROM u_user_resource
            WHERE resource_type = 1 and resource_id = %s
        """
        self.cursor_order.execute(sql, (self.master_id,))
        self.agent_id = self.cursor_order.fetchone()[0]

        sql = """
            SELECT project_id FROM m_project_resource
            WHERE resource_id = %s
        """
        self.cursor_order.execute(sql, (self.master_id,))
        self.project_id = self.cursor_order.fetchone()[0]

        self.tracking_ids = self._get_tracking_ids()
        self.product_ids = self._get_product_ids()
        logger.info("获取创意对应的投放账户信息")
        logger.info(
            f"agent_id：{self.agent_id}  master_id：{self.master_id}  campaign_id：{self.campaign_id}  project_id：{self.project_id}"
        )

    def _combine_variables(self):
        values = [OrderStatusList, self.tracking_ids, OrderDateList, ConversionTypeList]
        res = list(AllPairs(values))
        return res

    def _get_product_title(self, product_id):
        sql = """
            SELECT product_title FROM cps_product WHERE product_sign = %s
        """
        self.cursor_order.execute(sql, (product_id,))
        res = self.cursor_order.fetchone()[0]
        res = "No Title" if len(res) == 0 else res
        return res

    def _get_tracking_ids(self):
        sql = """
            SELECT DISTINCT(tracking_id) FROM m_tracking_id WHERE project_id = %s
        """
        self.cursor_order.execute(sql, (self.project_id,))
        tracking_ids = self.cursor_order.fetchall()
        res = [row[0] for row in tracking_ids]
        return res

    def _get_product_ids(self):
        if self.project_id == 25:
            self.order_category = AeProductCategoryList
            return AeProductIdList
        elif self.project_id == 26:
            self.order_category = AmazonProductCategoryList
            return AmazonProductIdList
        else:
            return []

    def _close_connection(self):
        if self.cursor_order and self.cursor_report:
            self.cursor_order.close()
            self.cursor_report.close()
        if self.db_order and self.db_report:
            self.db_order.close()
            self.db_report.close()

    def __del__(self):
        self._close_connection()

    def generate_cps_data(self):
        for creative_unit_id in self.creative_unit_ids:
            logger.info(f"开始生成创意{creative_unit_id}的cps订单")
            try:
                self.creative_unit_id = creative_unit_id
                self._init_info()
                self._generate_cps_order()
                logger.info(f"开始生成创意{creative_unit_id}的cps报表")
                self.generate_plan_hour_report()
            except Exception as e:
                logger.error(f"创意{creative_unit_id}生成cps订单或报表数据时出错：{str(e)}")

    def _generate_cps_order(self):
        vs = self._combine_variables()
        for v in vs:
            order_status = v[0]
            tracking_id = v[1]
            product_id = choice(self.product_ids)
            order_date = v[2]
            conversion_type = v[3]
            order_data = {
                'order_status': order_status,
                'tracking_id': tracking_id,
                'product_id': product_id,
                'order_date': order_date,
                'conversion_type': conversion_type,
            }
            self._insert_data(order_data)

    def delete_insert_data(self):
        logger.info("开始删除CPS订单及投放数据")
        sql = """
            DELETE FROM cps_order WHERE ifly_uid = %s
        """
        self.cursor_order.execute(sql, ("unique_sign_for_delete",))
        self.db_order.commit()

        sql = """
            DELETE FROM t_ads_dsp_flow_creative_unit_hour WHERE idx_action3 = %s
        """
        self.cursor_report.execute(sql, (715300,))
        self.db_report.commit()

    def generate_plan_hour_report(self,day):
        for ts in GenerateTimeStamp().generate_plan_day_hour_ts(day):
            base_info = [
                self.agent_id, self.master_id, self.campaign_id, self.plan_id, self.creative_id,
                self.creative_unit_id
            ]
            idx_info = [randint(10000, 30000)]
            for i in range(54):
                idx_info.append(randint(math.floor(idx_info[-1] * 0.7), idx_info[-1]))
            idx_info[7] = idx_info[7] * 1000000
            idx_info[8] = idx_info[8] * 500000
            idx_info[9] = idx_info[9] * 500000
            idx_info[15] = 715300
            data = ts + base_info + idx_info
            data_set = tuple(data)
            logger.debug(data_set)
            self.cursor_report.execute(self.insert_cps_plan_hour_sql, data_set)
            self.db_report.commit()


    # def execute(self, operation: str, **kwargs):
    #     if operation == "generate_cps_data":
    #         return self.generate_cps_data()
    #     elif operation == "regenerate":
    #         return self.regenerate()
    #     elif operation == "delete_insert_data":
    #         return self.delete_insert_data()
    #     elif operation == "test_generate_plan_hour_report":
    #         return self.test_generate_plan_hour_report()
    #     else:
    #         raise ValueError("Invalid operation for CpsOrderGenerate.")
