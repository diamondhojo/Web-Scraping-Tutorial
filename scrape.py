from bs4 import BeautifulSoup
import requests
import csv

source = requests.get('http://coreyms.com').text
soup = BeautifulSoup(source, 'lxml')

csv_file = open('scrape.csv', 'w')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Headline', 'Summary', 'Link'])

#prints are broken down to show how grabbing the video ID works 9uncomment prints to show)
for article in soup.find_all('article'):
    headline = article.h2.a.text
    print("Headline: \n" + headline + "\n")

    summary = soup.find('div', class_="entry-content").p.text
    print("Summary: \n" + summary + "\n")

    try:
        video_source = article.find('iframe', class_="youtube-player")['src']       #use indexing to grab the src tag within the iframe tag
        #print(video_source + "\n")
        #this might trigger 'TypeError: 'NoneType'' object is not subscriptable if video does not exist (can ignore)

        video_id = video_source.split('/')[4]      #splits URL into sections based on the '/' character, ID section is index 4
        #print(video_id + "\n")

        video_id = video_id.split('?')[0]       #grabs the actual ID of the ID section above
        #print(video_id + "\n")

        #YouTube URL format: https://youtube.com/watch?v=<video id>
        link = f'https://youtube.com/watch?v={video_id}'
        print("Link: \n" + link + "\n")
    except Exception as e:
        link = None
        print("Link: \nVideo does not exist for this article\n")
    
    csv_writer.writerow([headline, summary, link])

csv_file.close()


"""
EXAMPLE

with open('index.html', 'r') as html_file:
    soup = BeautifulSoup(html_file, 'lxml')

#example = soup.title       #this will print entire HTML line (including tag)
#example = soup.title.text      #this will print just the text in said tag
#article = soup.find('div', class_='article')       #this will print a specific div
for article in soup.find_all('div', class_='article'):        #this will return a list of all divs that match the given class
    headline = article.h2.a.text
    print(headline + "\n")

    summary = article.p.text
    print(summary + "\n")
"""
