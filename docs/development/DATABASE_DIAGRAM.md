# Database Schema Diagram

## Entity Relationship Diagram

```
┌─────────────────────────────────────┐
│        dropdown_group               │
├─────────────────────────────────────┤
│ id (PK)          INTEGER             │
│ text             VARCHAR(100)        │
│ value            VARCHAR(100)        │
│ is_active        BOOLEAN             │
│ created_at       DATETIME            │
└─────────────────────────────────────┘
          │
          │ 1
          │
          │ Has Many
          │
          │ *
          ▼
┌─────────────────────────────────────┐
│       dropdown_master               │
├─────────────────────────────────────┤
│ id (PK)          INTEGER             │
│ group_id (FK)    INTEGER             │◄──── Links to dropdown_group.id
│ text             VARCHAR(200)        │
│ value            VARCHAR(200)        │
│ is_active        BOOLEAN             │
│ sort_order       INTEGER             │
│ created_at       DATETIME            │
└─────────────────────────────────────┘
```

## Data Flow

```
┌──────────────┐
│   Browser    │
│  (User View) │
└──────┬───────┘
       │ 1. Request page
       ▼
┌──────────────────┐
│   Django View    │
│ candidate_profile│
│    _detail()     │
└──────┬───────────┘
       │ 2. Query database
       ▼
┌──────────────────┐
│   Database       │
│ - DropdownGroup  │
│ - DropdownMaster │
└──────┬───────────┘
       │ 3. Return data
       ▼
┌──────────────────┐
│  Django View     │
│  (Prepare context│
│   with data)     │
└──────┬───────────┘
       │ 4. Pass to template
       ▼
┌──────────────────┐
│   Template       │
│ candidate-profile│
│     .html        │
└──────┬───────────┘
       │ 5. Render dropdowns
       ▼
┌──────────────────┐
│   Browser        │
│ (Shows dropdowns │
│  from database)  │
└──────────────────┘
```

## Sample Data Structure

```
dropdown_group
├── 1: Education
│   └── dropdown_master
│       ├── 1: High School
│       ├── 2: Intermediate
│       ├── 3: Bachelor's Degree
│       ├── 4: Master's Degree
│       ├── 5: Post Graduate
│       └── 6: PhD
│
├── 2: Experience
│   └── dropdown_master
│       ├── 7: Fresher
│       ├── 8: 1+ Year
│       ├── 9: 2+ Years
│       ├── 10: 3+ Years
│       ├── 11: 4+ Years
│       ├── 12: 5+ Years
│       ├── 13: 7+ Years
│       └── 14: 10+ Years
│
├── 3: Country
│   └── dropdown_master
│       ├── 15: India
│       ├── 16: United States
│       ├── 17: United Kingdom
│       ├── 18: Australia
│       ├── 19: Russia
│       ├── 20: Canada
│       ├── 21: Germany
│       ├── 22: France
│       ├── 23: China
│       └── 24: Japan
│
└── 4: State/City
    └── dropdown_master
        ├── 25: California
        ├── 26: Denver
        ├── 27: New York
        ├── 28: Toronto
        ├── 29: Warsaw
        ├── 30: Mumbai
        ├── 31: Delhi
        ├── 32: Bangalore
        ├── 33: London
        └── 34: Sydney
```

## How Template Renders Dropdown

### Before (Hardcoded):
```html
<select>
    <option value="1">High School</option>
    <option value="2">Intermediate</option>
    <option value="3">Bachelor Degree</option>
</select>
```

### After (Database-Driven):
```html
<select name="education">
    <option value="">Select Education</option>
    {% for item in education_items %}
    <option value="{{ item.value }}">{{ item.text }}</option>
    {% endfor %}
</select>
```

### Rendered Output:
```html
<select name="education">
    <option value="">Select Education</option>
    <option value="High School">High School</option>
    <option value="Intermediate">Intermediate</option>
    <option value="Bachelor's Degree">Bachelor's Degree</option>
    <option value="Master's Degree">Master's Degree</option>
    <option value="Post Graduate">Post Graduate</option>
    <option value="PhD">PhD</option>
</select>
```

## Code Flow Example

### 1. View Code
```python
def candidate_profile_detail(request, username):
    # Fetch from database
    education_items = DropdownMaster.objects.filter(
        group__text='Education', 
        is_active=True
    )
    
    # Pass to template
    context = {
        'education_items': education_items,
        # ... other data
    }
    
    return render(request, 'candidate-profile.html', context)
```

### 2. Template Code
```html
<select name="education">
    <option value="">Select Education</option>
    {% for item in education_items %}
    <option value="{{ item.value }}">{{ item.text }}</option>
    {% endfor %}
</select>
```

### 3. Database Query (Behind the scenes)
```sql
SELECT * FROM dropdown_master 
WHERE group_id = (
    SELECT id FROM dropdown_group WHERE text = 'Education'
) 
AND is_active = 1
ORDER BY sort_order, text;
```

## Admin Interface Flow

```
┌──────────────────┐
│  Admin visits:   │
│ /admin/App/      │
│ dropdownmaster/  │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Django Admin    │
│  Shows list of   │
│  all dropdown    │
│  items           │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Admin can:      │
│  - Add new item  │
│  - Edit item     │
│  - Delete item   │
│  - Change order  │
│  - Toggle active │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Changes saved   │
│  to database     │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Dropdown on     │
│  candidate       │
│  profile updates │
│  immediately!    │
└──────────────────┘
```

## File Structure

```
Jobstock_Django/
│
├── App/
│   ├── models.py                    ← DropdownGroup, DropdownMaster classes
│   ├── admin.py                     ← Admin registration
│   ├── views.py                     ← candidate_profile_detail()
│   │
│   └── management/
│       └── commands/
│           └── populate_dropdowns.py ← Data population command
│
├── templates/
│   └── pages/
│       └── candidate-profile.html   ← Updated dropdowns
│
├── db.sqlite3                        ← Database with new tables
│
├── verify_dropdowns.py               ← Verification script
├── DROPDOWN_IMPLEMENTATION.md        ← Full documentation
├── STORING_USER_SELECTIONS.md        ← User selection guide
├── QUICK_START_GUIDE.md              ← Quick reference
└── DATABASE_DIAGRAM.md               ← This file
```

## Database Tables in SQLite

### View tables in SQLite:
```bash
python manage.py dbshell
```

```sql
-- List all tables
.tables

-- View dropdown_group table
SELECT * FROM dropdown_group;

-- View dropdown_master table
SELECT * FROM dropdown_master;

-- View data by group
SELECT 
    dg.text as group_name,
    dm.text as item_name,
    dm.sort_order
FROM dropdown_master dm
JOIN dropdown_group dg ON dm.group_id = dg.id
ORDER BY dg.id, dm.sort_order;

-- Count items per group
SELECT 
    dg.text as group_name,
    COUNT(dm.id) as item_count
FROM dropdown_group dg
LEFT JOIN dropdown_master dm ON dg.id = dm.group_id
GROUP BY dg.id;
```

## Relationship Cardinality

- One DropdownGroup can have Many DropdownMaster items (1:N)
- Each DropdownMaster belongs to One DropdownGroup (N:1)
- ForeignKey: `DropdownMaster.group_id → DropdownGroup.id`

## Benefits of This Structure

1. **Normalized**: No data duplication
2. **Flexible**: Easy to add categories
3. **Maintainable**: Update in one place
4. **Scalable**: Can grow to thousands of items
5. **Queryable**: Can filter and search efficiently
6. **Relational**: Maintains data integrity
