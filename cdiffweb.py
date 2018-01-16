from flask import *
import json
import actor, rname


app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({'header': ['hello', 'world']} )

@app.route('/cdiff/')
def basepage():
    return send_from_directory('static', 'cdiff_uibase.html')


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

@app.route('/<dp>/edgehostname/')
def get_edgehostname(dp):
    print('{}'.format(dp))
    rn=rname.rname()
    prod, stg = rn.get_akname(dp)
    ret={}
    ret['propertyhostname']=dp
    ret['edgehostname']={'prod': prod, 'stg': stg}

    return jsonify( ret )



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
