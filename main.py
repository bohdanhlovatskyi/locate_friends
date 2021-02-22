'''
Runs web-application with which you can display on the map data (field "location")
about friends (people you are subscribed to) of the specified account on Twitter.
'''

from flask import Flask, render_template, request, flash
from get_map_module import get_friends_locations

app = Flask(__name__, static_folder="templates")
app.config.update(SECRET_KEY='sdjflkdfjkjwerekj43kfjslkj')

@app.route('/', methods=['POST', 'GET'])
def get_user_name():
    if request.method == 'POST':
        user_name = str(request.form['user_name'])
        bearer_token = str(request.form['bearer_token'])
        friends_map = get_friends_locations(user_name, bearer_token)
        if friends_map:
            # can be done via get_route also without breaking laws of OOP)
            return friends_map._repr_html_()

        flash('There is no such person on Twitter', category='error')
        return render_template('index.html')

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
