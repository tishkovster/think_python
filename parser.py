from lxml import html
import requests
import pprint

page = requests.get("https://yadi.sk/d/stfqXHPA3NLUrs")
tree = html.fromstring(page.content)
#<div class="listing-item__title" data-reactid="119">A. Downey - Думать на языке Python (2013).pdf</div>
books = tree.xpath('//div[@class="listing-item__title"]/text()')
pprint.pprint(books)
