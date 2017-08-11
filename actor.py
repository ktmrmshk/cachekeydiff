import requests
import urllib3
import csv
import re
import json
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

AKAM_PRAGMA='akamai-x-get-request-id, akamai-x-cache-on, akamai-x-cache-remote-on, akamai-x-check-cacheable,akamai-x-get-cache-key, akamai-x-get-extracted-values, akamai-x-get-nonces, akamai-x-get-ssl-client-session-id, akamai-x-get-true-cache-key, akamai-x-serial-no, akamai-x-feo-trace'
AKAM_CHDR=['x-cache-key', 'x-true-cache-key', 'x-check-cacheable', 'x-akamai-staging']
DEFAULT_CHDR=['content-encoding', 'etag', 'server', 'content-length', 'last-modified', 'content-type', 'cache-control', 'edge-control', 'expires']


class Actor(object):
  def __init__(self, connhost=None):
    self.connhost=connhost
    self.req=None

  def get(self, url, params=None, **kargs):
    if 'headers' not in kargs:
      kargs['headers'] = dict()
    kargs['headers'].update({'Pragma': AKAM_PRAGMA})
    
    # spoofing
    if self.connhost is not None:
      # parse host 
      match = re.search('(http|https):\/\/([^\/]+)(\/.*$|$)', url)
      assert match is not None
      host=match.group(2)
      url=url.replace(host, self.connhost)
      
      if 'headers' not in kargs:
        kargs['headers'] = dict()
      kargs['headers'].update({'Host': host})
      
      if 'verify' not in kargs:
        kargs['verify']=False

    
    r=requests.get(url, params, **kargs)
    self.req=r
    #self.dump(r)

  def dump(self, req=None):
    #pre=r.prepare()
    if req is None:
      assert self.req is not None
      req=self.req

    print('{} {}'.format(req.request.method, req.request.url))
    for k,v in req.request.headers.items():
      print(k,v)
    else:
      print()

    print(req.status_code)
    for k,v in req.headers.items():
      print(k,v)

    
class Tester(object):
  '''
    feddata: [url] [tobe] [tobe code] [result] [result code] [judge]
  '''
  def __init__(self, prodhost, stghost):
    self.a=Actor()
    self.prod=Actor(prodhost)
    self.stg=Actor(stghost)
    

  def redirect(self, testcasefile):
    '''
      testcasefile should contain list of redirect testcase like:
      [from url] [to url] [status code]
      http://abc.com/a.html?abc=123 https://foo.com/erro.html 301
      http://abc.com/a.html https://bar.com/ 302
      ....
    '''
    rows=[]
    with open(testcasefile) as f:
      for line in f:
        rows.append( re.split('[ \t]+', line) )
    
    for r in rows:
      self.a.get(r[0], allow_redirects=False)
      ret='NG'
      if self.a.req.status_code == int(r[2]):
        assert 'Location' in self.a.req.headers or 'location' in self.a.req.headers
        if self.a.req.headers['location'] == r[1]:
          ret='Passed'
        elif r[1].endswith(self.a.req.headers['location']):
          ret='Contains'
        else:
          print('>>>> {} vs {}'.format(self.a.req.headers['location'], r[1]))
      
      akamemo=''
      if 'x-akamai-staging' in self.a.req.headers:
        akamemo = 'x-akamai-staging:{}'.format( self.a.req.headers['x-akamai-staging'] )
      # target(src), ret_code, ret_judge, memo
      print('{}, {}, {}, server:{} {}'.format(r[0], self.a.req.status_code, ret, self.a.req.headers['Server'], akamemo))

  def __redirect(self, url, query, prod_actor, stg_actor):
    # scan prod
    prod_location='-'
    prod_actor.get(url, query, allow_redirects=False)
    if 'location' in prod_actor.req.headers:
      prod_location = prod_actor.req.headers['location']

    # scan stg
    stg_location='-'
    stg_actor.get(url, query, allow_redirects=False)
    if 'location' in stg_actor.req.headers:
      stg_location = stg_actor.req.headers['location']

    # check 
    ret='NG'
    if prod_actor.req.status_code == stg_actor.req.status_code:
      if prod_location == stg_location:
        ret='Passed'
      elif prod_location.endswith(stg_location):
        ret='Passed (sub match)'
      elif stg_location.endswith(prod_location):
        ret='Passed (sub match)'

    # print: target, prod, prod_code, stg, stg_code, result
    print('{}, {}, {}, {}, {}, {}'.format(prod_actor.req.request.url, prod_location, prod_actor.req.status_code, stg_location, stg_actor.req.status_code, ret))



  def redirect2(self, testcasefile, query=''):
    rows=[]
    with open(testcasefile) as f:
      for line in f:
        rows.append( re.split('[ \t]+', line) )
        #rows.append(line.rstrip())

    for r in rows:
      #self.__redirect(r, self.prod, self.stg)
      #self.__redirect(r+query, self.prod, self.stg)
      self.__redirect(r[0], {r[3].rstrip(): 'users/omura/fund_touraku'}, self.prod, self.stg)

  def _diff_header(self, url, prod_actor, stg_actor, hdrs=[]):
    '''
    hdrs: list: [ 'etag', 'cache-control']
    result:
    ret['date']['prod'] = 'abc123'
    ret['date']['match'] = true
    {
      'status' : { 'prod': '200' , 'stg': '200', 'match': 'true'],
    }
    '''
    
    prod_actor.get(url, allow_redirects=False)
    stg_actor.get(url, allow_redirects=False)
    #for k,v in stg_actor.req.headers.items():
    #  print( '{}: {}'.format(k, v) )
    ret={}
    
    ret['status_code'] = { 'prod': prod_actor.req.status_code, 'stg': stg_actor.req.status_code}
    if prod_actor.req.status_code == stg_actor.req.status_code:
      ret['status_code']['match'] = True
    else:
      ret['status_code']['match'] = False


    chdr = AKAM_CHDR + DEFAULT_CHDR
    for h in hdrs:
      if h.lower() not in chdr:
        chdr.append(h.lower())

    for h in chdr:
      cret={}
      if h in prod_actor.req.headers:
        cret['prod']=prod_actor.req.headers[h]
      else:
        cret['prod']=''
      if h in stg_actor.req.headers:
        cret['stg']=stg_actor.req.headers[h]
      else:
        cret['stg']=''
      
      if cret['prod'] == cret['stg']:
        cret['match'] = True
      else:
        cret['match'] = False
      ret[h] = cret

    print(json.dumps(ret, indent=2))
    #stg_actor.dump()
    
if __name__ == '__main__':
  #a=Actor('www.omura.co.jp.edgekey-staging.net')
  #a.get('https://www.omura.co.jp/recruit/', headers={'cookie':'adb'})
  #a.dump()
  #t=Tester('www.omura.co.jp.edgekey-staging.net')
  #t=Tester('www.omura.co.jp.edgekey.net', 'www.omura.co.jp.edgekey-staging.net')
  #t.redirect2('redirectlist_q.txt', '?abc=123')

  
  t=Tester('www.wakodo.co.jp', 'www.wakodo.co.jp.edgekey-staging.net')
  t._diff_header('http://www.wakodo.co.jp/', t.prod, t.stg)

  
