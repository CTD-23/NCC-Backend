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

CONTAINER_NAME="container"    #with ml
CONTAINER_NAME2="container2"

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

}

def run_python(containerId):
    print("container allocated ",CONTAINER_NAME,containerId)
    # cmd = f"python3 {pyCodeFile}"  #1
    cmd  = f"sudo docker exec {CONTAINER_NAME}{containerId} sh -c 'timeout 2s  python3 src/pyCode.py < src/input.txt'"
    subprocessOutput = subprocess.Popen(
                cmd,
                shell=True,
                # preexec_fn=setLimit,
                # stdin=inputFile,
                stdout=outputFile,
                stderr=errorFile,
                text=True,
            )

    subprocessOutput.wait()
    
    print("******return code in judge python script*****")
    returnCode = subprocessOutput.returncode
    print("return code ",returnCode)
    # stdout,stderr = subprocessOutput.communicate()
    # print(stdout)
    # print(stderr)
    # returnCode = 69

    returnCodeFile.write(str(returnCode))


def run_cpp(containerId):
    # cmd = r"g++ " + f"{cppCodeFile}" + f" -o {directoryName}/cppExeFile"  #3   #runnning
    print("=>Cpp code compilation start")
    cmd = f"sudo docker exec {CONTAINER_NAME}{containerId} sh -c 'g++ src/cppCode.cpp -o src/cppExeFile'"  #3
    subprocessCppExe = subprocess.Popen(cmd, shell=True, stderr=errorFile)
    subprocessCppExe.wait()
    print("=>Cpp code compilation done")
    if subprocessCppExe.returncode == 0:
        # ExeCmd = r"{0}/./cppExeFile".format(directoryName)   #runnig
        print("Cpp bin file start")
        ExeCmd = f"sudo docker exec {CONTAINER_NAME2} sh -c 'timeout 2s  src/./cppExeFile < src/input.txt'"
        # ExeCmd = r"{0}./cppExeFile".format(directoryName)
        subprocessOutput = subprocess.Popen(
            ExeCmd,
            shell=True,
            preexec_fn=setLimit(),
            # stdin=inputFile,
            stdout=outputFile,
            stderr=errorFile,
            text=True,
        )
        subprocessOutput.wait()
        print("Cpp bin file execution done")
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


def run_c(containerId):
    # cmd = "gcc " + f"{cCodeFile}" + f" -o {directoryName}/cExeFile"
    cmd = f"sudo docker exec {CONTAINER_NAME}{containerId} sh -c 'g++ src/cCode.c -o src/cExeFile'"
    subprocessCExe = subprocess.Popen(cmd, shell=True, stderr=errorFile)
    subprocessCExe.wait()
    if subprocessCExe.returncode == 0:
        # ExeCmd = r"{0}/./cExeFile".format(directoryName)
        ExeCmd = f"sudo docker exec {CONTAINER_NAME} sh -c 'timeout 2s  src/./cExeFile < src/input.txt'"
        subprocessOutput = subprocess.Popen(
            ExeCmd,
            shell=True,
            # preexec_fn=setLimit(),
            # stdin=inputFile,
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


run_python(2)