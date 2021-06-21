from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def main():
    return render_template('main.html')

@app.route('/quan_ly_xe')
def quan_ly_xe():
    return render_template('quan_ly_xe.html')

if __name__ == '__main__':
    app.run(debug=True)
