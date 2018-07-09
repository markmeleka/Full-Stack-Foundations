from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from employee_database_setup import Base, Employee, Address

engine = create_engine('sqlite:///employeeData.db')

Base.metadata.bind = engine

DBSession = sessionmaker(bind = engine)

session = DBSession()

newEmployee = Employee(name = "Rebecca Allen")
session.add(newEmployee)
session.commit()

rebeccaAddress = Address(street = "512 Sycamore Road", 
	zip = "02001",
	employee = newEmployee)

session.add(rebeccaAddress)
session.commit()