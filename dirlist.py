import os
import re
from logAnalyzer import LogParser as log
import glob
import pprint
def get_txt_files(base_dir):
    return glob.iglob(f"{base_dir}/**/*", recursive=True)



def log_type_status(log):
    """ return result line  """
    # Ran 24194 tests in 475.800s
    nose_pattern = re.compile(r'^Ran \d+ tests in ')
    # === 12 failed, 283 passed, 1 skipped, 1 xfailed, 147 error in 171.88 seconds ===
    # Can be without '===' for long string like this:
    #  979 passed, 272 skipped, 36 xfailed, 42 xpassed, 3 pytest-warnings in 15.31 seconds
    # bokeh 0.12.4 :
    # 3 failed, 875 passed, 2 skipped, 8 deselected, 39 warnings, 35 error in 29.98 seconds
    #pytest_pattern = re.compile(r'^=*.* \d+ (passed|skipped|error|x?failed).+in \d+(\.\d+)? seconds =*$')
    log_type = None
    all_passed = None
    log_lines= []
    pytest_pattern = re.compile(
        '^=*.* \d+ (passed|skipped|deselected|error|x?failed|warnings).+in \d+(\.\d+)? seconds(\s)?=*$')
    with open(log, encoding='utf-8', newline='', errors='replace') as file:
            for line in file:
                log_lines.append(line.rstrip('\r\n'))
    for line in log_lines:
        if log_type is 'nose':
            if re.match(r'^OK\b', line) and all_passed is None:  
                print(line)
            if re.match(r'^FAILED\b', line):
                print(line)
            continue
        # Check type of testing system
        if re.search(pytest_pattern, line):
            log_type = 'pytest'
            print(line)
            head, sep, tail = re.search(pytest_pattern, line).group().partition('in')
            result = re.findall(r'\d+', head)
            result_int = map(int, result)
            passed = re.search(r'\d+ passed', head).group()
            passed = re.search(r'\d+', passed).group()
            if re.search(r'\d+ (failed|error)', line):
                all_passed = False
            else:
                all_passed = True
            break
        elif re.search(nose_pattern, line):
            log_type = 'nose'
            print(line)




path = "d:/Programming/repos/ZOSS/zoss-test-packs/test-packs/resources/python_packages"

stats = dir(log)
print(stats)
result = get_txt_files(path)
for item in result:
    if "result" in item and "alembic" in item :
        print("Filename:" + item)
        
        if(log(item).log_type == 'nose' ):
            print("+++++++++++++++++++++++++++++++++++++++++++++++++++++")
            log_type_status(item)
            print("+++++++++++++++++++++++++++++++++++++++++++++++++++++")
            print("Type and total: ",log(item).log_type," ",log(item).total)
            print("Passed: ",log(item).passed) #" errors:",len(log(item).error),"failures:",len(log(item).failed),"xfailed:",len(log(item).xfailed),"skipped:",len(log(item).skipped),"warnings:",len(log(item).warnings)
            print("Errors: ",len(log(item).error))
            print("Failures list qty: ",len(log(item).failed))
            print("Xpassed list qty: ", len(log(item).xfailed))
            print("Skipped list qty: ", len(log(item).skipped))
            print("Warning list qty: ", len(log(item).warnings))
            
