import os
import sys
import zipfile
import subprocess

class Zipper(object):
    """"Diagnose OMS client system"""

    def __init__(self, file_name):
        self.zip = zipfile.ZipFile(file_name, 'a')

    def addFile(self, file_path):
        self.zip.write(file_path)
        # zip.write('file.gif')
        # zip.write('folder/file.html')

    def close(self):
        print (str(self.zip.namelist()))
        print("closing")
        self.zip.close()

class Diagnose(object):

    def __init__(self, log_files, cmd_list, zip_file_name,cmd_output_file):
        self.log_files= log_files
        self.cmd_list= cmd_list
        self.zip_file_name=zip_file_name
        self.cmd_output_file= cmd_output_file

    def collect_files(self):
        file_list= self.log_files.strip().split(",")
        collect = Zipper(self.zip_file_name)

        for file in file_list:
            if not os.path.exists(file):
                print(file + " does not exist!")
            else:
                collect.addFile(file)
        collect.close()

    def run_commands(self):
        lines = []
        with open("commands.txt") as file:
            for line in file:
                line = line.strip()

    def read_omsdiag_resources(self):
        with open("omsdiag_resources.txt") as file:
            cmds=False
            for line in file:
                line = line.strip()
                if line== "#Files":
                    continue               
                if(line== "#Commands"):
                    cmds=True
                    continue
                if line and  not line.startswith('#'):
                    if  cmds:
                        self.log_files.append(line)
                    else:
                        self.cmd_list.append(line)
        print(self.cmd_list)
        print(self.log_files)
    
    def run_command(self, cmd):
        proc = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = proc.communicate()
        return_code = proc.poll()

        #output = proc.stdout.read()
        if (return_code is not None) and (return_code != 0):
            # return code is generally 1 if it failed
            #error = proc.stderr.read()
            print("cmd failed: " + cmd)
            print("output:" + str(output) + str(error))
            print("return code:" + str(return_code))
            return error
        else:
             return output


class Report(object):

    def __init__(self, report):
        self.report = open(report,'w')
        self.message=''
        
    
    def add_message(self, paragraph):
        row= """<tr>
                    <td>{0}</td> td>{1}</td>
                </tr>"""
        self.message= self.message + row.format('cmd',paragraph)   

    def write_report(self):
        #message_html = """<html>
         #   <head><center><h1>Linux OMS agent Diagnostic report<h1></head>
          #  <body>{0}</body>
           # </html>""".format(self.message)
        message_html= """<!DOCTYPE html>
            <html>
            <head>
            <title>OMS Linux Agent Diagnostic Report</title>
            <style>
            table {
                font-family: arial, sans-serif;
                border-collapse: collapse;
                width: 100%;
            }

            td, th {
                border: 1px solid #dddddd;
                text-align: left;
                padding: 8px;
            }

            tr:nth-child(even) {
                background-color: #dddddd;
            }
            </style>
            </head>
            <body>
            <header role="banner"> <center> <h1> OMS Linux Agent Diagnostic Report </h1></center></header>
            <hr/>
            <br/>
            <table style="width:90%" align="center">
            <tr>
                <th width="20%">Description</th>
                <th>Output</th> 

            </tr>""" 
        message_html= message_html+ self.message
            
            #{0}
        message_html= message_html +    """</table>
            </body>
            </html>
            """
            #.format(self.message)
        self.report.write(message_html)
        self.report.close()

def main(argv):
   # files_to_collect=['/mnt/c/code/Mgmt-Automation-LinuxUpdate/file.txt,/mnt/c/code/Mgmt-Automation-LinuxUpdate/owners1.txt']
   # cmd_list = ['ls -l /opt/microsoft/omsconfig/modules/nxOMSPlugin/DSCResources/MSFT_nxOMSPluginResource/Plugins']
    
    files_to_collect=[]
    cmd_list = []
    

    diag=Diagnose(files_to_collect, cmd_list, 'omsdiag.zip', 'out.txt')

    output=diag.run_command("dir")
    diag.read_omsdiag_resources()
    report= Report('oms_update.html')
    report.add_message(str(output))
    report.write_report()
    #diag.collect_files()


if __name__ == "__main__":
    main(sys.argv)

