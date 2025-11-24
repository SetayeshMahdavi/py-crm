import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or "a-default-secret-key"
    SQLALCHEMY_DATABASE_URI= 'sqlite:///' + os.path.join(basedir, 'crm.db')
    SQLALCHEMY_TRACK_MODIFICATIONS= False


app=Flask(__name__)
app.config.from_object(Config)
db=SQLAlchemy(app)

class Customer(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    firstname=db.Column(db.String(100),nullable=False)
    lastname=db.Column(db.String(100),nullable=False)
    phone=db.Column(db.String(20))
    email=db.Column(db.String(120),unique=True,nullable=False)
    company=db.Column(db.String(100))

    def __repr__(self):
        return f'<Customer {self.firstname} {self.lastname}>'
    
@app.route('/')
def index():
    customers = Customer.query.all()
    return render_template('customerd.html', customers=customers)


@app.route('/add', methods=['GET', 'POST'])
def add_customer():
    if request.method == 'POST':
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        phone = request.form.get('phone')
        email = request.form.get('email')
        company = request.form.get('company')

        new_customer = Customer(
            firstname=firstname,
            lastname=lastname,
            phone=phone,
            email=email,
            company=company
        )

        try:
            db.session.add(new_customer)
            db.session.commit()
            return redirect(url_for('index'))
        except Exception as e:
            return f"Error adding customer: {e}"

    return render_template('add_customer.html')


@app.route('/update/<int:id>',methods=['GET','POST'])
def update_customer(id):
    customer_to_update=Customer.query.get_or_404(id)
    if request.method == "POST":
        customer_to_update.firstname = request.form['firstname']
        customer_to_update.lastname = request.form['lastname']
        customer_to_update.phone = request.form['phone']
        customer_to_update.email = request.form['email']
        customer_to_update.company = request.form['company']

        try:
            db.session.commit()
            return redirect(url_for('index'))
        except:
            return "خطا در بروز رسانی مشتری"
        
    return render_template ('customer_form.html',customer=customer_to_update)


@app.route('/delete/<int:id>')
def delete_customer(id):
    customer_to_delete=Customer.query.get_or_404(id)
    try:
        db.session.delete(customer_to_delete)
        db.session.commit()
        return redirect(url_for("index"))
    except:
        return "خطا در حذف مشتری "
    

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        
    app.run(debug=True)