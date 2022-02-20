import requests
import re
import json
import math

def get_request(txt):
    headers = {"User-Agent": "Penguinone's DiscordBot (twitter @penguinone2580)"}
    url = "https://spla2.yuu26.com/"
    if "リグマ" in txt or "リーグ" in txt or "リーグマッチ" in txt:
        rule = "league"
    elif "ガチマ" in txt or "ガチ" in txt or "ガチマッチ" in txt:
        rule = "gachi"
    elif "ナワバリ" in txt or "ナワバリバトル" in txt or "レギュラー" in txt or "レギュラーマッチ" in txt:
        rule = "regular"
    else:
        return "不正なリクエストです！ルール名を確認してください！", "miss", "miss", "miss", "miss", "miss", "miss"

    match = re.search(r"[0-9]+", txt)

    if match == None:
        time = "now"
    else:
        time = "schedule"
        search_time = match.group()

    url = url + rule + "/" + time

    print(rule, time)

    r = requests.get(url, headers=headers)

    if r.status_code == 200:
        print("request successful")
        data = r.json()
        #print(data)
        #with open("getdata.txt", "w") as f:
        #    json.dump(data, f, ensure_ascii=False, indent=4)

        if time == "schedule":
            return search(data, search_time)
        else:
            return search(data)
    else:
        return "HTTPリクエスト時にエラーが発生しました！時間を空けてもう一度実行してください！", "miss", "miss", "miss", "miss", "miss", "miss"

def search(json_object, search_time = None):
    result = json_object["result"]

    if not search_time == None:
        search_time = math.ceil(float(search_time) / 2) * 2 - 1
        if 0 <= search_time <= 9:
            search_time = str(0) + str(search_time)
        else:
            search_time = str(search_time)

    #print(search_time)

    for i in range(len(result)):
        match = re.search(r"[0-2][0-9]:[0-5][0-9]:[0-5][0-9]", result[i]["start"])
        #print(match)
        if not match == None:
            hour = re.match(r"[0-2][0-9]", match.group())
            #print(hour)
            date = re.search(r"[0-9]{4}-", result[i]["start"])
            date = result[i]["start"].replace(match.group(), "").replace(date.group(), "").replace("T", "").replace("-", "/")
            if search_time == None:
                return result[i]["rule_ex"]["name"], result[i]["maps_ex"][0]["name"], result[i]["maps_ex"][0]["image"], result[i]["maps_ex"][1]["name"], result[i]["maps_ex"][1]["image"], date, hour.group(), str(int(hour.group()) + 2)
            if hour.group() == search_time:
                return result[i]["rule_ex"]["name"], result[i]["maps_ex"][0]["name"], result[i]["maps_ex"][0]["image"], result[i]["maps_ex"][1]["name"], result[i]["maps_ex"][1]["image"], date, hour.group(), str(int(hour.group()) + 2)
    #print(result)
    return "検索時にエラーが発生しました！jsonの破損、もしくはバグの可能性があります！時間を空けてもう一度実行しても同じメッセージが表示される場合は管理者に知らせてください！", "miss", "miss", "miss", "miss", "miss", "miss"

# 先頭一致でルールであるかを返す関数
def check_rule(txt):
    if re.match(r"リグマ|リーグマッチ|リーグ|ガチマ|ガチ|ガチマッチ|ナワバリ|ナワバリバトル|レギュラー|レギュラーマッチ", txt):
        return True
    else:
        return False