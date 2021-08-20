"""Seed file to make sample data for db."""

from models import Department, Employee, Project, EmployeeProject, db
from app import app

# Create all tables
db.drop_all()
db.create_all()

# Make a bunch of departments
# d1 = Department(dept_code="mktg", dept_name="Marketing")
# d2 = Department(dept_code="acct", dept_name="Accounting")
# d3 = Department(dept_code="r&d",
#                 dept_name="Research and Development", phone="908-7878")
# d4 = Department(dept_code="sales", dept_name="Sales", phone="225-6912")
# d5 = Department(
#     dept_code="it", dept_name="Information Technology", phone="888-4562")

# db.session.add_all([d1, d2, d3, d4, d5])

# db.session.commit()

# # Make a bunch of employees

# river = Employee(name="River Bottom", state="NY", dept_code="mktg")
# summer = Employee(name="Summer Winter", state="OR", dept_code="mktg")
# joaquin = Employee(name="Joaquin Phoenix", dept_code="acct")
# octavia = Employee(name="Octavia Spencer", dept_code="r&d")
# larry = Employee(name="Larry David", dept_code="r&d", state="NY")
# kurt = Employee(name="Kurt Cobain", dept_code="it", state="WA")
# rain = Employee(name="Rain Phoenix", dept_code="it")

# db.session.add_all([river, summer, joaquin, octavia, larry, kurt, rain])

# db.session.commit()

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
