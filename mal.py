from bs4 import BeautifulSoup
import requests
import time

#input mal show page url, returns title and image link
def titleimage(url):
    page=requests.get(url).text
    soup = BeautifulSoup(page, 'lxml')
    #check to make sure we are actually being fed a valid link
    title=soup.find('h1')
    if title is None:
        title='error'
    else:
        title=title.text
    image=soup.find('div', class_='leftside')
    if image is None:
        image='missing image'
    else:
        image=image.img['data-src']
    return title,image


#scrapes the top (amount) shows from mal and writes to html file.
amount=10
def scrapeMAL():
    #set url
    url='https://myanimelist.net/topanime.php'
    page=requests.get(url).text
    soup = BeautifulSoup(page, 'lxml')

    #get the table of shows
    table=soup.find('table',{'class':'top-ranking-table'})
    #get the rows 1-amount (excludes header) from the table
    rows=table.find_all('tr')[1:amount+1] 
    
    with open('index.html','w') as file:
        file.write('<html>\n<head>\n\t<link rel="stylesheet" href="styles.css">\n</head>\n<body>\n')
        for row in rows:
            #get the link to the show page
            link=row.find('a')['href']
            #get the title/image of the show
            title=titleimage(link)[0]
            image=titleimage(link)[1]
            file.write('\t<div>\n\t\t<h3>'+title+'</h3>\n\t\t'+'<img src="'+image+'">\n\t</div>\n')
        file.write('</body>\n</html>')


#check if the file is being run as a script
if __name__ == "__main__":
    scrapeMAL()
    '''
    #continuously scrape every x hours
    while True:
        scrapeMAL()
        #wait 24hours to run again
        hours=24
        print(f'Waiting {hours} hours to ping again')
        time.sleep(hours*60*60)
        '''