from html.parser import HTMLParser
from urllib.parse import urljoin


g_links=[]
class Htmlp(HTMLParser):
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
          g_links.append(a[1])
    elif tag == 'script':
      for a in attrs:
        if a[0] == 'src':
          g_links.append(a[1])
    elif tag == 'a':
      for a in attrs:
        if a[0] == 'href':
          g_links.append(a[1])
    elif tag == 'img':
      for a in attrs:
        if a[0] == 'src':
          g_links.append(a[1])

class Hp(object):
  def __init__(self):
    self.links=[]

  def parselink(self, html):
    hp = Htmlp()
    hp.feed(html)
    print(g_links)
    #print(html)
    self.links = list(g_links)
  
  def dump(self, base=''):
    print('-')
    for l in self.links:
      print( urljoin(base, l) )


if __name__ == '__main__':
  html=''
  with open('index.html') as f:
    html = f.read()
  
  base='https://www.ins.com/'
  hp=Hp()
  hp.parselink(html)
  hp.dump(base)


