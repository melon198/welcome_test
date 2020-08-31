import requests
from bs4 import BeautifulSoup
import csv
from datetime import date
import pyautogui

msgbox_ticker = pyautogui.prompt(title="Income Statement Extractor",\
    default="Please enter a ticker or symbol",\
    text="Income Statement Extractor\n\
        created by Ian")

ticker = msgbox_ticker.upper()

try:

    url = f"https://finance.yahoo.com/quote/{ticker}/financials?p={ticker}"

    res = requests.get(url)
    soup = BeautifulSoup(res.text, "lxml")

    # Income Statement 금액단위 표시
    unit = soup.find("span", attrs={"data-reactid":"42"})
    unit = [unit.get_text()]


    # Income Statement 타이틀
    headers = soup.find("div", attrs={"class":"D(tbr) C($primaryColor)"})
    title = []
    for header in headers:
        header = header.get_text().strip()
        title += [header]

    # 파일 생성 날짜
    today = date.today()
    mdy = today.strftime("%m_%d_%y")

    # csv 파일 생성
    filename = "{}_{}_fianacials.csv".format(mdy, ticker)
    f = open(filename, "w", newline="")
    writer = csv.writer(f)
    writer.writerow(unit) # 금액 단위 기입
    writer.writerow(title) # 타이틀 기입

    rows = soup.find_all("div", attrs={"data-test":"fin-row"})
    
    # Income Statement 금액 데이터

    for row in rows:
        account = row.find("span", attrs={"class": "Va(m)"})
        columns = row.find_all("div", attrs={"data-test" : "fin-col"})
        data1 = account.get_text()
        data2 = [column.get_text() for column in columns] # Columns에서 나온 Column 값들을 모두 Data 변수에 리스트로 저장
        data2.insert(0,data1)
        writer.writerow(data2)


    

except:
    pyautogui.alert(text="'Invalid ticker(symbol) founded, Please enter a valid ticker(symbol)'",\
        title="Alert")
    
    
