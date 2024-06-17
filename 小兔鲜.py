import requests
import json
from pymongo import MongoClient

class LittleRabbit:
    def __init__(self):
        # 准备车载用品类页面的 URL
        self.init_url = 'https://apipc-xiaotuxian-front.itheima.net/category/goods/temporary'
        # 请求头
        self.headers = {
            "Content-Type": "application/json",
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64)'
                          'AppleWebKit/537.36 (KHTML, like Gecko)'
                          'Chrome/90.0.4430.212 Safari/537.36'}
        # 连接 MongoDB 的客户端
        self.client = MongoClient('127.0.0.1', 27017)

    def load_category_page(self, page):
        """
        抓取车载用品类商品展示页面的数据
        :param page:待抓取的页码数
        :return:车载用品类下的所有商品
        """
        # 准备请求体，提交的表单
        payload = {"page": page, "pageSize": 20, "categoryId": "1005009"}
        # 将字典 request_payload 转换为 JSON 字符串
        json_data = json.dumps(payload)
        response = requests.post(url=self.init_url, data=json_data,headers=self.headers)
        # 将服务器返回的 JSON 字符串先转换成字典，再获取字典中的商品信息
        all_goods = json.loads(response.text)["result"]["items"]
        return all_goods

    def load_detail_page(self, all_goods):
        """
        抓取商品详情页的数据
        :param all_goods: 车载用品类下的所有商品
        :return: 所有商品的详情信息
        """
        # 准备基本 URL
        base_url = 'https://apipc-xiaotuxian-front.itheima.net/goods?'
        # 定义一个列表，保存抓取并解析后，所有商品的详情信息
        goods_detail_info = []
        for good in all_goods:
            # 提取商品的 ID 标识
            param = {}
            param['id'] = good['id']
            # 根据拼接商品详情页的完整 URL，发送 GET 请求
            response = requests.get(url=base_url, params=param)
            # 将服务器返回的 JSON 数据转换为字典
            good_detail = json.loads(response.text)
            temp_url = 'http://erabbit.itheima.net/#/product/'
            data={}
            data['商品名称']=good_detail['result']['name']
            data['商品描述'] = good_detail['result']['desc']
            data['商品价格'] = good_detail['result']['price']
            data['商品图片']=good_detail['result']['mainPictures'][0]
            data['商品链接'] = temp_url+good['id']
            lst=good_detail['result']['details']['properties']
            data['商品详情']=''.join([':'.join(info.values())+"\n" for info in lst])
            goods_detail_info.append(data)
            print(data)
            return goods_detail_info

    def save_data(self,goods_detail_info):
        db=self.client.little_rabbit
        coll=db.rabbit
        coll.insert_many(goods_detail_info)
        print("保存成功")
        result=coll.find()
        for doc in result:
            print(doc)


    def run(self):
        begin_page=int(input("起始页码:"))
        end_page=int(input("结束页码:"))
        if begin_page <=0:
            print("起始页码从1开始")
        else:
            for x in range (begin_page,end_page+1):
                print(f"正在抓取第{x}页")
                all_goods=self.load_category_page(x)
                goods_detail=self.load_detail_page(all_goods)
                self.save_data(goods_detail)
little=LittleRabbit()
little.run()
# all_goods=little.load_category_page(1)
# little.load_detail_page(all_goods)
