#!/usr/bin/env python3
"""xlsx の最初のシートを CSV にする。osspublish の変換サーバ（app.rb）が cto.pl・cts.pl に
渡すもの（Roo::Spreadsheet#to_csv）と同じ形を、Python の標準ライブラリだけで作る。

    python3 tools/xlsx_to_csv.py ontology/Ontology.xlsx > ontology/Ontology.csv

Roo の to_csv にならう：最初の行・列から最後の行・列まで、文字列は "…"（" は ""）、
数は整数なら整数で、空のセルは何も書かない。日付などの書式は見ない。
"""
import re
import sys
import zipfile
import xml.etree.ElementTree as ET

NS = {'m': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main',
      'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}


def col_index(ref):
    letters = re.match(r'[A-Z]+', ref).group(0)
    n = 0
    for ch in letters:
        n = n * 26 + (ord(ch) - 64)
    return n


def main(path):
    z = zipfile.ZipFile(path)
    shared = []
    if 'xl/sharedStrings.xml' in z.namelist():
        for si in ET.fromstring(z.read('xl/sharedStrings.xml')).findall('m:si', NS):
            shared.append(''.join(t.text or '' for t in si.iter(f"{{{NS['m']}}}t")))
    wb = ET.fromstring(z.read('xl/workbook.xml'))
    first = wb.find('m:sheets/m:sheet', NS)
    rid = first.get(f"{{{NS['r']}}}id")
    rels = ET.fromstring(z.read('xl/_rels/workbook.xml.rels'))
    target = next(r.get('Target') for r in rels if r.get('Id') == rid)
    sheet = ET.fromstring(z.read('xl/' + target.lstrip('/').removeprefix('xl/')))
    cells = {}
    for c in sheet.iter(f"{{{NS['m']}}}c"):
        ref = c.get('r')
        row = int(re.search(r'\d+', ref).group(0))
        col = col_index(ref)
        t = c.get('t')
        v = c.find('m:v', NS)
        if t == 's' and v is not None:
            cells[(row, col)] = ('s', shared[int(v.text)])
        elif t == 'inlineStr':
            cells[(row, col)] = ('s', ''.join(x.text or '' for x in c.iter(f"{{{NS['m']}}}t")))
        elif t == 'str' and v is not None:
            cells[(row, col)] = ('s', v.text or '')
        elif t == 'b' and v is not None:
            cells[(row, col)] = ('n', 'TRUE' if v.text == '1' else 'FALSE')
        elif v is not None and v.text is not None:
            num = float(v.text)
            cells[(row, col)] = ('n', str(int(num)) if num == int(num) else repr(num))
    if not cells:
        return
    rows = [r for r, _ in cells]
    cols = [c for _, c in cells]
    out = sys.stdout
    for r in range(min(rows), max(rows) + 1):
        fields = []
        for c in range(min(cols), max(cols) + 1):
            kind, text = cells.get((r, c), ('e', ''))
            if kind == 's':
                fields.append('"' + text.replace('"', '""') + '"')
            else:
                fields.append(text)
        out.write(','.join(fields) + '\n')


if __name__ == '__main__':
    main(sys.argv[1])
