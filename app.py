from flask import Flask, render_template, request, redirect, url_for, flash
from forms import ContactForm, PatientBedForm
from models import Contact, db, app, Hospital, Patient, Bed
from datetime import datetime

app.config['SECRET_KEY'] = 'mysecret'




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
        print('Validation error')
    return render_template('home.html', form=form)

@app.route('/profile')
def profile():
    pass

@app.route('/patients')
def patient_list():
    hospital = Hospital.query.first()
    page = request.args.get('page', 1, type=int)
    patients = Patient.query.order_by(Patient.admit_date.desc()).paginate(per_page=10, page=page)
    return render_template('patient.html', patients=patients, hospital=hospital)


@app.route('/patients/new',  methods=['GET','POST'])
def patient_add():
    form = PatientBedForm()
    if request.method == 'POST' and form.validate_on_submit() and form.gender.data != 'choose gender' and\
            form.status.data != 'choose patient status' and form.blood_group.data != 'choose blood group'\
            and form.bed_type.data != 'choose bed type':
        h = Hospital.query.first()
        b = Bed(bed_number=form.bed_number.data, bed_type=form.bed_type.data, cost=form.cost.data, hospital=h)
        db.session.add(b)
        p = Patient(name=form.name.data, age=form.age.data, gender=form.gender.data, status=form.status.data,\
                     phone=form.phone.data, address=form.address.data, blood_group=form.blood_group.data, bed=b)
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


if __name__ == '__main__':
    app.run(debug=True)