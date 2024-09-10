import sys, json
from flask import Flask, make_response, request, jsonify,send_from_directory

app = Flask(__name__)
configs = json.loads(open('./config/kaoru.core.json').read())


def find_program_by_simple_name(simple_name, programs_list):
    for program in programs_list:
        if isinstance(program, dict) and program.get('simple-name') == simple_name:
            return program
    return None



@app.route('/')
def handshake_info():
    return 'Kaoru Running on Python ' + sys.version + '\n A DoConnectTools Service Server.'


@app.route('/update', methods=['GET'])
def get_update_info():
    program_list_define = json.loads(open("config/programs.json", 'r').read())
    program_simple_name = request.args.get('psname')
    if program_simple_name is None:
        response = jsonify({'code': -20,'status': 'error', 'msg': 'psname is required'})
        response.status_code = 400
        return response
    target = find_program_by_simple_name(program_simple_name,program_list_define)
    if target is None:
        response = jsonify({'code': -10,'status': 'error', 'msg': 'program is not defined'})
        return response
    else:
        if target.get('localupdate'):
            defile_update_url = request.host_url + '/update/' + target.get('simple-name') + '.asar'
            data = {
                'code': 0,
                'simple-name': target.get('simple-name'),
                'version': target.get('version'),
                'update-url': defile_update_url
            }
            response = jsonify(data)
            return response
        else:
            data = {
                'code': 0,
                'simple-name': target.get('simple-name'),
                'version': target.get('version'),
                'update-url': target.get('update_url')
            }
            response = jsonify(data)
            return response



@app.route('/online', methods=['GET'])
def get_online_204():
    response = make_response()
    response.status_code = 204
    return response

@app.route('/update/<path:filename>')
def get_update_files(filename):
    return send_from_directory('./files/asar/',filename, as_attachment=True)

if __name__ == '__main__':
    print(configs)
    app.run(host=configs.get('host'), port=configs.get('port'), debug=False)
