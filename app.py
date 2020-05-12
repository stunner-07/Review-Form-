from flask import Flask, render_template, request, flash, redirect, url_for
from flask_wtf import Form
from wtforms import TextField, TextAreaField, SubmitField, RadioField, validators, ValidationError, StringField
import csv


app = Flask(__name__)
app.secret_key = 'key'


class ReviewForm(Form):
   name = TextField("Name", [
                    validators.Required("Please enter your name.")])
   productName = TextField(
       "Name of the Product", [validators.Required("Please enter the Product  Name.")])
   review = TextAreaField("Your Review", [validators.Required("Please enter your review .")])
   submit = SubmitField("Submit")


@app.route('/', methods=['GET', 'POST'])
def home():
  with open('reviews.csv', mode='r') as csv_file:
    data = csv.reader(csv_file, delimiter=',')
    first_line = True
    reviews = []
    for row in data:
      if not first_line:
        reviews.append({
         "Name": row[0],
         "Product": row[1],
         "Review": row[2],
      })
      else:
        first_line = False

  form = ReviewForm()

  if request.method == 'POST':
    if form.validate() == False:
      flash('All fields are required.')
      return render_template('index.html', form=form, reviews=reviews)
    else:
      userdata = dict(request.form)
      name = userdata["name"]
      product = userdata["productName"]
      review = userdata["review"]
      row = [(name, product, review)]
      csvfile = open('reviews.csv', 'a', newline='\n' )
      obj = csv.writer(csvfile)
      obj.writerows(row)
      return redirect(url_for('home'))
  elif request.method == 'GET':
    return render_template('index.html', form = form, reviews=reviews)

if __name__ == '__main__':
    app.run(debug=True)
