"""Sample file demonstrating SQLAlchemy joins & relationships."""

from flask_sqlalchemy import SQLAlchemy

# This is the connection to the database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()


##############################################################################
# Model definitions


class Employee(db.Model):
    """Employee."""

    __tablename__ = "employees"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    name = db.Column(db.Text, nullable=False, unique=True)
    state = db.Column(db.Text, nullable=False, default='CA')
    dept_code = db.Column(
        db.Text,
        db.ForeignKey('departments.dept_code'))

    dept = db.relationship('Department')

    # direct navigation: emp -> employeeproject & back
    assignments = db.relationship('EmployeeProject',
                                  backref='employee')

    # direct navigation: emp -> project & back
    projects = db.relationship('Project',
                               secondary='employees_projects',
                               backref='employees')

    def __repr__(self):
        e = self
        return f"<Employee {e.id} {e.name} {e.state}>"

class Department(db.Model):
    """Department. A department has many employees."""

    __tablename__ = "departments"

    dept_code = db.Column(db.Text, primary_key=True)
    dept_name = db.Column(db.Text,
                          nullable=False,
                          unique=True)
    phone = db.Column(db.Text)

    employees = db.relationship('Employee')

    def __repr__(self):
        return f"<Department {self.dept_code} {self.dept_name}>"


class Project(db.Model):
    """Project. Employees can be assigned to this."""

    __tablename__ = "projects"

    proj_code = db.Column(db.Text, primary_key=True)
    proj_name = db.Column(db.Text,
                          nullable=False,
                          unique=True)

    # direct navigation: proj -> employeeproject & back
    assignments = db.relationship('EmployeeProject',
                                  backref='project')

    def __repr__(self):
        return f"<Project {self.proj_code} {self.proj_name}>"


class EmployeeProject(db.Model):
    """Mapping of an employee to a project."""

    __tablename__ = "employees_projects"

    emp_id = db.Column(db.Integer,
                       db.ForeignKey("employees.id"),
                       primary_key=True)
    proj_code = db.Column(db.Text,
                          db.ForeignKey("projects.proj_code"),
                          primary_key=True)
    role = db.Column(db.Text)


##############################################################################
# Example queries

# This is inefficient, as it makes a query for each department!


def phone_dir_nav():
    """Show phone dir of emps & their depts."""

    emps = Employee.query.all()

    for emp in emps:  # [<Emp>, <Emp>]
        if emp.dept is not None:
            print(emp.name, emp.dept.dept_code, emp.dept.phone)
        else:
            print(emp.name, "-", "-")


def phone_dir_join():
    """Show employees with a join."""

    emps = (db.session.query(Employee.name,
                             Department.dept_name,
                             Department.phone)
            .join(Department).all())

    for name, dept, phone in emps:  # [(n, d, p), (n, d, p)]
        print(name, dept, phone)


def phone_dir_join_class():
    """Show employees with a join.

    This second version doesn't just get a list of data tuples,
    but a list of tuples of classes.
    """

    emps = (db.session.query(Employee, Department)
            .join(Department).all())

    for emp, dept in emps:  # [(<E>, <D>), (<E>, <D>)]
        print(emp.name, dept.dept_name, dept.phone)


def phone_dir_join_outerjoin():
    """Show all employees, even those without a dept."""

    emps = (db.session.query(Employee, Department)
            .outerjoin(Department).all())

    for emp, dept in emps:  # [(<E>, <D>), (<E>, <D>)]
        if dept:
            print(emp.name, dept.dept_name, dept.phone)
        else:
            print(emp.name, "-", "-")


##############################################################################
# Helper functions

def example_data():
    """Create some sample data."""

    # In case this is run more than once, empty out existing data
    EmployeeProject.query.delete()
    Employee.query.delete()
    Department.query.delete()
    Project.query.delete()

    # Add sample employees and departments
    df = Department(dept_code='fin', dept_name='Finance', phone='555-1000')
    dl = Department(dept_code='legal', dept_name='Legal', phone='555-2222')
    dm = Department(dept_code='mktg', dept_name='Marketing', phone='555-9999')

    leonard = Employee(name='Leonard', dept=dl)
    liz = Employee(name='Liz', dept=dl)
    maggie = Employee(name='Maggie', state='DC', dept=dm)
    nadine = Employee(name='Nadine')

    db.session.add_all([df, dl, dm, leonard, liz, maggie, nadine])
    db.session.commit()

    pc = Project(proj_code='car', proj_name='Design Car',
                 assignments=[EmployeeProject(emp_id=liz.id, role='Chair'),
                              EmployeeProject(emp_id=maggie.id)])
    ps = Project(proj_code='server', proj_name='Deploy Server',
                 assignments=[EmployeeProject(emp_id=liz.id),
                              EmployeeProject(emp_id=leonard.id, role='Auditor')])

    db.session.add_all([ps, pc])
    db.session.commit()


def connect_db(app):
    """Connect the database to our Flask app."""

    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    # So that we can use Flask-SQLAlchemy, we'll make a Flask app
    from app import app
    connect_db(app)

    db.drop_all()
    db.create_all()
    example_data()
