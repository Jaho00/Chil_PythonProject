import requests
from pymongo import MongoClient
from bs4 import BeautifulSoup
import re


class taidiDetail:
    def __init__(self):
        self.jobListApi_url = "https://www.5iai.com/api/enterprise/job/public/es"
        self.jobDetailApi_url = (
            "https://www.5iai.com/api/enterprise/job/public"  # 详情页数据接口
        )

        uri = "mongodb+srv://Chil:0705@childb.zq9crau.mongodb.net/?retryWrites=true&w=majority&appName=ChilDB"
        # self.client = MongoClient(uri)

    # end def
    def getDetailID(self):
        detailIdList = []
        detailList = []
        obj = {"detailIdList": [], "detailList": []}
        for j in range(0, 18):
            data = {"pageSize": 10, "pageNum": j}
            r = requests.get(self.jobListApi_url, params=data).json()
            content = r.get("data").get("content")

            for i in range(len(content)):
                detailId = content[i].get("id")  # 页面详情id
                detailIdList.append(detailId)
                detailList.append(content[i])
        obj["detailList"] = detailList
        obj["detailIdList"] = detailIdList
        return obj

    # end def
    def getDetailInfo(self, obj):
        content = obj["detailList"]
        detailIdList = obj["detailIdList"]
        detailInfo = []
        for i in range(len(detailIdList)):
            detailId = detailIdList[i]  # 页面详情id
            detailData = {"id": detailId}
            detailR = requests.get(self.jobDetailApi_url, params=detailData).json()
            detailData = detailR.get("data")

            obj = {}
            obj["_id"] = detailIdList[i]  # 详情id
            obj["公司名称"] = detailData.get("enterpriseName")  # 公司名称
            obj["招聘人数"] = detailData.get("count")  # 招聘人数

            jRhtml = BeautifulSoup(detailData.get("jobRequiredments"), "html.parser")
            jRhtmlList = jRhtml.find_all(name="p")  # 获取每一个p标签
            jobRequiredments = ""
            # 循环用get_text（）获取标签中的文字
            for n in range(len(jRhtmlList)):
                if n == 0:
                    jobRequiredments = jRhtmlList[n].get_text()
                else:
                    jobRequiredments = jobRequiredments + jRhtmlList[n].get_text()
            obj["职位描述"] = jobRequiredments  # 职位描述

            # obj["职位福利"] =
            welfareStrlist = detailData.get("welfare").split(" ")  # 职位福利(待优化)
            print(f"==>> welfareStrlist: {welfareStrlist}")
            for m in welfareStrlist:
                print(f"==>> : {re.findall(r'[\u4e00-\u9fa5]', m)}")

            obj["发布时间"] = detailData.get("publishTime")  # 发布时间
            obj["截止时间"] = detailData.get("deadline")  # 截止时间
            skillsList = detailData.get("skillsList")  # 技能要求
            for j in range(len(skillsList)):
                if j == 0:
                    obj["技能要求"] = str(skillsList[j].get("labelName"))
                else:
                    obj["技能要求"] = (
                        obj["技能要求"] + "、" + str(skillsList[j].get("labelName"))
                    )

            educationalRequirements = content[i].get(
                "educationalRequirements"
            )  # 学历要求码
            # 2 大专 1 技工 3 本科
            match (educationalRequirements):  # 学历要求
                case 0:
                    obj["学历要求"] = "不限"
                case 1:
                    obj["学历要求"] = "技工"
                case 2:
                    obj["学历要求"] = "大专"
                case 3:
                    obj["学历要求"] = "本科"
                case 4:
                    obj["学历要求"] = "硕士"
                case 5:
                    obj["学历要求"] = "博士"
            # end match
            obj["最高薪资"] = content[i].get("maximumWage")  # 最高薪资
            obj["最低薪资"] = content[i].get("minimumWage")  # 最低薪资
            obj["经验要求"] = content[i].get("exp")  # 经验要求
            obj["岗位名称"] = content[i].get("positionName")  # 岗位名称
            obj["单位性质"] = (
                content[i].get("enterpriseExtInfo").get("econKind")
            )  # 单位性质
            obj["所属行业"] = (
                content[i].get("enterpriseExtInfo").get("industry")
            )  # 所属行业（待优化）
            obj["公司人数"] = (
                content[i].get("enterpriseExtInfo").get("personScope")
            )  # 公司人数
            # print(obj)

            detailInfo.append(obj)
        return detailInfo

    # end def
    def save(self, detailInfo):
        database = self.client.taidiInfo  # 数据库名称
        coll = database.detailInfo
        print(coll)
        # coll.insert_many(detailInfo)
        # print(f"==>> detailInfo: {detailInfo}")
        # print("保存成功")
        # results = database.find({})
        # for result in results:
        #     print(result)

        # end def

    def run(self):
        obj = self.getDetailID()
        detailInfo = self.getDetailInfo(obj)
        # print(detailInfo)
        # self.save(detailInfo)
        # end def


taidi = taidiDetail()
taidi.run()
