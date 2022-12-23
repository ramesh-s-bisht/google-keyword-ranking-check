#importing the necessary modules 
import csv
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

#opening the website in incognito mode
chrome_options = Options()
chrome_options.add_argument("--incognito")
driver = webdriver.Chrome(options=chrome_options)

#importing the keywords.csv file
csv_file = csv.reader(open('ai-keywords.csv'))
for row in csv_file:
    keyword = row[0]
    driver.get('https://www.google.com/')
    driver.get('https://www.google.com/search?q='+keyword+'&num=50')
    time.sleep(5)
    #exclude results from class 'M8OgIe' and 'ULSxyf' on google.com results
    soup = BeautifulSoup(driver.page_source, 'lxml')
    for item in soup.find_all('div', {'class': ['M8OgIe', 'ULSxyf']}):
        item.decompose()
    # Getting keyword ranking position results only from class 'yuRUbf' on Google.com
    results = soup.find_all('div', {'class': 'yuRUbf'})
    #finding the ranking position of the website https://www.mygreatlearning.com 
    ranking_position = 0
    for result in results:
        link = result.find('a').get('href')
        if link.startswith('https://www.mygreatlearning.com'):
            ranking_position = results.index(result) + 1
            break
    #printing the results
    print('Keyword:', keyword, ' Ranking Position:', ranking_position)
    #exporting the csv including all keywords with the date and time
    with open('keyword_ranking_results.csv', 'a') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow([keyword, ranking_position, time.strftime('%Y-%m-%d %H:%M:%S')])
    
driver.quit()


