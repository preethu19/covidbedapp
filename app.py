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
from forms import ContactForm, PatientBedForm, LoginForm, RegistrationForm, InfoForm
from models import Contact, Hospital, Patient, Bed, User

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
        contacts = Contact.query.all()
        print(contacts)
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

@app.route('/profile')
@login_required
def profile():
    return redirect(url_for('home'))

@app.route('/patients')
def patient_list():
    hospital = Hospital.query.first()
    page = request.args.get('page', 1, type=int)
    patients = Patient.query.order_by(Patient.admit_date.desc()).paginate(per_page=10, page=page)
    return render_template('patient.html', patients=patients, hospital=hospital)


@app.route('/patients/new',  methods=['GET','POST'])
@login_required
def patient_add():
    form = PatientBedForm()
    if request.method == 'POST' and form.validate_on_submit() and form.gender.data != 'choose gender' and\
            form.status.data != 'choose patient status' and form.blood_group.data != 'choose blood group'\
            and form.bed_type.data != 'choose bed type':
        h = Hospital.query.first()
        b = Bed(bed_number=form.bed_number.data, bed_type=form.bed_type.data, cost=form.cost.data, hospital=h)
        db.session.add(b)
        p = Patient(name=form.name.data, age=form.age.data, gender=form.gender.data, status=form.status.data, phone=form.phone.data, address=form.address.data, blood_group=form.blood_group.data, bed=b)
        db.session.add(p)

        db.session.commit()
        print('Commit successful')
        flash('Patient Data is added', 'success')
    elif request.method == 'POST':
        flash('All fields are required', 'danger')
        print('Validation failed')
        print(form.errors)
    return render_template('patient_add.html', form=form)

@app.route('/patients/<int:patient_id>/update',methods=['GET', 'POST'])
@login_required
def patient_update(patient_id):
    form = PatientBedForm()
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
        p.bed.bed_number = form.bed_number.data
        p.bed.bed_type = form.bed_type.data
        p.bed.cost = form.cost.data
        if (not p.discharge_date) and form.status.data == 'discharged':
            p.discharge_date = datetime.utcnow()
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
def register():
    if current_user.is_authenticated:
        flash('Already Logged In','success')
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(name=form.name.data, role=form.role.data, gender=form.gender.data, age=form.age.data, phone=form.phone.data, email=form.email.data, address=form.address.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('User registered successfully. You may login now', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


if __name__ == '__main__':
    app.run(debug=True)


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Contact': Contact, 'Hospital': Hospital, 'Patient': Patient, 'Bed': Bed, 'User':User}
