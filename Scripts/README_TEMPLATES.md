# HVAC Product Description Templates - Complete Set

## Overview
This package contains 18 blank HTML templates for HVAC equipment product descriptions. All templates follow the exact structure and styling of your existing Goodman templates.

---

## SINGLE-SKU TEMPLATES (10 files)

These templates are for individual equipment pieces with a single model number.

### AC & Heat Pump Condensers
1. **template_ac_condenser_only_CORRECTED.html**
   - Air conditioner condenser unit
   - 2-card warranty (Parts + Compressor)

2. **template_heat_pump_condenser_only_CORRECTED.html**
   - Heat pump condenser unit
   - 2-card warranty (Parts + Compressor)

### Air Handlers & Coils
3. **template_air_handler_only_CORRECTED.html**
   - Multi-positional air handler
   - 1-card warranty (Parts only)

4. **template_upflow_evaporator_coil_only_CORRECTED.html**
   - Upflow evaporator coil
   - 1-card warranty (Parts only)

5. **template_horizontal_evaporator_coil_only_CORRECTED.html**
   - Horizontal evaporator coil
   - 1-card warranty (Parts only)

### Gas Furnaces
6. **template_80_percent_afue_gas_furnace_CORRECTED.html**
   - 80% AFUE gas furnace
   - 2-card warranty (Parts + Lifetime Heat Exchanger)

7. **template_92_percent_afue_gas_furnace_CORRECTED.html**
   - 92% AFUE gas furnace
   - 2-card warranty (Parts + Lifetime Heat Exchanger)

8. **template_96_percent_afue_gas_furnace_CORRECTED.html**
   - 96% AFUE gas furnace
   - 2-card warranty (Parts + Lifetime Heat Exchanger)

### Packaged Units
9. **template_packaged_gas_electric_unit_CORRECTED.html**
   - Packaged gas/electric unit
   - 2-card warranty (Parts + Compressor)

10. **template_packaged_heat_pump_electric_unit_CORRECTED.html**
    - Packaged heat pump/electric unit
    - 2-card warranty (Parts + Compressor)

---

## MULTI-SKU SYSTEM TEMPLATES (8 files)

These templates use a tab system for 2-3 component matched systems.

### 2-Component Systems
11. **template_system_ac_airhandler_CORRECTED.html**
    - AC condenser + Air handler
    - 2 tabs
    - 2-card warranty (Parts + Compressor)

12. **template_system_hp_airhandler_CORRECTED.html**
    - Heat pump + Air handler
    - 2 tabs
    - 2-card warranty (Parts + Compressor)

13. **template_system_furnace_coil_CORRECTED.html**
    - Gas furnace + Evaporator coil
    - 2 tabs
    - 2-card warranty (Parts + Lifetime Heat Exchanger)

14. **template_system_ac_coil_CORRECTED.html**
    - AC condenser + Evaporator coil
    - 2 tabs
    - 2-card warranty (Parts + Compressor)

15. **template_system_hp_coil_CORRECTED.html**
    - Heat pump + Evaporator coil
    - 2 tabs
    - 2-card warranty (Parts + Compressor)

16. **template_system_furnace_blower_motor_CORRECTED.html**
    - Gas furnace + Blower motor
    - 2 tabs
    - 2-card warranty (Parts + Lifetime Heat Exchanger)

### 3-Component Systems
17. **template_system_ac_furnace_coil_CORRECTED.html**
    - AC condenser + Gas furnace + Evaporator coil
    - 3 tabs
    - 3-card warranty (Parts + Compressor + Lifetime Heat Exchanger)

18. **template_system_hp_furnace_coil_dualfuel_CORRECTED.html**
    - Heat pump + Gas furnace + Evaporator coil (Dual Fuel)
    - 3 tabs
    - 3-card warranty (Parts + Compressor + Lifetime Heat Exchanger)

---

## TEMPLATE STRUCTURE

Every template follows this exact order:

1. **H1 Title** - `[PRODUCT TITLE PLACEHOLDER]`
2. **Intro Section** - `[INTRO PARAGRAPH PLACEHOLDER]`
3. **H2 "Technical Specifications"**
4. **Single Unified Spec Table** (Single-SKU) OR **Tab System with Spec Tables** (Multi-SKU)
   - All specifications in ONE table with two columns: "Specification" and "Value"
   - Multi-SKU templates have one table per component tab
5. **Warranty Section** (1, 2, or 3 cards depending on equipment type)
6. **CTA Section** - "Professional Installation Required"
7. **Compliance Badge Footer** - TWO versions included (see below)

---

## FOOTER TYPES

Each template includes BOTH footer types. You must manually delete the one you don't need.

### Footer Type A - FOR BELOW 14.3 SEER2 (Northern Regions Only)
**Title:** DOE Compliant for Northern Regions

**Text:** "This equipment is approved by the Department of Energy only for use in Northern U.S. climate zones. Check state and local codes and ordinances before purchasing. Product availability and compliance requirements may vary by region."

**Use for:** Any equipment with SEER2 rating below 14.3 (includes 13.4, 13.5, 13.6, 13.7, 13.8, 13.9, 14.0, 14.1, 14.2)

### Footer Type B - FOR 14.3 SEER2 AND ABOVE (Nationally Approved)
**Title:** DOE Compliant

**Text:** "This equipment meets Department of Energy minimum efficiency requirements for all U.S. climate zones. Check state and local codes and ordinances before purchasing. Product availability and compliance requirements may vary by region."

**Use for:** Any equipment with SEER2 rating 14.3 or higher (includes 14.3, 14.4, 14.5, 15.0, 15.2, 16.0, etc.)

---

## FOOTER SELECTION LOGIC

**Simple Rule:**
- SEER2 < 14.3 → Use Footer Type A (delete Footer Type B)
- SEER2 ≥ 14.3 → Use Footer Type B (delete Footer Type A)

**Examples:**
- 13.4 SEER2 → Footer Type A
- 14.2 SEER2 → Footer Type A
- 14.3 SEER2 → Footer Type B
- 15.2 SEER2 → Footer Type B

---

## HOW TO USE

1. **Select the appropriate template** for your equipment type
2. **Fill in all placeholders:**
   - `[PRODUCT TITLE PLACEHOLDER]`
   - `[INTRO PARAGRAPH PLACEHOLDER]`
   - All `[VALUE]` entries in spec tables
   - For multi-SKU: Update component names in tab buttons and H3 headers
3. **Delete the footer you don't need:**
   - If SEER2 < 14.3: Keep Footer Type A, delete Footer Type B
   - If SEER2 ≥ 14.3: Delete Footer Type A, keep Footer Type B
4. **Save and deploy**

---

## STYLING NOTES

- All styling is preserved from original Goodman templates
- Goodman colors: Red (#D53938), Blue (#57A9F9)
- Light gray CTA section background (#F8F9FA)
- Red compliance badge border with light red background tint
- Table hover effects turn rows red with white text
- Table striping (even rows light gray)
- Mobile-responsive design included
- Tab functionality for multi-SKU templates works via included JavaScript

---

## KEY DIFFERENCES FROM ORIGINAL TEMPLATES

✅ **CTA Section:** Light gray background (not red)
✅ **Compliance Badge:** Red border with light red tint (not white overlay)
✅ **Spec Tables:** Single unified table (not 4 separate tables)
✅ **Footer Logic:** Clear threshold at 14.3 SEER2
✅ **Footer Wording:** Uses "equipment" (never "system")

---

## IMPORTANT REMINDERS

✔ NEVER change "equipment" to "system" in footers
✔ Both footer types are included in every template
✔ Multi-SKU templates have identical spec table structure in each tab
✔ Warranty cards automatically adjust to 1, 2, or 3 columns
✔ All templates are mobile-responsive
✔ All spec values go in ONE unified table per component

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

---

## TECHNICAL SPECIFICATIONS TABLE STRUCTURE

Every spec table follows this format:

```html
<table class="specs-table">
    <thead>
        <tr>
            <th>Specification</th>
            <th>Value</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><strong>Manufacturer</strong></td>
            <td>Goodman</td>
        </tr>
        <tr>
            <td><strong>Model Number</strong></td>
            <td>[MODEL]</td>
        </tr>
        <!-- Additional rows as needed -->
    </tbody>
</table>
```

No separate Performance/Electrical/Refrigeration/Physical tables. Everything in one unified table.
