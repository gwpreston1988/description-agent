"""
Configuration file for HVAC Description Generator Pipeline
Contains all mappings, paths, and configuration settings
"""

import os
from pathlib import Path

# Base directory (description-agent root)
BASE_DIR = Path(__file__).parent.parent

# Template directory
TEMPLATES_DIR = BASE_DIR / "Scripts"

# SEER rating directories
SEER_DIRS = {
    "13.4": BASE_DIR / "13.4_SEER2",
    "14.3": BASE_DIR / "14.3_SEER2",
    "Solace_14.3": BASE_DIR / "Solace_14.3",
    "15.2": BASE_DIR / "15.2_SEER2",
    "16.2": BASE_DIR / "16.2_SEER2",
    "17.2": BASE_DIR / "17.2_SEER2",
    "17.5": BASE_DIR / "17.5_SEER2",
}

# Component type detection patterns (prefix-based)
COMPONENT_PATTERNS = {
    # Solace - 14.3 SEER2
    'S-GLXS4BA': 'AC_Condenser',
    'S-GLZS4BA': 'HP_Condenser',
    'S-AMST': 'AirHandler_Standard',
    'S-AWST': 'AirHandler_Wall',
    'S-GR9S80': 'Furnace_80AFUE',
    'S-GR9S92': 'Furnace_92AFUE',
    'S-CAPTA': 'Coil_Upflow',
    'S-CHPTA': 'Coil_Horizontal',
    'S-HKTS': 'Thermostat',

    # Condensers - 15.2 SEER2
    'GLXS5': 'AC_Condenser',
    'GLZS5': 'HP_Condenser',

    # Condensers - 16.2 SEER2
    'GXV6SS': 'AC_Condenser',
    'GZV6SA': 'HP_Condenser',

    # Condensers - 17.2 SEER2
    'GLXT7CA': 'AC_Condenser',
    'GLZT7CA': 'HP_Condenser',

    # Condensers - 17.5 SEER2
    'GZV7SA': 'HP_Condenser',
    'GSZV7SA': 'HP_Condenser',  # Same specs as GZV7SA

    # Air Handlers - 15.2 SEER2
    'AMST': 'AirHandler_Standard',
    'AWST': 'AirHandler_Wall',

    # Air Handlers - 16.2 SEER2
    'AHVE': 'AirHandler_Standard',

    # Air Handlers - 17.2 SEER2
    'AMVT': 'AirHandler_Standard',

    # Evaporator Coils - 15.2 SEER2
    'CAPTA': 'Coil_Upflow',
    'CHPTA': 'Coil_Horizontal',

    # Evaporator Coils - 16.2 SEER2
    'CAPEA': 'Coil_Upflow',
    'CHPEA': 'Coil_Horizontal',

    # Gas Furnaces - 15.2 SEER2
    'GR9S80': 'Furnace_80AFUE',
    'GR9S92': 'Furnace_92AFUE',
    'GR9S96': 'Furnace_96AFUE',

    # Gas Furnaces - 16.2 SEER2
    'GRVT8006': 'Furnace_80AFUE',
    'GRVT8008': 'Furnace_80AFUE',
    'GRVT8010': 'Furnace_80AFUE',
    'GRVT9604': 'Furnace_96AFUE',
    'GRVT9606': 'Furnace_96AFUE',
    'GRVT9608': 'Furnace_96AFUE',
    'GRVT9610': 'Furnace_96AFUE',
    'GRVT9612': 'Furnace_96AFUE',

    # Gas Furnaces - 17.2 SEER2 (same as 16.2)
    'GRVT80': 'Furnace_80AFUE',
    'GRVT96': 'Furnace_96AFUE',

    # Gas Furnaces - 17.5 SEER2 (same patterns as 16.2/17.2)
    # Already covered by GRVT80 and GRVT96 patterns above

    # Thermostats (to be ignored/skipped)
    'GTST': 'Thermostat',
    'ATST': 'Thermostat',
    'DTST': 'Thermostat',
}

# Template mapping for single-component systems
SINGLE_COMPONENT_TEMPLATES = {
    'AC_Condenser': 'template_ac_condenser_only_CORRECTED.html',
    'HP_Condenser': 'template_heat_pump_condenser_only_CORRECTED.html',
    'AirHandler_Standard': 'template_air_handler_only_CORRECTED.html',
    'AirHandler_Wall': 'template_air_handler_only_CORRECTED.html',  # Same template
    'Coil_Upflow': 'template_upflow_evaporator_coil_only_CORRECTED.html',
    'Coil_Horizontal': 'template_horizontal_evaporator_coil_only_CORRECTED.html',
    'Furnace_80AFUE': 'template_80_percent_afue_gas_furnace_CORRECTED.html',
    'Furnace_92AFUE': 'template_92_percent_afue_gas_furnace_CORRECTED.html',
    'Furnace_96AFUE': 'template_96_percent_afue_gas_furnace_CORRECTED.html',
}

# Template mapping for multi-component systems
MULTI_COMPONENT_TEMPLATES = {
    # 2-Component Systems
    ('AC_Condenser', 'AirHandler_Standard'): 'template_system_ac_airhandler_CORRECTED.html',
    ('AC_Condenser', 'AirHandler_Wall'): 'template_system_ac_airhandler_CORRECTED.html',
    ('HP_Condenser', 'AirHandler_Standard'): 'template_system_hp_airhandler_CORRECTED.html',
    ('HP_Condenser', 'AirHandler_Wall'): 'template_system_hp_airhandler_CORRECTED.html',
    ('AC_Condenser', 'Coil_Upflow'): 'template_system_ac_coil_CORRECTED.html',
    ('AC_Condenser', 'Coil_Horizontal'): 'template_system_ac_coil_CORRECTED.html',
    ('HP_Condenser', 'Coil_Upflow'): 'template_system_hp_coil_CORRECTED.html',
    ('HP_Condenser', 'Coil_Horizontal'): 'template_system_hp_coil_CORRECTED.html',
    ('Furnace_80AFUE', 'Coil_Upflow'): 'template_system_furnace_coil_CORRECTED.html',
    ('Furnace_80AFUE', 'Coil_Horizontal'): 'template_system_furnace_coil_CORRECTED.html',
    ('Furnace_92AFUE', 'Coil_Upflow'): 'template_system_furnace_coil_CORRECTED.html',
    ('Furnace_92AFUE', 'Coil_Horizontal'): 'template_system_furnace_coil_CORRECTED.html',

    # 3-Component Systems
    ('AC_Condenser', 'Furnace_80AFUE', 'Coil_Upflow'): 'template_system_ac_furnace_coil_CORRECTED.html',
    ('AC_Condenser', 'Furnace_80AFUE', 'Coil_Horizontal'): 'template_system_ac_furnace_coil_CORRECTED.html',
    ('AC_Condenser', 'Furnace_92AFUE', 'Coil_Upflow'): 'template_system_ac_furnace_coil_CORRECTED.html',
    ('AC_Condenser', 'Furnace_92AFUE', 'Coil_Horizontal'): 'template_system_ac_furnace_coil_CORRECTED.html',
    ('HP_Condenser', 'Furnace_80AFUE', 'Coil_Upflow'): 'template_system_hp_furnace_coil_dualfuel_CORRECTED.html',
    ('HP_Condenser', 'Furnace_80AFUE', 'Coil_Horizontal'): 'template_system_hp_furnace_coil_dualfuel_CORRECTED.html',
    ('HP_Condenser', 'Furnace_92AFUE', 'Coil_Upflow'): 'template_system_hp_furnace_coil_dualfuel_CORRECTED.html',
    ('HP_Condenser', 'Furnace_92AFUE', 'Coil_Horizontal'): 'template_system_hp_furnace_coil_dualfuel_CORRECTED.html',
}

# System type descriptions for intro paragraphs
SYSTEM_DESCRIPTIONS = {
    'AC_AirHandler': 'air conditioning system featuring a high-efficiency outdoor condenser matched with an indoor air handler',
    'AC_AirHandler_Wall': 'air conditioning system featuring a high-efficiency outdoor condenser matched with a space-saving wall-mounted air handler',
    'HP_AirHandler': 'heat pump system featuring a high-efficiency outdoor unit matched with an indoor air handler',
    'HP_AirHandler_Wall': 'heat pump system featuring a high-efficiency outdoor unit matched with a space-saving wall-mounted air handler',
    'AC_Furnace_Coil_Upflow': 'complete heating and cooling system combining a high-efficiency air conditioner, gas furnace, and upflow evaporator coil',
    'AC_Furnace_Coil_Horizontal': 'complete heating and cooling system combining a high-efficiency air conditioner, gas furnace, and horizontal evaporator coil',
    'HP_Furnace_Coil_Upflow': 'dual fuel system combining a high-efficiency heat pump with a gas furnace backup and upflow evaporator coil',
    'HP_Furnace_Coil_Horizontal': 'dual fuel system combining a high-efficiency heat pump with a gas furnace backup and horizontal evaporator coil',
}

# Footer logic based on SEER2 rating
FOOTER_THRESHOLD = 14.3

def get_footer_type(seer_rating):
    """
    Determine which footer to use based on SEER2 rating
    Returns: 'A' for < 14.3, 'B' for >= 14.3
    """
    try:
        seer = float(seer_rating)
        return 'A' if seer < FOOTER_THRESHOLD else 'B'
    except (ValueError, TypeError):
        return 'B'  # Default to nationwide compliant

# Filename generation patterns
def get_filename(seer_rating, component_types, model_numbers):
    """Generate standardized filename for HTML output"""
    if len(model_numbers) == 1:
        # Single component
        return f"Goodman_R410A_{model_numbers[0]}.html"
    elif len(model_numbers) == 2:
        # 2-component system
        comp1_type = component_types[0]
        tonnage = "Unknown"  # Will be extracted from specs
        if 'AC_Condenser' in comp1_type:
            system_type = 'AC_System'
        elif 'HP_Condenser' in comp1_type:
            system_type = 'HP_System'
        else:
            system_type = 'System'
        return f"Goodman_{tonnage}Ton_R410A_{system_type}_{'_'.join(model_numbers)}.html"
    else:
        # 3-component system
        comp1_type = component_types[0]
        if 'AC_Condenser' in comp1_type:
            if 'Coil_Upflow' in component_types:
                orientation = 'Upflow'
            else:
                orientation = 'Horizontal'
            if '80AFUE' in str(component_types):
                afue = '80AFUE'
            else:
                afue = '92AFUE'
            return f"Goodman_R410A_AC_{afue}_{orientation}_System_{'_'.join(model_numbers)}.html"
        elif 'HP_Condenser' in comp1_type:
            if 'Coil_Upflow' in component_types:
                orientation = 'Upflow'
            else:
                orientation = 'Horizontal'
            if '80AFUE' in str(component_types):
                afue = '80AFUE'
            else:
                afue = '92AFUE'
            return f"Goodman_R410A_DualFuel_{afue}_{orientation}_System_{'_'.join(model_numbers)}.html"

    return f"Goodman_System_{'_'.join(model_numbers)}.html"

# Validation
def validate_config():
    """Validate that all paths and templates exist"""
    errors = []

    # Check template directory
    if not TEMPLATES_DIR.exists():
        errors.append(f"Templates directory not found: {TEMPLATES_DIR}")

    # Check SEER directories
    for seer, path in SEER_DIRS.items():
        if not path.exists():
            errors.append(f"SEER directory not found: {path}")

    # Check template files exist
    all_templates = set(SINGLE_COMPONENT_TEMPLATES.values()) | set(MULTI_COMPONENT_TEMPLATES.values())
    for template in all_templates:
        template_path = TEMPLATES_DIR / template
        if not template_path.exists():
            errors.append(f"Template file not found: {template_path}")

    return errors

if __name__ == "__main__":
    # Test configuration
    print("HVAC Description Generator - Configuration Test")
    print("=" * 60)

    errors = validate_config()
    if errors:
        print("❌ Configuration Errors:")
        for error in errors:
            print(f"  - {error}")
    else:
        print("✅ All configuration validated successfully!")
        print(f"\n📁 Base Directory: {BASE_DIR}")
        print(f"📁 Templates Directory: {TEMPLATES_DIR}")
        print(f"📁 SEER Directories: {len(SEER_DIRS)}")
        print(f"📄 Single Component Templates: {len(SINGLE_COMPONENT_TEMPLATES)}")
        print(f"📄 Multi Component Templates: {len(MULTI_COMPONENT_TEMPLATES)}")
