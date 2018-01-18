from flask import *
import json
import actor, rname, htmlp


app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({'header': ['hello', 'world']} )

@app.route('/cdiff/')
def basepage():
    return send_from_directory('static', 'cdiff_uibase.html')

@app.route('/cdiff/<path:filename>')
def static_file(filename):
    return send_from_directory('static', filename)

@app.route('/cdiff/debug/', methods=['GET'])
def cdiff_get():
    print('{}'.format(request.args))
    url=request.args['url']
    prod=request.args['serverA']
    stg=request.args['serverB']
    t=actor.Tester(prod, stg)
    res=t.diff([url])
    print(res)
    print('url={}, s1={}, s2={}'.format(url, prod, stg))

    ret = make_response(jsonify( res ))
    ret.status_code = 200
    return ret
    #return 'ok'

@app.route('/cdiff/diff/')
def cdiff_diff():
    url=request.args['url']
    prod=request.args['serverA']
    stg=request.args['serverB']
    t=actor.Tester(prod, stg)
    res=t.diff([url])

    ret = make_response(jsonify( res ))
    ret.status_code = 200

    return ret


@app.route('/<dp>/edgehostname/')
def get_edgehostname(dp):
    print('{}'.format(dp))
    rn=rname.rname()
    prod, stg = rn.get_akname(dp)
    ret={}
    ret['propertyhostname']=dp
    ret['edgehostname']={'prod': prod, 'stg': stg}

    return jsonify( ret )

@app.route('/cdiff/urllist/')
def get_urllist():
    assert 'basepage' in request.args
    hp=htmlp.Hp()
    hp.parsePage(request.args['basepage'])
    return jsonify( hp.links )





if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
