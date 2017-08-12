import dns.resolver, dns.rdatatype
import re

class rname(object):
  def __init__(self):
    pass

  def get_akname(self, hostname):
    '''
    get_ProdStgName('www.jins.com')
    return ('www.jins.com.edgekey.net', 'www.jins.com.edgekey-staging.net') 
    return (None, None)
  
    www.hoge.com
    www.akamaized.net
    www.edgesuite.net
    www.edgekey.net
    '''
  
    m = re.search('(.+)(edgesuite|edgekey|akamaized)(\.net)$', hostname)
    if m is not None:
      return (hostname, self.Stgname(hostname))
    else:
      #CNAME check
      try:
        ans=dns.resolver.query(hostname, 'CNAME')
        if ans.rrset.rdtype == dns.rdatatype.CNAME:
          cn = ans.rrset.items[0].to_text()
          if cn[-1] == '.':
            cn=cn[:-1]
          m = re.search('(.+)(edgesuite|edgekey|akamaized)(\.net)$', cn)
          if m is not None:
            return (cn, self.Stgname(cn))
      except Exception as err:
        pass
      return (hostname, None)

  def Stgname(self, prodname):
    m = re.search('(.+)(edgesuite|edgekey|akamaized)(\.net)$', prodname)
    assert m is not None
    return m.group(1) + m.group(2) + '-staging' + m.group(3)
    

if __name__ == '__main__':
  rs=dns.resolver.Resolver()
  ans=rs.query('www.jins.com', 'A')
  
  rn = rname()
  #stg=rn.Stgname('www.space.ktmrmshk.com.edgekey.net')
  stg = rn.get_akname('www.jins.com')
  #stg = rn.get_akname('www.google.com')
  print(stg)



