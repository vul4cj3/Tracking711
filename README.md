[![GitHub release](https://img.shields.io/github/pipenv/locked/python-version/vul4cj3/Tracking711)]()
# Tracking711
 台灣7-11超商貨況爬蟲
# File info
|Name|Description|
|----|----|
|/catpcha|放置測試用的驗證碼|
|valid.py|取得驗證碼文字|
|get711tracking.py|從台灣7-11貨況查詢網站取得貨況資料|
# Install
1. 下載source code  
2. 安裝python相關套件
3. 安裝tesseractOCR  
   [Linux 安裝 tesseract](https://github.com/tesseract-ocr/tesseract/wiki)   
   [Windows 安裝 tesseract](https://github.com/UB-Mannheim/tesseract/wiki)
# How to use
1. 打開 valid.py 設定tesseract.exe路徑
2. call get711tracking.py getTacking函式
```python
# return Result
{'Store': '台興', 
 'StoreAddr': '高雄市岡山區台上里嘉新東路136號', 
 'ExpireDate': '2022-07-27', 
 'Payment': '取貨不付款', 
 'Details': [{'Time': '2022/07/15 10:10', 'Status': '交貨便訂單已成立，尚未至門市寄件'}, 
             {'Time': '2022/07/18 12:33', 'Status': '寄件門市已收件'}, 
             {'Time': '2022/07/18 13:01', 'Status': '包裹已送往物流中心'}, 
             {'Time': '2022/07/19 06:08', 'Status': '包裹已送達物流中心，將配至取件門市'}, 
             {'Time': '2022/07/19 16:50', 'Status': '包裹等待配送中'}, 
             {'Time': '2022/07/19 22:45', 'Status': '包裹進行配送中'}, 
             {'Time': '2022/07/20 01:52', 'Status': '包裹配達取件門市'}, 
             {'Time': '2022/07/20 05:23', 'Status': '已完成包裹成功取件'}]
}
```
# Other 
tesseractOCR驗證碼識別率約80%
