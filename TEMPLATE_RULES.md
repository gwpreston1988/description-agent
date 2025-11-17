# HVAC Description Template Rules & Guidelines

## CRITICAL: Template Structure

**USE THIS STRUCTURE ONLY:**
1. **Title** (H1)
2. **Intro Section** (gray gradient background, red left border)
3. **Technical Specifications** (H2) with tabbed tables
4. **Warranty Section** (gray gradient background)
5. **CTA Section** (professional installation + DOE compliance badge)

**DO NOT INCLUDE:**
- ❌ Component/Feature cards
- ❌ Benefits lists
- ❌ Extra fluff or sections
- ❌ Heavy gradient backgrounds on body

## CSS Styling Rules

**MUST USE THIS EXACT STYLING:**
```css
body {
    /* NO gradient background */
    /* Clean white background */
}

#product-container {
    background: #fff;  /* White only */
    max-width: 1200px;
    padding: 20px;
}

.intro-section {
    background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
    border-left: 5px solid #D53938;
}

.tab-button {
    background: #f8f9fa;
    border: 2px solid #D53938;
    color: #D53938;
}

.tab-button.active {
    background: #D53938;
    color: white;
}
```

**Brand Colors:**
- Red: `#D53938` (primary)
- Blue: `#57A9F9` (h3 headings)

## File Naming Convention

`Goodman_[Tonnage]Ton_R32_[Type]_System_[Model1]_[Model2]_[Model3].html`

**Examples:**
- `Goodman_15Ton_R32_AC_System_GLXS4BA1810_GR9S800403ANA_CAPTA2422A3.html`
- `Goodman_3Ton_R32_HeatPump_System_GLZS4BA3610_AWST36SU1310.html`

**Tonnage Format:**
- 1.5 ton = `15Ton`
- 2.0 ton = `2Ton`
- 2.5 ton = `25Ton`
- 3.0 ton = `3Ton`
- etc.

## System Types & Configurations

### Wall-Hung Systems
- **Components:** Outdoor Unit (GLXS4BA or GLZS4BA) + Wall-Hung Air Handler (AWST)
- **Tabs:** 2 tabs (Outdoor Unit, Air Handler)
- **Heat Kit:** Integrated in AWST models - extract kW from last 2 digits (05=5kW, 08=8kW, 10=10kW)
- **Title Format:** "with Wall-Hung Air Handler"

### 80% Furnace Systems (Upflow)
- **Components:** AC/HP Unit (GLXS4BA/GLZS4BA) + Furnace (GR9S800xxx) + Upflow Coil (CAPTA)
- **Tabs:** 3 tabs (Air Conditioner/Heat Pump, Gas Furnace, Evaporator Coil)
- **Title Format:** "80% AFUE AC System (Upflow Coil)" or "80% AFUE Dual Fuel System (Upflow Coil)"

### 80% Furnace Systems (Horizontal)
- **Components:** AC/HP Unit + Furnace (GR9S800xxx) + Horizontal Coil (CHPTA)
- **Tabs:** 3 tabs (Air Conditioner/Heat Pump, Gas Furnace, Evaporator Coil)
- **Title Format:** "(Horizontal Coil)"

### 92% Furnace Systems
- Same as 80% but with GR9S92xxxx furnaces
- **Title Format:** "92% AFUE..."

## Technical Specifications

### Model Decoding

**Outdoor Units:**
- GLXS4BA = AC (cooling only)
- GLZS4BA = Heat Pump (heating + cooling)
- Last 4 digits = tonnage (1810=1.5T, 2410=2T, 3010=2.5T, 3610=3T, 4210=3.5T, 4810=4T, 6010=5T)

**Furnaces:**
- GR9S800xxx = 80% AFUE
- GR9S92xxxx = 92% AFUE
- Digits after "800" or "92" = BTU input in thousands (0403=40k, 0603=60k, 0804=80k, 1005=100k)

**Coils:**
- CAPTA = Upflow/Vertical
- CHPTA = Horizontal
- First 2-4 digits indicate tonnage range

**Wall-Hung Air Handlers (AWST):**
- Last 2 digits before "A" = heat kit size in kW
- AWST18SU1305A = 5kW heat kit (17,060 BTU/h, 21.7A @ 230V, 2-stage)
- AWST30LU1308A = 8kW heat kit (27,297 BTU/h, 34.8A @ 230V, 3-stage)
- AWST36LU1310A = 10kW heat kit (34,121 BTU/h, 43.5A @ 230V, 3-stage)

### Standard Ratings
- All systems: **14.3 SEER2**
- Heat Pumps: **7.5 HSPF2**
- All use **R-32 refrigerant**
- Compressor: Single-Stage Rotary
- Metering: TXV (Thermal Expansion Valve) included

## Warranty Section

**Always include 3 cards:**
1. 10-Year Parts Warranty
2. 10-Year Compressor Warranty
3. ∞ (Lifetime) Heat Exchanger Warranty

Use infinity symbol: `∞`

## File Output Location

**ALWAYS save to:**
`/Users/georgepreston/description-agent/Description Directory/`

**NEVER save to:**
- Root of description-agent folder
- Any other location

## Workflow

1. Read SKUS file to get system combinations
2. Create descriptions in batches by category
3. Use TodoWrite tool to track progress
4. Mark todos as in_progress → completed as you go
5. Generate all files for a category before moving to next

## Content Guidelines

### Intro Section
- Brief, 1-2 paragraphs
- Mention: tonnage, SEER2, refrigerant type (R-32), key components
- For dual fuel: explain intelligent switching between heat pump and gas
- Keep professional, no excessive marketing fluff

### Technical Specs
- Use exact model numbers with "A" suffix where applicable
- Include all electrical specs (RLA, LRA, MCA, MOCP)
- Dimensions in H×W×D format
- Weight in lbs
- Line sizes in fractions (⅜", ¾", 1⅛")
- Use proper symbols: × (times), – (en dash for ranges), ° (degree)

### DOE Compliance
- AC systems: "DOE Compliant Nationwide"
- Heat Pumps: "DOE Compliant Nationwide" (meets all U.S. climate zones)

## Reference Example

When unsure, refer to completed 92% Dual Fuel Horizontal systems in:
`/Users/georgepreston/Library/CloudStorage/OneDrive-SharedLibraries-AmericanComfortAC/BCD Shared Files - Documents/Big Commerce Descriptions/Live/`

**But remember: Remove component cards from the template!**

## Quick Checklist

Before generating descriptions:
- [ ] Correct template structure (no component cards)
- [ ] White background on body
- [ ] Simple gray gradient on intro/warranty/CTA sections
- [ ] 3-tab structure for furnace systems, 2-tab for wall-hung
- [ ] All files go to Description Directory
- [ ] Use TodoWrite to track progress
- [ ] Proper file naming with tonnage format
- [ ] Include all 3 warranty cards with infinity symbol
- [ ] Verify model numbers and specifications

---

**Last Updated:** 2025-11-12
**Current Progress:** 12/105 descriptions complete (Wall-hung systems done)
