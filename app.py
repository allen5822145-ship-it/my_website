from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup as bs

app = Flask(__name__)

def get_invoice_data():
    url = 'https://invoice.etax.nat.gov.tw/index.html'
    print("開始爬蟲...")
    try:
        # 強制設定 5 秒逾時
        htmlfile = requests.get(url, timeout=5)
        print("爬蟲抓取成功！")
    except Exception as e:
        print(f"爬蟲發生錯誤或逾時：{e}")
        return "連線逾時", "連線逾時", ["暫時無法取得"]

    soup = bs(htmlfile.text, 'lxml')
    start_tag = soup.find("tbody")
    
    rows = start_tag.find_all("tr")
    special_num = rows[0].find("span", class_="fw-bold etw-color-red").text
    special_num2 = rows[1].find("span", class_="fw-bold etw-color-red").text
    
    f_prize_tags = rows[2].find_all("p", class_="etw-tbiggest mb-md-4")
    f_prize = [i.text for i in f_prize_tags]
    
    return special_num, special_num2, f_prize

@app.route('/')
def index():
    s1, s2, f_list = get_invoice_data()
    return render_template('index.html', super_prize=s1, special_prize=s2, first_prizes=f_list)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001, debug=False)