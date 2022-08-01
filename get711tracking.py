import requests as req
from bs4 import BeautifulSoup
import datetime
import re
import valid

# ----- setting ----- #
domain = 'https://eservice.7-11.com.tw/e-tracking/'
url = 'search.aspx'
captchaurl = 'ValidateImage.aspx?ts='
dirpath = '.\\captcha\\'
img = 'codeImg.jpg'

browser = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'

# ----- function ----- #


def getResource():
    with req.get(domain + url, headers={'User-Agent': browser}) as response:
        if response.status_code != 200:
            response.raise_for_status()
        cookies = response.cookies
        body = BeautifulSoup(response.text, 'html.parser')
    __VIEWSTATE = body.find('input', {'id': '__VIEWSTATE'}).get('value', None)
    __VIEWSTATEGENERATOR = body.find(
        'input', {'id': '__VIEWSTATEGENERATOR'}).get('value', None)
    headers_tmp_cookie = []
    for k, v in cookies.get_dict().items():
        headers_tmp_cookie.append(f'{k}={v}')
    headers = {
        'Cookie': ';'.join(headers_tmp_cookie),
        'User-Agent': browser
    }
    resource = {
        'headers': headers,
        '__VIEWSTATE': __VIEWSTATE,
        '__VIEWSTATEGENERATOR': __VIEWSTATEGENERATOR,
        'code': f'{domain}{captchaurl}{datetime.datetime.now().strftime("%H%M%S%m%d")}'
    }
    codeImg(
        f'{domain}{captchaurl}{datetime.datetime.now().strftime("%H%M%S%m%d")}', headers)
    return resource


# save captcha image
def codeImg(codeImgURL, headers):
    with req.get(codeImgURL, headers=headers) as response:
        if response.status_code != 200:
            response.raise_for_status()
        with open(f'{dirpath}{img}', 'wb') as file_io:
            file_io.write(response.content)


def tracker(txtProductNum):
    resource = getResource()
    code = valid.getCaptchatxt(img)

    if not code:
        # recrusion until code valid
        return tracker(txtProductNum)

    payload = {
        '__LASTFOCUS': '',
        '__EVENTTARGET': '',
        '__EVENTARGUMENT': '',
        '__VIEWSTATE': resource['__VIEWSTATE'],
        '__VIEWSTATEGENERATOR': resource['__VIEWSTATEGENERATOR'],
        'txtProductNum': txtProductNum,
        'tbChkCode': code,
        'aaa': '',
        'txtIMGName': '',
        'txtPage': '1'
    }
    with req.post(domain + url, headers=resource['headers'], data=payload, allow_redirects=False) as response:
        if response.status_code != 200:
            response.raise_for_status()
        body = BeautifulSoup(response.text, 'html.parser')
        if (body.find('input', {'id': 'txtPage'})['value']) == '2':
            info_children = body.find('div', {'class': 'info'}).find_all(
                'div', recursive=False)
            shipping = body.find('div', {'class': 'shipping'})
            pickup_info = info_children[0]
            # Store
            store_name = pickup_info.find('span', {'id': 'store_name'}).text
            # StoreAddr
            store_address = pickup_info.find('p', {'id': 'store_address'}).text
            # ExpireDate
            pickup_deadline = pickup_info.find('span', {'id': 'deadline'}).text
            # Payment
            payment_type = info_children[1].find(
                'h4', {'id': 'servicetype'}).text
            # Details
            status = []
            for subitem in shipping.find_all('li'):
                status_date = re.findall(
                    r"\d{4}/\d{2}/\d{2} \d{2}:\d{2}", subitem.text)[0]
                status.append({'Time': status_date, 'Status': (
                    subitem.text).replace(status_date, '')})
            status.reverse()
            data = {
                "Store": store_name,
                "StoreAddr": store_address,
                "ExpireDate": pickup_deadline,
                "Payment": payment_type,
                "Details": status
            }
            return data
        else:
            # recrusion until code valid
            return tracker(txtProductNum)


def getTacking(trackingno: str):
    return tracker(trackingno)


# ----- Execute section ----- #
print(getTacking('G16919388853'))
