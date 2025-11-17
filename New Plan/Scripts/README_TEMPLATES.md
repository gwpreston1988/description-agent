# HVAC Product Description Templates - Complete Set

## Overview
This package contains 18 blank HTML templates for HVAC equipment product descriptions. All templates follow the exact structure and styling of your existing Goodman templates.

---

## SINGLE-SKU TEMPLATES (10 files)

These templates are for individual equipment pieces with a single model number.

### AC & Heat Pump Condensers
1. **template_ac_condenser_only.html**
   - Air conditioner condenser unit
   - 2-card warranty (Parts + Compressor)

2. **template_heat_pump_condenser_only.html**
   - Heat pump condenser unit
   - 2-card warranty (Parts + Compressor)

### Air Handlers & Coils
3. **template_air_handler_only.html**
   - Multi-positional air handler
   - 2-card warranty (Parts + Compressor)

4. **template_upflow_evaporator_coil_only.html**
   - Upflow evaporator coil
   - 2-card warranty (Parts + Compressor)

5. **template_horizontal_evaporator_coil_only.html**
   - Horizontal evaporator coil
   - 2-card warranty (Parts + Compressor)

### Gas Furnaces
6. **template_80_percent_afue_gas_furnace.html**
   - 80% AFUE gas furnace
   - 3-card warranty (Parts + Compressor + Lifetime Heat Exchanger)

7. **template_92_percent_afue_gas_furnace.html**
   - 92% AFUE gas furnace
   - 3-card warranty (Parts + Compressor + Lifetime Heat Exchanger)

8. **template_96_percent_afue_gas_furnace.html**
   - 96% AFUE gas furnace
   - 3-card warranty (Parts + Compressor + Lifetime Heat Exchanger)

### Packaged Units
9. **template_packaged_gas_electric_unit.html**
   - Packaged gas/electric unit
   - 3-card warranty (Parts + Compressor + Lifetime Heat Exchanger)

10. **template_packaged_heat_pump_electric_unit.html**
    - Packaged heat pump/electric unit
    - 2-card warranty (Parts + Compressor)

---

## MULTI-SKU SYSTEM TEMPLATES (8 files)

These templates use a tab system for 2-3 component matched systems.

### 2-Component Systems
11. **template_system_ac_airhandler.html**
    - AC condenser + Air handler
    - 2 tabs
    - 2-card warranty

12. **template_system_hp_airhandler.html**
    - Heat pump + Air handler
    - 2 tabs
    - 2-card warranty

13. **template_system_furnace_coil.html**
    - Gas furnace + Evaporator coil
    - 2 tabs
    - 3-card warranty (includes Lifetime Heat Exchanger)

14. **template_system_ac_coil.html**
    - AC condenser + Evaporator coil
    - 2 tabs
    - 2-card warranty

15. **template_system_hp_coil.html**
    - Heat pump + Evaporator coil
    - 2 tabs
    - 2-card warranty

16. **template_system_furnace_blower_motor.html**
    - Gas furnace + Blower motor
    - 2 tabs
    - 3-card warranty (includes Lifetime Heat Exchanger)

### 3-Component Systems
17. **template_system_ac_furnace_coil.html**
    - AC condenser + Gas furnace + Evaporator coil
    - 3 tabs
    - 3-card warranty (includes Lifetime Heat Exchanger)

18. **template_system_hp_furnace_coil_dualfuel.html**
    - Heat pump + Gas furnace + Evaporator coil (Dual Fuel)
    - 3 tabs
    - 3-card warranty (includes Lifetime Heat Exchanger)

---

## TEMPLATE STRUCTURE

Every template follows this exact order:

1. **H1 Title** - `[PRODUCT TITLE PLACEHOLDER]`
2. **Intro Section** - `[INTRO PARAGRAPH PLACEHOLDER]`
3. **H2 "Technical Specifications"**
4. **Spec Tables** (Single-SKU) OR **Tab System** (Multi-SKU)
   - Each tab contains identical spec table structure
   - Tables: Performance / Electrical / Refrigeration / Physical
5. **Warranty Section** (2 or 3 cards depending on equipment type)
6. **CTA Section** - "Professional Installation Required"
7. **Compliance Badge Footer** - TWO versions included (see below)

---

## FOOTER TYPES

Each template includes BOTH footer types. You must manually delete the one you don't need.

### Footer Type A - FOR 13.4 SEER2 OR LOWER
**Title:** DOE Compliant for Northern Regions
**Text:** "This equipment is approved by the Department of Energy only for use in Northern U.S. climate zones. Check state and local codes and ordinances before purchasing. Product availability and compliance requirements may vary by region."

**Use for:** Equipment with SEER2 rating below 14.3 (only legal in Northern regions)

### Footer Type B - FOR 14.3 SEER2 OR HIGHER
**Title:** DOE Compliant
**Text:** "This equipment meets Department of Energy minimum efficiency requirements for all U.S. climate zones. Check state and local codes and ordinances before purchasing. Product availability and compliance requirements may vary by region."

**Use for:** Equipment with SEER2 rating 14.3 or higher (nationally approved)

---

## HOW TO USE

1. **Select the appropriate template** for your equipment type
2. **Fill in all placeholders:**
   - `[PRODUCT TITLE PLACEHOLDER]`
   - `[INTRO PARAGRAPH PLACEHOLDER]`
   - `[SPEC NAME]` and `[SPEC VALUE]` in tables
   - For multi-SKU: `[COMPONENT 1 NAME]`, `[COMPONENT 2 NAME]`, `[COMPONENT 3 NAME]`
3. **Delete the footer you don't need:**
   - If SEER2 ≤ 13.4: Keep Footer Type A, delete Footer Type B
   - If SEER2 ≥ 14.3: Delete Footer Type A, keep Footer Type B
4. **Save and deploy**

---

## STYLING NOTES

- All styling is preserved from original Goodman templates
- Goodman colors: Red (#D53938), Blue (#57A9F9)
- Hover effects, table striping, and mobile responsiveness included
- No modifications to CSS should be necessary
- Tab functionality for multi-SKU templates works via included JavaScript

---

## IMPORTANT REMINDERS

✓ NEVER change "equipment" to "system" in footers
✓ Both footer types are included in every template
✓ Multi-SKU templates have identical spec table structure in each tab
✓ Warranty cards automatically adjust to 2 or 3 columns
✓ All templates are mobile-responsive

---

## FILES SUMMARY

**10 Single-SKU Templates**
- 2 Condensers (AC, HP)
- 1 Air Handler
- 2 Evaporator Coils (Upflow, Horizontal)
- 3 Gas Furnaces (80%, 92%, 96% AFUE)
- 2 Packaged Units (Gas/Electric, HP/Electric)

**8 Multi-SKU System Templates**
- 6 Two-component systems
- 2 Three-component systems

**Total: 18 Complete Templates**