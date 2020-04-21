#!/usr/bin/env python
import re
from fpdf import FPDF
from datetime import datetime,date 


class CustomPDF(FPDF):

    def header(self):
        # Set up a logo
        self.image('./static/img/juniper-networks-black-rgb.png',12,20,144)
        self.set_font('Times', '', 10)

        # Add an address
        self.cell(100)
        self.cell(0, 10, '2251 Corporate Park Dr #100', 0, 0, 'R')
        self.ln(10)

        self.cell(100)
        self.cell(0, 10, 'Herndon, VA 20171', 0, 0, 'R')
        self.ln(10)

        self.cell(100)
        self.cell(0, 10, 'Phone: (571) 203-1700', 0, 0, 'R')
        # Line break
        self.ln(10)
        self.set_font('Arial', 'B', 12)
        title = 'Weekly Upload Report for ' + str(date.today())
        self.cell(0, 12, title, 0, 0, 'C')
        self.ln(24)
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
    pdf = CustomPDF('L','pt','Legal')
    # Create the special value {nb}
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_font('Arial', 'BU', 9)
    line_no = 1
    logfile = input('Enter the LOG FILE to process: ')
    report_data = []
    filename = 'logs/{}'.format(logfile)

    with open(filename, 'r') as download_report:
        # data = download_report.readlines()
        # # first_line = data[0].split(' ')[0]
        # last_line = data[len(data) - 1].split(' ')[0]
        pdf.cell(0, 10, "Upload Date     Upload Time     Upload User                                          Uploader IP            Verifier                                                     Verify Date        File Uploaded", 0,1)
        pdf.set_font('Courier', '', 10)
        logs = []
        for line in download_report:
            line = re.sub('\s+', ',', line)
            line = line.strip().split(',')
            # pdf.cell(0, 10, txt="Line #{}".format(line_no), ln=1)
            if line[13]=="|uploaded_file:":
                newlog={}
                newlog['uploaddate']=line[0]
                newlog['uploadtime']=line[1]
                newlog['uploaduser']=line[9]
                newlog['uploadip']=line[12]
                newlog['filename']=line[14]
                logs.append(newlog)
            elif line[13]=="|verified_file:":
                for logentry in logs:
                    if logentry['filename']==line[14]:
                        logentry['verifydate']=line[0]
                        logentry['verifytime']=line[1]
                        logentry['verifyuser']=line[9]
                        logentry['verifyip']=line[12]
                        continue
        for logentry in logs:
            if 'verifyuser' in logentry:
                pdf.cell(0, 10, txt="{} {}   {}{} {} {} {}".format(logentry['uploaddate'], logentry['uploadtime'], logentry['uploaduser'].ljust(26), logentry['uploadip'], logentry['verifyuser'].ljust(26),logentry['verifydate'],logentry['filename']), ln=1)
            else:
                pdf.cell(0, 10, txt="{} {}   {}{} {}            {}".format(logentry['uploaddate'], logentry['uploadtime'], logentry['uploaduser'].ljust(26), logentry['uploadip'],"unverified".ljust(26),logentry['filename']), ln=1)
            line_no += 1
    pdf.output(pdf_path)


if __name__ == '__main__':
    report_name="./reports/upload_report-{}.pdf".format(str(date.today()))
    create_pdf(report_name)


# logfile = input('Enter the LOG FILE to process: ')
# report_data = []
# filename = 'logs/{}'.format(logfile)
# with open(filename, 'r') as download_report:
#     for line in download_report:
#         line = re.sub('\s+', ',', line)
#         line = line.strip().split(',')
#         print(line[0],line[1],line[9],line[12],line[14])


