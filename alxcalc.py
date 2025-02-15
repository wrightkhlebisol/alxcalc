#!/usr/bin/env python3
"""Main module for the alxcalc program.
"""

import sys
import os
import subprocess

from task import Task
from project import Project
from month import Month


class Calc:
    def __init__(self, filename, args, master=None):
        self.filename = filename
        self.args = args
        self.master = master
        self.calc()

    def calc(self):
        if isinstance(self.master, Task) is True:
            print(str(self.master.cal_task()) + "%")
        elif isinstance(self.master, Month) is True:
            print(str(self.master.cal_month()) + "%")

            return


class Main:
    def __init__(self, master=None):
        self.master = master
        self.args = sys.argv

        if len(self.args) <= 2:
            print("Usage: alxcalc <option> <value>")
            sys.exit()

        if self.args[1] != "-M" and self.args[1] != "-m":
            print("Error: Invalid option: {}".format(self.args[1]))
            sys.exit()

        if self.args[2].isdigit() is False:
            print("Error: Invalid input value for option {}: {}".
                  format(self.args[1], self.args[2]))
            sys.exit()

        home = os.environ['HOME']
        self.filename = '{}/.alxcalc/month_{}/month_{}'.format(home,
                                                               self.args[2],
                                                               self.args[2])

    def main(self):
        """Entry point.
        """

        try:
            os.stat(self.filename)
        except (FileNotFoundError, IsADirectoryError):
            print("DEBUGGER 4: File Not Found")
            sys.exit()

        if self.args[1] == "-M":
            subprocess.run(f'editor {self.filename}', shell=True, text=True)


        length = len(self.args)

        if length == 3:
            month = Month(self.filename, self.args)
            self.master = month
        elif length == 7 and self.args[5] == '-t':
            if self.args[6].isdigit() is False:
                print("Error: Invalid Input Value for {}: {}".
                      format(self.args[5], self.args[6]))
                sys.exit()
            if self.args[3] != '-p':
                print()
                print("Error: Invalid Syntax")
                sys.exit()
            if self.args[1] != '-m' and self.args[1] != '-M':
                print()
                print("Error: Invalid Syntax.")
                sys.exit()
            if self.args[2].isdigit() is False:
                print()
                print("Error: Invalid Input Value")
                sys.exit()

            month = "month_" + self.args[2]

            project = Project(self.filename, self.args)
            project = project.project_key()

            task = "task_" + self.args[6]

            filename = self.filename

            my_task = Task(project, task, filename, self.args)
            self.master = my_task

        else:
            self.master = None

        calc = Calc(self.filename, self.args, self.master)


if __name__ == '__main__':
    Main().main()
