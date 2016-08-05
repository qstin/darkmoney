import pdfquery
def scrape(pdf):
    pdf = pdfquery.PDFQuery(pdf)
    pdf.load()
    label = pdf.pq('LTTextLineHorizontal:contains("Transaction Date")')
    left_corner = float(label.attr('x0'))
    bottom_corner = float(label.attr('y0'))
    bottom_corner1 = bottom_corner - 30

    row = 'Advocating'
    while 'Advocating' in row:
        if row != 'Advocating':
            print(row)
        row = pdf.pq('LTTextLineHorizontal:in_bbox("%s, %s, %s, %s")' % (left_corner,
        bottom_corner1, left_corner+1200, bottom_corner)).text()
        bottom_corner1 -= 40
        bottom_corner -= 40

