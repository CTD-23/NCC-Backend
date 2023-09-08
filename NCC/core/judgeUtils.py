import subprocess
import shutil
import os
from .models import  Testcase
from subprocess import STDOUT, check_output
# from celery import shared_task
JudgeFolderPath = os.path.abspath("Judge")
# JudgeFolderPath="Clash_RC_2/Code_Runner"
judgeUtilsDirPath = os.path.dirname(__file__)


ErrorCodes={
    0:"AC",
    1:"CE",

    #py
    # 137:"TLE",    
    134:"MLE",
    127:"MLE",  #in py when memory is too less 2mb

    #cpp
    136:"RE",   #Floating point exception (core dumped)


    #c
    139:"MLE",  #Segmentation fault (core dumped)

    #Docker
    124:"TLE",
    137:"MLE",


    # Custom
    69:"WA",
    6969:"Unknown Error"    #We will throw this return code when user uses some diff code syntax in code as our machine is not have such library or module to handle that part

}

def execute(code, language,containerId,input):
    copy_run_py(language,containerId)
    copy_code(code,language)
    copy_input(input)
    run = subprocess.run(f"python3 {JudgeFolderPath}/main.py", shell=True)
    # run = subprocess.run(f"python {JudgeFolderPath}/code_run.py", shell=True)
    
    return get_output_files()


def compare(output, tc):
    try:
        with open(tc.outputFile.path, "r") as correct_output:
            x = correct_output.read().strip()
            # print("actual : ",x,"user : ",output)
            return output.strip() == x
    except:
        return False


def copy_run_py(language,containerId):
    src = f"{judgeUtilsDirPath}/JudgePythonScript.py"
    dst = f"{JudgeFolderPath}/main.py"
    shutil.copyfile(src, dst)
    file1 = open(dst, "a")  # append mode
    file1.write(f"\nrun_{language}({containerId})")
    file1.close()

def copy_code(code,language):
    if (language=="python"):
        file_path = f"{JudgeFolderPath}/pyCode.py"
    elif (language=="cpp"):
        file_path = f"{JudgeFolderPath}/cppCode.cpp"
    elif (language=="c"):
        file_path = f"{JudgeFolderPath}/cCode.c"
    with open(file_path, 'w+') as file:
        file.write(code)
        file.close()

def copy_input(tc):
    dst = f"{JudgeFolderPath}/input.txt"
    src = tc.inputFile.path
    shutil.copy(src, dst)

def get_output_files():
    output = open(f"{JudgeFolderPath}/output.txt").read()
    err = open(f"{JudgeFolderPath}/error.txt").read()
    try :
        rc = int(open(f"{JudgeFolderPath}/returnCode.txt").read())
    except:
        print("******Error*******")
        print("Judge did not return any return code")
        
        rc = 6969

    print("******return code in utils*****")
    print("Return code -> ",rc)
    return output, err, rc

#Helps to clear previous data in txt files
def clearAll():
    with open(f"{JudgeFolderPath}/output.txt", 'w') as f:
        f.write('')
    with open(f"{JudgeFolderPath}/error.txt", 'w') as f:
        f.write('')
    with open(f"{JudgeFolderPath}/returnCode.txt", 'w') as f:
        f.write('')

#When run clicked
def copy_input_for_run(tc):
    dst = open(f"{JudgeFolderPath}/input.txt","w")
    if tc:
        dst.write(tc)
    dst.close()

def execute_run(code, language,containerId,tc):
    copy_run_py(language,containerId)
    copy_code(code,language)
    copy_input_for_run(tc)
    run = subprocess.run(f"python3 {JudgeFolderPath}/main.py", shell=True)

    return get_output_files()



# def runCode(question, code, language,isSubmitted,input=None):             #btn_click_status true = submit and false = run
def runCode(question,code, language,isSubmitted,containerId,input=None):             #btn_click_status true = submit and false = run
    TC_Status = {}


    if not (isSubmitted):
        output, err, rc = execute_run(code, language,containerId,input)

        TC_Status["error"]=err
        if rc !=0:
            # TC_Status["error"]=err
            if rc == 124:
                TC_Status["error"]="Time Limit Exeed"
            if rc == 137:
                TC_Status["error"]="Memory Limit Exeed"
            TC_Status["returnCode"]=rc
            TC_Status["status"]=ErrorCodes[rc]
        else:
            TC_Status["output"]=output
            TC_Status["returnCode"]=rc
            TC_Status["status"]=ErrorCodes[rc]
        # clearAll()
        return TC_Status
    
    TCs = Testcase.objects.filter(question=question).order_by('testcaseNumber')

    for tc in TCs:
        output, err, rc = execute(code, language,containerId,tc)

        if rc != 0:
            individualTestcase={}
            individualTestcase["returnCode"] = rc
            individualTestcase["status"] = ErrorCodes[rc]

            TC_Status[f"TESTCASE{tc.testcaseNumber}"] = individualTestcase
            return TC_Status
        elif compare(output, tc):
            individualTestcase={}
            individualTestcase["returnCode"] = rc
            individualTestcase["status"] = ErrorCodes[rc]
            
            TC_Status[f"TESTCASE{tc.testcaseNumber}"] = individualTestcase
   
        else:
            individualTestcase={}
            individualTestcase["returnCode"] = 69
            individualTestcase["status"] = ErrorCodes[69]
            TC_Status[f"TESTCASE{tc.testcaseNumber}"] = individualTestcase

        # clearAll()
        
    return TC_Status