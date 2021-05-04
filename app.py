from flask import Flask, render_template, request, flash, redirect, url_for, session
from hashids import Hashids
import uuid

app = Flask(__name__)
hashids = Hashids(min_length=4, salt=str(uuid.uuid1()))
app.secret_key = "1ad7d379a20cb894w"
LISTA_URLS = {}


@app.route('/erro', methods=['GET'])
def NaoEncontrado():
    return render_template('erro.html')


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url_i = request.form['URL']
        if len(url_i) > 0:
            link_gerado = hashids.encode(len(LISTA_URLS))
            LISTA_URLS[link_gerado] = url_i
            session["url"] = request.host_url + "l" + link_gerado
        return redirect(url_for('index'))
    elif request.method == 'GET':
        if "url" in session:
            nova_url = session["url"]
            return render_template('index.html', nova_url=nova_url)
        return render_template('index.html')


@app.route('/l<string:lnk>', methods=['GET'])
def link(lnk):
    if lnk in LISTA_URLS:
        return redirect(LISTA_URLS[lnk])
    else:
        return redirect(url_for('NaoEncontrado'))


@app.errorhandler(404)
def not_found(e):
    return redirect(url_for('NaoEncontrado'))


if __name__ == "__main__":
    app.run(debug=False)
