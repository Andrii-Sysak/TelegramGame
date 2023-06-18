from flask import send_file, Flask


app = Flask('ssl')


@app.route('/.well-known/pki-validation/<file>')
def verify(file):
    return send_file(file)


app.run(host='0.0.0.0', port=80)
