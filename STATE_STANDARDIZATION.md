# State Name Standardization

## Official List of Indian States and Union Territories

### States (28)
1. Andhra Pradesh
2. Arunachal Pradesh
3. Assam
4. Bihar
5. Chhattisgarh
6. Goa
7. Gujarat
8. Haryana
9. Himachal Pradesh
10. Jharkhand
11. Karnataka
12. Kerala
13. Madhya Pradesh
14. Maharashtra
15. Manipur
16. Meghalaya
17. Mizoram
18. Nagaland
19. Odisha
20. Punjab
21. Rajasthan
22. Sikkim
23. Tamil Nadu
24. Telangana
25. Tripura
26. Uttar Pradesh
27. Uttarakhand
28. West Bengal

### Union Territories (8)
1. Andaman and Nicobar Islands
2. Chandigarh
3. Dadra and Nagar Haveli and Daman and Diu
4. Delhi
5. Jammu and Kashmir
6. Ladakh
7. Lakshadweep
8. Puducherry

**Total: 36 States/UTs**

## Solution

All state names in the data are now standardized to match the official list above. Any misspellings, variations, or old names are automatically mapped to the correct official name.

## Common Variations Handled

| Variations Found | Standardized To |
|------------------|-----------------|
| ODISHA, Odisha, Orissa | **Odisha** |
| WEST BENGAL, West Bengal, Westbengal, West Bangal | **West Bengal** |
| Jammu & Kashmir, Jammu And Kashmir | **Jammu and Kashmir** |
| Pondicherry | **Puducherry** |
| Uttaranchal | **Uttarakhand** |
| Dadra & Nagar Haveli, Daman & Diu | **Dadra and Nagar Haveli and Daman and Diu** |
| Delhi (National Capital Territory), NCT of Delhi | **Delhi** |
| Andaman & Nicobar Islands | **Andaman and Nicobar Islands** |

## How It Works

1. **Case-Insensitive Matching**: All comparisons ignore case
2. **Exact Mapping**: Only states in the official list are kept
3. **Invalid States Removed**: Any state not in the mapping is filtered out
4. **No Duplicates**: Aggregation ensures each state appears only once

## Expected Result

After standardization, the dropdown will show **exactly 36 states/UTs** (or fewer if some have no data):
- 28 States
- 8 Union Territories
- No duplicates
- No misspellings
- Official names only

## How to Apply

### Step 1: Delete Cached Data
```bash
# Delete these files if they exist:
del master_aadhaar_data.csv
del featured_aadhaar_data.csv
```

### Step 2: Restart Server
```bash
python start_web_interface.py
```

### Step 3: Verify
1. Open `http://localhost:5000`
2. Check "Affected States" dropdown
3. Should see exactly 36 unique states (or fewer)
4. No duplicates like "West Bengal" and "Westbengal"

## Expected Result

**Before:**
- 54 entries with duplicates
- Multiple cases and spellings
- Confusing for users

**After:**
- 36 unique states/UTs
- Consistent naming
- Clean dropdown list

## Notes

- Standardization is case-insensitive
- Handles common misspellings
- Follows official Indian state names
- Aggregates data from all variations into one state

## If You Need to Add More Mappings

Edit `data_loader.py` and add to the `state_mapping` dictionary:

```python
state_mapping = {
    # ... existing mappings ...
    'your_variation': 'Official State Name',
    'another_variation': 'Official State Name',
}
```

Then delete cached files and restart the server.
