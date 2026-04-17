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
            { "name": "Congress.gov (美国国会)", "url": "https://www.congress.gov/", "type": "立法法规", "desc": "美国国会官方网站，提供全面的联邦立法数据、法案追踪、国会记录和法律文本。" },
            { "name": "Supreme Court (美国最高法院)", "url": "https://www.supremecourt.gov/", "type": "司法判例", "desc": "最高法院官方网站，发布最新的法庭意见、口头辩论音频/转录、案件案卷及法院规则。" },
            { "name": "PACER (联邦法院电子记录)", "url": "https://pacer.uscourts.gov/", "type": "诉讼档案", "desc": "美国联邦法院官方电子记录系统，可查询联邦上诉法院、地区法院和破产法院的详细案件卷宗。" },
            { "name": "eCFR (联邦法规电子版)", "url": "https://www.ecfr.gov/", "type": "行政法规", "desc": "提供每日更新的美国联邦行政法规（Code of Federal Regulations）官方数字化版本。" },
            { "name": "GovInfo (美国政府信息网)", "url": "https://www.govinfo.gov/", "type": "综合政府文件", "desc": "由美国政府出版局运营，提供联邦政府立法、行政、司法三大分支的官方出版物和法律文件。" },
            { "name": "LII (康奈尔法律信息研究所)", "url": "https://www.law.cornell.edu/", "type": "综合法律数据", "desc": "康奈尔大学法学院创办的非营利网站，免费提供结构化检索的《美国法典》、联邦法规及最高法院判例。" },
            { "name": "Oyez Project", "url": "https://www.oyez.org/", "type": "多媒体档案", "desc": "专注于美国最高法院的非营利多媒体档案库，提供详尽的案件摘要、判决结果和口头辩论音频。" },
            { "name": "CourtListener", "url": "https://www.courtlistener.com/", "type": "司法判例", "desc": "由 Free Law Project 运营，提供数百万份联邦和州法院判例，并整合了大量免费公开的 PACER 案件档案。" },
            { "name": "Caselaw Access Project", "url": "https://case.law/", "type": "历史司法判例", "desc": "哈佛大学法学院图书馆主导，将美国历史上几乎所有公开发表的州和联邦法院判例进行了全面数字化并免费开放。" },
            { "name": "Justia", "url": "https://www.justia.com/", "type": "综合法律数据", "desc": "全球最大的免费法律信息平台之一，提供海量美国判例法、法典、法规全文及免费的法律文章检索。" },
            { "name": "Supreme Court Database", "url": "http://scdb.wustl.edu/", "type": "司法数据分析", "desc": "由华盛顿大学法学院维护，提供最高法院自 1791 年以来所有案件的数百项详尽编码统计数据，是实证法律研究的权威资源。" }
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
            { "name": "legislation.gov.uk", "url": "https://www.legislation.gov.uk/", "type": "立法法规", "desc": "英国国家档案馆管理的官方网站，提供英国所有成文法（包含初级和次级立法）的原始版本和修订版本。" },
            { "name": "BAILII", "url": "https://www.bailii.org/", "type": "司法判例", "desc": "英国及爱尔兰法律信息研究所运营的免费权威数据库，提供各级法院判例法和部分条约数据。" },
            { "name": "The Gazette", "url": "https://www.thegazette.co.uk/", "type": "政府公告", "desc": "英国官方公共记录发布平台，每日发布政府通告、法定声明及破产公告。" },
            { "name": "Westlaw UK", "url": "https://legal.thomsonreuters.com/en/products/westlaw-uk", "type": "综合数据", "desc": "全球知名的商业法律平台，提供深度解析的英国判例、法规、法律评论和实务指南。" }
        ]
    elif code == 'DE':
        status = "已完成"
        resources = [
            { "name": "Gesetze im Internet", "url": "https://www.gesetze-im-internet.de/", "type": "立法法规", "desc": "德国联邦司法部运营的官方数据库，提供德国现行联邦法律和行政法规全文。" },
            { "name": "Bundesgesetzblatt", "url": "https://www.recht.bund.de/", "type": "政府公告", "desc": "德国官方电子发布门户，负责发布新颁布的联邦法律和政令的法定生效公告。" },
            { "name": "Rechtsprechung im Internet", "url": "https://www.rechtsprechung-im-internet.de/", "type": "司法判例", "desc": "联邦法院系统的官方判决数据库，涵盖最高法院、宪法法院及专业最高法院的高级别判例。" },
            { "name": "beck-online", "url": "https://beck-online.beck.de/", "type": "综合数据", "desc": "德国本土最权威的商业法律数据库，涵盖全面的法规、判例库以及核心法学评注和期刊文献。" }
        ]
    elif code == 'FR':
        status = "已完成"
        resources = [
            { "name": "Légifrance", "url": "https://www.legifrance.gouv.fr/", "type": "综合数据", "desc": "法国政府官方公共法律门户，提供法国宪法、法典、法规、法院判例以及官方公报的全面检索。" },
            { "name": "Cour de cassation", "url": "https://www.courdecassation.fr/", "type": "司法判例", "desc": "法国最高司法法院官网，提供民事和刑事案件的最高级别判例与司法解释。" },
            { "name": "Conseil constitutionnel", "url": "https://www.conseil-constitutionnel.fr/", "type": "司法判例", "desc": "法国宪法委员会官方网站，发布关于法律合宪性审查的裁决与决定文件。" },
            { "name": "Dalloz", "url": "https://www.dalloz.fr/", "type": "综合数据", "desc": "法国极具权威的老牌商业法律数据库，提供海量法国判例法、法律评注及实务分析。" }
        ]
    elif code == 'KP':
        status = "已完成"
        resources = [
            { "name": "Naenara (我的国家)", "url": "http://www.naenara.com.kp/", "type": "官方门户", "desc": "朝鲜官方对外的综合国家门户网站，其法律栏目提供朝鲜宪法及部分重要法律的官方外语译本。" },
            { "name": "北韩资料中心", "url": "https://nkinfo.unikorea.go.kr/", "type": "综合数据", "desc": "韩国统一部运营的朝鲜信息数据库，是外部获取和研究朝鲜法律法规、政策文件及官方出版物的权威渠道。" },
            { "name": "世界法制信息中心", "url": "https://world.moleg.go.kr/", "type": "立法法规", "desc": "韩国政府法制处运营的外部平台，收集并翻译了大量朝鲜法律条文，供学术与实务研究参考。" }
        ]
    elif code == 'RU':
        status = "已完成"
        resources = [
            { "name": "Pravo.gov.ru", "url": "http://pravo.gov.ru/", "type": "立法法规", "desc": "俄罗斯联邦官方的法律信息门户，发布所有联邦宪法、法律、总统令和政府决议的正式版本。" },
            { "name": "Верховный Суд РФ", "url": "https://vsrf.ru/", "type": "司法判例", "desc": "俄罗斯联邦最高法院官网，提供俄罗斯最高司法机关的案件判决、司法实践总结及全会决议。" },
            { "name": "КонсультантПлюс (ConsultantPlus)", "url": "https://www.consultant.ru/", "type": "综合数据", "desc": "俄罗斯国内使用最广泛的商业法律参考系统，提供海量的联邦和地方法规、判例及法学评论。" },
            { "name": "ГАРАНТ (Garant)", "url": "https://www.garant.ru/", "type": "综合数据", "desc": "俄罗斯另一大主流专业法律信息系统，提供详尽的法律文本、司法实践数据库及在线法律咨询资源。" }
        ]
    elif code == 'KR':
        status = "已完成"
        resources = [
            { "name": "国家法令信息中心 (National Law Information Center)", "url": "https://www.law.go.kr/", "type": "立法法规", "desc": "韩国最权威、最全面的国家级法律数据库。提供所有现行法律法规、行政规则、自治法规以及大法院、宪法法院的权威判例和法制处解释，支持多语种检索。" },
            { "name": "大法院综合法律信息系统", "url": "https://glaw.scourt.go.kr/", "type": "司法判例", "desc": "韩国大法院（最高法院）运营的官方系统。主要提供大法院及各级下属法院的详细司法判例、法院内部规章、司法行政公告及法律文献库。" },
            { "name": "韩国法务部 (Ministry of Justice)", "url": "https://www.moj.go.kr/", "type": "政府公告", "desc": "韩国法务部官方网站。发布关于司法行政、出入境与移民政策、人权保护的最新动态、政府法务公告及相关法律修改草案。" },
            { "name": "韩国宪法法院 (Constitutional Court of Korea)", "url": "https://www.ccourt.go.kr/", "type": "司法判例", "desc": "提供涉及违宪审查、弹劾、政党解散及国家机关权限争议等宪法级诉讼的权威判决书、决定文和相关宪法公告。" },
            { "name": "韩国法制处 (Ministry of Government Legislation)", "url": "https://www.moleg.go.kr/", "type": "立法法规", "desc": "负责统筹韩国政府立法的核心机构。网站提供政府年度立法计划、权威的法定解释、立法动向及各类法制行政公告。" },
            { "name": "韩国国会议案信息系统", "url": "http://likms.assembly.go.kr/bill/", "type": "立法追踪", "desc": "追踪正在审议或已通过的国会议案（法案）的权威平台。可查询法案的提出者、审改进度、会议记录及立法预告。" },
            { "name": "LBox (엘박스)", "url": "https://lbox.kr/", "type": "综合法律检索", "desc": "韩国发展最快的法律科技初创公司之一。拥有韩国最大规模的下级法院判例数据库，利用AI技术提供高度精确的判例检索、相似判例推荐服务。" },
            { "name": "CaseNote (케이스노트)", "url": "https://casenote.kr/", "type": "司法判例", "desc": "韩国极受欢迎的免费判例搜索引擎。界面简洁易用，提供包括大法院和下级法院的判例、相关学术论文以及法律条文的交叉检索。" },
            { "name": "Lawnb (로앤비)", "url": "https://www.lawnb.com/", "type": "综合商业数据库", "desc": "韩国历史最悠久、最专业的综合法律商业数据库之一。提供极度细致的法律、判例、法学文献、企业法务指南及法律实务工具（部分深度内容需付费订阅）。" }
        ]
    elif code == 'JP':
        status = "已完成"
        resources = [
            { "name": "e-Gov法令検索", "url": "https://elaws.e-gov.go.jp/", "type": "立法法规", "desc": "日本政府官方电子法律法规检索系统，提供现行宪法、法律、政令及省令等权威条文全文。" },
            { "name": "法务省 (Ministry of Justice)", "url": "https://www.moj.go.jp/", "type": "政府公告", "desc": "日本法务省官方网站，发布最新法律修订动向、司法行政政策、政府公告及相关法律草案。" },
            { "name": "互联网官报 (Kanpou)", "url": "https://kanpou.npb.go.jp/", "type": "政府公告", "desc": "国立印刷局发行的官方公报，每日发布新制定的法律、政令、条约、国家机关公告及破产公告。" },
            { "name": "日本法令外文翻译数据库", "url": "https://www.japaneselawtranslation.go.jp/", "type": "官方翻译", "desc": "由法务省运营，提供日本主要法律法规的权威英文翻译及双语对照库，是涉外法律研究的核心工具。" },
            { "name": "日本法令索引", "url": "https://hourei.ndl.go.jp/", "type": "立法索引", "desc": "由国立国会图书馆维护，提供自明治时期以来的法令索引、法案审议过程及废止与修改的历史轨迹。" },
            { "name": "最高裁判所 (Courts in Japan)", "url": "https://www.courts.go.jp/", "type": "司法判例", "desc": "日本最高裁判所官方网站，内置检索系统提供最高裁判所、高等裁判所及下级法院的重要判例与裁判文书。" },
            { "name": "Westlaw Japan", "url": "https://www.westlawjapan.com/", "type": "综合数据", "desc": "知名商业法律数据库，由汤森路透合资运营，提供海量判例、法令、法学文献及实务操作指南。" },
            { "name": "TKC Law Library", "url": "https://www.tkc.jp/law/", "type": "综合数据", "desc": "日本最大级别的法律信息数据库之一，涵盖判例体系（LEX/DB）、法令及丰富的法学期刊，广受律所与法学院使用。" },
            { "name": "D1-Law.com", "url": "https://www.d1-law.com/", "type": "综合数据", "desc": "由老牌法律出版社“第一法规”运营，提供现行法规、判例体系、法学评注及文献的全面检索服务。" }
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
