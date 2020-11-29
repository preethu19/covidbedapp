from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, IntegerField, SelectField, PasswordField, BooleanField, RadioField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from models import User


class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()], render_kw={"placeholder": "Enter your Name"})
    phone = IntegerField('Phone', validators=[DataRequired()], render_kw={"placeholder": "Enter your Mobile number"})
    content = TextAreaField('Content', validators=[DataRequired()], render_kw={"placeholder": "Enter your message"})
    submit = SubmitField('Contact')


class PatientBedForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()], render_kw={"placeholder": "Enter Name"})
    age = IntegerField('Age', validators=[DataRequired()], render_kw={"placeholder": "Enter Age"})
    gender = SelectField('Gender', choices=[('choose gender', 'Choose Gender'),('male','Male'),('female','Female')])
    status = SelectField('Status', choices=[('choose patient status', 'Choose Patient Status'),('admitted', 'Admitted'),('discharged', 'Discharged')])
    phone = IntegerField('Phone', validators=[DataRequired()], render_kw={"placeholder": "Enter Mobile number"})
    address = StringField('Address', validators=[DataRequired()], render_kw={"placeholder": "Enter Address"})
    blood_group = SelectField('Blood Group', choices=[('choose blood group', 'Choose Blood Group'),('a +ve', 'A +ve'),('a -ve','A -ve'), ('b +ve', 'B +ve'), ('b -ve', 'B -ve'), ('ab +ve', 'AB +ve'), ('ab -vr', 'AB -vr'), ('o +ve', 'O +ve'), ('o -ve', 'O -ve')])
    bed_number = IntegerField('Bed Number', validators=[DataRequired()], render_kw={"placeholder": "Enter Bed Number"})
    bed_type = SelectField('Blood Group', choices=[('choose bed type','Choose Bed Type'),('ward', 'Ward'),('ward with oxygen', 'Ward with oxygen'),('icu', 'ICU'),('icu with oxygen', 'ICU with oxygen')])
    cost = IntegerField('Cost', validators=[DataRequired()], render_kw={"placeholder": "Enter Cost"})
    doctor_name = StringField('Name', validators=[DataRequired()], render_kw={"placeholder": "Enter Name"})
    submit = SubmitField('Submit')

class LoginForm(FlaskForm):
    name = StringField('User Name', validators=[DataRequired()], render_kw={"placeholder": "Enter Name"})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "Enter Password"})
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')], render_kw={"placeholder": "Re-Enter Password"})
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    name = StringField('User Name', validators=[DataRequired()], render_kw={"placeholder": "Enter User Name"})
    role = SelectField('Role', validators=[DataRequired()],choices=[('choose role', 'Choose Role'),('admin', 'Admin'),('hospital','Hospital')])
    gender = SelectField('Gender', choices=[('choose gender', 'Choose Gender'),('male','Male'),('female','Female'),('non-binary','Non-Binary')])
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "Enter Password"})
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')], render_kw={"placeholder": "Re-Enter Password"})
    age = IntegerField('Age', validators=[DataRequired()], render_kw={"placeholder": "Enter Age"})
    phone = IntegerField('Phone', validators=[DataRequired()], render_kw={"placeholder": "Enter Mobile number"})
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={'placeholder':'Email'})
    address = StringField('Address', validators=[DataRequired()], render_kw={"placeholder": "Enter Address"})
    submit = SubmitField('Register')

    def validate_name(self, name):
        user = User.query.filter_by(name=name.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

    def validate_phone(self, phone):
        if not 5000000000 < phone.data < 9999999999:
            raise ValidationError('Enter valid phone')

class InfoForm(FlaskForm):
    name = SelectField('Name', choices=[('Please Select','Please Select'),('Preetham emergency','Preetham emergency'),('Nandan clinic','Nandan clinic'),('Siddarth multispeciality','Siddarth multispeciality'),('Father Muller Hospital','Father Muller Hospital')])
    district = SelectField('District: ', choices=[('Please Select','Please Select'),('D.K','D.K'),('Banglore','Banglore')])
    state = SelectField('State: ', choices=[('Please Select','Please Select'),('Andra','Andra'),('Karnataka','Karnataka')])
    area = SelectField('Area: ', choices=[('Please Select','Please Select'),('badyar','badyar'),('mattikere','mattikere')])
    beds = SelectField('Sort bed results by ', validators=[DataRequired()], choices=[('total_beds','total_beds'),('available_beds','available_beds'),('available_ward_beds','available_ward_beds'),('available_ward_beds_with_oxygen','available_ward_beds_with_oxygen'),('available_icu_beds','available_icu_beds'),('available_icu_beds_with_oxygen','available_icu_beds_with_oxygen')], default='total_beds')
    submit = SubmitField('Search')

class addhospitalform(FlaskForm):
    hospitalname = StringField('Hospital Name', validators=[DataRequired()])
    area = StringField('area', validators=[DataRequired()])
    district = StringField('district', validators=[DataRequired()])
    state = StringField('state', validators=[DataRequired()])
    phone = StringField('phone', validators=[DataRequired()])
    user = StringField('User Name', validators=[DataRequired()], render_kw={"placeholder": "Enter User Name"})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "Enter Password"})
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')], render_kw={"placeholder": "Re-Enter Password"})
    total_beds = IntegerField('total_beds', validators=[DataRequired()])
    total_ward_beds = IntegerField('total_ward_beds', validators=[DataRequired()])
    total_ward_beds_with_oxygen = IntegerField('total_ward_beds_with_oxygen', validators=[DataRequired()])
    total_icu_beds = IntegerField('total_icu_beds', validators=[DataRequired()])
    total_icu_beds_with_oxygen = IntegerField('total_icu_beds_with_oxygen', validators=[DataRequired()])
    submit = SubmitField('Enter')    

    def validate_user(self, user):
        user = User.query.filter_by(name=user.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

    def validate_phone(self, phone):
        if not 5000000000 < int(phone.data) < 9999999999:
            raise ValidationError('Enter valid phone')

class DoctorForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()], render_kw={"placeholder": "Enter Name"})
    age = IntegerField('Age', validators=[DataRequired()], render_kw={"placeholder": "Enter Age"})
    gender = SelectField('Gender', choices=[('choose gender', 'Choose Gender'),('male','Male'),('female','Female')])
    submit = SubmitField('Submit')
  
class edithospitalform(FlaskForm):
    total_beds = IntegerField('total_beds', validators=[DataRequired()])
    total_ward_beds = IntegerField('total_ward_beds', validators=[DataRequired()])
    total_ward_beds_with_oxygen = IntegerField('total_ward_beds_with_oxygen', validators=[DataRequired()])
    total_icu_beds = IntegerField('total_icu_beds', validators=[DataRequired()])
    total_icu_beds_with_oxygen = IntegerField('total_icu_beds_with_oxygen', validators=[DataRequired()])
    submit = SubmitField('Enter') 



