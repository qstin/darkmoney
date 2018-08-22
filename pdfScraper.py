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
    """
    ### This was used when I would start by finding the 'Transaction Date'. 
    ### Now I'm going to look for Advocating and scan the line to the right and
    ### left of it.

    label = pdf.pq('LTTextLineHorizontal:contains("Transaction Date")')
    left_corner = float(label.attr('x0'))   #x0
    bottom_corner = float(label.attr('y0')) #y0
    bottom_corner1 = bottom_corner - 22.5     #y1
    """

    rows = []
    label = pdf.pq('LTTextLineHorizontal:contains("Advocating")')
    for item in label:
        left_corner = float(item.get('x0'))
        bottom_corner = float(item.get('y0'))
        row = pdf.pq('LTTextLineHorizontal:in_bbox("%s, %s, %s, %s")' % (
        left_corner-600, bottom_corner, left_corner+1200,
        bottom_corner+20)).text()
        
        rows.append(row)

    if num_pages > 2:
        for page in range(num_pages):
            if page <=1:
                continue
            pdf.load(page)
            label = pdf.pq('LTTextLineHorizontal:contains("Advocating")')
            for item in label:
                left_corner = float(item.get('x0'))
                bottom_corner = float(item.get('y0'))
                row = pdf.pq('LTTextLineHorizontal:in_bbox("%s, %s, %s, %s")' % (
                left_corner-600, bottom_corner, left_corner+1200,
                bottom_corner+20)).text()
                
                rows.append(row)

    return rows
