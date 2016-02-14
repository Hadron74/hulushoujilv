# -*-coding:utf-8-*-

""" 下载葫芦语录帖子网页
"""
__author__ = 'luhongc'

import urllib2


def get_url(num, url):
    """ Download url base function
    :param num: id number
    :param url: urlbase
    :return: return urlopen contents
    """
    import sys
    import time
    while True:
        try:
            time.sleep(0.25)
            f = urllib2.urlopen(url.format(num), timeout=10).read()
            return f
        except urllib2.URLError, e:
            sys.stderr.write(str(e) + "\n")


url_1 = "http://guba.eastmoney.com/news,002030,168639100,d_{}.html"


def get_page1(num):
    """
    Download a page with given page number
    :param num: page number
    :return: huifuid_list, empty(to be used in future)
    """
    f = get_url(num, url_1)
    import re
    p = re.compile('data-huifuid="(\d+)"', re.MULTILINE)
    pr = re.compile('<a href="javascript:;" target="_self" data-replyid="(\d+)" data-rootid="(\d+)"', re.MULTILINE)
    ids = [i for i in p.findall(f)]
    # links = [i for i in pr.findall(f)]
    return ids, []


url_ajax = "http://iguba.eastmoney.com/interf/guba.aspx?action=Getreplyinfo&topicid=168639100&huifuid={}"


def get_yasuo(huifuid):
    """
    Download yasuo jason for a reply
    :param huifuid:
    :return:
    """
    import json
    response = get_url(huifuid, url_ajax)
    return json.dumps(response)


url_link = "http://iguba.eastmoney.com/interf/guba.aspx?action=gettalk&replyids={}"


def get_link(replyid):
    """
    Download link of replyid to rootid, give the relationship of replys,
    :param replyid:
    :return:
    """
    import json
    response = get_url(replyid, url_link)
    return json.dumps(response)


def main_download():
    """
    Download the whole dataset, save to disk as JSON.
    :return:
    """
    with open("reply.json", "w") as OUT, open("links.json", "w") as LOUT:
        for i in range(1, 600):
            import sys
            sys.stderr.write(str(i) + "\n")
            ids, links = get_page1(str(i))
            for id in ids:
                line = get_yasuo(id)
                line2 = get_link(id)
                OUT.write(line + "\n")
                LOUT.write(line2 + "\n")


def download_new(pages=50):
    """
    Download newest 50 pages to update the data base.
    :param pages:
    :return:
    """
    from mysql_database import connect, insert_link, insert_reply
    conn = connect()
    stop = False
    import json
    for i in range(1, pages):
        ids, links = get_page1(str(i))
        if stop: break
        import sys
        sys.stderr.write(str(i) + "\n")
        ids, links = get_page1(str(i))
        for id in ids:
            reply = get_yasuo(id)
            link = get_link(id)
            id, sql, data = parseReply2sql(json.loads(reply))
            rst = insert_reply(conn, id, sql)
            id, sql, data = parseLink2sql(json.loads(link))
            if id is not None:
                insert_link(conn, id, sql)
    conn.close()


def parseLink2sql(link):
    """
    :param link:
    :return:
    """
    link = eval(link)
    rst = link["result"]
    if len(rst) == 0:
        return None, None, None
    assert len(rst) == 1
    linkids = rst[0]
    replyID = linkids["replyID"]
    rootID = linkids["rootID"]

    data = (replyID, rootID)
    sqlbase = "insert into LINKS (REPLYID,ROOTID) values ({},{});"
    return replyID, sqlbase.format(replyID, rootID), data


def parseReply2sql(reply):
    """
    :param reply:
    :return:
    """
    reply = eval(reply)
    res = reply['re']

    assert len(res) == 1
    res0 = res[0]

    ip = res0["ip"]  # '辽宁葫芦岛网友'

    tu = res0["tu"]
    assert tu == '9753094145455898'  # 葫芦uid

    tvu = res0["tvu"]
    assert tvu == '0'

    pic = res0["pic"]
    assert pic == ''

    cd = res0["cd"]
    assert cd == "002030"

    vu = res0["vu"]
    assert vu == '0'

    zw = res0[
        "zw"]  # 这个帖子只用来记录个人简要操盘笔记，不对别人构成建议，否则责任自负。请不要问我个股，因为我的交易系统不允许我预测指数和个股短期走势，而且我真的没有那个能力，我只按照纪律操作。欢迎朋友们来作客，交流探讨技术问题。骂人者、做广告者、素质低下者请绕行。

    id = res0["id"]  # reply id

    pr = res0["pr"]
    assert pr == 0

    yid = res0["yid"]
    assert yid == 0

    ty = res0["ty"]
    assert ty == 0

    tt = res0["tt"]  # 葫芦守纪律简要操盘笔记

    nc = res0["nc"]  # nicname

    tp = res0["tp"]  # "辽宁葫芦岛网友"

    tn = res0["tn"]  # "葫芦守纪律"

    tm = res0["tm"]
    assert tm == '2015-05-22 19:10:03'

    ti = res0["ti"]  # time of the reply

    td = res0["td"]
    assert td == 168639100

    te = res0["te"]  # reply text

    de = res0["de"]
    assert de == 0

    tde = res0["tde"]
    assert tde == 0

    ze = res0["ze"]  # []
    assert len(ze) == 0

    mc = res0["mc"]
    assert mc == "002030.sz"

    st = res0["st"]
    assert st == 0

    mu = res0["mu"]
    assert mu == "False"

    sn = res0["sn"]
    assert sn == "达安基因"

    ud = res0["ud"]  # replyer id
    if ud == "":
        ud = -1

    data = (id, ip, nc, ti, te, ud)
    seqbase = "insert into REPLY (id,ip,nc,ti,te,ud) values ({},'{}','{}','{}','{}',{});".format(id, ip, nc, ti, te, ud)
    return id, seqbase, data


def fileLink2sql():
    """
    :return:
    """
    import json
    from mysql_database import connect, insert_link
    conn = connect()
    with open("links.json") as LINKS, open("links.sql", "w") as SQL:
        for line in LINKS:
            id, sql = parseLink2sql(json.loads(line))
            if id:
                insert_link(conn, id, sql)
    conn.close()


def fileReply2sql():
    """
    :return:
    """
    import json
    from mysql_database import connect, insert_reply
    conn = connect()
    with open("reply.json") as REPLY, open("reply.sql", "w") as SQL:
        for line in REPLY:
            id, sql = parseReply2sql(json.loads(line))
            insert_reply(conn, id, sql)
    conn.close()


if __name__ == "__main__":
    pass
    # main_download()
    # fileLink2sql()
    # fileReply2sql()
    download_new()
