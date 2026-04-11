import xml.etree.ElementTree as ET

NS = 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'

def parse_sheet_xml(filepath):
    tree = ET.parse(filepath)
    root = tree.getroot()
    
    # Get headers from row 1
    headers = {}
    data_rows = []
    
    for row in root.iter(f'{{{NS}}}row'):
        row_num = int(row.get('r', 0))
        cells = {}
        for cell in row:
            ref = cell.get('r', '')
            col = ''.join(c for c in ref if c.isalpha())
            t = cell.get('t', '')
            v_el = cell.find(f'{{{NS}}}v')
            is_el = cell.find(f'{{{NS}}}is')
            
            if is_el is not None:
                texts = is_el.findall(f'.//{{{NS}}}t')
                val = ''.join(tx.text or '' for tx in texts)
            elif v_el is not None:
                val = v_el.text or ''
            else:
                val = ''
            cells[col] = val
        
        if row_num == 1:
            headers = cells
        else:
            data_rows.append(cells)
    
    return headers, data_rows

sheets = {
    'Summary': '/Users/mike/.openclaw/workspace-bacottibot/kdp_sheets/worksheets_sheet2.xml',
    'Combined Sales': '/Users/mike/.openclaw/workspace-bacottibot/kdp_sheets/worksheets_sheet3.xml',
    'eBook Royalty': '/Users/mike/.openclaw/workspace-bacottibot/kdp_sheets/worksheets_sheet4.xml',
    'Paperback Royalty': '/Users/mike/.openclaw/workspace-bacottibot/kdp_sheets/worksheets_sheet5.xml',
    'Hardcover Royalty': '/Users/mike/.openclaw/workspace-bacottibot/kdp_sheets/worksheets_sheet6.xml',
    'Audiobook Royalty': '/Users/mike/.openclaw/workspace-bacottibot/kdp_sheets/worksheets_sheet7.xml',
    'Orders Processed': '/Users/mike/.openclaw/workspace-bacottibot/kdp_sheets/worksheets_sheet8.xml',
    'eBook Orders Placed': '/Users/mike/.openclaw/workspace-bacottibot/kdp_sheets/worksheets_sheet9.xml',
    'KENP': '/Users/mike/.openclaw/workspace-bacottibot/kdp_sheets/worksheets_sheet10.xml',
}

for name, path in sheets.items():
    print(f"\n{'='*80}")
    print(f"SHEET: {name}")
    print('='*80)
    headers, rows = parse_sheet_xml(path)
    print(f"Headers: {headers}")
    print(f"Total rows: {len(rows)}")
    for r in rows[:50]:
        if any(v for v in r.values()):
            print(r)
