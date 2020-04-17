import logging
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

def process_upload_log(filename):
    with open(filename, 'r') as upload_log:
        logs = []
        for line in upload_log:
            line = re.sub('\s+', ',', line)
            line = line.strip().split(',')
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
    return logs

def process_download_log(filename):
    with open(filename, 'r') as dload_log:
        logs = []
        for line in dload_log:
            line = re.sub('\s+', ',', line)
            line = line.strip().split(',')
            newlog={}
            newlog['dloaddate']=line[0]
            newlog['dloadtime']=line[1]
            newlog['dloaduser']=line[9]
            newlog['dloadip']=line[12]
            newlog['filename']=line[14]
            logs.append(newlog)
    return logs

def generate_upload_report_pdf(log_file,pdf_file):
    pdf = CustomPDF('L','pt','Legal')
    # Create the special value {nb}
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 12)
    title = 'Weekly Upload Report for ' + str(date.today())
    pdf.cell(0, 12, title, 0, 0, 'C')
    pdf.ln(24)
    pdf.set_font('Arial', 'BU', 9)
    line_no = 1
    logs=process_upload_log(log_file)

    pdf.cell(0, 10, "Upload Date     Upload Time     Upload User                                          Uploader IP            Verifier                                                     Verify Date        File Uploaded", 0,1)
    pdf.set_font('Courier', '', 10)
    for logentry in logs:
        if 'verifyuser' in logentry:
            pdf.cell(0, 10, txt="{} {}   {}{} {} {} {}".format(logentry['uploaddate'], logentry['uploadtime'], logentry['uploaduser'].ljust(26), logentry['uploadip'], logentry['verifyuser'].ljust(26),logentry['verifydate'],logentry['filename']), ln=1)
        else:
            pdf.cell(0, 10, txt="{} {}   {}{} {}            {}".format(logentry['uploaddate'], logentry['uploadtime'], logentry['uploaduser'].ljust(26), logentry['uploadip'],"unverified".ljust(26),logentry['filename']), ln=1)
        line_no += 1
    pdf.output(pdf_file)
    return len(logs)

def generate_download_report_pdf(log_file,pdf_file):
    pdf = CustomPDF('L','pt','Letter')
    # Create the special value {nb}
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 12)
    title = 'Weekly Download Report for ' + str(date.today())
    pdf.cell(0, 12, title, 0, 0, 'C')
    pdf.ln(24)
    pdf.set_font('Arial', 'BU', 9)
    line_no = 1
    logs=process_download_log(log_file)

    pdf.cell(0, 10, "Date                   Time                  User                                                       IP                              Filename", 0,1)
    pdf.set_font('Courier', '', 10)
    for logentry in logs:
        pdf.cell(0, 10, txt="{} {}   {}{} {}".format(logentry['dloaddate'], logentry['dloadtime'], logentry['dloaduser'].ljust(26), logentry['dloadip'],logentry['filename']), ln=1)
        line_no += 1
    pdf.output(pdf_file)
    return len(logs)


def do_user_logging(request, action='query'):
    """
    Write page user activity info to log.
    :param request: The request posted to the page.
    :param action:
    the action being logged

    :return:
    """
    logger = logging.getLogger('project_user')
    request_data = ''
    for k, v in request.POST.lists():
        if k not in ('csrfmiddlewaretoken', 'submit', 'submit_records', 'searchBtn', 'sid'):
            request_data = request_data + k + ':'
            for x in v:
                request_data = request_data + x + '|'
    referer = request.META.get('HTTP_REFERER') or ''
    path = request.path or ''
    method = request.method or ''
    logger.info("|action: " + action + "|" + "method: " + method + "|" + "path: " + path + "|" + "http_referer: " + referer + "|" + "userid: " + str(request.user) + "|" + request_data)
    # Track the pages that the user visits
    if 's_pages_visited' in request.session:
        all_pages = request.session['s_pages_visited']
        if path not in request.session['s_pages_visited']:
            all_pages = all_pages + path + '|'
            request.session['s_pages_visited'] = all_pages
    else:
        request.session['s_pages_visited'] = str(str(request.user)) + ':' + path + '|'
    logger.info('|Pages visited by: ' + str(request.session['s_pages_visited']))
