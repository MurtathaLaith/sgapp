#!/usr/bin/env python3
"""
Database initialization script for Motor Switchgear Selection API
Populates the database with sample manufacturers, starting methods, contactors, and overload relays
"""

import os
import sys
import json

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.main import app
from src.models.user import db
from src.models.switchgear import (
    Manufacturer, StartingMethod, Contactor, OverloadRelay, Motor
)

def init_manufacturers():
    """Initialize manufacturers data"""
    manufacturers_data = [
        {'name': 'ABB', 'country': 'Switzerland', 'website': 'https://www.abb.com'},
        {'name': 'Schneider Electric', 'country': 'France', 'website': 'https://www.schneider-electric.com'},
        {'name': 'Siemens', 'country': 'Germany', 'website': 'https://www.siemens.com'},
        {'name': 'Eaton', 'country': 'Ireland', 'website': 'https://www.eaton.com'},
        {'name': 'Allen-Bradley', 'country': 'USA', 'website': 'https://www.rockwellautomation.com'},
        {'name': 'Mitsubishi Electric', 'country': 'Japan', 'website': 'https://www.mitsubishielectric.com'},
        {'name': 'LS Electric', 'country': 'South Korea', 'website': 'https://www.lselectric.com'},
        {'name': 'Chint', 'country': 'China', 'website': 'https://www.chint.com'}
    ]
    
    for data in manufacturers_data:
        if not Manufacturer.query.filter_by(name=data['name']).first():
            manufacturer = Manufacturer(**data)
            db.session.add(manufacturer)
    
    print("✓ Manufacturers initialized")

def init_starting_methods():
    """Initialize starting methods data"""
    starting_methods_data = [
        {
            'name': 'DOL',
            'description': 'Direct On-Line starter - simplest and most economical method',
            'min_power_hp': 0.5,
            'max_power_hp': 5.0,
            'starting_current_reduction': 0.0,
            'starting_torque_reduction': 0.0,
            'complexity_level': 1,
            'cost_factor': 1.0
        },
        {
            'name': 'Star-Delta',
            'description': 'Star-Delta starter - reduces starting current to 1/3',
            'min_power_hp': 15.0,
            'max_power_hp': 200.0,
            'starting_current_reduction': 0.67,
            'starting_torque_reduction': 0.67,
            'complexity_level': 2,
            'cost_factor': 2.5
        },
        {
            'name': 'Soft Starter',
            'description': 'Electronic soft starter - gradual voltage increase',
            'min_power_hp': 5.0,
            'max_power_hp': 500.0,
            'starting_current_reduction': 0.5,
            'starting_torque_reduction': 0.3,
            'complexity_level': 2,
            'cost_factor': 3.0
        },
        {
            'name': 'VFD',
            'description': 'Variable Frequency Drive - full speed and torque control',
            'min_power_hp': 1.0,
            'max_power_hp': 1000.0,
            'starting_current_reduction': 0.8,
            'starting_torque_reduction': 0.0,
            'complexity_level': 3,
            'cost_factor': 5.0
        },
        {
            'name': 'Autotransformer',
            'description': 'Autotransformer starter - better torque than star-delta',
            'min_power_hp': 25.0,
            'max_power_hp': 300.0,
            'starting_current_reduction': 0.5,
            'starting_torque_reduction': 0.36,
            'complexity_level': 2,
            'cost_factor': 3.5
        }
    ]
    
    for data in starting_methods_data:
        if not StartingMethod.query.filter_by(name=data['name']).first():
            method = StartingMethod(**data)
            db.session.add(method)
    
    print("✓ Starting methods initialized")

def init_contactors():
    """Initialize contactors data"""
    contactors_data = [
        # ABB Contactors
        {'model': 'AF09-30-10', 'manufacturer': 'ABB', 'current_rating': 9, 'voltage_rating': 690, 'utilization_category': 'AC-3', 'poles': 3, 'auxiliary_contacts': '1NO+1NC', 'coil_voltage': 230, 'frame_size': 'AF09', 'price': 45.00},
        {'model': 'AF12-30-10', 'manufacturer': 'ABB', 'current_rating': 12, 'voltage_rating': 690, 'utilization_category': 'AC-3', 'poles': 3, 'auxiliary_contacts': '1NO+1NC', 'coil_voltage': 230, 'frame_size': 'AF12', 'price': 52.00},
        {'model': 'AF16-30-10', 'manufacturer': 'ABB', 'current_rating': 16, 'voltage_rating': 690, 'utilization_category': 'AC-3', 'poles': 3, 'auxiliary_contacts': '1NO+1NC', 'coil_voltage': 230, 'frame_size': 'AF16', 'price': 58.00},
        {'model': 'AF25-30-11', 'manufacturer': 'ABB', 'current_rating': 25, 'voltage_rating': 690, 'utilization_category': 'AC-3', 'poles': 3, 'auxiliary_contacts': '1NO+1NC', 'coil_voltage': 230, 'frame_size': 'AF25', 'price': 68.00},
        {'model': 'AF38-30-11', 'manufacturer': 'ABB', 'current_rating': 38, 'voltage_rating': 690, 'utilization_category': 'AC-3', 'poles': 3, 'auxiliary_contacts': '1NO+1NC', 'coil_voltage': 230, 'frame_size': 'AF38', 'price': 85.00},
        {'model': 'AF50-30-11', 'manufacturer': 'ABB', 'current_rating': 50, 'voltage_rating': 690, 'utilization_category': 'AC-3', 'poles': 3, 'auxiliary_contacts': '1NO+1NC', 'coil_voltage': 230, 'frame_size': 'AF50', 'price': 105.00},
        {'model': 'AF65-30-11', 'manufacturer': 'ABB', 'current_rating': 65, 'voltage_rating': 690, 'utilization_category': 'AC-3', 'poles': 3, 'auxiliary_contacts': '1NO+1NC', 'coil_voltage': 230, 'frame_size': 'AF65', 'price': 125.00},
        {'model': 'AF80-30-11', 'manufacturer': 'ABB', 'current_rating': 80, 'voltage_rating': 690, 'utilization_category': 'AC-3', 'poles': 3, 'auxiliary_contacts': '1NO+1NC', 'coil_voltage': 230, 'frame_size': 'AF80', 'price': 145.00},
        {'model': 'AF95-30-11', 'manufacturer': 'ABB', 'current_rating': 95, 'voltage_rating': 690, 'utilization_category': 'AC-3', 'poles': 3, 'auxiliary_contacts': '1NO+1NC', 'coil_voltage': 230, 'frame_size': 'AF95', 'price': 165.00},
        
        # Schneider Electric Contactors
        {'model': 'LC1D09M7', 'manufacturer': 'Schneider Electric', 'current_rating': 9, 'voltage_rating': 690, 'utilization_category': 'AC-3', 'poles': 3, 'auxiliary_contacts': '1NO+1NC', 'coil_voltage': 230, 'frame_size': 'D09', 'price': 42.00},
        {'model': 'LC1D12M7', 'manufacturer': 'Schneider Electric', 'current_rating': 12, 'voltage_rating': 690, 'utilization_category': 'AC-3', 'poles': 3, 'auxiliary_contacts': '1NO+1NC', 'coil_voltage': 230, 'frame_size': 'D12', 'price': 48.00},
        {'model': 'LC1D18M7', 'manufacturer': 'Schneider Electric', 'current_rating': 18, 'voltage_rating': 690, 'utilization_category': 'AC-3', 'poles': 3, 'auxiliary_contacts': '1NO+1NC', 'coil_voltage': 230, 'frame_size': 'D18', 'price': 55.00},
        {'model': 'LC1D25M7', 'manufacturer': 'Schneider Electric', 'current_rating': 25, 'voltage_rating': 690, 'utilization_category': 'AC-3', 'poles': 3, 'auxiliary_contacts': '1NO+1NC', 'coil_voltage': 230, 'frame_size': 'D25', 'price': 65.00},
        {'model': 'LC1D32M7', 'manufacturer': 'Schneider Electric', 'current_rating': 32, 'voltage_rating': 690, 'utilization_category': 'AC-3', 'poles': 3, 'auxiliary_contacts': '1NO+1NC', 'coil_voltage': 230, 'frame_size': 'D32', 'price': 78.00},
        {'model': 'LC1D40M7', 'manufacturer': 'Schneider Electric', 'current_rating': 40, 'voltage_rating': 690, 'utilization_category': 'AC-3', 'poles': 3, 'auxiliary_contacts': '1NO+1NC', 'coil_voltage': 230, 'frame_size': 'D40', 'price': 95.00},
        {'model': 'LC1D50M7', 'manufacturer': 'Schneider Electric', 'current_rating': 50, 'voltage_rating': 690, 'utilization_category': 'AC-3', 'poles': 3, 'auxiliary_contacts': '1NO+1NC', 'coil_voltage': 230, 'frame_size': 'D50', 'price': 115.00},
        {'model': 'LC1D65M7', 'manufacturer': 'Schneider Electric', 'current_rating': 65, 'voltage_rating': 690, 'utilization_category': 'AC-3', 'poles': 3, 'auxiliary_contacts': '1NO+1NC', 'coil_voltage': 230, 'frame_size': 'D65', 'price': 135.00},
        {'model': 'LC1D80M7', 'manufacturer': 'Schneider Electric', 'current_rating': 80, 'voltage_rating': 690, 'utilization_category': 'AC-3', 'poles': 3, 'auxiliary_contacts': '1NO+1NC', 'coil_voltage': 230, 'frame_size': 'D80', 'price': 155.00},
        
        # Siemens Contactors
        {'model': '3RT1015-1BB42', 'manufacturer': 'Siemens', 'current_rating': 9, 'voltage_rating': 690, 'utilization_category': 'AC-3', 'poles': 3, 'auxiliary_contacts': '1NO+1NC', 'coil_voltage': 230, 'frame_size': 'S00', 'price': 48.00},
        {'model': '3RT1016-1BB42', 'manufacturer': 'Siemens', 'current_rating': 12, 'voltage_rating': 690, 'utilization_category': 'AC-3', 'poles': 3, 'auxiliary_contacts': '1NO+1NC', 'coil_voltage': 230, 'frame_size': 'S00', 'price': 52.00},
        {'model': '3RT1023-1BB40', 'manufacturer': 'Siemens', 'current_rating': 16, 'voltage_rating': 690, 'utilization_category': 'AC-3', 'poles': 3, 'auxiliary_contacts': '1NO+1NC', 'coil_voltage': 230, 'frame_size': 'S0', 'price': 58.00},
        {'model': '3RT1025-1BB40', 'manufacturer': 'Siemens', 'current_rating': 25, 'voltage_rating': 690, 'utilization_category': 'AC-3', 'poles': 3, 'auxiliary_contacts': '1NO+1NC', 'coil_voltage': 230, 'frame_size': 'S0', 'price': 68.00},
        {'model': '3RT1034-1BB40', 'manufacturer': 'Siemens', 'current_rating': 40, 'voltage_rating': 690, 'utilization_category': 'AC-3', 'poles': 3, 'auxiliary_contacts': '1NO+1NC', 'coil_voltage': 230, 'frame_size': 'S2', 'price': 88.00},
        {'model': '3RT1035-1BB40', 'manufacturer': 'Siemens', 'current_rating': 50, 'voltage_rating': 690, 'utilization_category': 'AC-3', 'poles': 3, 'auxiliary_contacts': '1NO+1NC', 'coil_voltage': 230, 'frame_size': 'S2', 'price': 108.00},
        {'model': '3RT1044-1BB40', 'manufacturer': 'Siemens', 'current_rating': 65, 'voltage_rating': 690, 'utilization_category': 'AC-3', 'poles': 3, 'auxiliary_contacts': '1NO+1NC', 'coil_voltage': 230, 'frame_size': 'S3', 'price': 128.00},
        {'model': '3RT1045-1BB40', 'manufacturer': 'Siemens', 'current_rating': 80, 'voltage_rating': 690, 'utilization_category': 'AC-3', 'poles': 3, 'auxiliary_contacts': '1NO+1NC', 'coil_voltage': 230, 'frame_size': 'S3', 'price': 148.00},
        
        # Eaton Contactors
        {'model': 'DILM9-10', 'manufacturer': 'Eaton', 'current_rating': 9, 'voltage_rating': 690, 'utilization_category': 'AC-3', 'poles': 3, 'auxiliary_contacts': '1NO+1NC', 'coil_voltage': 230, 'frame_size': 'DILM9', 'price': 44.00},
        {'model': 'DILM12-10', 'manufacturer': 'Eaton', 'current_rating': 12, 'voltage_rating': 690, 'utilization_category': 'AC-3', 'poles': 3, 'auxiliary_contacts': '1NO+1NC', 'coil_voltage': 230, 'frame_size': 'DILM12', 'price': 50.00},
        {'model': 'DILM17-10', 'manufacturer': 'Eaton', 'current_rating': 18, 'voltage_rating': 690, 'utilization_category': 'AC-3', 'poles': 3, 'auxiliary_contacts': '1NO+1NC', 'coil_voltage': 230, 'frame_size': 'DILM17', 'price': 56.00},
        {'model': 'DILM25-10', 'manufacturer': 'Eaton', 'current_rating': 25, 'voltage_rating': 690, 'utilization_category': 'AC-3', 'poles': 3, 'auxiliary_contacts': '1NO+1NC', 'coil_voltage': 230, 'frame_size': 'DILM25', 'price': 66.00},
        {'model': 'DILM32-10', 'manufacturer': 'Eaton', 'current_rating': 32, 'voltage_rating': 690, 'utilization_category': 'AC-3', 'poles': 3, 'auxiliary_contacts': '1NO+1NC', 'coil_voltage': 230, 'frame_size': 'DILM32', 'price': 76.00},
        {'model': 'DILM40-10', 'manufacturer': 'Eaton', 'current_rating': 40, 'voltage_rating': 690, 'utilization_category': 'AC-3', 'poles': 3, 'auxiliary_contacts': '1NO+1NC', 'coil_voltage': 230, 'frame_size': 'DILM40', 'price': 92.00},
        {'model': 'DILM50-10', 'manufacturer': 'Eaton', 'current_rating': 50, 'voltage_rating': 690, 'utilization_category': 'AC-3', 'poles': 3, 'auxiliary_contacts': '1NO+1NC', 'coil_voltage': 230, 'frame_size': 'DILM50', 'price': 112.00},
        {'model': 'DILM65-10', 'manufacturer': 'Eaton', 'current_rating': 65, 'voltage_rating': 690, 'utilization_category': 'AC-3', 'poles': 3, 'auxiliary_contacts': '1NO+1NC', 'coil_voltage': 230, 'frame_size': 'DILM65', 'price': 132.00}
    ]
    
    for data in contactors_data:
        if not Contactor.query.filter_by(model=data['model']).first():
            contactor = Contactor(**data)
            db.session.add(contactor)
    
    print("✓ Contactors initialized")

def init_overload_relays():
    """Initialize overload relays data"""
    overload_relays_data = [
        # ABB Overload Relays
        {'model': 'TF42-0.24', 'manufacturer': 'ABB', 'current_range_min': 0.16, 'current_range_max': 0.24, 'trip_class': 10, 'reset_type': 'Manual', 'compatible_contactor_frames': '["AF09"]', 'price': 35.00},
        {'model': 'TF42-0.4', 'manufacturer': 'ABB', 'current_range_min': 0.25, 'current_range_max': 0.4, 'trip_class': 10, 'reset_type': 'Manual', 'compatible_contactor_frames': '["AF09"]', 'price': 35.00},
        {'model': 'TF42-0.63', 'manufacturer': 'ABB', 'current_range_min': 0.4, 'current_range_max': 0.63, 'trip_class': 10, 'reset_type': 'Manual', 'compatible_contactor_frames': '["AF09"]', 'price': 35.00},
        {'model': 'TF42-1.0', 'manufacturer': 'ABB', 'current_range_min': 0.63, 'current_range_max': 1.0, 'trip_class': 10, 'reset_type': 'Manual', 'compatible_contactor_frames': '["AF09"]', 'price': 35.00},
        {'model': 'TF42-1.6', 'manufacturer': 'ABB', 'current_range_min': 1.0, 'current_range_max': 1.6, 'trip_class': 10, 'reset_type': 'Manual', 'compatible_contactor_frames': '["AF09", "AF12"]', 'price': 35.00},
        {'model': 'TF42-2.5', 'manufacturer': 'ABB', 'current_range_min': 1.6, 'current_range_max': 2.5, 'trip_class': 10, 'reset_type': 'Manual', 'compatible_contactor_frames': '["AF12"]', 'price': 35.00},
        {'model': 'TF42-4.0', 'manufacturer': 'ABB', 'current_range_min': 2.5, 'current_range_max': 4.0, 'trip_class': 10, 'reset_type': 'Manual', 'compatible_contactor_frames': '["AF12", "AF16"]', 'price': 35.00},
        {'model': 'TF42-6.3', 'manufacturer': 'ABB', 'current_range_min': 4.0, 'current_range_max': 6.3, 'trip_class': 10, 'reset_type': 'Manual', 'compatible_contactor_frames': '["AF16"]', 'price': 35.00},
        {'model': 'TF42-10', 'manufacturer': 'ABB', 'current_range_min': 6.3, 'current_range_max': 10, 'trip_class': 10, 'reset_type': 'Manual', 'compatible_contactor_frames': '["AF16", "AF25"]', 'price': 38.00},
        {'model': 'TF42-16', 'manufacturer': 'ABB', 'current_range_min': 10, 'current_range_max': 16, 'trip_class': 10, 'reset_type': 'Manual', 'compatible_contactor_frames': '["AF25"]', 'price': 38.00},
        {'model': 'TF42-25', 'manufacturer': 'ABB', 'current_range_min': 16, 'current_range_max': 25, 'trip_class': 10, 'reset_type': 'Manual', 'compatible_contactor_frames': '["AF25", "AF38"]', 'price': 42.00},
        {'model': 'TF42-40', 'manufacturer': 'ABB', 'current_range_min': 25, 'current_range_max': 40, 'trip_class': 10, 'reset_type': 'Manual', 'compatible_contactor_frames': '["AF38"]', 'price': 42.00},
        {'model': 'TF42-63', 'manufacturer': 'ABB', 'current_range_min': 40, 'current_range_max': 63, 'trip_class': 10, 'reset_type': 'Manual', 'compatible_contactor_frames': '["AF50", "AF65"]', 'price': 48.00},
        {'model': 'TF42-80', 'manufacturer': 'ABB', 'current_range_min': 63, 'current_range_max': 80, 'trip_class': 10, 'reset_type': 'Manual', 'compatible_contactor_frames': '["AF65", "AF80"]', 'price': 48.00},
        {'model': 'TF42-100', 'manufacturer': 'ABB', 'current_range_min': 80, 'current_range_max': 100, 'trip_class': 10, 'reset_type': 'Manual', 'compatible_contactor_frames': '["AF80", "AF95"]', 'price': 52.00},
        
        # Schneider Electric Overload Relays
        {'model': 'LRD01', 'manufacturer': 'Schneider Electric', 'current_range_min': 0.1, 'current_range_max': 0.16, 'trip_class': 10, 'reset_type': 'Manual', 'compatible_contactor_frames': '["D09"]', 'price': 32.00},
        {'model': 'LRD02', 'manufacturer': 'Schneider Electric', 'current_range_min': 0.16, 'current_range_max': 0.25, 'trip_class': 10, 'reset_type': 'Manual', 'compatible_contactor_frames': '["D09"]', 'price': 32.00},
        {'model': 'LRD03', 'manufacturer': 'Schneider Electric', 'current_range_min': 0.25, 'current_range_max': 0.4, 'trip_class': 10, 'reset_type': 'Manual', 'compatible_contactor_frames': '["D09"]', 'price': 32.00},
        {'model': 'LRD04', 'manufacturer': 'Schneider Electric', 'current_range_min': 0.4, 'current_range_max': 0.63, 'trip_class': 10, 'reset_type': 'Manual', 'compatible_contactor_frames': '["D09"]', 'price': 32.00},
        {'model': 'LRD05', 'manufacturer': 'Schneider Electric', 'current_range_min': 0.63, 'current_range_max': 1.0, 'trip_class': 10, 'reset_type': 'Manual', 'compatible_contactor_frames': '["D09"]', 'price': 32.00},
        {'model': 'LRD06', 'manufacturer': 'Schneider Electric', 'current_range_min': 1.0, 'current_range_max': 1.6, 'trip_class': 10, 'reset_type': 'Manual', 'compatible_contactor_frames': '["D09", "D12"]', 'price': 32.00},
        {'model': 'LRD07', 'manufacturer': 'Schneider Electric', 'current_range_min': 1.6, 'current_range_max': 2.5, 'trip_class': 10, 'reset_type': 'Manual', 'compatible_contactor_frames': '["D12"]', 'price': 32.00},
        {'model': 'LRD08', 'manufacturer': 'Schneider Electric', 'current_range_min': 2.5, 'current_range_max': 4.0, 'trip_class': 10, 'reset_type': 'Manual', 'compatible_contactor_frames': '["D12", "D18"]', 'price': 32.00},
        {'model': 'LRD10', 'manufacturer': 'Schneider Electric', 'current_range_min': 4.0, 'current_range_max': 6.0, 'trip_class': 10, 'reset_type': 'Manual', 'compatible_contactor_frames': '["D18"]', 'price': 35.00},
        {'model': 'LRD12', 'manufacturer': 'Schneider Electric', 'current_range_min': 5.5, 'current_range_max': 8.0, 'trip_class': 10, 'reset_type': 'Manual', 'compatible_contactor_frames': '["D18", "D25"]', 'price': 35.00},
        {'model': 'LRD14', 'manufacturer': 'Schneider Electric', 'current_range_min': 7.0, 'current_range_max': 10.0, 'trip_class': 10, 'reset_type': 'Manual', 'compatible_contactor_frames': '["D25"]', 'price': 35.00},
        {'model': 'LRD16', 'manufacturer': 'Schneider Electric', 'current_range_min': 9.0, 'current_range_max': 13.0, 'trip_class': 10, 'reset_type': 'Manual', 'compatible_contactor_frames': '["D25"]', 'price': 38.00},
        {'model': 'LRD21', 'manufacturer': 'Schneider Electric', 'current_range_min': 12.0, 'current_range_max': 18.0, 'trip_class': 10, 'reset_type': 'Manual', 'compatible_contactor_frames': '["D25", "D32"]', 'price': 38.00},
        {'model': 'LRD22', 'manufacturer': 'Schneider Electric', 'current_range_min': 16.0, 'current_range_max': 24.0, 'trip_class': 10, 'reset_type': 'Manual', 'compatible_contactor_frames': '["D32"]', 'price': 42.00},
        {'model': 'LRD25', 'manufacturer': 'Schneider Electric', 'current_range_min': 23.0, 'current_range_max': 32.0, 'trip_class': 10, 'reset_type': 'Manual', 'compatible_contactor_frames': '["D32", "D40"]', 'price': 42.00},
        {'model': 'LRD32', 'manufacturer': 'Schneider Electric', 'current_range_min': 30.0, 'current_range_max': 40.0, 'trip_class': 10, 'reset_type': 'Manual', 'compatible_contactor_frames': '["D40"]', 'price': 45.00},
        {'model': 'LRD35', 'manufacturer': 'Schneider Electric', 'current_range_min': 37.0, 'current_range_max': 50.0, 'trip_class': 10, 'reset_type': 'Manual', 'compatible_contactor_frames': '["D50"]', 'price': 48.00},
        {'model': 'LRD340', 'manufacturer': 'Schneider Electric', 'current_range_min': 48.0, 'current_range_max': 65.0, 'trip_class': 10, 'reset_type': 'Manual', 'compatible_contactor_frames': '["D65"]', 'price': 52.00},
        {'model': 'LRD350', 'manufacturer': 'Schneider Electric', 'current_range_min': 63.0, 'current_range_max': 80.0, 'trip_class': 10, 'reset_type': 'Manual', 'compatible_contactor_frames': '["D80"]', 'price': 55.00}
    ]
    
    for data in overload_relays_data:
        if not OverloadRelay.query.filter_by(model=data['model']).first():
            relay = OverloadRelay(**data)
            db.session.add(relay)
    
    print("✓ Overload relays initialized")

def init_sample_motors():
    """Initialize sample motor data"""
    motors_data = [
        {'power_hp': 0.5, 'power_kw': 0.37, 'voltage': 415, 'frequency': 50, 'phases': 3, 'full_load_current': 1.1, 'power_factor': 0.75, 'efficiency': 0.85, 'starting_current_multiplier': 6.0},
        {'power_hp': 0.75, 'power_kw': 0.55, 'voltage': 415, 'frequency': 50, 'phases': 3, 'full_load_current': 1.5, 'power_factor': 0.76, 'efficiency': 0.86, 'starting_current_multiplier': 6.0},
        {'power_hp': 1.0, 'power_kw': 0.75, 'voltage': 415, 'frequency': 50, 'phases': 3, 'full_load_current': 2.0, 'power_factor': 0.77, 'efficiency': 0.87, 'starting_current_multiplier': 6.5},
        {'power_hp': 1.5, 'power_kw': 1.1, 'voltage': 415, 'frequency': 50, 'phases': 3, 'full_load_current': 2.8, 'power_factor': 0.78, 'efficiency': 0.88, 'starting_current_multiplier': 6.5},
        {'power_hp': 2.0, 'power_kw': 1.5, 'voltage': 415, 'frequency': 50, 'phases': 3, 'full_load_current': 3.6, 'power_factor': 0.79, 'efficiency': 0.89, 'starting_current_multiplier': 7.0},
        {'power_hp': 3.0, 'power_kw': 2.2, 'voltage': 415, 'frequency': 50, 'phases': 3, 'full_load_current': 5.2, 'power_factor': 0.80, 'efficiency': 0.89, 'starting_current_multiplier': 7.0},
        {'power_hp': 5.0, 'power_kw': 3.7, 'voltage': 415, 'frequency': 50, 'phases': 3, 'full_load_current': 8.2, 'power_factor': 0.81, 'efficiency': 0.90, 'starting_current_multiplier': 7.5},
        {'power_hp': 7.5, 'power_kw': 5.5, 'voltage': 415, 'frequency': 50, 'phases': 3, 'full_load_current': 12.0, 'power_factor': 0.82, 'efficiency': 0.91, 'starting_current_multiplier': 7.5},
        {'power_hp': 10.0, 'power_kw': 7.5, 'voltage': 415, 'frequency': 50, 'phases': 3, 'full_load_current': 15.8, 'power_factor': 0.83, 'efficiency': 0.91, 'starting_current_multiplier': 8.0},
        {'power_hp': 15.0, 'power_kw': 11.0, 'voltage': 415, 'frequency': 50, 'phases': 3, 'full_load_current': 23.0, 'power_factor': 0.84, 'efficiency': 0.92, 'starting_current_multiplier': 8.0},
        {'power_hp': 20.0, 'power_kw': 15.0, 'voltage': 415, 'frequency': 50, 'phases': 3, 'full_load_current': 30.0, 'power_factor': 0.85, 'efficiency': 0.92, 'starting_current_multiplier': 8.5},
        {'power_hp': 25.0, 'power_kw': 18.5, 'voltage': 415, 'frequency': 50, 'phases': 3, 'full_load_current': 36.5, 'power_factor': 0.85, 'efficiency': 0.93, 'starting_current_multiplier': 8.5},
        {'power_hp': 30.0, 'power_kw': 22.0, 'voltage': 415, 'frequency': 50, 'phases': 3, 'full_load_current': 43.0, 'power_factor': 0.86, 'efficiency': 0.93, 'starting_current_multiplier': 9.0},
        {'power_hp': 40.0, 'power_kw': 30.0, 'voltage': 415, 'frequency': 50, 'phases': 3, 'full_load_current': 57.0, 'power_factor': 0.86, 'efficiency': 0.94, 'starting_current_multiplier': 9.0},
        {'power_hp': 50.0, 'power_kw': 37.0, 'voltage': 415, 'frequency': 50, 'phases': 3, 'full_load_current': 70.0, 'power_factor': 0.87, 'efficiency': 0.94, 'starting_current_multiplier': 9.5},
        {'power_hp': 60.0, 'power_kw': 45.0, 'voltage': 415, 'frequency': 50, 'phases': 3, 'full_load_current': 84.0, 'power_factor': 0.87, 'efficiency': 0.94, 'starting_current_multiplier': 9.5},
        {'power_hp': 75.0, 'power_kw': 55.0, 'voltage': 415, 'frequency': 50, 'phases': 3, 'full_load_current': 102.0, 'power_factor': 0.88, 'efficiency': 0.95, 'starting_current_multiplier': 10.0},
        {'power_hp': 100.0, 'power_kw': 75.0, 'voltage': 415, 'frequency': 50, 'phases': 3, 'full_load_current': 138.0, 'power_factor': 0.88, 'efficiency': 0.95, 'starting_current_multiplier': 10.0}
    ]
    
    for data in motors_data:
        if not Motor.query.filter_by(power_hp=data['power_hp'], voltage=data['voltage']).first():
            motor = Motor(**data)
            db.session.add(motor)
    
    print("✓ Sample motors initialized")

def main():
    """Main initialization function"""
    print("🚀 Initializing Motor Switchgear Selection Database...")
    
    with app.app_context():
        # Create all tables
        db.create_all()
        print("✓ Database tables created")
        
        # Initialize data
        init_manufacturers()
        init_starting_methods()
        init_contactors()
        init_overload_relays()
        init_sample_motors()
        
        # Commit all changes
        db.session.commit()
        print("✓ All data committed to database")
        
        # Print summary
        print("\n📊 Database Summary:")
        print(f"   Manufacturers: {Manufacturer.query.count()}")
        print(f"   Starting Methods: {StartingMethod.query.count()}")
        print(f"   Contactors: {Contactor.query.count()}")
        print(f"   Overload Relays: {OverloadRelay.query.count()}")
        print(f"   Sample Motors: {Motor.query.count()}")
        
        print("\n✅ Database initialization completed successfully!")

if __name__ == '__main__':
    main()

