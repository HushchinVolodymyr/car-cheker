import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, Date, String, Float, Text, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine("sqlite:///database/main.db", echo=False)

Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()


class Inherit(Base):
    __abstract__ = True

    @classmethod
    def get_table(cls):
        elements = session.query(cls).all()
        return elements

    @classmethod
    def get_element_by_id(cls, id):
        try:
            element = session.query(cls).filter_by(id=id).first()
            return element
        except:
            return "Element not found!"


    def __repr__(self):
        return f"{self.__class__.__name__}"


class Car(Inherit):
    __tablename__ = 'Car'

    id = Column(Integer, primary_key=True, autoincrement = True)
    car_brand = Column(Text)
    car_model = Column(Text)
    car_year = Column(Integer)
    car_number = Column(String(8))
    car_vin_number = Column(String(17))
    date = Column(Date)

    marks = relationship("Marks", back_populates="car", cascade="all, delete-orphan", uselist=False, lazy="joined")
    upper_body = relationship("UpperBody", back_populates="car", cascade="all, delete-orphan", uselist=False, lazy="joined")
    side_body = relationship("SideBody", back_populates="car", cascade="all, delete-orphan", uselist=False, lazy="joined")
    doors = relationship("Doors", back_populates="car", cascade="all, delete-orphan", uselist=False, lazy="joined")
    glass_mirrors = relationship("GlassMirrors", back_populates="car", cascade="all, delete-orphan", uselist=False, lazy="joined")
    wheels = relationship("Wheels", back_populates="car", cascade="all, delete-orphan", uselist=False, lazy="joined")
    under_hood = relationship("UnderHood", back_populates="car", cascade="all, delete-orphan", uselist=False, lazy="joined")
    trunk = relationship("Trunk", back_populates="car", cascade="all, delete-orphan", uselist=False, lazy="joined")
    lift_inspect = relationship("LiftInspect", back_populates="car", cascade="all, delete-orphan", uselist=False, lazy="joined")
    repair = relationship("Repair", back_populates="car", cascade="all, delete-orphan", uselist=False, lazy="joined")

    def __init__(self, id=None, car_brand = None, car_model = None, car_year = None, car_number = None, car_vin_number = None):
        self.id = id
        self.car_brand = car_brand
        self.car_model = car_model
        self.car_year = car_year
        self.car_number = car_number
        self.car_vin_number = car_vin_number
        self.date = date
        self.marks = Marks()
        self.upper_body = UpperBody()
        self.side_body = SideBody()
        self.doors = Doors()
        self.glass_mirrors = GlassMirrors()
        self.wheels = Wheels()
        self.under_hood = UnderHood()
        self.trunk = Trunk()
        self.lift_inspect = LiftInspect()
        self.repair = Repair()



class Marks(Inherit):
    __tablename__ = 'Marks'

    id = Column(Integer, primary_key=True)
    car_id = Column(Integer, ForeignKey('Car.id'))
    main = Column(Integer)
    outside_body = Column(Integer)
    under_hood = Column(Integer)
    trunk = Column(Integer)

    car = relationship("Car", back_populates="marks")


class UpperBody(Inherit):
    __tablename__ = 'UpperBody'

    id = Column(Integer, primary_key=True)
    car_id = Column(Integer, ForeignKey('Car.id'))
    hood_MKR_min = Column(Integer)
    hood_MKR_max = Column(Integer)
    roof_MKR_min = Column(Integer)
    roof_MKR_max = Column(Integer)
    trunk_MKR_min = Column(Integer)
    trunk_MKR_max = Column(Integer)
    bumper_front_verdict = Column(Text)
    bumper_back_verdict = Column(Text)

    car = relationship("Car", back_populates="upper_body")


class SideBody(Inherit):
    __tablename__ = 'SideBody'

    id = Column(Integer, primary_key=True)
    car_id = Column(Integer, ForeignKey('Car.id'))
    left_front_fender_min = Column(Integer)
    left_front_fender_max = Column(Integer)
    left_back_fender_min = Column(Integer)
    left_back_fender_max = Column(Integer)
    right_front_fender_min = Column(Integer)
    right_front_fender_max = Column(Integer)
    right_back_fender_min = Column(Integer)
    right_back_fender_max = Column(Integer)

    car = relationship("Car", back_populates="side_body")


class Doors(Inherit):
    __tablename__ = 'Doors'

    id = Column(Integer, primary_key=True)
    car_id = Column(Integer, ForeignKey('Car.id'))
    left_front_door_min = Column(Integer)
    left_front_door_max = Column(Integer)
    left_back_door_min = Column(Integer)
    left_back_door_max = Column(Integer)
    right_front_door_min = Column(Integer)
    right_front_door_max = Column(Integer)
    right_back_door_min = Column(Integer)
    right_back_door_max = Column(Integer)

    car = relationship("Car", back_populates="doors")


class GlassMirrors(Inherit):
    __tablename__ = 'GlassMirrors'

    id = Column(Integer, primary_key=True)
    car_id = Column(Integer, ForeignKey('Car.id'))
    left_light = Column(Text)
    left_PTF = Column(Text)
    left_mirror = Column(Text)
    right_light = Column(Text)
    right_PTF = Column(Text)
    right_mirror = Column(Text)

    car = relationship("Car", back_populates="glass_mirrors")


class Wheels(Inherit):
    __tablename__ = 'Wheels'

    id = Column(Integer, primary_key=True)
    car_id = Column(Integer, ForeignKey('Car.id'))
    left_front_wheel = Column(Text)
    left_front_disk = Column(Text)
    left_front_block = Column(Text)
    left_back_wheel = Column(Text)
    left_back_disk = Column(Text)
    left_back_block = Column(Text)
    right_front_wheel = Column(Text)
    right_front_disk = Column(Text)
    right_front_block = Column(Text)
    right_back_wheel = Column(Text)
    right_back_disk = Column(Text)
    right_back_block = Column(Text)

    car = relationship("Car", back_populates="wheels")


class UnderHood(Inherit):
    __tablename__ = 'UnderHood'

    id = Column(Integer, primary_key=True)
    car_id = Column(Integer, ForeignKey('Car.id'))
    lkp_status = Column(Text)
    plastic_details = Column(Text)
    engine_tools = Column(Text)

    car = relationship("Car", back_populates="under_hood")


class Trunk(Inherit):
    __tablename__ = 'Trunk'

    id = Column(Integer, primary_key=True)
    car_id = Column(Integer, ForeignKey('Car.id'))
    floor_light_upholstery = Column(Text)
    additional_wheel = Column(Text)
    tools = Column(Text)

    car = relationship("Car", back_populates="trunk")


class LiftInspect(Inherit):
    __tablename__ = 'LiftInspect'

    id = Column(Integer, primary_key=True)
    car_id = Column(Integer, ForeignKey('Car.id'))
    ag_ak_inspect = Column(Text)
    front_suspension = Column(Text)
    back_suspension = Column(Text)
    hoses_wiring = Column(Text)
    exhaust_system = Column(Text)

    car = relationship("Car", back_populates="lift_inspect")


class Repair(Inherit):
    __tablename__ = 'Repair'

    id = Column(Integer, primary_key=True)
    car_id = Column(Integer, ForeignKey('Car.id'))
    add_wheel_complect = Column(Text)
    anti_theft_heating_system = Column(Text)
    electricity = Column(Text)
    body_glasses = Column(Text)
    engine_transmission = Column(Text)
    brakes_suspension = Column(Text)
    cabin = Column(Text)
    others = Column(Text)
    cost = Column(Integer)

    car = relationship("Car", back_populates="repair")


Base.metadata.create_all(engine)
