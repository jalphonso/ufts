#!/usr/bin/env python
import re
from fpdf import FPDF
from datetime import datetime


class CustomPDF(FPDF):

    def header(self):
        # Set up a logo
        self.image('./static/img/juniper-networks-black-rgb.png', 10, 8, 33)
        self.set_font('Times', '', 10)

        # Add an address
        self.cell(100)
        self.cell(0, 5, '2251 Corporate Park Dr #100', 0, 0, 'R')
        self.ln(4)

        self.cell(100)
        self.cell(0, 5, 'Herndon, VA 20171', 0, 0, 'R')
        self.ln(4)

        self.cell(100)
        self.cell(0, 5, 'Phone: (571) 203-1700', 0, 0, 'R')
        # Line break
        self.ln(10)
        self.set_font('Times', 'B', 12)
        title = 'Download Report'
        self.cell(0, 10, title, 0, 0, 'C')
        self.ln(10)
        # sub_title = first_line + ' - ' + last_line
        # self.cell(0, 5, sub_title, 0, 0, 'C')

    def footer(self):
        self.set_y(-10)

        self.set_font('Arial', 'I', 8)
        """Add date report was run"""
        report_date = str(datetime.today())
        self.cell(0, 10, report_date, 0, 0, 'L')
        # Add a page number
        page = 'Page: ' + str(self.page_no()) + '/{nb}'
        self.cell(0, 10, page, 0, 0, 'R')


def create_pdf(pdf_path):
    pdf = CustomPDF('P','mm','Letter')
    # Create the special value {nb}
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_font('Times', '', 10)
    line_no = 1
    logfile = input('Enter the LOG FILE to process: ')
    report_data = []
    filename = 'logs/{}'.format(logfile)

    with open(filename, 'r') as download_report:
        # data = download_report.readlines()
        # # first_line = data[0].split(' ')[0]
        # last_line = data[len(data) - 1].split(' ')[0]
        pdf.cell(0, 5, txt="Date               Time          User                                   IP Address        File Downloaded", ln=1)
        pdf.cell(0, 5, txt="_______________________________________________________________________________________________________", ln=1 )
        for line in download_report:
            line = re.sub('\s+', ',', line)
            line = line.strip().split(',')
            # pdf.cell(0, 10, txt="Line #{}".format(line_no), ln=1)
            pdf.cell(0, 10, txt="{}    {}    {}       {}           {}".format(line[0], line[1], line[9], line[12], line[14]), ln=1)
            line_no += 1
    pdf.output(pdf_path)


if __name__ == '__main__':
    create_pdf('./reports/download_report.pdf')


# logfile = input('Enter the LOG FILE to process: ')
# report_data = []
# filename = 'logs/{}'.format(logfile)
# with open(filename, 'r') as download_report:
#     for line in download_report:
#         line = re.sub('\s+', ',', line)
#         line = line.strip().split(',')
#         print(line[0],line[1],line[9],line[12],line[14])


