states = {
"Andhra Pradesh": [
	"Srikakulam","Sri Potti Sriramulu Nellore","Visakhapatnam","Vizianagaram","West Godavari"
],
"Arunachal Pradesh":[
	"Anjaw","Changlang","Dibang Valley","East Kameng","East Siang"
],
"Assam": [
	"Baksa","Barpeta","Biswanath","Chirang","Darrang"
],
"Bihar": [
	"Araria", "Arwal","Aurangabad", "Banka", "Begusarai"
],
"Chhattisgarh":[
	"Balod", "Dantewada", "Durg", "Jashpur", "Kanker"
],
"Goa":[
	"North Goa", "South Goa"
],
"Gujarat": [
	"Ahmedabad", "Amreli", "Botad", "Dang", "Gandhinagar"
],
"Haryana": [
	"Ambala", "Bhiwani", "Faridabad", "Gurgaon", "Kurukshetra"
],
"Himachal Pradesh":[
	"Bilaspur", "Chamba", "Hamirpur", "Kangra", "Kullu"
],
"Jammu and Kashmir":[
	"Anantnag", "Badgam", "Bandipora", "Baramulla", "Doda"
],
"Jharkhand":[
	"Bokaro", "Chatra", "Deoghar", "Giridih","Gumla" 
],
"Karnataka":[
	"Bangalore", "Dakshina Kannada", "Belgaum", "Dharwad", "Hassan"
],
"Kerala":[
	"Alappuzha", "Kasaragod", "Kozhikode", "Palakkad", "Wayanad"
],
"Madhya Pradesh":[
	"Ashok Nagar", "Bhopal", "Gwalior", "Indore","	Ujjain"
],
"Maharashtra":[
	"Ahmednagar", "Amravati", "Chandrapur", "Jalgaon", "Mumbai"
],
"Manipur":[
	"Bishnupur", "Imphal", "Noney", "Senapati", "Thoubal" 
],
"Meghalaya":[
	"East Garo Hills", "East Khasi Hills", "North Garo Hills", "South Garo Hills"
],
"Mizoram":[
	"Aizawl", "Champhai", "Khawzawl", "Lawngtlai", "Mamit"
],
"Nagaland":[
	"Dimapur", "Kiphire", "Longleng", "Mon", "Peren"
],
"Odisha":[
	"Angul", "Bhadrak", "Balasore", "Cuttack",  "Gajapati"
],
"Punjab": [
	"Amritsar", "Barnala", "Firozpur", "Fatehgarh Sahib", "Gurdaspur"
],
"Rajasthan":[
	"Ajmer", "Alwar", "Banswara", "Churu", "Chittorgarh"
],
"Sikkim": [
	"East Sikkim", "North Sikkim", "South Sikkim", "West Sikkim"
],
"Tamil Nadu": [
	"Ariyalur", "Chengalpattu", "Chennai", "Coimbatore", "Dindigul"
],
"Telangana": [
	"Adilabad", "Jagtial", "Hyderabad", "Karimnagar", "Nalgonda"
],
"Tripura": [
	"Dhalai", "Gomati", "North Tripura", "South Tripura", "West Tripura"
],
"Uttar Pradesh":[
	"Agra", "Ambedkar Nagar", "Amethi", "Auraiya", "Bareilly"
],
"Uttarakhand": [
	"Almora", "Chamoli", "Haridwar", "Nainital","Uttarkashi" 
],
"West Bengal":[
	"Alipurduar", "Birbhum", "Hooghly", "Howrah"
],
"Andaman and Nicobar Islands": [
	"Nicobar", "North and Middle Andaman","South Andaman" 
],
"Chandigarh":[
	"Chandigarh"
],
"Dadra and Nagar Haveli":[
	"Daman", "Diu", "Dadra and Nagar Haveli"
],
"Lakshadweep":[
	"Lakshadweep"
],
"Delhi":[
	"Central Delhi", "East Delhi", "New Delhi", "South Delhi"
],
"Puducherry":[
	"Karaikal", "Mahé", "Puducherry", "Yanam"
]
}

from faker import Faker
from random import randint
import random
from models import *

def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)

faker = Faker()

Faker.seed(0)


beds = {
		'10000': [2500,3500,2000,2000],
		'20000': [5000,7000,4000,4000],
		'30000': [10000, 5000, 12000, 8000],
		'40000': [15000, 10000, 8000, 7000],
		'50000': [20000, 10000, 15000, 5000]
		}

random_id=0
for i in states:
	for j in states[i]:
		for _ in range(5):
			x = random.choice(['10000','20000','30000','40000','50000'])
			h = Hospital(faker.first_name()+' Hospital',faker.street_name(),j,i,random_with_N_digits(10),int(x),int(x),beds[x][0],beds[x][0],beds[x][1],beds[x][1],beds[x][2],beds[x][2],beds[x][3],beds[x][3])
			db.session.add(h)
			u = User(h.name+str(random_id),'hospital',h)
			u.set_password('test')
			db.session.add(u)
			random_id+=1
			for _ in range(5):
				d = Doctor(faker.name(),randint(30,50),random.choice(['male', 'female']),h)
				db.session.add(d)
				for _ in range(5):
					b = Bed(random.randint(1,10000), random.choice(['ward','ward with oxygen','icu','icu with oxygen']), random.randint(10000, 100000),h)
					db.session.add(b)
					p = Patient(faker.name(),randint(1,100),random.choice(['male', 'female']), 'admitted', random_with_N_digits(10), faker.address(), random.choice(['a +ve','a -ve','b +ve','b -ve','ab +ve','ab -ve','o +ve','o -ve']),b,d)
					db.session.add(p)
	db.session.commit()

for _ in range(100):
	c = Contact(faker.name(),random_with_N_digits(10),faker.sentence(20))
	db.session.add(c)
	db.session.commit()




h = Hospital.query.all()
for i in h:
	b = Bed.query.filter_by(hospital_id=i.id)
	x = b.count()
	i.available_beds -= x
	b = Bed.query.filter_by(hospital_id=i.id,bed_type='ward')
	x = b.count()
	i.available_ward_beds -= x
	b = Bed.query.filter_by(hospital_id=i.id,bed_type='ward with oxygen')
	x = b.count()
	i.available_ward_beds_with_oxygen -= x
	b = Bed.query.filter_by(hospital_id=i.id,bed_type='icu')
	x = b.count()
	i.available_icu_beds -= x
	b = Bed.query.filter_by(hospital_id=i.id,bed_type='icu with oxygen')
	x = b.count()
	i.available_icu_beds_with_oxygen -= x
db.session.commit()
