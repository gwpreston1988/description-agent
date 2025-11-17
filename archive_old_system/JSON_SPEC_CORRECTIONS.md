# JSON Spec File Corrections

## Required Changes for PDF Extraction Tool

---

## 1. Standardize Field Naming

### Current Issues:
- Some entries use `"dimensions_w"`, `"d"`, `"h"` (mixed format)
- Some entries use `"w"`, `"d"`, `"h"` (no prefix)
- Some use `"ship_weight_lbs"` (string), some use integers

### Required Standard Format:
```json
"dimensions": {
  "width": "14\"",
  "depth": "21\"",
  "height": "22\""
},
"weight": 37
```

---

## 2. Furnace Specification Corrections

### GR9S920403AN (currently line 598)
**Current:**
```json
"dimensions_w": "14\"",
"d": "28⅞",
"h": "34½"
```

**Should be:**
```json
"dimensions": {
  "width": "14\"",
  "depth": "23\"",
  "height": "34½\""
},
"cabinet_width": "14\"",
"filter_size": "(1) 16\" × 25\" (side) or (1) 14\" × 25\" (bottom)",
"temperature_rise": "30-60°F",
"vent_diameter": "2\"",
"blower_motor": "Multi-Speed ECM (9-Speed)",
"blower_hp": "1/2",
"blower_size": "10\" × 6\"",
"stages": "Single-Stage",
"min_circuit_ampacity": 9.7,
"max_breaker": 15
```

### GR9S920603BN (currently line 610)
**Current:**
```json
"dimensions_w": "17½",
"d": "28⅞",
"h": "34½"
```

**Should be:**
```json
"dimensions": {
  "width": "17½\"",
  "depth": "23\"",
  "height": "34½\""
},
"cabinet_width": "17½\"",
"filter_size": "(1) 16\" × 25\" (side or bottom)",
"temperature_rise": "35-65°F",
"vent_diameter": "2\" - 3\"",
"blower_motor": "Multi-Speed ECM (9-Speed)",
"blower_hp": "1/2",
"blower_size": "10\" × 8\"",
"stages": "Single-Stage",
"min_circuit_ampacity": 10.1,
"max_breaker": 15
```

### GR9S920804CN (currently line 634)
**Current:**
```json
"dimensions_w": "21\"",
"d": "28⅞",
"h": "34½"
```

**Should be:**
```json
"dimensions": {
  "width": "21\"",
  "depth": "23\"",
  "height": "34½\""
},
"cabinet_width": "21\"",
"filter_size": "(1) 16\" × 25\" (side or bottom)",
"temperature_rise": "35-65°F",
"vent_diameter": "2\" - 3\"",
"blower_motor": "Multi-Speed ECM (9-Speed)",
"blower_hp": "3/4",
"blower_size": "10\" × 10\"",
"stages": "Single-Stage",
"min_circuit_ampacity": 13.7,
"max_breaker": 20
```

### GR9S921005CN (currently line 677)
**Current:**
```json
"dimensions_w": "21\"",
"d": "28⅞",
"h": "34½",
"ship_weight_lbs": "142"
```

**Should be:**
```json
"dimensions": {
  "width": "21\"",
  "depth": "23\"",
  "height": "34½\""
},
"weight": 141,
"cabinet_width": "21\"",
"filter_size": "(1) 20\" × 25\" (bottom) or (2) 16\" × 25\" (side)",
"temperature_rise": "35-65°F",
"vent_diameter": "2\" - 3\"",
"blower_motor": "Multi-Speed ECM (9-Speed)",
"blower_hp": "3/4",
"blower_size": "10\" × 10\"",
"stages": "Single-Stage",
"min_circuit_ampacity": 13.7,
"max_breaker": 20
```

---

## 3. Heat Pump Specification Additions

### GLZS4BA1810 (currently line 701)
**Add these fields:**
```json
"cooling_capacity_btu": 18000,
"heating_capacity_btu": 18000,
"seer2_max": 15.2,
"hspf2_max": 7.8,
"compressor_type": "Single-Stage Rotary",
"compressor_rla": 8.2,
"compressor_lra": 41.2,
"fan_motor_type": "PSC",
"fan_motor_hp": "1/6",
"fan_motor_fla": 0.95,
"min_circuit_ampacity": 11.2,
"max_breaker": 15,
"sound_level_db": 74.0,
"refrigerant_charge_oz": 70,
"weight": 150
```

### GLZS4BA2410 (currently line 715)
**Add these fields:**
```json
"cooling_capacity_btu": 24000,
"heating_capacity_btu": 24000,
"seer2_max": 15.2,
"hspf2_max": 7.8,
"compressor_type": "Single-Stage Rotary",
"compressor_rla": 8.2,
"compressor_lra": 41.2,
"fan_motor_type": "PSC",
"fan_motor_hp": "1/6",
"fan_motor_fla": 0.95,
"min_circuit_ampacity": 11.2,
"max_breaker": 15,
"sound_level_db": 74.0,
"refrigerant_charge_oz": 70,
"weight": 150
```

### GLZS4BA3010 (currently line 729)
**Add these fields:**
```json
"cooling_capacity_btu": 30000,
"heating_capacity_btu": 30000,
"seer2_max": 15.2,
"hspf2_max": 7.8,
"compressor_type": "Single-Stage Rotary",
"compressor_rla": 10.2,
"compressor_lra": 51.0,
"fan_motor_type": "PSC",
"fan_motor_hp": "1/5",
"fan_motor_fla": 1.10,
"min_circuit_ampacity": 14.1,
"max_breaker": 20,
"sound_level_db": 77.0,
"refrigerant_charge_oz": 88,
"weight": 190
```

### GLZS4BA3610 (currently line 743)
**Add these fields:**
```json
"cooling_capacity_btu": 36000,
"heating_capacity_btu": 36000,
"seer2_max": 15.2,
"hspf2_max": 7.8,
"compressor_type": "Single-Stage Scroll",
"compressor_rla": 14.1,
"compressor_lra": 71.0,
"fan_motor_type": "PSC",
"fan_motor_hp": "1/4",
"fan_motor_fla": 1.40,
"min_circuit_ampacity": 19.2,
"max_breaker": 25,
"sound_level_db": 75.0,
"refrigerant_charge_oz": 112,
"weight": 211
```

### GLZS4BA4210 (currently line 757)
**Add these fields:**
```json
"cooling_capacity_btu": 42000,
"heating_capacity_btu": 42000,
"seer2_max": 15.2,
"hspf2_max": 7.8,
"compressor_type": "Single-Stage Scroll",
"compressor_rla": 17.9,
"compressor_lra": 90.0,
"fan_motor_type": "PSC",
"fan_motor_hp": "1/3",
"fan_motor_fla": 1.80,
"min_circuit_ampacity": 24.4,
"max_breaker": 30,
"sound_level_db": 72.0,
"refrigerant_charge_oz": 144,
"weight": 277
```

### GLZS4BA4810 (currently line 771)
**Add these fields:**
```json
"cooling_capacity_btu": 48000,
"heating_capacity_btu": 48000,
"seer2_max": 15.2,
"hspf2_max": 7.8,
"compressor_type": "Single-Stage Scroll",
"compressor_rla": 20.4,
"compressor_lra": 102.0,
"fan_motor_type": "PSC",
"fan_motor_hp": "1/3",
"fan_motor_fla": 1.80,
"min_circuit_ampacity": 27.7,
"max_breaker": 35,
"sound_level_db": 74.0,
"refrigerant_charge_oz": 156,
"weight": 284
```

### GLZS4BA6010
**Add complete entry:**
```json
"GLZS4BA6010": {
  "type": "heat_pump",
  "manufacturer": "Goodman",
  "nominal_capacity_tons_cooling": 5,
  "nominal_capacity_tons_heating": 5,
  "cooling_capacity_btu": 60000,
  "heating_capacity_btu": 60000,
  "voltage_phase": "208/230-1",
  "seer2_max": 15.2,
  "hspf2_max": 7.8,
  "refrigerant": "R-32",
  "compressor_type": "Single-Stage Scroll",
  "compressor_rla": 24.7,
  "compressor_lra": 123.0,
  "fan_motor_type": "PSC",
  "fan_motor_hp": "1/3",
  "fan_motor_fla": 1.80,
  "min_circuit_ampacity": 33.4,
  "max_breaker": 40,
  "sound_level_db": 75.0,
  "dimensions": {
    "width": "35½\"",
    "depth": "35½\"",
    "height": "39½\""
  },
  "weight": 309,
  "refrigerant_charge_oz": 192,
  "line_sizes": {
    "liquid": "⅜\"",
    "suction": "1⅛\""
  }
}
```

---

## 4. Evaporator Coil Corrections

### All CAPTA Coils - Add Missing Fields:
```json
"coil_type": "Cased Upflow",
"expansion_device": "TXV",
"refrigerant": "R-32",
"construction": "All-Aluminum A-Coil",
"cabinet_style": "Cased with Drain Pan"
```

### All CHPTA Coils - Add Missing Fields:
```json
"coil_type": "Cased Horizontal",
"expansion_device": "TXV",
"refrigerant": "R-32",
"construction": "All-Aluminum A-Coil",
"cabinet_style": "Cased with Drain Pan"
```

---

## 5. General Data Type Standards

### Numbers (no quotes):
- `"weight": 106` (not `"106"`)
- `"tonnage": 1.5` (not `"1.5"`)
- `"cooling_capacity_btu": 18000` (not `"18,000"`)
- `"seer2_max": 15.2` (not `"Up to 15.2"`)
- `"compressor_rla": 8.2` (not `"8.2 A"`)

### Strings (with quotes):
- `"voltage_phase": "208/230-1"`
- `"filter_size": "(1) 16\" × 25\""`
- `"dimensions": { "width": "14\"" }` (keep the quotes and inch marks)

---

## 6. Remove/Fix Incorrect Entries

### Lines to Remove or Fix:
- **AMST air handlers** (lines 317-416) - These have malformed dimension data (a, b, c, etc.)
- **HKTSN05X1** (line 27) - Incomplete/incorrect data
- **HKTSD15XA** (line 419) - Incomplete data
- **0230K00044** (line 594) - No useful data
- **CHPT6030D3** (line 312) - Malformed data

---

## 7. Additional Furnace Models to Add

If these models exist in your PDFs, add them:
- GR9S920403ANA (with "A" suffix)
- GR9S920603BNA (with "A" suffix)
- GR9S920804CNA (with "A" suffix)
- GR9S921005CNA (with "A" suffix)

---

## Summary of Critical Fixes:

1. ✅ Standardize all dimensions to nested object format
2. ✅ Fix all furnace depths from "28⅞" to "23\""
3. ✅ Add missing furnace specs (filter size, cabinet width, blower info)
4. ✅ Add complete heat pump electrical specs (RLA, LRA, ampacity, breaker)
5. ✅ Add heat pump weights and BTU capacities
6. ✅ Convert all numeric strings to actual numbers
7. ✅ Add coil_type field to all coils ("Cased Upflow" or "Cased Horizontal")
8. ✅ Remove malformed air handler entries
9. ✅ Fix GR9S921005CN weight from 142 to 141

---

**Once these corrections are made, the JSON will be clean and ready for automated processing!**
