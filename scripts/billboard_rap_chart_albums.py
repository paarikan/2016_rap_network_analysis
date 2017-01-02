import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

INITIAL_WEEK = '2016-01-02'
END_DATE = '2016-12-31'

def main():
    week = datetime.strptime(INITIAL_WEEK, '%Y-%m-%d')
    albums = set()
    while datetime.strftime(week,'%Y-%m-%d') < END_DATE:
        print datetime.strftime(week,'%Y-%m-%d')
        albums = albums.union(get_albums_for_week(datetime.strftime(week,'%Y-%m-%d')))
        week = week + timedelta(days=7)

    o = open('../data/billboard_rap_chart_albums.csv', 'w')
    for album in albums:
        o.write(album[0] + ',' + album[1] + '\n')

    o.close()


def get_albums_for_week(week):
    base_chart_url = 'http://www.billboard.com/charts/rap-albums/'
    response = requests.get(base_chart_url + week)
    soup = BeautifulSoup(response.text, 'html.parser')
    chart_row_title_divs = soup.find_all('div',{'class':'chart-row__title'})
    albums = set()
    for div in chart_row_title_divs:
        album_name = div.find_all('h2',{'class':'chart-row__song'})[0].text.strip()
        artist_name_as = div.find_all('a',{'class':'chart-row__artist'})
        if artist_name_as:
            artist_name = artist_name_as[0].text.strip()
        else:
            artist_name = div.find_all('h3',{'class':'chart-row__artist'})[0].text.strip()
        album = (album_name, artist_name)
        albums.add(album)
    return albums

if __name__ == "__main__":
    main()