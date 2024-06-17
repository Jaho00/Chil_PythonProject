import requests
import json


data = {"pageSize": 1765}
url = "https://www.5iai.com/api/enterprise/job/public/es"
r = requests.get(url, params=data).json()
content = r.get("data").get("content")
# result = json.loads(r.text)
# print(r.text)
for i in range(len(content)):
    detailId = content[i].get("id")  # 页面详情id
    detailUrl = "https://www.5iai.com/api/enterprise/job/public"  # 详情页数据接口
    detailData = {"id": detailId}
    detailR = requests.get(detailUrl, params=detailData).json()

    company = detailR.get("data").get("enterpriseName")  # 公司名称
    companyNum = detailR.get("data").get("count")  # 招聘人数
    jobRequiredments = detailR.get("data").get("jobRequiredments")  # 职位描述（待优化）
    welfare = detailR.get("data").get("welfare")  # 职位福利(待优化)
    publishTime = detailR.get("data").get("publishTime")  # 发布时间
    deadline = detailR.get("data").get("deadline")  # 截止时间
    skillsList = detailR.get("data").get("skillsList")  # 技能要求
    for j in range(len(skillsList)):
        if j == 0:
            labelName = str(skillsList[j].get("labelName"))
        else:
            labelName = labelName + "、" + str(skillsList[j].get("labelName"))

    educationalRequirements = content[i].get("educationalRequirements")  # 学历要求码
    # 2 大专 1 技工 3 本科
    match (educationalRequirements):  # 学历
        case 1:
            educationName = "技工"
        case 2:
            educationName = "大专"
        case 3:
            educationName = "本科"
    # end match
    maximumWage = content[i].get("maximumWage")  # 最高薪资
    minimumWage = content[i].get("minimumWage")  # 最低薪资
    expRequirements = content[i].get("exp")  # 经验要求
    positionName = content[i].get("positionName")  # 岗位名称
    companyType = content[i].get("enterpriseExtInfo").get("econKind")  # 单位性质
    industry = content[i].get("enterpriseExtInfo").get("industry")  # 所属行业（待优化）
    personScope = content[i].get("enterpriseExtInfo").get("personScope")  # 公司人数
    print(labelName)
