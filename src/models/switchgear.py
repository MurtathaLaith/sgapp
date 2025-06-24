from src.models.user import db
import json

class Manufacturer(db.Model):
    __tablename__ = 'manufacturers'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(50))
    website = db.Column(db.String(200))
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'country': self.country,
            'website': self.website
        }

class StartingMethod(db.Model):
    __tablename__ = 'starting_methods'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    min_power_hp = db.Column(db.Float)
    max_power_hp = db.Column(db.Float)
    starting_current_reduction = db.Column(db.Float)  # Percentage reduction (0.0-1.0)
    starting_torque_reduction = db.Column(db.Float)   # Percentage reduction (0.0-1.0)
    complexity_level = db.Column(db.Integer)          # 1=Simple, 2=Medium, 3=Complex
    cost_factor = db.Column(db.Float)                 # Cost multiplier
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'min_power_hp': self.min_power_hp,
            'max_power_hp': self.max_power_hp,
            'starting_current_reduction': self.starting_current_reduction,
            'starting_torque_reduction': self.starting_torque_reduction,
            'complexity_level': self.complexity_level,
            'cost_factor': self.cost_factor
        }

class Contactor(db.Model):
    __tablename__ = 'contactors'
    
    id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String(50), nullable=False)
    manufacturer = db.Column(db.String(100), nullable=False)
    current_rating = db.Column(db.Float, nullable=False)  # Amperes
    voltage_rating = db.Column(db.Integer, nullable=False)  # Volts
    utilization_category = db.Column(db.String(10), default='AC-3')
    poles = db.Column(db.Integer, default=3)
    auxiliary_contacts = db.Column(db.String(20))
    coil_voltage = db.Column(db.Integer)
    frame_size = db.Column(db.String(20))
    price = db.Column(db.Float)
    image_url = db.Column(db.String(200))
    datasheet_url = db.Column(db.String(200))
    
    def to_dict(self):
        return {
            'id': self.id,
            'model': self.model,
            'manufacturer': self.manufacturer,
            'current_rating': self.current_rating,
            'voltage_rating': self.voltage_rating,
            'utilization_category': self.utilization_category,
            'poles': self.poles,
            'auxiliary_contacts': self.auxiliary_contacts,
            'coil_voltage': self.coil_voltage,
            'frame_size': self.frame_size,
            'price': self.price,
            'image_url': self.image_url,
            'datasheet_url': self.datasheet_url
        }

class OverloadRelay(db.Model):
    __tablename__ = 'overload_relays'
    
    id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String(50), nullable=False)
    manufacturer = db.Column(db.String(100), nullable=False)
    current_range_min = db.Column(db.Float, nullable=False)  # Minimum current in Amperes
    current_range_max = db.Column(db.Float, nullable=False)  # Maximum current in Amperes
    trip_class = db.Column(db.Integer, default=10)           # Trip class (10, 20, 30)
    reset_type = db.Column(db.String(20), default='Manual')  # Manual or Auto
    compatible_contactor_frames = db.Column(db.Text)         # JSON array of compatible frame sizes
    price = db.Column(db.Float)
    image_url = db.Column(db.String(200))
    datasheet_url = db.Column(db.String(200))
    
    def to_dict(self):
        return {
            'id': self.id,
            'model': self.model,
            'manufacturer': self.manufacturer,
            'current_range_min': self.current_range_min,
            'current_range_max': self.current_range_max,
            'current_range': f"{self.current_range_min}-{self.current_range_max}A",
            'trip_class': self.trip_class,
            'reset_type': self.reset_type,
            'compatible_contactor_frames': json.loads(self.compatible_contactor_frames) if self.compatible_contactor_frames else [],
            'price': self.price,
            'image_url': self.image_url,
            'datasheet_url': self.datasheet_url
        }

class Motor(db.Model):
    __tablename__ = 'motors'
    
    id = db.Column(db.Integer, primary_key=True)
    power_hp = db.Column(db.Float, nullable=False)
    power_kw = db.Column(db.Float, nullable=False)
    voltage = db.Column(db.Integer, nullable=False)
    frequency = db.Column(db.Integer, default=50)
    phases = db.Column(db.Integer, default=3)
    full_load_current = db.Column(db.Float)
    power_factor = db.Column(db.Float, default=0.8)
    efficiency = db.Column(db.Float, default=0.9)
    starting_current_multiplier = db.Column(db.Float, default=7.0)
    
    def to_dict(self):
        return {
            'id': self.id,
            'power_hp': self.power_hp,
            'power_kw': self.power_kw,
            'voltage': self.voltage,
            'frequency': self.frequency,
            'phases': self.phases,
            'full_load_current': self.full_load_current,
            'power_factor': self.power_factor,
            'efficiency': self.efficiency,
            'starting_current_multiplier': self.starting_current_multiplier
        }

