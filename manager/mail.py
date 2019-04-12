import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class MailSender(object):
    def __init__(self):
        self.server = "smtp.qq.com"
        self.sender = "yuchentianx@qq.com"
        self.key = "gfuwqqqxqlpudegc"
        self.subject = "Vulnerability Scanning Report"
        self.main_text = """
        Hi,

        You've received this email because your email address was used for registering our Vulnerability Scanning System.
        
        The attachment(s) in this email serve as detailed reports about your recent scan task(s).
        
        Best regards.
            
        --
        Yuchen Tian
        """
        self.msg = MIMEMultipart()

    def add_attachment(self, file_content, file_name):
        attachment = MIMEText(file_content, "base64", "utf-8")
        attachment["Content-Type"] = "application/octet-stream"
        attachment['Content-Disposition'] = "attachment; filename={0}".format(file_name)
        self.msg.attach(attachment)

    def reliable_send(self, receiver):
        send_num = 0
        self.msg['From'] = self.sender
        self.msg['To'] = receiver
        self.msg['Subject'] = self.subject

        # mail body
        self.msg.attach(MIMEText(self.main_text, "plain", "utf-8"))

        while send_num < 3:
            try:
                server = smtplib.SMTP()
                server.connect(self.server)
                server.login(self.sender, self.key)
                server.sendmail(self.sender, receiver, self.msg.as_string())
                server.quit()
                print("[email] report sent successfully")
                break
            except Exception as e:
                print("[email] report-sending error")
                print(e)
                print("[email] trying resending after 3 seconds...")
                time.sleep(3)
                send_num += 1

        self.msg = MIMEMultipart()      # reset msg content


mail_sender = MailSender()
