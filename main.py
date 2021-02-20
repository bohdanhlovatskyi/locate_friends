'''
Runs web-application with which you can display on the map data (field "location")
about friends (people you are subscribed to) of the specified account on Twitter.
'''

from flask import Flask, render_template, request
from get_map_module import main

app = Flask(__name__, static_folder="templates")


@app.route('/')
def homepage():
    return render_template('index.html')

@app.route('/get_user', methods=['POST', 'GET'])
def get_user_name():
    user_name = request.form.get('user_name')
    if user_name:
        try:
            file_name = main(user_name).split('/')[-1]
        except ValueError:
            return file_name
        return render_template(file_name)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)