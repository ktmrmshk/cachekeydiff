from html.parser import HTMLParser
from urllib.parse import urljoin
import requests

class Htmlp(HTMLParser):
  def kickfeed(self, html):
    self.links=[]
    self.feed(html)

  def handle_starttag(self, tag, attrs):
    '''
    pickupt links
    <link rel="apple-touch-icon" href="/jp/img/sp/app_icon.png">
    <script src="/jp/common/js/lib/slick.js"></script>
    <a href="//www.jins.com/jp/st/sunglasses/" class="ss-link linkBtn">
    <img src="/jp/common/img/home/style_men.jpg" width="347" alt="MEN">
    '''
    if tag == 'link':
      for a in attrs:
        if a[0] == 'href':
          self.links.append(a[1])
    elif tag == 'script':
      for a in attrs:
        if a[0] == 'src':
          self.links.append(a[1])
    elif tag == 'a':
      for a in attrs:
        if a[0] == 'href':
          self.links.append(a[1])
    elif tag == 'img':
      for a in attrs:
        if a[0] == 'src':
          self.links.append(a[1])

class Hp(object):
  def __init__(self):
    self.links=[]
    self.visited=[]

  def parselink(self, html, url):
    hp = Htmlp()
    hp.kickfeed(html)
    for l in hp.links:
      if urljoin(url, l) not in self.links:
        self.links.append( urljoin(url, l) )
  
  def dump(self):
    for l in self.links:
      print( l )
    print(self.visited)


  def parsePage(self, url):
    r=requests.get(url, timeout=1.0)
    self.visited.append(url)
    if url != r.request.url:
      self.visited.append(r.request.url)
    if r.status_code == 200 and 'text/html' in r.headers['content-type']:
      #print (r.encoding)
      html=r.content.decode(r.encoding)
      self.parselink(html, r.request.url)
    

if __name__ == '__main__':
  html=''
  with open('index.html') as f:
    html = f.read()
  
  base='https://www.jins.com/'
  hp=Hp()
  #hp.parselink(html)
  hp.parsePage(base)
  hp.dump()


