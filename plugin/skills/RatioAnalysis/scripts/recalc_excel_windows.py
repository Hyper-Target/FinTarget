import sys
import win32com.client as win32

path = sys.argv[1]

excel = win32.gencache.EnsureDispatch("Excel.Application")
excel.Visible = False
excel.DisplayAlerts = False
try:
    wb = excel.Workbooks.Open(path)
    excel.CalculateFullRebuild()
    wb.Save()
    wb.Close(SaveChanges=True)
    print("Recalc OK")
finally:
    excel.Quit()
