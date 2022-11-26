import csv
import requests

from flask import Flask, render_template, request, redirect

app = Flask(__name__)


@app.route('/')
def my_home():
    return render_template('index.html')


#
# @app.route('/about.html')
# def about():
#     return render_template('about.html')
#
#
# @app.route('/works.html')
# def work():
#     return render_template('works.html')

# we can make these above methods more dynamic, like incorporate all above methods in single methods

@app.route('/<string:page_name>')
def load_html_page(page_name):
    return render_template(page_name)


# feeding data to text file
def write_to_file(data):
    with open('database.txt', mode='a') as database:
        email = data["email"]
        subject = data["subject"]
        message = data["message"]
        file = database.write(f'\n{email}, {subject}, {message}')


# feeding data to cvs file.. i.e using cvs file as data base
def write_to_csv(data):
    with open('database.csv', mode='a', newline='') as database2:
        email = data["email"]
        subject = data["subject"]
        message = data["message"]
        csv_writer = csv.writer(database2, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([email, subject, message])


# to submit a form from web page
@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
    # When user submits the form, we can grab the data using below code
    if request.method == 'POST':
        try:
            webdata = request.form.to_dict()
            write_to_csv(webdata)
            # {'email': 'sridhar6261@gmail.com', 'subject': 'Hi', 'message': 'hello'}
            requests.post("https://ntfy.sh/sri_alerts_rvsk",
                          data=r"MAIL from %s with SUBJECT %s ;CONTENT: %s" % (
                              webdata['email'], webdata['subject'], webdata['message']),
                          headers={
                              "Title": "new contact request from %s" % webdata['email'],
                              "Tags": "loudspeaker"
                          })
            print(webdata)
            return redirect('/thankyou.html')
        except Exception as err:
            return "did not return to database", err
    else:
        return "something went wrong, try again!"
