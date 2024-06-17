import requests
from pymongo import MongoClient


class taidiDetail:
    def __init__(self):
        self.jobList_url = "https://www.5iai.com/api/enterprise/job/public/es"
        self.jobDetail_url = (
            "https://www.5iai.com/api/enterprise/job/public"  # 详情页数据接口
        )
        myClient = MongoClient("mongodb://23.158.104.186/32:27017")

    # end def
    def getDetailID(self):
        detailIdList = []
        for j in range(0, 18):
            data = {"pageSize": 10, "pageNum": j}
            r = requests.get(self.jobList_url, params=data).json()
            content = r.get("data").get("content")
            for i in range(len(content)):
                detailId = content[i].get("id")  # 页面详情id
                detailIdList.append(detailId)
        return detailIdList

    # end def
    def getDetailInfo(self, detailIdList):
        detailInfo = []
        for i in range(len(detailIdList)):
            detailId = detailIdList[i]  # 页面详情id
            detailData = {"id": detailId}
            detailR = requests.get(self.jobDetail_url, params=detailData).json()
            detailData = detailR.get("data")

            obj = {}
            obj["公司名称"] = detailData.get("enterpriseName")  # 公司名称
            obj["招聘人数"] = detailData.get("count")  # 招聘人数
            obj["职位描述"] = detailData.get("jobRequiredments")  # 职位描述（待优化）
            obj["职位福利"] = detailData.get("welfare")  # 职位福利(待优化)
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

            educationalRequirements = self.content[i].get(
                "educationalRequirements"
            )  # 学历要求码
            # 2 大专 1 技工 3 本科
            match (educationalRequirements):  # 学历
                case 1:
                    obj["学历要求"] = "技工"
                case 2:
                    obj["学历要求"] = "大专"
                case 3:
                    obj["学历要求"] = "本科"
            # end match
            obj["最高薪资"] = self.content[i].get("maximumWage")  # 最高薪资
            obj["最低薪资"] = self.content[i].get("minimumWage")  # 最低薪资
            obj["经验要求"] = self.content[i].get("exp")  # 经验要求
            obj["岗位名称"] = self.content[i].get("positionName")  # 岗位名称
            obj["单位性质"] = (
                self.content[i].get("enterpriseExtInfo").get("econKind")
            )  # 单位性质
            obj["所属行业"] = (
                self.content[i].get("enterpriseExtInfo").get("industry")
            )  # 所属行业（待优化）
            obj["公司人数"] = (
                self.content[i].get("enterpriseExtInfo").get("personScope")
            )  # 公司人数
            # print(obj)
            detailInfo.append(obj)
        return detailInfo

    # end def
    def save(self, detailInfo):
        db = self.client.ChilDB
        coll = db.taidi
        coll.insert_test_Info(detailInfo)
        print("保存成功")
        result = coll.find()
        for doc in result:
            print(doc)
        # end def

    def run(self):
        detailIdList = self.getDetailID()
        detailInfo = self.getDetailInfo(detailIdList)
        self.save(detailInfo)
        # end def


taidi = taidiDetail()
taidi.run()
