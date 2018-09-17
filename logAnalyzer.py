import time
import optparse
import re
import sys
import glob
import os
import pdb
import logging

class LogParser():
    def __init__(self, logfile):
        #Read and parse logfile
        #Set up:
        #self.total - number of all tests in the log
        self.total = 0
        #self.passed - number (or list?) of passed tests
        self.passed = 0
        #self.failed - list of failed tests
        self.failed = []
        #self.xfailed - list
        self.xfailed = []
        #self.error - list
        self.error = []
        #self.skipped - list
        self.skipped = []
        #self.warnings - list
        self.log_lines = []
        self.all_passed = None
        self.log_type = None
        self.logfile = logfile
        with open(self.logfile, encoding='utf-8', newline='', errors='replace') as file:
            for line in file:
                self.log_lines.append(line.rstrip('\r\n'))
        #pdb.set_trace()
        self.log_type_status()
        if self.log_type == 'nose':
            self.parse_nose()
        if self.log_type == 'pytest':
            self.parse_pytest()

    def log_type_status(self):
        """
        Analyse log type and status (passed/failed). Save values to self.log_type
        and self.all_passed variables
        """
        # Ran 24194 tests in 475.800s
        nose_pattern = re.compile(r'^Ran \d+ tests in ')
        # === 12 failed, 283 passed, 1 skipped, 1 xfailed, 147 error in 171.88 seconds ===
        # Can be without '===' for long string like this:
        #  979 passed, 272 skipped, 36 xfailed, 42 xpassed, 3 pytest-warnings in 15.31 seconds
        pytest_pattern = re.compile(r'^=*.* \d+ (passed|skipped|error|x?failed).+in \d+(\.\d+)? seconds =*$')
        for line in self.log_lines:
            # nose pattern for passed test:
            if re.match(r'.* ... ok', line) or re.match(r'ok', line):
                self.passed += 1
            # For 'nose' find a status in follow strings
            if self.log_type is 'nose':
                if re.match(r'^OK\b', line) and self.all_passed is None:  # Not OK if once failed (like in Python self-tests)
                    self.all_passed = True
                if re.match(r'^FAILED\b', line):
                    self.all_passed = False
                continue
            # Check type of testing system
            if re.search(pytest_pattern, line):
                self.log_type = 'pytest'
                head, sep, tail = re.search(pytest_pattern, line).group().partition('in')
                result = re.findall(r'\d+', head)
                result_int = map(int, result)
                passed = re.search(r'\d+ passed', head).group()
                self.passed = re.search(r'\d+', passed).group()
                #self.passed = re.search(r'\d+ passed', head)
                self.total = sum(result_int)
                if re.search(r'\d+ (failed|error)', line):
                    self.all_passed = False
                else:
                    self.all_passed = True
                break
            elif re.search(nose_pattern, line):
                self.log_type = 'nose'
        if self.log_type is None:
            logging.warning("Unknown log type for '%s'." % self.filename)
        if self.all_passed is None:
            logging.warning("Test status for '%s' is unknown." % self.filename)

    def parse_nose(self):
        """
        Parse logs in nose (nosetest) format
        """
        # --- From plotly ---
        # plotly.tests.test_core.test_graph_objs.test_update.test_update_list_make_copies_false ... SKIP: See https://github.com/plotly/python-api/issues/291
        skipped_pattern_1 = re.compile(r'^(.+)\s+\.\.\.\s+SKIP(:\s+(.+))?$')
        # --- From Django ---
        # test_cyclic (admin_views.tests.AdminViewDeletedObjectsTest) ... skipped "Database doesn't support feature(s): can_defer_constraint_checks"
        skipped_pattern_2 = re.compile(r'^(.+)\s+\.\.\.\s+skipped(\s+[\"\'](.+)[\"\'])?$')
        # --- From Pandas ---
        # SKIP: 'lxml' not found
        skipped_pattern_3 = re.compile(r'^SKIP:\s(.+)$')
        nose_pattern = re.compile(r'^Ran \d+ tests in ')
        top_delimiter_pattern = re.compile(r'^={70}$')
        failure_pattern = re.compile(r'^FAIL: (.+)$')
        error_pattern = re.compile(r'^ERROR: (.+)$')
        #'.* ... expected failure'
        xfailed_pattern = re.compile('.* ... expected failure')
        top_delimiter_started = False
        for line in self.log_lines:
            #Parse failed tests
            if re.search(top_delimiter_pattern, line):
                top_delimiter_started = True
                continue
            if top_delimiter_started:
                top_delimiter_started = False
                res = re.search(failure_pattern, line)
                if res:
                    self.failed.append(res.group(1))
                    continue
                res = re.search(error_pattern, line)
                if res:
                    self.error.append(res.group(1))
                    continue
            if re.search(nose_pattern, line):
                if self.total == 0:
                    self.total = int(re.search(r'\d+', line).group())
                else:
                    self.total = self.total + int(re.search(r'\d+', line).group())

            #Parse skipped tests
            res = re.search(skipped_pattern_1, line)
            if res:
                text = res.group(1)
                text += '' if res.group(3) is None else ' (' + res.group(3) + ')'
                self.skipped.append(text)
                continue
            res = re.search(skipped_pattern_2, line)
            if res:
                text = res.group(1)
                text += '' if res.group(3) is None else ' (' + res.group(3) + ')'
                self.skipped.append(text)
                continue
            res = re.search(skipped_pattern_3, line)
            if res:
                self.skipped.append(res.group(1))
                continue
            #parse expected failed tests
            if re.match(xfailed_pattern, line):
                head, sep, tail = line.partition(' ...')
                self.xfailed.append(head)

    def parse_pytest(self):
        """
        Parse logs in pytest format
        """
        failures_started_pattern = re.compile(r'^=+ FAILURES =+$')
        failure_pattern = re.compile(r'^_* (.*[A-Za-z0-9].*) _*$')
        errors_started_pattern = re.compile(r'^=+ ERRORS =+$')
        error_pattern = re.compile(r'^_* ERROR at (.+) _*$')
        error_collecting_pattern = re.compile(r'^_* ERROR collecting (.+) _*$')
        skipped_pattern = re.compile(r'^(.+)\s+SKIPPED$')
        xfailed_pattern = re.compile('.*.py.* xfail *')
        failures_started = False
        errors_started = False
        for line in self.log_lines:
            # Search for errors/failures section start
            if re.search(failures_started_pattern, line):
                failures_started = True
                errors_started = False
                continue
            elif re.search(errors_started_pattern, line):
                failures_started = False
                errors_started = True
                continue
            # Search for error/failure titles
            if failures_started:
                res = re.search(failure_pattern, line)
                if res:
                    self.failed.append(res.group(1))
            elif errors_started:
                res = re.search(error_pattern, line)
                if res:
                    self.error.append(res.group(1))
                    continue
                res = re.search(error_collecting_pattern, line)
                if res:
                    self.error.append(res.group(1))
                    continue
            # Search for skipped tests
            res = re.search(skipped_pattern, line)
            if res:
                self.skipped.append(res.group(1))

            # Search for expected failed tests
            res = re.search(xfailed_pattern, line)
            if res:
                head, sep, tail = line.partition(' ')
                self.xfailed.append(head)


class LogAnalyzer():
    def __init__(self, logfile):
        self.__current = LogParser(logfile)

    def exclude_known_issues(self, known_issues):
        #Parse file with known issues.
        #Need to choose format of this file. YAML? It has been being used for configuration file
        pass
    def compare_with(self, logfile):
        reference = LogParser(logfile)
        #Compare with data parsed before:
        #if self.__current.total != reference.total:
        #   ...
        #Set up variables, e.g.:
        #self.new_passed
        #self.new_failed

file_list = os.listdir("c:/tmp/1")
for file in file_list:
    if True:
        start_time = time.time()
        print(file, " type:", LogParser("c:/tmp/1/" + file).log_type)
        print(file, "total:", LogParser("c:/tmp/1/" + file).total)
        print(file, "passed:", LogParser("c:/tmp/1/" + file).passed)
        print(file, "error:", LogParser("c:/tmp/1/" + file).error)
        print(file, "error:", len(LogParser("c:/tmp/1/" + file).error))
        print(file, "failed:", LogParser("c:/tmp/1/" + file).failed)
        print(file, "failed:", len(LogParser("c:/tmp/1/" + file).failed))
        print(file, "skipped:", LogParser("c:/tmp/1/" + file).skipped)
        print(file, "skipped:", len(LogParser("c:/tmp/1/" + file).skipped))
        print(file, "xfailed:", LogParser("c:/tmp/1/" + file).xfailed)
        print(file, "xfailed:", len(LogParser("c:/tmp/1/" + file).xfailed))
        print("--- %s seconds ---" % (time.time() - start_time))