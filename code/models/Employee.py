from config import db


class AuthenticationModel(db.Model):
    __tablename__ = 'authentication'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True)
    password = db.Column(db.String(25), nullable=False)
    role = db.Column(db.String(10), nullable=False)

    personal_details = db.relationship(
        'PersonalDetailsModel', backref='authentication')
    address_details = db.relationship(
        'AddressModel', backref='authentication')

    qualification_details = db.relationship(
        'QualificationModel', backref='authentication')

    emp_sal_details = db.relationship(
        'EmployeeSalaryDetailsModel', backref='authentication')

    joining_details = db.relationship(
        'JoiningDetailsModel', backref='authentication')

    grade_details = db.relationship(
        'GradeModel', backref='authentication')

    def __init__(self, username, password, role):
        self.username = username
        self.password = password
        self.role = role

    def json(self):
        return {
            "username": self.username,
            "role": self.role
        }

    @classmethod
    def find_by_username(cls, username):
        return AuthenticationModel.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, id):
        return AuthenticationModel.query.filter_by(id=id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()


class PersonalDetailsModel(db.Model):
    __tablename__ = 'personaldetails'
    id = db.Column(db.Integer, primary_key=True)
    emp_id = db.Column(db.Integer, db.ForeignKey('authentication.id'))
    firstname = db.Column(db.String(45), nullable=False)
    lastname = db.Column(db.String(45), nullable=False)
    gender = db.Column(db.String(7), nullable=False)
    dob = db.Column(db.String(15), nullable=False)
    bloodgroup = db.Column(db.String(3), nullable=False)
    email = db.Column(db.String(26), nullable=False)
    contactno = db.Column(db.String(16), nullable=False)
    pancardno = db.Column(db.String(16), nullable=False)
    aadharcardno = db.Column(db.String(16), nullable=False)

    def __init__(self, emp_id, fname, lname, gender, dob, bloodgroup, email, contactno, pancardno, aadharcardno):
        self.emp_id = emp_id
        self.firstname = fname
        self.lastname = lname
        self.gender = gender
        self.dob = dob
        self.bloodgroup = bloodgroup
        self.email = email
        self.contactno = contactno
        self.pancardno = pancardno
        self.aadharcardno = aadharcardno

    def json(self):
        return {

            "FirstName": self.firstname,
            "LastName": self.lastname,
            "Gender": self.gender,
            "DateofBirth": self.dob,
            "BloodGroup": self.bloodgroup,
            "Email": self.email,
            "Contact No.": self.contactno,
            "PanCard No.": self.pancardno,
            "AadharCard No.": self.aadharcardno
        }

    @classmethod
    def find_by_id(cls, id):
        return PersonalDetailsModel.query.filter_by(id=id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def update_to_db(self, fname, lname, gender, dob, bloodgroup, email, contactno, pancardno, aadharcardno):
        self.firstname = fname
        self.lastname = lname
        self.gender = gender
        self.dob = dob
        self.bloodgroup = bloodgroup
        self.email = email
        self.contactno = contactno
        self.pancardno = pancardno
        self.aadharcardno = aadharcardno

        db.session.commit()


class AddressModel(db.Model):
    __tablename__ = 'address'
    id = db.Column(db.Integer, primary_key=True)
    emp_id = db.Column(db.Integer, db.ForeignKey('authentication.id'))
    city = db.Column(db.String(16), nullable=False)
    state = db.Column(db.String(16), nullable=False)
    pincode = db.Column(db.String(10), nullable=False)
    fulladdress = db.Column(db.String(80), nullable=False)

    def __init__(self, emp_id, city, state, pincode, fulladdress):
        self.emp_id = emp_id
        self.city = city
        self.state = state
        self.pincode = pincode
        self.fulladdress = fulladdress

    def json(self):
        return {
            "city": self.city,
            "state": self.state,
            "pincode": self.pincode,
            "address": self.fulladdress
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, id):
        return AddressModel.query.filter_by(id=id).first()

    def update_to_db(self, city, state, pincode, fulladdress):
        self.city = city
        self.state = state
        self.pincode = pincode
        self.fulladdress = fulladdress

        db.session.commit()


class QualificationModel(db.Model):
    __tablename__ = 'qualification'
    id = db.Column(db.Integer, primary_key=True)
    emp_id = db.Column(db.Integer, db.ForeignKey('authentication.id'))
    qualification = db.Column(db.String(16), nullable=False)
    pass_year = db.Column(db.Integer, nullable=False)
    work_experience = db.Column(db.Float(precision=1), nullable=False)

    def __init__(self, emp_id, qualification, pass_year, work_experience):
        self.emp_id = emp_id
        self.qualification = qualification
        self.pass_year = pass_year
        self.work_experience = work_experience

    def json(self):
        return {
            "Qualification": self.qualification,
            "Passing Year":  self.pass_year,
            "Work Experience": self.work_experience
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def update_to_db(self, qualification, pass_year, work_experience):
        self.qualification = qualification
        self.pass_year = pass_year
        self.work_experience = work_experience

        db.session.commit()

    @classmethod
    def find_by_id(cls, id):
        return QualificationModel.query.filter_by(id=id).first()


class EmployeeSalaryDetailsModel(db.Model):
    __tablename__ = 'emp_sal_info'
    id = db.Column(db.Integer, primary_key=True)
    emp_id = db.Column(db.Integer, db.ForeignKey('authentication.id'))
    account_no = db.Column(db.String(25), nullable=False)
    ifsc_code = db.Column(db.String(10), nullable=False)
    bankname = db.Column(db.String(30), nullable=False)
    pfaccount_no = db.Column(db.String(30), nullable=False)
    esi_no = db.Column(db.String(30), nullable=False)

    def __init__(self, emp_id, account_no, ifsc_code, bankname, pfaccount_no, esi_no):
        self.emp_id = emp_id
        self.account_no = account_no
        self.ifsc_code = ifsc_code
        self.pfaccount_no = pfaccount_no
        self.bankname = bankname
        self.esi_no = esi_no

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, id):
        return EmployeeSalaryDetailsModel.query.filter_by(id=id).first()

    def json(self):
        return {
            "Account No.": self.account_no,
            "IFSC Code": self.ifsc_code,
            "BankName": self.bankname,
            "ESI No.": self.esi_no
        }

    def update_to_db(self, account_no, ifsc_code, bankname, pfaccount_no, esi_no):
        self.account_no = account_no
        self.ifsc_code = ifsc_code
        self.bankname = bankname
        self.esi_no = esi_no

        db.session.commit()


class GradeModel(db.Model):
    __tablename__ = 'grade'
    id = db.Column(db.Integer, primary_key=True)
    emp_id = db.Column(db.Integer, db.ForeignKey('authentication.id'))
    grade = db.Column(db.String(25), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)

    def __init__(self, emp_id, grade, start_date, end_date):
        self.emp_id = emp_id
        self.grade = grade
        self.start_date = start_date
        self.end_date = end_date

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, id):
        return GradeModel.query.filter_by(id=id).first()


class JoiningDetailsModel(db.Model):
    __tablename__ = 'joiningdetails'
    id = db.Column(db.Integer, primary_key=True)
    emp_id = db.Column(db.Integer, db.ForeignKey('authentication.id'))
    deactivate_by = db.Column(db.Integer, default=None)
    join_date = db.Column(db.DateTime, nullable=False)
    leave_date = db.Column(db.DateTime, default=None)
    status = db.Column(db.Boolean, default=True)

    def __init__(self, emp_id, join_date):
        self.emp_id = emp_id
        self.join_date = join_date

    def json(self):
        return{
            "Join Date": self.join_date
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, id):
        return JoiningDetailsModel.query.filter_by(id=id).first()
