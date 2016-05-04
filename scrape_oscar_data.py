import urllib2
import urllib
from lxml import html
import re

def get_tree(url):
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
    values = {'name' : 'Michael Foord',
	      'location' : 'Northampton',
	      'language' : 'Python' }
    headers = { 'User-Agent' : user_agent }

    data = urllib.urlencode(values)
    req = urllib2.Request(url, data, headers)
    response = urllib2.urlopen(req)
    the_page = response.read()
    tree = html.fromstring(the_page)	
    return tree

def get_win_nom_data(wn_block):
    movies = wn_block.xpath('./div')

    info = []

    
    for i, m in enumerate(movies):
    	mov_title = m.xpath('./strong/a/text()')[0]
        won='LOST'
        if i==0:
            won='WON'
	people = m.xpath('./a/text()')
	for p in people:
	    info.append((mov_title, p, won))


    return info

#get all year links 
#get 2016 results from first page
#get all results from each year

oscar_page = 'http://www.imdb.com/awards-central/oscars'
tree = get_tree(oscar_page)
blurbs = "//div[@id='sidebar']//div[@class='aux-content-widget-2']//a"
"//div[@class='ab_ninja']/p[@class='blurb']"
oscar_year_page_links = tree.body.xpath(blurbs)

base = 'http://www.imdb.com'
urls = []
for p in oscar_year_page_links:
    if re.match(r'\d{4}', p.text):

       year = re.findall(r'\d{4}', p.text).pop()

       urls.append((year,base+p.body.xpath('//a[text()="'+year+'"]/@href')[0] ))     

oscar_pages = []
for y, p in urls:
    t = get_tree(p)
    oscar_pages.append((y,t))

t = get_tree('http://www.imdb.com/event/ev0000003/2016')	
oscar_pages.append(("2016",t))

award_titles = []
for a in oscar_pages:
    award_title_list = a[1].xpath('//div[@class="award"][h1[text()="Oscar"]]/blockquote/h2/text()')
    award_titles.append((a[0], award_title_list))

win_noms = []
for i, a in enumerate(oscar_pages):
    win_nom_blocks = a[1].xpath('//div/div/div[@class="award"][h1[text()="Oscar"]]/blockquote/blockquote')
    win_noms.append((a[0], win_nom_blocks))


with codecs.open('testoscarout.txt', 'w', encoding='utf-8') as w:
    for i, at in enumerate(award_titles[:1]):
        win_nom_set = win_noms[i]
        year = win_nom_set[0]

        for j, wn_block in enumerate(win_nom_set[1]):
            for k, (movie, person, won) in enumerate(get_win_nom_data(wn_block)):
                w.write(year+ " ||| " +at[1][j]+ " ||| " +movie+ " ||| " + person +" ||| "+ won +"\n")
