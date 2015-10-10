#!/usr/bin/python3

import sys
import os
from FileSequence.FileSequence import ls

blenderexe = "/usr/local/bin/blender/blender"

header = """
Executable = {blenderexe}
Universe = vanilla
initialdir = {inputFilePath}
should_transfer_files = No
getenv = True
log = log-{inputFileName}/{inputFileName}.log
"""

job = """
error = log-{inputFileName}/err.{frame}
arguments = -b {fileName} -s {frame} -e {frame} -a
output = log-{inputFileName}/out.{frame}
queue
"""

def RangeJob( inputFile, startframe, endframe):
	inputFileName = os.path.splitext(inputFile)[0]
	inputFilePath = os.path.dirname((os.path.abspath(inputFile)))

	submittxt = ""

	submittxt += header.format(blenderexe=blenderexe,inputFilePath=inputFilePath,inputFileName=inputFileName)
	submittxt += "\n"
	for frame in range(startframe,endframe+1):
		submittxt += job.format(frame=frame,fileName=inputFile,inputFileName=inputFileName)
		submittxt += "\n"

	logdir = "log-" + inputFileName

	if not os.path.exists(logdir):
		os.mkdir(logdir)

	print(submittxt)

def MissingFramesJob( inputFile, renderPath ):
	inputFileName = os.path.splitext(inputFile)[0]
	inputFilePath = os.path.dirname((os.path.abspath(inputFile)))

	submittxt = ""

	submittxt += header.format(blenderexe=blenderexe,inputFilePath=inputFilePath,inputFileName=inputFileName)
	submittxt += "\n"

	dfs = ls(renderPath)

	lfs = list(dfs.values())

	ofs = lfs[0]
	for s,e in ofs.holes:
		for frame in range(s,e+1):
			submittxt += job.format(frame=frame,fileName=inputFile,inputFileName=inputFileName)
			submittxt += "\n"

	logdir = "log-" + inputFileName

	if not os.path.exists(logdir):
		os.mkdir(logdir)

	print(submittxt)

inputFile = sys.argv[1]
# startframe = int(sys.argv[2])
# endframe = int(sys.argv[3])
# RangeJob( inputFile, startframe, endframe )
# -----
renderPath = sys.argv[2]
MissingFramesJob(inputFile,renderPath)
