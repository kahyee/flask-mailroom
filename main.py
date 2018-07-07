import os
import base64

from flask import Flask, render_template, request, redirect, url_for, session

from model import Donation, db, Donor


app = Flask(__name__)
app.secret_key = b'\x9d\x9a\x0eT\xa8\xc5\x1aN\t\x9d\xc9\xb8}\xe2\xa2\xd6Co\x1f\x84a\x13\xe3x'

@app.route('/')
def home():
    return redirect(url_for('all'))

@app.route('/donations/')
def all():
        
    donations = Donation.select()
    return render_template('donations.jinja2', donations=donations)
    
@app.route('/creation/', methods=['GET', 'POST'])
def creation():
    
    if request.method == 'POST':
        donor_name = request.form['name']
        existing_donor = [donor for donor in Donor if donor_name == donor.name]
        
        #creates new donor if it doesn't exist. probably a better way
        donor_update = ''
        if len(existing_donor) == 1:
            donor_update = existing_donor[0]
        else:
            donor_update = Donor(name=donor_name)
            donor_update.save()
            
        Donation(donor=donor_update, value=request.form['amount']).save()
    
    return render_template('creation.jinja2')
    
@app.route('/Summary/')
def summary():
    
    summary_dict = {}
    donations = Donation.select()
    for donation in donations:
        summary_dict.setdefault(donation.donor.name, 0)
        summary_dict[donation.donor.name] += donation.value
        
    return render_template('summary.jinja2', summary = summary_dict)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6738))
    app.run(debug = True)
    app.run(host='0.0.0.0', port=port)

