import sys
import win32com.client as win32

path = sys.argv[1]
sheet_name = sys.argv[2]
rng = sys.argv[3]
out_png = sys.argv[4]

excel = win32.gencache.EnsureDispatch("Excel.Application")
excel.Visible = False
excel.DisplayAlerts = False
try:
    wb = excel.Workbooks.Open(path)
    ws = wb.Sheets(sheet_name)
    ws.Activate()
    r = ws.Range(rng)
    r.CopyPicture(Appearance=1, Format=2)  # xlScreen, xlBitmap
    chart = wb.Charts.Add()
    chart.Paste()
    chart.Export(out_png)
    chart.Delete()
    wb.Close(SaveChanges=False)
    print("Exported", out_png)
finally:
    excel.Quit()
