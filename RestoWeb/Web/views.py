from xml.dom import ValidationErr
from flask import render_template,redirect,url_for,flash,request
from Web import app,model,db
from Web.forms import LoginForm,RegisterForm,ItemForm,AddForm
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_required,login_user,logout_user,current_user
cart=dict()
total=0
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/culogin',methods=['POST','GET'])
def culogin():
    form=LoginForm()
    if form.validate_on_submit():
        em=model.User.query.filter_by(email=form.email.data).first()
        if em and em.job=='C':
            if check_password_hash(em.password,form.password.data):
                login_user(em)
                flash(f"You have succesfully logged in as {em.name}")
                return redirect(url_for('home'))
            else:
                flash('You entered Incorrect Password',category='error')
        else:
            flash('The User not found with this Email',category='errorr')
    if form.errors!={}:
        for error in form.errors.values():
            flash(error)
    return render_template('culogin.html',form=form)

@app.route('/cusignup',methods=['POST','GET'])
def cusignup():
    form=RegisterForm()
    if form.validate_on_submit():
        user=model.User(name=form.name.data,
                        email=form.email.data,
                        job='C',
                        password=generate_password_hash(form.password.data,method='sha256'))
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash(f"You have succesfully created account as {user.name}")
        return redirect(url_for('home'))
    if form.errors!={}:
        for error in form.errors.values():
            flash('{error}')
    return render_template('cusignup.html',form=form)

@app.route('/chlogin',methods=['POST','GET'])
def chlogin():
    form=LoginForm()
    if form.validate_on_submit():
        em=model.User.query.filter_by(email=form.email.data).first()
        if em and em.job=='S':
            if check_password_hash(em.password,form.password.data):
                login_user(em)
                flash(f"You have succesfully logged in as {em.name}")
                return redirect(url_for('staff'))
            else:
                flash('You entered Incorrect Password',category='error')
        else:
            flash('The Staff not found with this Email',category='errorr')
    if form.errors!={}:
        for error in form.errors.values():
            flash(error,category='error')
    return render_template('chlogin.html',form=form)


@app.route('/chsignup',methods=['POST','GET'])
def chsignup():
    form=RegisterForm()
    if form.validate_on_submit():
        user=model.User(name=form.name.data,
                        email=form.email.data,
                        job='S',
                        password=generate_password_hash(form.password.data,method='sha256'))
        db.session.add(user)
        db.session.commit()
        flash(f"You have succesfully created account as {user.name}")
        login_user(user)
        return redirect(url_for('staff'))
    if form.errors!={}:
        for error in form.errors.values():
            flash('The Staff cannot be Created bcoz :{error}',category='error')
    return render_template('chsignup.html',form=form)

@app.route('/home')
@login_required
def home():
    items=model.Items.query.all()
    orders=model.Orders.query.filter(model.Orders.user_id==current_user.id)
    pending=[]
    complete=[]
    for i in orders:
        if i.status=='pending':
            pending.append(i)
        else:
            complete.append(i)
    return render_template('home.html',items=items,orders=orders,pending=pending,complete=complete)

@app.route('/staff',methods=['POST','GET'])
@login_required
def staff():
    items=model.Items.query.all()
    form=ItemForm()
    order=model.Orders.query.filter(model.Orders.status=='pending')
    orders=[]
    for i in order:
        orders.append(i)
    return render_template('staff.html',form=form,items=items,orders=orders)

@app.route('/logout')
def logout():
    logout_user()
    flash('Successfully logged out')
    return redirect(url_for('index'))

@app.route('/delete/<id>',methods=["POST","GET"])
def delete(id):
    item=model.Items.query.get(id)
    db.session.delete(item)
    db.session.commit()
    flash("Item deleted")
    return redirect(url_for('staff'))

@app.route('/accept/<id>',methods=["POST","GET"])
def accept(id):
    item=model.Orders.query.get(id)
    item.status='completed'
    db.session.commit()
    flash("Order Accepted")
    return redirect(url_for('staff'))

@app.route('/insert/',methods=['POST','GET'])
def insert():
    try:
        if request.method=='POST':
            item=model.Items(name=request.form['name'],
                         price=request.form['price'])
            db.session.add(item)
            db.session.commit()
            flash("Item added")
    except:
        flash("item already exists")
    return redirect(url_for('staff'))

@app.route('/update/<id>',methods=['POST','GET'])
def update(id):
    item=model.Items.query.get(id)
    item.name=request.form['name']
    item.price=request.form['price']
    db.session.commit()
    return redirect(url_for('staff'))
        

@app.route('/purchase/<id>/<userid>',methods=['POST','GET'])
def purchase(id,userid):
    item=model.Items.query.get(id)
    order=model.Orders(user_id=userid,item_name=item.name,bill=item.price,status='pending')
    db.session.add(order)
    db.session.commit()
    flash('Order placed Successfully')
    return redirect(url_for('home'))