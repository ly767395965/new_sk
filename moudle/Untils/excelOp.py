#!/usr/bin/python3
import xlrd


class excelOp:
    def testRd(self,path):
        workbook = xlrd.open_workbook(r'C:\release\doc\test.xls')
        sheet1_name = workbook.sheet_names()[0]  # 获取第几个sheet的名字  从0开始
        print(sheet1_name)
        sheet1 = workbook.sheet_by_name('Sheet1')

        rows = sheet1.row_values(3)  # 获取第四行内容
        cols = sheet1.col_values(2)  # 获取第三列内容
        val1 = sheet1.cell(1, 0).value.encode('utf-8')  # 这三个可获取具体的值, 如果为乱码可去掉encode方法,或更换编码  (1,0) 表示获取第二行第一列的值
        val2 = sheet1.cell_value(1, 0).encode('utf-8')
        val3 = sheet1.row(1)[0].value.encode('utf-8')

    def dfskExcelRd(self, path):  # 东方excel读取
        print()


