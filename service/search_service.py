import sqlite3

import jieba
from hanlp_restful import HanLPClient
import hanlp
import time
import math
from bottle import run
sts = hanlp.load(hanlp.pretrained.sts.STS_ELECTRA_BASE_ZH)

# 搜索服务实现
def search_fun(keyword, mask, p,related_flag=True):
    # 分页
    status = 0  # 首页状态

    if p == "":
        p = 1
    else:
        p = int(p)
        if p > 1:
            status = 1
    start = time.time()
    cut = list(jieba.cut(keyword))
    mask_cut = list(jieba.cut(mask))
    # 根据索引查询包含关键词的网页编号
    page_id_list = get_page_id_list_from_key_word_cut(cut)
    cut_page_id_list = get_page_id_list_from_key_word_cut(mask_cut)
    print(page_id_list)
    print(cut_page_id_list)
    # 关键词过滤
    for re in cut_page_id_list:
        print(page_id_list.count(re))
        if page_id_list.count(re) > 0:
            page_id_list.remove(re)
    # 根据网页编号 查询网页具体内容
    page_list = get_page_list_from_page_id_list(page_id_list)
    # 根据查询关键字和网页包含的关键字，进行相关度排序 余弦相似度
    page_list = sort_page_list(page_list, keyword)

    related_keyword = []
    # sts = hanlp.load(hanlp.pretrained.sts.STS_ELECTRA_BASE_ZH)
    if related_flag:
        # page_list 获取关键字
        related_keyword = get_related_word(page_list, keyword, cut)


    total_pages = int(math.ceil(len(page_list) / 10.0))
    dic = get_page(total_pages, p)

    end = time.time()
    print(p)

    context = {
        "status": status,
        "page_list": page_list[(p-1)*10: p*10],
        "keyword": keyword,
        "p":int(p),
        "dic_list": dic,
        "count": len(page_list),
        "total_pages":total_pages,
        "time": "{:.3f}".format(end-start),
        "related": related_keyword,
        "mask":mask
    }
    return context


def get_page(total, page):
    show_page = 5
    page_offset = 2
    start = 1
    end = total

    if total > show_page:
        if page > page_offset:
            start = page - page_offset
            if total > page + page_offset:
                end = page + page_offset
            else:
                end = total
        else:
            start = 1
            if total > show_page:
                end = show_page
            else:
                end = total
        if page + page_offset > total:
            start = start - (page + page_offset - end)

    dic = range(start, end + 1)
    return dic

def swap(a, b):
    return b, a
# 相关搜索
def get_related_word(page_list, text, cut, num=6):
    # HanLP = HanLPClient('https://hanlp.hankcs.com/api', auth=None, language='zh')
    cal = []
    cal_copy = []
    for page in page_list:
        print(page)
        words = page[1]
        for i in words.split(" "):
            if i not in cut and (i, text) not in cal:
                cal.append((i, text))

    # score = HanLP.semantic_textual_similarity(cal[:30])
    global sts
    score = sts(cal)
    for i, wi in enumerate(cal):
        cal_copy.append([score[i], wi[0]])
    for i in range(len(score)):
        for j in range(i, len(score)):
            if cal_copy[i][0] < cal_copy[j][0]:
                cal_copy[i], cal_copy[j] = swap(cal_copy[i], cal_copy[j])

    return cal_copy[:num]


# 计算page_list中每个page 和 cut的余弦相似度
def sort_page_list(page_list, cut):
    con_list = []
    for page in page_list:
        # print(page)
        url = page[1]
        words = page[2]
        title = page[3]
        vector = words.split(" ")
        same = 0
        for i in vector:
            if i in cut:
                same += 1
        cos = same / (len(vector) * len(cut))
        con_list.append([cos, url, words, title])
    con_list = sorted(con_list, key=lambda i: i[0], reverse=True)
    return con_list


# 根据网页id列表获取网页详细内容列表
def get_page_list_from_page_id_list(page_id_list):
    id_list = "("
    for k in page_id_list:
        id_list += "%s," % k
    id_list = id_list.strip(",") + ")"
    conn = sqlite3.connect("./data/database.db")
    c = conn.cursor()
    sql = "select * " \
          + "from page_info  " \
          + "where id in " + id_list + ";"
    res = c.execute(sql)
    res = [r for r in res]
    return res


# 根据关键词在索引中获取网页编号
def get_page_id_list_from_key_word_cut(cut):
    keyword = "("
    for k in cut:
        if k == " ":
            continue
        keyword += "'%s'," % k
    keyword = keyword.strip(",") + ")"
    conn = sqlite3.connect("./data/database.db")
    c = conn.cursor()
    sql = "select page_id " \
          + "from page_index  " \
          + "where keyword in " + keyword + ";"
    res = c.execute(sql)
    res = [r[0] for r in res]
    return res

