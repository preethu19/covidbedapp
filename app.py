from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime
import os
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'mysecret'

login = LoginManager(app)
login.login_view = 'login'

from models import db
from forms import ContactForm, PatientBedForm, LoginForm, RegistrationForm, InfoForm, addhospitalform, DoctorForm
from models import Contact, Hospital, Patient, Bed, User, Doctor

@app.route('/', methods=['GET','POST'])
def home():
    form = ContactForm()
    if request.method == 'POST' and form.validate_on_submit():
        name = form.name.data
        phone = form.phone.data
        content = form.content.data
        c = Contact(name, phone, content)
        db.session.add(c)
        db.session.commit()
        return redirect(url_for('home'))
    else:
        print('Home loaded')
        return render_template('home.html', form=form)

@app.route('/hospital', methods=['GET','POST'])
def hospital():
    name=False
    district=False
    state=False
    area=False
    beds= False
    form = InfoForm() 
    page = request.args.get('page', 1, type=int)
    print('page: ', page)
    
    if request.method == 'POST':
        name = form.name.data
        district = form.district.data
        state = form.state.data
        area = form.area.data
        beds = form.beds.data
        page = 1
        print(name)
        print(district)
    
    if request.method == 'GET':
        name = request.args.get('name')
        state = request.args.get('state')
        district = request.args.get('district')
        area = request.args.get('area')
        beds = request.args.get('beds')
    # data = Hospital.query.order_by(Hospital.total_beds.desc()).paginate(per_page=5, page=page) 
    if form.validate_on_submit() and request.method == "POST":
        print('POST request')
        
        
        #print(request.form['name'])
        # print(form.name.data)
        
    data = Hospital.query.order_by(Hospital.total_beds.desc()).paginate(per_page=5, page=page)
    # if request.method == "POST":
        
        #print(request.form['name'])
        # if name =='Please Select':
        #     name_avail = False
        # if district =='Please Select':
        #     district_avail = False
        # if state =='Please Select':
        #     state_avail = False
        # if area =='Please Select':
        #     area_avail = False
        
    if(name =='Please Select' and district =='Please Select' and state =='Please Select' and area =='Please Select'):
        if beds == 'total_beds':
            data = Hospital.query.order_by(Hospital.total_beds.desc()).paginate(per_page=5, page=page)        
        elif beds== 'available_beds':
            data = Hospital.query.order_by(Hospital.available_beds.desc()).paginate(per_page=5, page=page)
        elif beds == 'available_ward_beds':
            data = Hospital.query.order_by(Hospital.available_ward_beds.desc()).paginate(per_page=5, page=page)        
        elif beds == 'available_ward_beds_with_oxygen':
            data = Hospital.query.order_by(Hospital.available_ward_beds_with_oxygen.desc()).paginate(per_page=5, page=page)
        elif beds == 'available_icu_beds':
            data = Hospital.query.order_by(Hospital.available_icu_beds.desc()).paginate(per_page=5, page=page)
        elif beds == 'available_icu_beds_with_oxygen':
            data = Hospital.query.order_by(Hospital.available_icu_beds_with_oxygen.desc()).paginate(per_page=5, page=page)

    elif(name !=  'Please Select' and district =='Please Select' and state =='Please Select' and area =='Please Select'):
        if beds == 'total_beds':
            data = Hospital.query.filter_by(name=name).order_by(Hospital.total_beds.desc()).paginate(per_page=5, page=page)
        elif beds== 'available_beds':
            data = Hospital.query.filter_by(name=name).order_by(Hospital.available_beds).paginate(per_page=5, page=page)
        elif beds == 'available_ward_beds':
            data = Hospital.query.filter_by(name=name).order_by(Hospital.available_ward_beds.desc()).paginate(per_page=5, page=page)        
        elif beds == 'available_ward_beds_with_oxygen':
            data = Hospital.query.filter_by(name=name).order_by(Hospital.available_ward_beds_with_oxygen.desc()).paginate(per_page=5, page=page)
        elif beds == 'available_icu_beds':
            data = Hospital.query.filter_by(name=name).order_by(Hospital.available_icu_beds.desc()).paginate(per_page=5, page=page)
        elif beds == 'available_icu_beds_with_oxygen':
            data = Hospital.query.filter_by(name=name).order_by(Hospital.available_icu_beds_with_oxygen.desc()).paginate(per_page=5, page=page)

    elif(name ==  'Please Select' and district !='Please Select' and state =='Please Select' and area =='Please Select'):
        if beds == 'total_beds':
            data = Hospital.query.filter_by(district=district).order_by(Hospital.total_beds.desc()).paginate(per_page=5, page=page)
        elif beds== 'available_beds':
            data = Hospital.query.filter_by(district=district).order_by(Hospital.available_beds).paginate(per_page=5, page=page)
        elif beds == 'available_ward_beds':
            data = Hospital.query.filter_by(district=district).order_by(Hospital.available_ward_beds.desc()).paginate(per_page=5, page=page)        
        elif beds == 'available_ward_beds_with_oxygen':
            data = Hospital.query.filter_by(district=district).order_by(Hospital.available_ward_beds_with_oxygen.desc()).paginate(per_page=5, page=page)
        elif beds == 'available_icu_beds':
            data = Hospital.query.filter_by(district=district).order_by(Hospital.available_icu_beds.desc()).paginate(per_page=5, page=page)
        elif beds == 'available_icu_beds_with_oxygen':
            data = Hospital.query.filter_by(district=district).order_by(Hospital.available_icu_beds_with_oxygen.desc()).paginate(per_page=5, page=page)

    elif(name ==  'Please Select' and district =='Please Select' and state !='Please Select' and area =='Please Select'):
        if beds == 'total_beds':
            data = Hospital.query.filter_by(state=state).order_by(Hospital.total_beds.desc()).paginate(per_page=5, page=page)
        elif beds== 'available_beds':
            data = Hospital.query.filter_by(state=state).order_by(Hospital.available_beds).paginate(per_page=5, page=page)
        elif beds == 'available_ward_beds':
            data = Hospital.query.filter_by(state=state).order_by(Hospital.available_ward_beds.desc()).paginate(per_page=5, page=page)        
        elif beds == 'available_ward_beds_with_oxygen':
            data = Hospital.query.filter_by(state=state).order_by(Hospital.available_ward_beds_with_oxygen.desc()).paginate(per_page=5, page=page)
        elif beds == 'available_icu_beds':
            data = Hospital.query.filter_by(state=state).order_by(Hospital.available_icu_beds.desc()).paginate(per_page=5, page=page)
        elif beds == 'available_icu_beds_with_oxygen':
            data = Hospital.query.filter_by(state=state).order_by(Hospital.available_icu_beds_with_oxygen.desc()).paginate(per_page=5, page=page)
    
    elif(name ==  'Please Select' and district =='Please Select' and state =='Please Select' and area !='Please Select'):
        if beds == 'total_beds':
            data = Hospital.query.filter_by(area=area).order_by(Hospital.total_beds.desc()).paginate(per_page=5, page=page)
        elif beds== 'available_beds':
            data = Hospital.query.filter_by(area=area).order_by(Hospital.available_beds).paginate(per_page=5, page=page)
        elif beds == 'available_ward_beds':
            data = Hospital.query.filter_by(area=area).order_by(Hospital.available_ward_beds.desc()).paginate(per_page=5, page=page)        
        elif beds == 'available_ward_beds_with_oxygen':
            data = Hospital.query.filter_by(area=area).order_by(Hospital.available_ward_beds_with_oxygen.desc()).paginate(per_page=5, page=page)
        elif beds == 'available_icu_beds':
            data = Hospital.query.filter_by(area=area).order_by(Hospital.available_icu_beds.desc()).paginate(per_page=5, page=page)
        elif beds == 'available_icu_beds_with_oxygen':
            data = Hospital.query.filter_by(area=area).order_by(Hospital.available_icu_beds_with_oxygen.desc()).paginate(per_page=5, page=page)
    
    elif(name !=  'Please Select' and district !='Please Select' and state =='Please Select' and area =='Please Select'):
        if beds == 'total_beds':
            data = Hospital.query.filter_by(name=name, district=district).order_by(Hospital.total_beds.desc()).paginate(per_page=5, page=page)
        elif beds== 'available_beds':
            data = Hospital.query.filter_by(name=name, district=district).order_by(Hospital.available_beds).paginate(per_page=5, page=page)
        elif beds == 'available_ward_beds':
            data = Hospital.query.filter_by(name=name, district=district).order_by(Hospital.available_ward_beds.desc()).paginate(per_page=5, page=page)        
        elif beds == 'available_ward_beds_with_oxygen':
            data = Hospital.query.filter_by(name=name, district=district).order_by(Hospital.available_ward_beds_with_oxygen.desc()).paginate(per_page=5, page=page)
        elif beds == 'available_icu_beds':
            data = Hospital.query.filter_by(name=name, district=district).order_by(Hospital.available_icu_beds.desc()).paginate(per_page=5, page=page)
        elif beds == 'available_icu_beds_with_oxygen':
            data = Hospital.query.filter_by(name=name, district=district).order_by(Hospital.available_icu_beds_with_oxygen.desc()).paginate(per_page=5, page=page)

    elif(name !=  'Please Select' and district =='Please Select' and state !='Please Select' and area =='Please Select'):
        if beds == 'total_beds':
            data = Hospital.query.filter_by(name=name, state=state).order_by(Hospital.total_beds.desc()).paginate(per_page=5, page=page)
        elif beds== 'available_beds':
            data = Hospital.query.filter_by(name=name, state=state).order_by(Hospital.available_beds).paginate(per_page=5, page=page)
        elif beds == 'available_ward_beds':
            data = Hospital.query.filter_by(name=name, state=state).order_by(Hospital.available_ward_beds.desc()).paginate(per_page=5, page=page)        
        elif beds == 'available_ward_beds_with_oxygen':
            data = Hospital.query.filter_by(name=name, state=state).order_by(Hospital.available_ward_beds_with_oxygen.desc()).paginate(per_page=5, page=page)
        elif beds == 'available_icu_beds':
            data = Hospital.query.filter_by(name=name, state=state).order_by(Hospital.available_icu_beds.desc()).paginate(per_page=5, page=page)
        elif beds == 'available_icu_beds_with_oxygen':
            data = Hospital.query.filter_by(name=name, state=state).order_by(Hospital.available_icu_beds_with_oxygen.desc()).paginate(per_page=5, page=page)

    elif(name !=  'Please Select' and district =='Please Select' and state =='Please Select' and area !='Please Select'):
        if beds == 'total_beds':
            data = Hospital.query.filter_by(name=name, area=area).order_by(Hospital.total_beds.desc()).paginate(per_page=5, page=page)
        elif beds== 'available_beds':
            data = Hospital.query.filter_by(name=name, area=area).order_by(Hospital.available_beds).paginate(per_page=5, page=page)
        elif beds == 'available_ward_beds':
            data = Hospital.query.filter_by(name=name, area=area).order_by(Hospital.available_ward_beds.desc()).paginate(per_page=5, page=page)        
        elif beds == 'available_ward_beds_with_oxygen':
            data = Hospital.query.filter_by(name=name, area=area).order_by(Hospital.available_ward_beds_with_oxygen.desc()).paginate(per_page=5, page=page)
        elif beds == 'available_icu_beds':
            data = Hospital.query.filter_by(name=name, area=area).order_by(Hospital.available_icu_beds.desc()).paginate(per_page=5, page=page)
        elif beds == 'available_icu_beds_with_oxygen':
            data = Hospital.query.filter_by(name=name, area=area).order_by(Hospital.available_icu_beds_with_oxygen.desc()).paginate(per_page=5, page=page)

    elif(name ==  'Please Select' and district !='Please Select' and state !='Please Select' and area =='Please Select'):
        if beds == 'total_beds':
            data = Hospital.query.filter_by(district=district, state=state).order_by(Hospital.total_beds.desc()).paginate(per_page=5, page=page)
        elif beds== 'available_beds':
            data = Hospital.query.filter_by(district=district, state=state).order_by(Hospital.available_beds).paginate(per_page=5, page=page)
        elif beds == 'available_ward_beds':
            data = Hospital.query.filter_by(district=district, state=state).order_by(Hospital.available_ward_beds.desc()).paginate(per_page=5, page=page)        
        elif beds == 'available_ward_beds_with_oxygen':
            data = Hospital.query.filter_by(district=district, state=state).order_by(Hospital.available_ward_beds_with_oxygen.desc()).paginate(per_page=5, page=page)
        elif beds == 'available_icu_beds':
            data = Hospital.query.filter_by(district=district, state=state).order_by(Hospital.available_icu_beds.desc()).paginate(per_page=5, page=page)
        elif beds == 'available_icu_beds_with_oxygen':
            data = Hospital.query.filter_by(district=district, state=state).order_by(Hospital.available_icu_beds_with_oxygen.desc()).paginate(per_page=5, page=page)

    elif(name ==  'Please Select' and district !='Please Select' and state =='Please Select' and area !='Please Select'):
        if beds == 'total_beds':
            data = Hospital.query.filter_by(district=district, area=area).order_by(Hospital.total_beds.desc()).paginate(per_page=5, page=page)
        elif beds== 'available_beds':
            data = Hospital.query.filter_by(district=district, area=area).order_by(Hospital.available_beds).paginate(per_page=5, page=page)
        elif beds == 'available_ward_beds':
            data = Hospital.query.filter_by(district=district, area=area).order_by(Hospital.available_ward_beds.desc()).paginate(per_page=5, page=page)        
        elif beds == 'available_ward_beds_with_oxygen':
            data = Hospital.query.filter_by(district=district, area=area).order_by(Hospital.available_ward_beds_with_oxygen.desc()).paginate(per_page=5, page=page)
        elif beds == 'available_icu_beds':
            data = Hospital.query.filter_by(district=district, area=area).order_by(Hospital.available_icu_beds.desc()).paginate(per_page=5, page=page)
        elif beds == 'available_icu_beds_with_oxygen':
            data = Hospital.query.filter_by(district=district, area=area).order_by(Hospital.available_icu_beds_with_oxygen.desc()).paginate(per_page=5, page=page)

    elif(name ==  'Please Select' and district =='Please Select' and state !='Please Select' and area !='Please Select'):
        if beds == 'total_beds':
            data = Hospital.query.filter_by(state=state, area=area).order_by(Hospital.total_beds.desc()).paginate(per_page=5, page=page)
        elif beds== 'available_beds':
            data = Hospital.query.filter_by(state=state, area=area).order_by(Hospital.available_beds).paginate(per_page=5, page=page)
        elif beds == 'available_ward_beds':
            data = Hospital.query.filter_by(state=state, area=area).order_by(Hospital.available_ward_beds.desc()).paginate(per_page=5, page=page)        
        elif beds == 'available_ward_beds_with_oxygen':
            data = Hospital.query.filter_by(state=state, area=area).order_by(Hospital.available_ward_beds_with_oxygen.desc()).paginate(per_page=5, page=page)
        elif beds == 'available_icu_beds':
            data = Hospital.query.filter_by(state=state, area=area).order_by(Hospital.available_icu_beds.desc()).paginate(per_page=5, page=page)
        elif beds == 'available_icu_beds_with_oxygen':
            data = Hospital.query.filter_by(state=state, area=area).order_by(Hospital.available_icu_beds_with_oxygen.desc()).paginate(per_page=5, page=page)


    elif(name !=  'Please Select' and district !='Please Select' and state !='Please Select' and area =='Please Select'):
        if beds == 'total_beds':
            data = Hospital.query.filter_by(name=name, district=district, state=state).order_by(Hospital.total_beds.desc()).paginate(per_page=5, page=page)
        elif beds== 'available_beds':
            data = Hospital.query.filter_by(name=name, district=district, state=state).order_by(Hospital.available_beds).paginate(per_page=5, page=page)
        elif beds == 'available_ward_beds':
            data = Hospital.query.filter_by(name=name, district=district, state=state).order_by(Hospital.available_ward_beds.desc()).paginate(per_page=5, page=page)        
        elif beds == 'available_ward_beds_with_oxygen':
            data = Hospital.query.filter_by(name=name, district=district, state=state).order_by(Hospital.available_ward_beds_with_oxygen.desc()).paginate(per_page=5, page=page)
        elif beds == 'available_icu_beds':
            data = Hospital.query.filter_by(name=name, district=district, state=state).order_by(Hospital.available_icu_beds.desc()).paginate(per_page=5, page=page)
        elif beds == 'available_icu_beds_with_oxygen':
            data = Hospital.query.filter_by(name=name, district=district, state=state).order_by(Hospital.available_icu_beds_with_oxygen.desc()).paginate(per_page=5, page=page)

    elif(name !=  'Please Select' and district !='Please Select' and state =='Please Select' and area !='Please Select'):
        if beds == 'total_beds':
            data = Hospital.query.filter_by(name=name, district=district, area=area).order_by(Hospital.total_beds.desc()).paginate(per_page=5, page=page)
        elif beds== 'available_beds':
            data = Hospital.query.filter_by(name=name, district=district, area=area).order_by(Hospital.available_beds).paginate(per_page=5, page=page)
        elif beds == 'available_ward_beds':
            data = Hospital.query.filter_by(name=name, district=district, area=area).order_by(Hospital.available_ward_beds.desc()).paginate(per_page=5, page=page)        
        elif beds == 'available_ward_beds_with_oxygen':
            data = Hospital.query.filter_by(name=name, district=district, area=area).order_by(Hospital.available_ward_beds_with_oxygen.desc()).paginate(per_page=5, page=page)
        elif beds == 'available_icu_beds':
            data = Hospital.query.filter_by(name=name, district=district, area=area).order_by(Hospital.available_icu_beds.desc()).paginate(per_page=5, page=page)
        elif beds == 'available_icu_beds_with_oxygen':
            data = Hospital.query.filter_by(name=name, district=district, area=area).order_by(Hospital.available_icu_beds_with_oxygen.desc()).paginate(per_page=5, page=page)


    elif(name !=  'Please Select' and district =='Please Select' and state !='Please Select' and area !='Please Select'):
        if beds == 'total_beds':
            data = Hospital.query.filter_by(name=name, state=state, area=area).order_by(Hospital.total_beds.desc()).paginate(per_page=5, page=page)
        elif beds== 'available_beds':
            data = Hospital.query.filter_by(name=name, state=state, area=area).order_by(Hospital.available_beds).paginate(per_page=5, page=page)
        elif beds == 'available_ward_beds':
            data = Hospital.query.filter_by(name=name, state=state, area=area).order_by(Hospital.available_ward_beds.desc()).paginate(per_page=5, page=page)        
        elif beds == 'available_ward_beds_with_oxygen':
            data = Hospital.query.filter_by(name=name, state=state, area=area).order_by(Hospital.available_ward_beds_with_oxygen.desc()).paginate(per_page=5, page=page)
        elif beds == 'available_icu_beds':
            data = Hospital.query.filter_by(name=name, state=state, area=area).order_by(Hospital.available_icu_beds.desc()).paginate(per_page=5, page=page)
        elif beds == 'available_icu_beds_with_oxygen':
            data = Hospital.query.filter_by(name=name, state=state, area=area).order_by(Hospital.available_icu_beds_with_oxygen.desc()).paginate(per_page=5, page=page)

    elif(name ==  'Please Select' and district !='Please Select' and state !='Please Select' and area !='Please Select'):
        if beds == 'total_beds':
            data = Hospital.query.filter_by(district=district, state=state, area=area).order_by(Hospital.total_beds.desc()).paginate(per_page=5, page=page)
        elif beds== 'available_beds':
            data = Hospital.query.filter_by(district=district, state=state, area=area).order_by(Hospital.available_beds).paginate(per_page=5, page=page)
        elif beds == 'available_ward_beds':
            data = Hospital.query.filter_by(district=district, state=state, area=area).order_by(Hospital.available_ward_beds.desc()).paginate(per_page=5, page=page)        
        elif beds == 'available_ward_beds_with_oxygen':
            data = Hospital.query.filter_by(district=district, state=state, area=area).order_by(Hospital.available_ward_beds_with_oxygen.desc()).paginate(per_page=5, page=page)
        elif beds == 'available_icu_beds':
            data = Hospital.query.filter_by(district=district, state=state, area=area).order_by(Hospital.available_icu_beds.desc()).paginate(per_page=5, page=page)
        elif beds == 'available_icu_beds_with_oxygen':
            data = Hospital.query.filter_by(district=district, state=state, area=area).order_by(Hospital.available_icu_beds_with_oxygen.desc()).paginate(per_page=5, page=page)

    elif(name !=  'Please Select' and district !='Please Select' and state !='Please Select' and area !='Please Select'):
        if beds == 'total_beds':
            data = Hospital.query.filter_by(name=name, district=district, state=state, area=area).order_by(Hospital.total_beds.desc()).paginate(per_page=5, page=page)
        elif beds== 'available_beds':
            data = Hospital.query.filter_by(name=name, district=district, state=state, area=area).order_by(Hospital.available_beds).paginate(per_page=5, page=page)
        elif beds == 'available_ward_beds':
            data = Hospital.query.filter_by(name=name, district=district, state=state, area=area).order_by(Hospital.available_ward_beds.desc()).paginate(per_page=5, page=page)        
        elif beds == 'available_ward_beds_with_oxygen':
            data = Hospital.query.filter_by(name=name, district=district, state=state, area=area).order_by(Hospital.available_ward_beds_with_oxygen.desc()).paginate(per_page=5, page=page)
        elif beds == 'available_icu_beds':
            data = Hospital.query.filter_by(name=name, district=district, state=state, area=area).order_by(Hospital.available_icu_beds.desc()).paginate(per_page=5, page=page)
        elif beds == 'available_icu_beds_with_oxygen':
            data = Hospital.query.filter_by(name=name, district=district, state=state, area=area).order_by(Hospital.available_icu_beds_with_oxygen.desc()).paginate(per_page=5, page=page)

    else:
        data = Hospital.query.order_by(Hospital.total_beds.desc()).paginate(per_page=5, page=page)
        print("Get Request")
    form.name.data = name
    form.district.data = district
    form.state.data = state
    form.area.data = area
    form.beds.data = beds
    return render_template('index.html', form=form, name=name, district=district, state=state, area=area, beds=beds, hospitals=data)


@app.route('/hospital/add', methods=['POST', 'GET'])
def addhospital():
    form = addhospitalform()   
    if request.method=='POST' and form.validate_on_submit():
        hospital = Hospital(name=form.hospitalname.data,area=form.area.data,\
                            district=form.district.data, phone=form.phone.data, total_beds=form.total_beds.data,\
                            state=form.state.data,total_ward_beds=form.total_ward_beds.data,\
                            total_ward_beds_with_oxygen=form.total_ward_beds_with_oxygen.data,total_icu_beds=form.total_icu_beds.data,\
                            total_icu_beds_with_oxygen=form.total_icu_beds_with_oxygen.data,available_beds=form.total_beds.data,\
                            available_ward_beds=form.total_ward_beds.data,available_ward_beds_with_oxygen=form.total_ward_beds_with_oxygen.data,\
                            available_icu_beds=form.total_icu_beds.data,available_icu_beds_with_oxygen=form.total_icu_beds_with_oxygen.data)
        db.session.add(hospital)
        user = User(name=form.user.data, role='hospital', hospital=hospital)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('hospital'))
    for error in form.errors:
        print(error)
        if error == 'user':
            flash('Use different username', 'danger')
        if error == 'password2':
            flash('Password Mismatch', 'danger')
    return render_template('hospitaladd.html', form=form, title="Add Hospital")

@app.route("/hospital/<int:hospital_id>/edit", methods=['GET', 'POST'])
def edithospital(hospital_id):

    if current_user.role != 'admin':
        flash('Unauthorised', 'danger')
        return redirect(url_for('hospital'))

    hospital = Hospital.query.get_or_404(hospital_id)
    form = addhospitalform()
    if request.method=='POST' and form.validate_on_submit():
        if hospital.total_beds <= form.total_beds.data and hospital.total_ward_beds <= form.total_ward_beds.data and\
        hospital.total_ward_beds_with_oxygen <= form.total_ward_beds_with_oxygen.data and hospital.total_icu_beds <= form.total_icu_beds.data and\
        hospital.total_icu_beds_with_oxygen <= form.total_icu_beds_with_oxygen.data:                                                                    
            db.session.query(Hospital).filter_by(id=hospital_id).update({Hospital.total_beds: form.total_beds.data, Hospital.total_ward_beds: form.total_ward_beds.data,\
                                                                  Hospital.total_ward_beds_with_oxygen: form.total_ward_beds_with_oxygen.data, Hospital.total_icu_beds: form.total_icu_beds.data,\
                                                                  Hospital.total_icu_beds_with_oxygen:form.total_icu_beds_with_oxygen.data}, synchronize_session = False) 
            db.session.commit()
            return redirect(url_for('hospital')) 
        else:
            return redirect(url_for('home'))
    else:
        form.hospitalname.data = hospital.name
        form.area.data = hospital.area
        form.district.data = hospital.district
        form.state.data = hospital.state
        form.phone.data = hospital.phone
        form.total_beds.data = hospital.total_beds
        form.total_ward_beds.data = hospital.total_ward_beds
        form.total_ward_beds_with_oxygen.data = hospital.total_ward_beds_with_oxygen
        form.total_icu_beds.data = hospital.total_icu_beds
        form.total_icu_beds_with_oxygen.data = hospital.total_icu_beds_with_oxygen
    return render_template('hospitaledit.html',hospital=hospital, form=form, title="Edit Hospital")

@app.route('/doctors/new', methods=['GET', 'POST'])
@login_required
def doctor_add():
    form = DoctorForm()
    if request.method == 'POST' and form.validate_on_submit():
        doctor = Doctor(name=form.name.data, age=form.age.data, gender=form.gender.data, hospital=current_user.hospital)
        db.session.add(doctor)
        db.session.commit()
        return redirect('home')
    return render_template('doctor_add.html', form=form)


@app.route('/profile')
@login_required
def profile():
    return redirect(url_for('home'))

@app.route('/patients')
@login_required
def patient_list():
    hospital = current_user.hospital
    page = request.args.get('page', 1, type=int)
    patients = Patient.query.join(Bed).filter(Bed.id==Patient.bed_id).join(Hospital).filter(Bed.hospital_id==Hospital.id, Hospital.id==hospital.id).order_by(Patient.admit_date.desc()).paginate(per_page=1, page=page)
    return render_template('patient.html', patients=patients, hospital=hospital)


@app.route('/patients/new',  methods=['GET','POST'])
@login_required
def patient_add():
    form = PatientBedForm()
    if request.method == 'POST' and form.validate_on_submit() and form.gender.data != 'choose gender' and\
            form.status.data != 'choose patient status' and form.blood_group.data != 'choose blood group'\
            and form.bed_type.data != 'choose bed type':
        h = current_user.hospital
        if form.bed_type.data=='ward':
            if h.available_ward_beds<=h.total_ward_beds:
                h.available_ward_beds -= 1
                h.available_beds -= 1
            else:
                flash('Ward beds are filled', 'danger')
                redirect(url_for('patient_add'))
        elif form.bed_type.data=='ward with oxygen':
            if h.available_ward_beds_with_oxygen<=h.total_ward_beds_with_oxygen:
                h.available_ward_beds_with_oxygen -= 1
                h.available_beds -= 1
            else:
                flash('Ward beds with oxygen are filled', 'danger')
                redirect(url_for('patient_add'))
        elif form.bed_type.data=='icu':
            if h.available_icu_beds<=h.total_icu_beds:
                h.available_icu_beds -= 1
                h.available_beds -= 1
            else:
                flash('ICU beds are filled', 'danger')
                redirect(url_for('patient_add'))
        elif form.bed_type.data=='icu with oxygen':
            if h.available_icu_beds_with_oxygen<=h.total_icu_beds_with_oxygen:
                h.available_icu_beds_with_oxygen -= 1
                h.available_beds -= 1
            else:
                flash('ICU beds with oxygen are filled', 'danger')
                redirect(url_for('patient_add'))
        d = Doctor.query.filter_by(name = form.doctor_name.data, hospital=current_user.hospital).first()
        b = Bed(bed_number=form.bed_number.data, bed_type=form.bed_type.data, cost=form.cost.data, hospital=h)
        db.session.add(b)
        p = Patient(name=form.name.data, age=form.age.data, gender=form.gender.data, status=form.status.data, phone=form.phone.data, address=form.address.data, blood_group=form.blood_group.data, bed=b, doctor=d)
        db.session.add(p)
        db.session.commit()
        print('Commit successful')
        flash('Patient Data is added', 'success')
    elif request.method == 'POST':
        flash('All fields are required', 'danger')
        print('Validation failed')
        print(form.errors)
    return render_template('patient_add.html', form=form)


@app.route('/patients/<int:patient_id>/update', methods=['GET', 'POST'])
@login_required
def patient_update(patient_id):
    form = PatientBedForm()
    h = current_user.hospital
    p = Patient.query.get_or_404(patient_id)
    if request.method == 'POST' and form.validate_on_submit() and form.gender.data != 'choose gender' and \
            form.status.data != 'choose patient status' and form.blood_group.data != 'choose blood group' \
            and form.bed_type.data != 'choose bed type':
        p.name = form.name.data
        p.age = form.age.data
        p.gender = form.gender.data
        p.status = form.status.data
        p.phone = form.phone.data
        p.blood_group = form.blood_group.data
        p.address = form.address.data
        p.doctor = Doctor.query.filter_by(name = form.doctor_name.data, hospital=current_user.hospital).first_or_404()
        p.bed.bed_number = form.bed_number.data
        p.bed.bed_type = form.bed_type.data
        p.bed.cost = form.cost.data
        if (not p.discharge_date) and form.status.data == 'discharged':
            p.discharge_date = datetime.utcnow()
            if form.bed_type.data=='ward':
                h.available_ward_beds += 1
                h.available_beds += 1
            elif form.bed_type.data=='ward with oxygen':
                h.available_ward_beds_with_oxygen += 1
                h.available_beds += 1
            elif form.bed_type.data=='icu':
                h.available_icu_beds += 1
                h.available_beds += 1
            elif form.bed_type.data=='icu with oxygen':
                h.available_icu_beds_with_oxygen += 1
                h.available_beds += 1
        db.session.commit()
        flash('Patient Data is updated', 'success')
    elif request.method == 'POST':
        flash('All fields are required', 'danger')
    form.name.data = p.name
    form.age.data = p.age
    form.gender.data = p.gender
    form.status.data = p.status
    form.phone.data = p.phone
    form.blood_group.data = p.blood_group
    form.address.data = p.address
    form.bed_number.data = p.bed.bed_number
    form.bed_type.data = p.bed.bed_type
    form.cost.data = p.bed.cost
    form.doctor_name.data = p.doctor.name
    admit_date = p.admit_date
    discharge_date = p.discharge_date
    return render_template('patient_update.html', form=form, admit_date=admit_date, discharge_date=discharge_date)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash('You are already logged in', 'success')
        return redirect(url_for('home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(name = form.name.data).first()
        print(user)
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password','danger')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('home')
        flash('Logged In Successfully', 'success')
        return redirect(next_page)
        
    return render_template('login.html', title='Log In', form=form)

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    flash('Logged Out Successfully', 'success')
    return redirect(url_for('home'))

@app.route('/register', methods=['GET','POST'])
@login_required
def register():
    if current_user.is_authenticated and current_user.role=='hospital':
        flash('Already Logged In','success')
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(name=form.name.data, role=form.role.data, gender=form.gender.data, age=form.age.data, phone=form.phone.data, email=form.email.data, address=form.address.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Hospital registered successfully.', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


if __name__ == '__main__':
    app.run(debug=True)


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Contact': Contact, 'Hospital': Hospital, 'Patient': Patient, 'Bed': Bed, 'User':User}
