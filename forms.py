from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, IntegerField, SelectField
from wtforms.validators import DataRequired


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
    submit = SubmitField('Submit')
