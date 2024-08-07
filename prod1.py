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

            obj["岗位名称"] = content[i].get("positionName")  # 岗位名称

            educationalRequirements = content[i].get(
                "educationalRequirements"
            )  # 学历要求码
            if educationalRequirements == 0:  # 学历要求
                obj["学历要求"] = "不限"
            elif educationalRequirements == 1:
                obj["学历要求"] = "技工"
            elif educationalRequirements == 2:
                obj["学历要求"] = "大专"
            elif educationalRequirements == 3:
                obj["学历要求"] = "本科"
            elif educationalRequirements == 4:
                obj["学历要求"] = "硕士"
            elif educationalRequirements == 5:
                obj["学历要求"] = "博士"

            obj["经验要求"] = content[i].get("exp")  # 经验要求

            skillsList = detailData.get("skillsList")  # 技能要求
            for j in range(len(skillsList)):
                if j == 0:
                    obj["技能要求"] = str(skillsList[j].get("labelName"))
                else:
                    obj["技能要求"] = (
                        obj["技能要求"] + "、" + str(skillsList[j].get("labelName"))
                    )

            obj["招聘人数"] = detailData.get("count")  # 招聘人数

            obj["薪资范围"] = (
                str(content[i].get("minimumWage"))
                + " ~ "
                + str(content[i].get("maximumWage"))
            )  # 薪资范围 = 最低薪资 + 最高薪资

            welfareStrlist = detailData.get("welfare").split(",")
            obj["职位福利"] = self.dataProcessing(welfareStrlist, ",")  # 职位福利

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

            obj["公司名称"] = detailData.get("enterpriseName")  # 公司名称

            obj["公司人数"] = (
                content[i].get("enterpriseExtInfo").get("personScope")
            )  # 公司人数

            industryList = (
                content[i].get("enterpriseExtInfo").get("industry").split(",")
            )
            obj["所属行业"] = self.dataProcessing(industryList, "/")  # 所属行业

            obj["单位性质"] = (
                content[i].get("enterpriseExtInfo").get("econKind")
            )  # 单位性质

            obj["单位地址"] = detailData.get("enterpriseAddress").get(
                "detailedAddress"
            )  # 发布时间

            obj["发布时间"] = detailData.get("publishTime")  # 发布时间

            obj["截止时间"] = detailData.get("deadline")  # 截止时间

            obj["序号"] = i + 1

            detailInfo.append(obj)
        print(detailInfo)
        return detailInfo

    # end def

    # 封装数据处理
    def dataProcessing(self, dataList, separator):
        data = ""
        for m in dataList:
            list = re.findall(r"[\u4e00-\u9fa5]", m)
            str = "".join(list)
            str1 = ""
            if data != "" and separator == ",":
                str1 = ","
            elif data != "" and separator == "/":
                str1 = "/"
            data = data + str1 + str
        return data

    # end def

    def run(self):
        obj = self.getDetailID()
        self.getDetailInfo(obj)
        # end def


taidi = taidiDetail()
taidi.run()
