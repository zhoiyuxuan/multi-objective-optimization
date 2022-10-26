from docx import Document
from docx.shared import Pt
doc = Document('model.docx')
for table in doc.tables:
    for row in table.rows:
        for cell in row.cells:
            cell.text = cell.text.replace('年月日','2022年10月21日')

            print(cell.text)

doc.save(f'大连理工大学社团活动申请审批表(Kon10.21).docx')