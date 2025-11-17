# Goodman 15.2 SEER2 Outdoor Units - Spec Extraction

## Objective
Extract technical specifications for the Goodman 15.2 SEER2 **outdoor units** from PDF documentation, then combine with the indoor equipment from the 13.4 SEER system to create a complete `15.2_SEER.json` file.

**SIMPLE PROCESS**:
1. Extract specs for the 14 outdoor units (7 GLZS5BA heat pumps + 7 GLXS5BA AC units) from the PDFs
2. Copy ALL indoor equipment specs from `13-4-specs.json` (coils, air handlers, furnaces, heat kits)
3. Combine into `15.2_SEER.json` - outdoor units at the top, indoor units below

**The 15.2 SEER2 outdoor units pair with the same indoor equipment as the 13.4 SEER system**, so just copy those specs over!

## Target Equipment

**ONLY EXTRACT THESE FROM PDFs** (outdoor units only):

### Outdoor Units

### Heat Pumps (GLZS5BA Series)
- GLZS5BA1810 (1.5 ton)
- GLZS5BA2410 (2 ton)
- GLZS5BA3010 (2.5 ton)
- GLZS5BA3610 (3 ton)
- GLZS5BA4210 (3.5 ton)
- GLZS5BA4810 (4 ton)
- GLZS5BA6010 (5 ton)

### Air Conditioner Condensers (GLXS5BA Series)
- GLXS5BA1810 (1.5 ton)
- GLXS5BA2410 (2 ton)
- GLXS5BA3010 (2.5 ton)
- GLXS5BA3610 (3 ton)
- GLXS5BA4210 (3.5 ton)
- GLXS5BA4810 (4 ton)
- GLXS5BA6010 (5 ton)

**For indoor equipment**: Copy directly from `13-4-specs.json` file (coils, air handlers, furnaces, heat kits)

## Important Notes

### Indoor Equipment is Same as 13.4 SEER System
The 15.2 SEER2 outdoor units use the **exact same indoor equipment** as the 13.4 SEER system. Instead of re-extracting from PDFs:

**COPY all indoor equipment from `13-4-specs.json`**:
- Air Handlers (ARUF/AMST/AWST series)
- Heat Kits (HKTSN/HKTSD series)
- 80% Furnaces (GR9S800 series)
- 96% Furnaces (GR9S920/GR9S921 series)
- Upflow Coils (CAPTA series)
- Horizontal Coils (CHPTA series)

**Your task**:
1. Extract ONLY the 14 outdoor units from the PDFs (7 heat pumps + 7 AC units)
2. Copy ALL indoor equipment entries from `13-4-specs.json`
3. Combine them into `15.2_SEER.json` (outdoor units first, then indoor units)

## JSON Template Structure

**Reference**: The file `15.2_SEER.json` in your directory contains the template structures to follow.

**For outdoor units you extract from PDFs, use these templates**:

### For Heat Pump Condensers
- Use the field structure from `template_heat_pump_condenser` in the existing file
- Key fields: model_number, brand, equipment_type, tonnage, cooling_capacity_btuh, heating_capacity_btuh, seer2, eer2, hspf2, low_ambient_cooling, voltage, phase, mca, mop, refrigerant_type, factory_charge_oz, line sizes, compressor_type, defrost_type, sound_level_dba, dimensions, shipping_weight_lb

### For Air Conditioner Condensers
- Use the field structure from `template_air_conditioner_condenser` in the existing file  
- Key fields: model_number, brand, equipment_type, tonnage, cooling_capacity_btuh, seer2, eer2, voltage, phase, mca, mop, refrigerant_type, factory_charge_oz, line sizes, compressor_type, sound_level_dba, dimensions, shipping_weight_lb

**For indoor equipment**: Simply copy the existing entries from `13-4-specs.json` - they're already in the correct format!

## Key Specifications to Extract

### Critical Fields (Priority 1)
- Model number
- Tonnage (1.5, 2, 2.5, 3, 3.5, 4, 5)
- Cooling capacity (BTUH)
- Heating capacity (BTUH) - heat pumps only
- SEER2 rating
- EER2 rating
- HSPF2 rating - heat pumps only

### Electrical Specifications (Priority 2)
- Voltage (typically 208-230V)
- Phase (single phase = 1)
- Frequency (60 Hz)
- MCA (Minimum Circuit Ampacity)
- MOP (Maximum Overcurrent Protection)

### Refrigerant & Lines (Priority 3)
- Refrigerant type (typically R-410A)
- Factory charge (oz)
- Liquid line OD (inches)
- Suction line OD (inches)

### Physical Specifications (Priority 4)
- Height (inches)
- Width (inches)
- Depth (inches)
- Shipping weight (lbs)
- Sound level (dBA)

### Additional Technical Details
- Compressor type (scroll, rotary, etc.)
- Defrost type (heat pumps only)
- Low ambient cooling capability (heat pumps only)

## Output Format

**CRITICAL: Use the JSON template structure with model numbers as top-level keys**

### Structure Requirements:
1. **Top-level keys**: Use model number (e.g., `"GLZS5BA3610"`)
2. **Organize**: Heat pumps first (GLZS5BA series), then AC units (GLXS5BA series)
3. **Sort**: By tonnage within each category (1.5, 2, 2.5, 3, 3.5, 4, 5 ton)
4. **Include ALL fields** from the templates, even if null

### Heat Pump Output Example:
```json
{
  "GLZS5BA3610": {
    "model_number": "GLZS5BA3610",
    "brand": "Goodman",
    "equipment_type": "Heat Pump Condenser",
    "tonnage": 3.0,
    "cooling_capacity_btuh": 36000,
    "heating_capacity_btuh": null,
    "seer2": 15.2,
    "eer2": null,
    "hspf2": null,
    "low_ambient_cooling": null,
    "voltage": "208/230",
    "phase": 1,
    "frequency_hz": 60,
    "mca": null,
    "mop": null,
    "refrigerant_type": "R-410A",
    "factory_charge_oz": null,
    "liquid_line_od_in": null,
    "suction_line_od_in": null,
    "compressor_type": null,
    "defrost_type": null,
    "sound_level_dba": null,
    "height_in": null,
    "width_in": null,
    "depth_in": null,
    "shipping_weight_lb": null
  }
}
```

### AC Condenser Output Example:
```json
{
  "GLXS5BA3610": {
    "model_number": "GLXS5BA3610",
    "brand": "Goodman",
    "equipment_type": "Air Conditioner Condenser",
    "tonnage": 3.0,
    "cooling_capacity_btuh": 36000,
    "seer2": 15.2,
    "eer2": null,
    "voltage": "208/230",
    "phase": 1,
    "frequency_hz": 60,
    "mca": null,
    "mop": null,
    "refrigerant_type": "R-410A",
    "factory_charge_oz": null,
    "liquid_line_od_in": null,
    "suction_line_od_in": null,
    "compressor_type": null,
    "sound_level_dba": null,
    "height_in": null,
    "width_in": null,
    "depth_in": null,
    "shipping_weight_lb": null
  }
}
```

## File Naming & Location Convention
- **File name**: `15.2_SEER.json` (already exists in the directory with templates)
- **Action**: **REPLACE** the entire contents of `15.2_SEER.json` with the extracted + copied specs
- **Remove**: All template entries (template_air_conditioner_condenser, template_heat_pump_condenser, template_gas_furnace, template_air_handler, template_evaporator_coil, template_heat_kit, template_gas_electric_package_unit, template_electric_package_unit)
- **Include**: 
  - 14 outdoor units extracted from PDFs (GLZS5BA and GLXS5BA series)
  - ALL indoor equipment copied from `13-4-specs.json` (coils, air handlers, furnaces, heat kits)
- **Total**: 50+ equipment entries (14 outdoor + ~40+ indoor units)

### Data Type Requirements:
- `tonnage`: Number (e.g., 1.5, 2.0, 3.0, not "1.5 ton")
- `cooling_capacity_btuh`: Number (e.g., 36000, not "36,000 BTU/h")
- `heating_capacity_btuh`: Number (heat pumps only)
- `seer2`, `eer2`, `hspf2`: Number or null
- `voltage`: String (e.g., "208/230")
- `phase`: Number (typically 1)
- `mca`, `mop`: Number (decimal if needed, e.g., 17.5, 30.0)
- `factory_charge_oz`: Number (e.g., 74.0)
- `liquid_line_od_in`, `suction_line_od_in`: Number (decimal, e.g., 0.375, 0.875)
- All dimensions: Numbers (e.g., 32.5, not "32.5 inches")
- `shipping_weight_lb`: Number (e.g., 136.0)

### Expected File Structure (Final Result):
The `15.2_SEER.json` file should contain:
1. **14 outdoor units** extracted from PDFs
2. **All indoor equipment** copied from `13-4-specs.json`

```json
{
  // === OUTDOOR UNITS (extracted from PDFs) ===
  "GLZS5BA1810": { /* 1.5 ton heat pump specs */ },
  "GLZS5BA2410": { /* 2 ton heat pump specs */ },
  "GLZS5BA3010": { /* 2.5 ton heat pump specs */ },
  "GLZS5BA3610": { /* 3 ton heat pump specs */ },
  "GLZS5BA4210": { /* 3.5 ton heat pump specs */ },
  "GLZS5BA4810": { /* 4 ton heat pump specs */ },
  "GLZS5BA6010": { /* 5 ton heat pump specs */ },
  "GLXS5BA1810": { /* 1.5 ton AC specs */ },
  "GLXS5BA2410": { /* 2 ton AC specs */ },
  "GLXS5BA3010": { /* 2.5 ton AC specs */ },
  "GLXS5BA3610": { /* 3 ton AC specs */ },
  "GLXS5BA4210": { /* 3.5 ton AC specs */ },
  "GLXS5BA4810": { /* 4 ton AC specs */ },
  "GLXS5BA6010": { /* 5 ton AC specs */ },
  
  // === INDOOR EQUIPMENT (copied from 13-4-specs.json) ===
  "CAPTA1824A4": { /* evaporator coil - copied */ },
  "CHPTA1824A4": { /* evaporator coil - copied */ },
  "ARUF25B14": { /* air handler - copied */ },
  "GR9S800603BNA": { /* gas furnace - copied */ },
  "HKTSN0501": { /* heat kit - copied */ },
  /* ... ALL other indoor equipment from 13-4-specs.json ... */
}
```

**All template entries removed. Just real equipment data (14 extracted + indoor equipment copied).**

## System Pairing Information
These outdoor units pair with the indoor equipment from the 13.4 SEER system. Contractors can mix and match:
- Any outdoor unit with compatible tonnage air handler
- Air handlers can be paired with electric heat kits (HKTSN/HKTSD series)
- Air handlers can be paired with gas furnaces (GR9S series)
- Evaporator coils (CAPTA/CHPTA) match with furnaces by tonnage

## Final Checklist

Before completing the task, verify:
- [ ] All 7 GLZS5BA heat pump models extracted from PDFs
- [ ] All 7 GLXS5BA air conditioner models extracted from PDFs
- [ ] Opened `13-4-specs.json` file
- [ ] Copied ALL indoor equipment from `13-4-specs.json` (coils, air handlers, furnaces, heat kits)
- [ ] Combined outdoor units + indoor equipment into `15.2_SEER.json`
- [ ] All 8 template entries removed from `15.2_SEER.json`
- [ ] Final JSON file contains outdoor units at top, indoor units below
- [ ] No null values, no templates in final file

**SIMPLE FORMULA**: 14 outdoor units (from PDFs) + ALL indoor equipment (from 13-4-specs.json) = Complete 15.2_SEER.json

The final file should have 50+ equipment entries total.