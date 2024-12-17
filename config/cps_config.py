import time
from datetime import datetime

ONE_DAY = 86400
ONE_HOUR = 3600


# 获取当前时间戳
class GenerateTimeStamp:
    """
    列表时间筛选框测试，生成凌晨时间戳
    """

    def __init__(self):
        # 获取当前时间凌晨的时间戳
        self.now = datetime.now()
        self.now_timestamp = int(time.mktime(self.now.timetuple()))
        self.current_midnight = int(
            time.mktime(datetime.now().replace(hour=0, minute=0, second=0, microsecond=0).timetuple()))

    def generate_order_timestamp(self):

        diff = [1, 7, 8, 30, 31]
        first_day_of_month = int(
            time.mktime(datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0).timetuple()))
        last_day_of_last_month = first_day_of_month - ONE_DAY
        res = [self.current_midnight, first_day_of_month, last_day_of_last_month]
        for days in diff:
            timestamp = self.current_midnight - ONE_DAY * days
            res.append(timestamp)
        return res

    def generate_plan_day_hour_ts(self, n):
        """
        获取近n天和当天24小时整点的时间戳
        :return:
        """
        start = self.current_midnight - n * ONE_DAY
        res = []
        for i in range(n+1):
            day_ts = start + i * ONE_DAY
            for j in range(24):
                hour = j
                hour_ts = day_ts + j * ONE_HOUR
                if hour_ts > self.now_timestamp:
                    break
                res.append([day_ts, hour_ts, hour])
        return res


CountryConfig = {
    'BG': '保加利亚',
    'MM': '缅甸',
    'CA': '加拿大',
    'CL': '智利',
    'CO': '哥伦比亚',
    'HR': '克罗地亚',
    'CY': '塞浦路斯',
    'CZ': '捷克',
    'DK': '丹麦',
    'EE': '爱沙尼亚',
    'FI': '芬兰',
    'FR': '法国',
    'DE': '德国',
    'GR': '希腊',
    'HU': '匈牙利',
    'IN': '印度',
    'AU': '澳大利亚',
    'ID': '印度尼西亚',
    'IE': '爱尔兰',
    'IL': '以色列',
    'IT': '意大利',
    'AF': '阿富汗',
    'AT': '奥地利',
    'KR': '韩国',
    'LV': '拉脱维亚',
    'LT': '立陶宛',
    'LU': '卢森堡',
    'MY': '马来西亚',
    'MT': '马耳他',
    'MX': '墨西哥',
    'BD': '孟加拉',
    'NP': '尼泊尔',
    'NL': '荷兰',
    'BE': '比利时',
    'PK': '巴基斯坦',
    'PH': '菲律宾',
    'PL': '波兰',
    'PT': '葡萄牙',
    'RO': '罗马尼亚',
    'RU': '俄罗斯',
    'SA': '沙特阿拉伯',
    'SG': '新加坡',
    'SK': '斯洛伐克',
    'VN': '越南',
    'SI': '斯洛文尼亚',
    'ES': '西班牙',
    'SE': '瑞典',
    'BR': '巴西',
    'TH': '泰国',
    'TR': '土耳其',
    'UA': '乌克兰',
    'EG': '埃及',
    'GB': '英国',
    'UK': '英国（勿用）',
    'US': '美国',
    'YE': '也门'
}

InsertCpsOrderSql = """INSERT INTO cps_order (
                            project_id, master_id, plan_id, creative_unit_id, event_id,
                            order_id, parent_order_id, order_status, tracking_id, product_id,
                            category, product_count, product_title, bid_id, ifly_uid, info,
                            order_date, order_time, pay_time, finished_time, settlement_time,
                            country, currency, estimate_amount, estimate_commission, actual_amount,
                            actual_commission, new_buyer_commission, conversion_type, is_hot_product,
                            is_affiliate_product, is_new_buyer, is_sync, product_status, bid_time, adx_id, bundle, 
                            action_type, account_type
                          ) VALUES (
                            %(project_id)s, %(master_id)s, %(plan_id)s, %(creative_unit_id)s, %(event_id)s,
                            %(order_id)s, %(parent_order_id)s, %(order_status)s, %(tracking_id)s, %(product_id)s,
                            %(category)s, %(product_count)s, %(product_title)s, %(bid_id)s, %(ifly_uid)s, %(info)s,
                            %(order_date)s, %(order_time)s, %(pay_time)s, %(finished_time)s, %(settlement_time)s,
                            %(country)s, %(currency)s, %(estimate_amount)s, %(estimate_commission)s, %(actual_amount)s,
                            %(actual_commission)s, %(new_buyer_commission)s, %(conversion_type)s, %(is_hot_product)s,
                            %(is_affiliate_product)s, %(is_new_buyer)s, %(is_sync)s, %(product_status)s, %(bid_time)s,
                             %(adx_id)s, %(bundle)s, %(action_type)s, %(account_type)s
                          )
                        """
InsertCpsPlanHourSql = """INSERT INTO t_ads_dsp_flow_creative_unit_hour 
                            (dim_day, dim_report_hour, dim_hour, dim_agent_id, dim_master_id, dim_campaign_id, 
                            dim_plan_id, dim_creative_id, dim_creative_unit_id, idx_bid, idx_inner_bid, idx_win, 
                            idx_view, idx_user_view, idx_click, idx_user_click, idx_media_cost, idx_platform_cost,
                            idx_report_cost, idx_reach, idx_action, idx_num_action, idx_action1, idx_action2, 
                            idx_action3, idx_action4, idx_action5, idx_action6, idx_action7, idx_action8, idx_action9, 
                            idx_action10, idx_action11, idx_action12, idx_action13, idx_action14, idx_action15, 
                            idx_action16, idx_action17, idx_action18, idx_action19, idx_action20, idx_action21, 
                            idx_action22, idx_action23, idx_action24, idx_action25, idx_action26, idx_action27, 
                            idx_action28, idx_action29, idx_action30, idx_action31, idx_action32, idx_action33, 
                            idx_action34, idx_action35, idx_action36, idx_action37, idx_action38, idx_action39, 
                            idx_action40, idx_settlement, idx_click_uniq_session) VALUES (%s, %s, %s, %s, %s, %s,
                             %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
OrderStatusConfig = {
    0: '未知',
    1: '已付款',
    2: '已收货',
    3: '佣金已结算',
    4: 'Invalid'
}
ConversionTypeConfig = {
    0: '未知',
    1: '直接转化',
    2: '间接转化'
}
AmazonProductCategoryConfig = {
    186606: '书籍-德国',
    229816: 'CDs & Vinyl-英国',
    255882: 'CDs & Vinyl-德国',
    266239: '书籍-英国',
    284266: 'DVD & Blu-ray-德国',
    300703: 'PC & Video Games-英国',
    300992: 'PC & Video Games-德国',
    468292: 'Toys & Games-英国',
    560798: 'Electronics & Photo-英国',
    562066: 'Electronics & Photo-德国',
    3146281: 'Home & Garden-英国',
    3167641: 'Home & Kitchen-德国',
    10925031: 'Garden-德国',
    11052671: 'Garden-英国',
    11052681: 'Home & Kitchen-英国',
    12950651: 'Toys-德国',
    16435051: 'Sports & Outdoors-德国',
    59624031: 'Baby Products-英国',
    64187031: 'Health & Personal Care-德国',
    65801031: 'Health & Personal Care-英国',
    72921031: 'Everything Else-德国',
    78191031: 'Automotive-德国',
    79903031: 'DIY & Tools-英国',
    80084031: 'DIY & Tools-德国',
    84230031: 'Beauty-德国',
    117332031: 'Beauty-英国',
    192413031: 'Stationery & Office Supplies-英国',
    192416031: 'Stationery & Office Supplies-德国',
    213077031: 'Lighting-英国',
    213083031: 'Lighting-德国',
    245407031: 'Outlet-英国',
    248877031: 'Automotive-英国',
    318949011: 'Sports & Outdoors-英国',
    340831031: 'Computers & Accessories-英国',
    340834031: 'Grocery-英国',
    340837031: 'Musical Instruments & DJ-英国',
    340840031: 'Pet Supplies-英国',
    340843031: 'Computer & Accessories-德国',
    340846031: 'Grocery-德国',
    340849031: 'Musical Instruments & DJ-德国',
    340852031: 'Pet Supplies-德国',
    341677031: 'Kindle Store-英国',
    355007011: 'Baby Products-德国',
    908798031: 'Large Appliances-英国',
    3765352031: 'Premium Beauty-德国',
    5866054031: 'Business, Industry & Science-英国',
    5866098031: 'Business, Industry & Science-德国',
    9699254031: 'Handmade Products-英国',
    11961407031: 'Fashion-英国',
    11961464031: 'Fashion-德国'
}
AeProductCategoryConfig = {
    2: 'Food',
    3: 'Apparel & Accessories',
    6: 'Home Appliances',
    7: 'Computer & Office',
    13: 'Home Improvement',
    15: 'Home & Garden',
    18: 'Sports & Entertainment',
    21: 'Office & School Supplies',
    26: 'Toys & Hobbies',
    30: '安全防护',
    34: 'Automobiles, Parts & Accessories',
    36: 'Jewelry & Accessories',
    39: 'Lights & Lighting',
    44: 'Consumer Electronics',
    66: 'Beauty & Health',
    320: 'Weddings & Events',
    322: 'Shoes',
    502: 'Electronic Components & Supplies',
    509: 'Phones & Telecommunications',
    1420: 'Tools',
    1501: 'Mother & Kids',
    1503: 'Furniture',
    1511: 'Watches',
    1524: 'Luggage & Bags',
    127698009: 'Test category 06',
    200000297: 'Apparel Accessories',
    200000343: "Men's Clothing",
    200000345: "Women's Clothing",
    200000532: 'Novelty & Special Use',
    200001075: 'Special Category',
    200165144: 'Hair Extensions & Wigs',
    200574005: 'Underwear',
    201169612: 'Virtual Products',
    201355758: 'Motorcycle Equipments & Parts',
    201520802: 'Second-Hand',
    201768104: 'Sports Shoes,Clothing&Accessories'
}

# 需要的配置列表
OrderDateList = GenerateTimeStamp().generate_order_timestamp()
CountryList = list(CountryConfig.keys())
OrderStatusList = list(OrderStatusConfig.keys())
ConversionTypeList = list(ConversionTypeConfig.keys())
AeProductIdList = ["1005005493079964", "1005005517790286", "1005005561054760", "1005005566313024", "1005005617964997",
                   "1005005626310545", "1005005906108510", "1005005941095596", "1005005957962592", "1005005959924051",
                   "1005005981682566", "1005006001026794", "1005006002768816", "1005006034207939", "1005006261794062",
                   "1005006332268799", "1005006396266701", "1005006440760707", "1005006483682747", "1005006539067453",
                   "3256806797723614", "4000518194943"]
AmazonProductIdList = ["0005164885", "059035342X", "B0CP9GGRJM", "B0CMCGYFLB", "B09YC9YD9R", "B0CDPQWLQ4", "B07NCZVZTC",
                       "B0C4FWRDKG", "B0D4TBTYNZ", "B0BBGDWVPX", "B0C65KZ17N", "B0B9BVSTHD", "B0B5DP3L53", "B0CFQ8V6SZ",
                       "B0C24Z287Y", "B0053YLTBC", "B095HYR2GK", "B08V1PR7NS", "B0787GLQ5G", "B07RHTW6GL", "B09LHZRH6F",
                       "B0C54CSBFB", "B09J1H79YM", "B0CDM4663P"]
AmazonProductCategoryList = list(AmazonProductCategoryConfig.keys())
AeProductCategoryList = list(AeProductCategoryConfig.keys())

if __name__ == '__main__':
    ts = GenerateTimeStamp()
    print(ts.generate_plan_day_hour_ts(2))
