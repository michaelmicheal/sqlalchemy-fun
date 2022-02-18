from sqlalchemy import Column, Integer, String, ForeignKey, create_engine, ForeignKeyConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref, sessionmaker, joinedload, selectinload

# For this example we will use an in-memory sqlite DB.
# Let's also configure it to echo everything it does to the screen.
engine = create_engine('sqlite:///:memory:', echo=True)

# The base class which our objects will be defined on.
Base = declarative_base()

# Our User object, mapped to the 'users' table
class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)

    name = Column(String)
    fullname = Column(String)
    password = Column(String)

    def __repr__(self):
       return "<User(name='%s', fullname='%s', password'%s')>" % (
                               self.name, self.fullname, self.password)


class Address(Base):
    __tablename__ = 'addresses'
    id = Column(Integer, primary_key=True)
    email_address = Column(String, nullable=False)

    user_id = Column(Integer, nullable=False)

    cars = relationship(
        "Car", back_populates="addresses", cascade='save-update, merge, delete, delete-orphan'
    )


    def __repr__(self):
        return "<Address(email_address='%s')>" % self.email_address

class Car(Base):
    __tablename__ = 'cars'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, primary_key=True)
    address_id = Column(Integer, primary_key=True)


    license_plate = Column(String, nullable=False)

    ForeignKeyConstraint(
            [user_id, address_id],
            ["addresses.user_id", "addresses.id"],
            name='task_instance_dag_run_fkey',
            ondelete="CASCADE",
        )

    users = relationship(
        "User",
        primaryjoin="Car.user_id == User.id",
        foreign_keys=user_id,
        uselist=False,
        innerjoin=True,
        viewonly=True,
    )

    addresses = relationship("Address", back_populates="cars", lazy='joined', innerjoin=True)
    addresses = relationship("Address", back_populates="cars")#, lazy='joined', innerjoin=True)


Base.metadata.create_all(engine) 

Session = sessionmaker(bind=engine)
session = Session()

ed_user = User(name='ed', fullname='Ed Jones', password='edspassword')
ed_user.addresses = [Address(email_address='ed@google.com'), Address(email_address='e25@yahoo.com')]

session.add(ed_user)
session.commit()




test_query = session.query(Car).join(Car.users).join(Car.addresses).all()

print(test_query)