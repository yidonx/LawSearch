import urllib.request
import json
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = "https://restcountries.com/v3.1/all?fields=name,region,subregion,translations,flag,cca2,unMember"
req = urllib.request.Request(url)
with urllib.request.urlopen(req, context=ctx) as response:
    data = json.loads(response.read().decode())

# 综合实力/热度排名 (GDP Top 20)
gdp_ranks = {
    'US': 1, 'CN': 2, 'DE': 3, 'JP': 4, 'IN': 5, 'GB': 6, 'FR': 7, 'IT': 8, 'BR': 9, 'CA': 10,
    'RU': 11, 'MX': 12, 'AU': 13, 'KR': 14, 'ES': 15, 'ID': 16, 'NL': 17, 'TR': 18, 'SA': 19, 'CH': 20,
}

# 地区/次区域翻译映射
regions_zh = {
    "Asia": "亚洲", "Europe": "欧洲", "Africa": "非洲", 
    "Americas": "美洲", "Oceania": "大洋洲"
}

subregions_zh = {
    "Eastern Asia": "东亚", "South-Eastern Asia": "东南亚", "Southern Asia": "南亚", "Central Asia": "中亚", "Western Asia": "西亚",
    "Eastern Europe": "东欧", "Northern Europe": "北欧", "Southern Europe": "南欧", "Western Europe": "西欧", "Central Europe": "中欧",
    "Eastern Africa": "东非", "Middle Africa": "中非", "Northern Africa": "北非", "Southern Africa": "南部非洲", "Western Africa": "西非",
    "Northern America": "北美洲", "North America": "北美洲", "Caribbean": "加勒比地区", "Central America": "中美洲", "South America": "南美洲",
    "Australia and New Zealand": "澳新地区", "Melanesia": "美拉尼西亚", "Micronesia": "密克罗尼西亚", "Polynesia": "波利尼西亚"
}

countries = []

for c in data:
    code = c.get("cca2", "")
    is_un = c.get("unMember", False)
    
    # 过滤：只保留联合国成员国 + 特殊地区（港澳台、巴勒斯坦、梵蒂冈）
    if not is_un and code not in ['HK', 'MO', 'TW', 'PS', 'VA']:
        continue
        
    region_en = c.get("region", "")
    subregion_en = c.get("subregion", "")
            
    if region_en not in regions_zh:
        continue
        
    region_zh = regions_zh[region_en]
    
    # 强制将欧洲东南欧归入东欧（确保只有北、西、中、南、东）
    if region_en == "Europe" and subregion_en == "Southeast Europe":
        subregion_en = "Eastern Europe"
        
    subregion_zh = subregions_zh.get(subregion_en, subregion_en if subregion_en else "其他")
    
    # 确保 North America 改为中文名
    if "North America" in subregion_en or "Northern America" in subregion_en:
        subregion_zh = "北美洲"
    
    name_zh = c.get("translations", {}).get("zho", {}).get("common", c.get("name", {}).get("common"))
    
    # 特殊处理港澳台及个别未提供中文翻译的国家
    if code == 'HK':
        name_zh = "中国香港"
    elif code == 'MO':
        name_zh = "中国澳门"
    elif code == 'TW':
        name_zh = "中国台湾"
    elif code == 'SG':
        name_zh = "新加坡"
        
    name_en = c.get("name", {}).get("common")
    flag = c.get("flag", "")
    
    rank = gdp_ranks.get(code, 100)
    status = "进行中"
    
    resources = [
        { "name": "资源名称（待补充）", "url": "", "type": "类型（待补充）", "desc": "描述（待补充）" }
    ]
    
    if code == 'US':
        status = "已完成"
        resources = [
            { "name": "Supreme Court Database", "url": "http://scdb.wustl.edu/", "type": "司法判例", "desc": "美国最高法院的全面案例数据与统计信息。" },
            { "name": "Congress.gov", "url": "https://www.congress.gov/", "type": "立法法规", "desc": "美国国会官方网站，提供联邦立法数据。" },
            { "name": "PACER", "url": "https://pacer.uscourts.gov/", "type": "诉讼档案", "desc": "美国联邦法院电子记录公共访问系统。" }
        ]
    elif code == 'CN':
        status = "已完成"
        resources = [
            { "name": "中国裁判文书网", "url": "https://wenshu.court.gov.cn/", "type": "司法判例", "desc": "中国最高人民法院设立的全国法院裁判文书公开平台。" },
            { "name": "国家法律法规数据库", "url": "https://flk.npc.gov.cn/", "type": "立法法规", "desc": "全国人大常委会办公厅维护的权威法律法规数据。" },
            { "name": "北大法宝 (Pkulaw)", "url": "https://www.pkulaw.com/", "type": "综合数据", "desc": "中国广泛使用的综合性法律数据库。" }
        ]
    elif code == 'GB':
        status = "已完成"
        resources = [
            { "name": "legislation.gov.uk", "url": "https://www.legislation.gov.uk/", "type": "立法法规", "desc": "英国国家档案馆维护的完整立法数据库。" },
            { "name": "BAILII", "url": "https://www.bailii.org/", "type": "司法判例", "desc": "英国及爱尔兰法律信息研究所。" }
        ]
    elif code == 'JP':
        status = "已完成"
        resources = [
            { "name": "e-Gov法令検索", "url": "https://elaws.e-gov.go.jp/", "type": "立法法规", "desc": "日本政府官方电子法律法规检索系统。" },
            { "name": "裁判所 Courts in Japan", "url": "https://www.courts.go.jp/", "type": "司法判例", "desc": "日本最高裁判所判例搜索系统。" }
        ]
        
    countries.append({
        "id": code,
        "name": f"{name_zh} ({name_en})",
        "flag": flag,
        "regionId": region_en.lower().replace(" ", "-"),
        "regionName": region_zh,
        "subregionId": subregion_en.lower().replace(" ", "-") if subregion_en else "other",
        "subregionName": subregion_zh,
        "status": status,
        "rank": rank,
        "resources": resources
    })

# 增加跨国组织 (作为一级目录)
orgs = [
    {
        "id": "UN",
        "name": "联合国 (United Nations)",
        "flag": "🇺🇳",
        "regionId": "organizations",
        "regionName": "跨国组织",
        "subregionId": "global",
        "subregionName": "全球性组织",
        "status": "已完成",
        "rank": 0,
        "resources": [
            { "name": "联合国宪章 (UN Charter)", "url": "https://www.un.org/zh/about-us/un-charter", "type": "基础性文件", "desc": "联合国的建立条约和核心文件。" },
            { "name": "UN Treaty Collection", "url": "https://treaties.un.org/", "type": "条约数据", "desc": "联合国条约汇编，包含国际条约及多边协定。" },
            { "name": "International Court of Justice", "url": "https://www.icj-cij.org/", "type": "司法判例", "desc": "联合国国际法院案件与判决数据。" }
        ]
    },
    {
        "id": "EU",
        "name": "欧盟 (European Union)",
        "flag": "🇪🇺",
        "regionId": "organizations",
        "regionName": "跨国组织",
        "subregionId": "regional",
        "subregionName": "区域性组织",
        "status": "已完成",
        "rank": 0,
        "resources": [
            { "name": "EUR-Lex", "url": "https://eur-lex.europa.eu/", "type": "综合数据", "desc": "免费获取欧盟法律文件的官方门户。" },
            { "name": "CURIA", "url": "https://curia.europa.eu/", "type": "司法判例", "desc": "欧洲联盟法院的判例法与文件。" }
        ]
    },
    {
        "id": "WTO",
        "name": "世界贸易组织 (WTO)",
        "flag": "🌐",
        "regionId": "organizations",
        "regionName": "跨国组织",
        "subregionId": "global",
        "subregionName": "全球性组织",
        "status": "已完成",
        "rank": 0,
        "resources": [
            { "name": "WTO Documents Online", "url": "https://docs.wto.org/", "type": "法律文件", "desc": "世贸组织官方文件及法律文本。" },
            { "name": "Dispute Settlement", "url": "https://www.wto.org/english/tratop_e/dispu_e/dispu_e.htm", "type": "争端解决", "desc": "世贸组织争端解决机制判例与报告。" }
        ]
    }
]
countries.extend(orgs)

# 按热度(rank)和名称排序
countries.sort(key=lambda x: (x["rank"], x["name"]))

with open("data.json", "w", encoding="utf-8") as f:
    json.dump(countries, f, ensure_ascii=False, indent=4)
print("Data rebuilt successfully.")
