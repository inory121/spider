import xlwt

workbook = xlwt.Workbook(encoding="utf-8")
worksheet = workbook.add_sheet('sheet1')
# worksheet.write(0, 0, 'hello')
# workbook.save('student.xls')
for i in range(0,7):
    for j in range(0,7):
        worksheet.write(i,j,)
workbook.save('student.xls')