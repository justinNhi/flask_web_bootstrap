from flask import Flask, render_template

app = Flask(__name__)


@app.route('/main')
def main():
    return render_template('main.html')

@app.route('/quan_ly_xe')
def quan_ly_xe():
    return render_template('quan_ly_xe.html')
@app.route('/')
@app.route("/list_xe")
def list_xe():
    return render_template('list_xe.html')

@app.route("/them_xe")
def them_xe():
    return render_template('them_xe.html')

@app.route("/xe", methods=['POST'])
def xe():
    return render_template('xe.html')

if __name__ == '__main__':
    app.run(debug=True)
