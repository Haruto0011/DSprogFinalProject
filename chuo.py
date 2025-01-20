import requests
from bs4 import BeautifulSoup
import time
import pandas as pd

# 中央区のSUUMO賃貸ページURL
url = "https://suumo.jp/chintai/tokyo/sc_chuo/"

# ヘッダー設定
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# スクレイピング処理（全ページ対応）
def scrape_rental_properties(base_url):
    properties = []
    page = 1  # ページ数カウント用
    while base_url:
        print(f"アクセス中: {base_url} (ページ {page})")
        response = requests.get(base_url, headers=headers)
        
        if response.status_code != 200:
            print(f"失敗: ステータスコード {response.status_code}")
            break
        
        soup = BeautifulSoup(response.text, "html.parser")
        
        # SUUMOページ内の賃貸物件リストを取得
        property_list = soup.find_all("div", class_="cassetteitem")
        if not property_list:
            print("物件リストが取得できませんでした。HTML構造を確認してください。")
            break

        for property in property_list:
            try:
                # 必要なデータを抽出
                name = property.find("div", class_="cassetteitem_content-title").text.strip()
                address = property.find("li", class_="cassetteitem_detail-col1").text.strip()
                stations = [station.text.strip() for station in property.find_all("li", class_="cassetteitem_detail-col2")]
                rent = property.find("span", class_="cassetteitem_price--rent").text.strip()
                layout = property.find("span", class_="cassetteitem_madori").text.strip()  # 間取り
                area = property.find("span", class_="cassetteitem_area").text.strip()  # 面積
                
                # データをリストに追加
                properties.append({
                    "物件名": name,
                    "住所": address,
                    "最寄り駅": stations,
                    "賃料": rent,
                    "間取り": layout,
                    "面積": area
                })
            except AttributeError:
                continue

        # 次ページへのリンクを取得
        next_page = soup.find("a", class_="pagination__next")
        if next_page and next_page.get("href"):
            base_url = "https://suumo.jp" + next_page.get("href")
            page += 1
            time.sleep(3)  # サーバー負荷軽減のため待機
        else:
            base_url = None
    
    return properties

# スクレイピング開始
properties = scrape_rental_properties(url)

# データをCSVに保存
if properties:
    df = pd.DataFrame(properties)
    df.to_csv("chuo_rental_properties.csv", index=False, encoding="utf-8-sig")
    print("データをCSVに保存しました: chuo_rental_properties.csv")
else:
    print("物件データが取得できませんでした。")