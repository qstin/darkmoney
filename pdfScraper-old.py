import pdfquery

def scrape(pdf_file):
    """Uses the coordinates of a defined bounding box below 'Transaction Date'
       and subtracts by 40px until each row has been stored as a string in a
       list.

       return list of rows
    """
    pdf = pdfquery.PDFQuery(pdf_file)
    pdf.load()
    num_pages = 0
    for page in pdf.get_layouts():
        num_pages += 1

    pdf = pdfquery.PDFQuery(pdf_file)
    pdf.load(1)
    label = pdf.pq('LTTextLineHorizontal:contains("Transaction Date")')
    left_corner = float(label.attr('x0'))   #x0
    bottom_corner = float(label.attr('y0')) #y0
    bottom_corner1 = bottom_corner - 22.5     #y1

    row = 'Advocating'
    rows = []
    # Check for the word 'Advocating' to eliminate invalid rows or blank lines
    while 'Advocating' in row:
        if row != 'Advocating':
            rows.append(row)
        row = pdf.pq('LTTextLineHorizontal:in_bbox("%s, %s, %s, %s")' % (left_corner,
        bottom_corner1, left_corner+1200, bottom_corner)).text()
        bottom_corner1 -= 32.5
        bottom_corner -= 32.5

    """Third page:
        left_corner = float(label.attr('x0'))
        bottom_corner = float(label.attr('y0'))-12.5
        bottom_corner1 = float(label.attr('y0'))-22.5
            ++32.5
    """
    if num_pages > 2:
        for page in range(num_pages):
            if page <=1:
                continue
            pdf.load(page)
            label = pdf.pq('LTTextLineHorizontal:contains("Transaction Date")')
            left_corner = float(label.attr('x0'))        #x0
            bottom_corner = float(label.attr('y0'))-12.5 #y0
            bottom_corner1 = bottom_corner - 22.5        #y1

            row = 'Advocating'
            # Check for the word 'Advocating' to eliminate invalid rows or blank lines
            while 'Advocating' in row:
                if row != 'Advocating':
                    rows.append(row)
                row = pdf.pq('LTTextLineHorizontal:in_bbox("%s, %s, %s, %s")' % (left_corner,
                bottom_corner1, left_corner+1200, bottom_corner)).text()
                bottom_corner1 -= 32.5
                bottom_corner -= 32.5
    return rows
