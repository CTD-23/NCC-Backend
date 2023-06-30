import subprocess 
import os
import resource

#To get directory name in which Code Running python script is present
directoryName = os.path.dirname(__file__)


pyCodeFile = "{}/pyCode.py".format(directoryName)   #Users python code file path
cppCodeFile = "{}/cppCode.cpp".format(directoryName)   #Users cpp code file path
cCodeFile = "{}/cCode.c".format(directoryName)   #Users c code file path


#Input testcase file path
inputFilePath = "{}/input.txt".format(directoryName) 
outputFilePath = "{}/output.txt".format(directoryName) 
errorFilePath = "{}/error.txt".format(directoryName)
returnCodeFilePath = "{}/returnCode.txt".format(directoryName)

inputFile = open(inputFilePath,"r")
outputFile = open(outputFilePath,"w+")
errorFile = open(errorFilePath,"w+")
returnCodeFile = open(returnCodeFilePath,"w+")


#Limiting Resources 
def setLimit():
    timeLimit = 2
    memoryLimit = 512*1024*1024

    def setlimits():
        resource.setrlimit(resource.RLIMIT_CPU, (timeLimit, timeLimit))
        resource.setrlimit(resource.RLIMIT_AS, (memoryLimit, memoryLimit))

    return setlimits

ErrorCodes={
    0:"AC",
    1:"CE",

    #py
    137:"TLE",
    134:"MLE",
    127:"MLE",  #in py when memory is too less 2mb

    #cpp
    136:"RE",   #Floating point exception (core dumped)


    #c
    139:"MLE",  #Segmentation fault (core dumped)


}

def run_python():
    cmd = f"python3 {pyCodeFile}"
    subprocessOutput = subprocess.Popen(
                cmd,
                shell=True,
                preexec_fn=setLimit(),
                stdin=inputFile,
                stdout=outputFile,
                stderr=errorFile,
                text=True,
            )

    subprocessOutput.wait()
    returnCode = subprocessOutput.returncode
    # print(returnCode)
    # print(ErrorCodes[returnCode])
    returnCodeFile.write(str(returnCode))


def run_cpp():
    cmd = r"g++ " + f"{cppCodeFile}" + f" -o {directoryName}/cppExeFile"
    # cmd = r"g++" + f"{cppCodeFile}" + f" -o {directoryName}/cppExeFile"
    subprocessCppExe = subprocess.Popen(cmd, shell=True, stderr=errorFile)
    subprocessCppExe.wait()
    if subprocessCppExe.returncode == 0:
        ExeCmd = r"{0}/./cppExeFile".format(directoryName)
        # ExeCmd = r"{0}./cppExeFile".format(directoryName)
        subprocessOutput = subprocess.Popen(
            ExeCmd,
            shell=True,
            preexec_fn=setLimit(),
            stdin=inputFile,
            stdout=outputFile,
            stderr=errorFile,
            text=True,
        )
        subprocessOutput.wait()
        returnCode = subprocessOutput.returncode
        # print(returnCode)
        # print(ErrorCodes[returnCode])
        returnCodeFile.write(str(returnCode))
    else:
        # print("May be CE")
        returnCode = subprocessCppExe.returncode
        # print(returnCode)
        # print(ErrorCodes[returnCode])
        returnCodeFile.write(str(returnCode))


def run_c():
    cmd = "gcc " + f"{cCodeFile}" + f" -o {directoryName}/cExeFile"
    subprocessCExe = subprocess.Popen(cmd, shell=True, stderr=errorFile)
    subprocessCExe.wait()
    if subprocessCExe.returncode == 0:
        ExeCmd = r"{0}/./cExeFile".format(directoryName)
        subprocessOutput = subprocess.Popen(
            ExeCmd,
            shell=True,
            preexec_fn=setLimit(),
            stdin=inputFile,
            stdout=outputFile,
            stderr=errorFile,
            text=True,
        )
        subprocessOutput.wait()

        returnCode = subprocessOutput.returncode
        # print(returnCode)
        # print(ErrorCodes[returnCode])
        returnCodeFile.write(str(returnCode))
    else:
        print("May be CE")
        returnCode = subprocessCExe.returncode
        # print(returnCode)
        # print(ErrorCodes[returnCode])
        returnCodeFile.write(str(returnCode))

# runPython()
# runCpp()
# runC()


run_python()