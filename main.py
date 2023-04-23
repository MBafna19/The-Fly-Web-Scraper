import requests
from datetime import date
from bs4 import BeautifulSoup
import pandas as pd

#CONFIGURATION
#Date (in format YYYY-MM-DD)
today_date = date.today()

#WORDS TO ASSOCIATE
upgrade_stock = ['raised', 'upgrade']
downgrade_stock = ['downgrade', 'lower']

headers = { 'Accept-Language' : "en-GB,en-US;q=0.9,en;q=0.8",
            'User-Agent':"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
            'Accept':"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7"}

URL = "https://thefly.com/news.php?fecha=" + str(today_date) + "&analyst_recommendations=on&upgrade_filter=on&downgrade_filter=on&initiate_filter=on&no_change_filter=on&symbol="

# sending get request and saving the response as response object
r = requests.get(url = URL, headers=headers)
  
# extracting data in json format
data = r.text

soup = BeautifulSoup(data, features="html.parser")
res = soup.find_all("a", class_="newsTitleLink")


f = open("history/the_fly_webscraped-" + str(today_date)  + ".txt", "w")
for each in res:
    f.write(str(each) + '\n')
f.close()



f = open("history/the_fly-" + str(today_date)  + ".txt", "w")
f.write(data)
f.close()



results = []
for each in res:
    #Pull out the stock symbol
    link = each.get('href')
    get_title = link.split("/")[-1]
    get_symbol = get_title.split("-", 1)[0]
    
    for i in upgrade_stock:
        if i in get_title:
            results.append({'symbol': get_symbol, 'result': 'upgrade', 'link': link, 'date': str(today_date)})
    
    for i in downgrade_stock:
        if i in get_title:
            results.append({'symbol': get_symbol, 'result': 'downgrade', 'link': link, 'date': str(today_date)})

    #Determine if its good news or bad news


df = pd.DataFrame(results)
df.to_csv('current.csv', mode='w', index=False, header=False)

print(df)





