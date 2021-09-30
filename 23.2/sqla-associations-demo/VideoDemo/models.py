from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def connect_db(app):
    db.app = app
    db.init_app(app)

# MODELS GO BELOW!


class Department(db.Model):
    """Department Model"""

    __tablename__ = "departments"

    dept_code = db.Column(db.Text, primary_key=True)
    dept_name = db.Column(db.Text, nullable=False, unique=True)
    phone = db.Column(db.Text)

    # sets up reference so we can query associated data from the Employee model
    employees = db.relationship('Employee')

    def __repr__(self):
        return f"<Department {self.dept_code} {self.dept_name} {self.phone}>"


class Employee(db.Model):
    """Employee Model"""

    __tablename__ = "employees"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False, unique=True)
    state = db.Column(db.Text, nullable=False, default='CA')
    # db.ForeignKey('reference_table_name.ref_column') sets up foreign key
    dept_code = db.Column(db.Text, db.ForeignKey('departments.dept_code'))
    # sets up reference so we can query associated data from the Department model
    dept = db.relationship('Department')
    # dept = db.relationship('Department', backref='employees') # can refactor the above line and the db.relationship line in the Department class through 'backref'

    def __repr__(self):
        return f"<Employee {self.name} {self.state} {self.dept_code}>"


# def get_directory_join():
#     directory = db.session.query(
#         Employee.name, Department.dept_name, Department.phone).join(Department).all()

#     for name, dept, phone in directory:
#         print(name, dept, phone)


# def get_directory_join_class():
#     directory = db.session.query(Employee, Department).join(Department).all()

#     for emp, dept in directory:
#         print(emp.name, dept.dept_name, dept.phone)


# def get_directory_all_join():
#     directory = db.session.query(
#         Employee.name, Department.dept_name, Department.phone).outerjoin(Department).all()

#     for name, dept, phone in directory:
#         print(name, dept, phone)
