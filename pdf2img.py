import pdfplumber
import plotdigitizer

reportPath = r'C:\Users\921722\Box\BI3753 Team\30 - Geotech\01-Calculations\02 APM HH\01 Settlements\Layout Plans\BI3753-NAC-SK-GE-0012 - 2022 APM HH ADDITIONAL GI SETTLEMENTS AT +13mNADD.pdf'

with pdfplumber.open(reportPath) as pdf:
    totalPages = len(pdf.pages)
    for k in range(totalPages):
        testPage = pdf.pages[k]
        print(testPage.width, testPage.height)
        boundingBox = (0, 0, 1191, 842)
        target_pageLocation = testPage.crop(boundingBox, relative=False)
        im = target_pageLocation.to_image(resolution=600)
        im.save(f"img/BI3753-NAC-SK-GE-0012 - 2022 APM HH ADDITIONAL GI SETTLEMENTS AT +13mNADD", format="PNG")

