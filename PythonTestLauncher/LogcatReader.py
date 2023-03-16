import re

class ParsedLogs:
    def __init__(self, gpuP, cpuP):
        self.gpuP = gpuP
        self.cpuP = cpuP

def parseLogs(logs):
    # get relevant lines from log
    parsedLines = []
    lines = logs.split('\n')
    for line in reversed(lines):
        #only take last 10 logs of game running to average
        if len(parsedLines) >= 10:
            break
        if "CPU&GPU=" in line:
            gpuP = line.split(",GPU%=", maxsplit=1)[1].split(",", 1)[0]
            cpuP = re.split(',',line.split(",CPU%=", maxsplit=1)[1].replace("(", ","))[0]
            # for each line, make a parsed log
            parsedLines.append(ParsedLogs(gpuP, cpuP))
    # for each parsed log, get the average over all of them or the last 10 seconds, whichever is less
    totalGpu = 0
    totalCpu = 0
    for plog in parsedLines:
        totalGpu += float(plog.gpuP)
        totalCpu += float(plog.cpuP)
    #return average ParsedLogs object
    finalAvg = ParsedLogs(totalGpu/len(parsedLines),totalCpu/len(parsedLines))
    return finalAvg


def getTestString():
    return """03-07 00:43:30.005  2029 12974 I VrApi   : FPS=90/90,Prd=31ms,Tear=0,Early=0,Stale=0,Stale2/5/10/max=0/0/0/0,VSnc=0,Lat=-1,Fov=0,CPU4/GPU=4/4,1478/525MHz,OC=FF,TA=0/70/0,SP=N/F/N,Mem=2092MHz,Free=5284MB,PLS=0,Temp=30.7C/0.0C,TW=2.02ms,App=6.27ms,GD=0.13ms,CPU&GPU=8.58ms,LCnt=4(DR0,LM3),GPU%=0.79,CPU%=0.16(W0.29),DSF=1.00,CFL=14.65/19.92,LD=0
03-07 00:43:31.004  2029 12974 I VrApi   : FPS=90/90,Prd=30ms,Tear=0,Early=0,Stale=0,Stale2/5/10/max=0/0/0/0,VSnc=0,Lat=-1,Fov=0,CPU4/GPU=4/4,1478/525MHz,OC=FF,TA=0/70/0,SP=N/F/N,Mem=2092MHz,Free=5284MB,PLS=0,Temp=30.7C/0.0C,TW=2.02ms,App=6.27ms,GD=0.13ms,CPU&GPU=9.08ms,LCnt=4(DR0,LM3),GPU%=0.79,CPU%=0.15(W0.25),DSF=1.00,CFL=14.73/20.14,LD=0
03-07 00:43:32.003  2029 12974 I VrApi   : FPS=90/90,Prd=30ms,Tear=0,Early=0,Stale=0,Stale2/5/10/max=0/0/0/0,VSnc=0,Lat=-1,Fov=0,CPU4/GPU=4/4,2342/525MHz,OC=FF,TA=0/70/0,SP=N/F/N,Mem=2092MHz,Free=5284MB,PLS=0,Temp=30.7C/0.0C,TW=2.02ms,App=6.30ms,GD=0.14ms,CPU&GPU=9.34ms,LCnt=4(DR0,LM3),GPU%=0.79,CPU%=0.17(W0.29),DSF=1.00,CFL=14.58/19.51,LD=0
03-07 00:43:32.654  2029  2239 D VrApi   : targetSDKVersion 29
03-07 00:43:32.666  2029 12974 I VrApi   : FPS=90/90,Prd=30ms,Tear=0,Early=0,Stale=0,Stale2/5/10/max=0/0/0/0,VSnc=0,Lat=-1,Fov=0,CPU4/GPU=4/4,1574/525MHz,OC=FF,TA=0/70/0,SP=N/F/N,Mem=2092MHz,Free=5284MB,PLS=0,Temp=30.7C/0.0C,TW=2.01ms,App=6.38ms,GD=0.12ms,CPU&GPU=9.59ms,LCnt=4(DR0,LM3),GPU%=0.80,CPU%=0.12(W0.26),DSF=1.00,CFL=14.65/19.45,LD=0
03-07 00:43:32.717  2029  2239 I VrApi   : OVR::Stats thread stopped
03-07 00:43:32.835 24737  3946 D VrApi   : targetSDKVersion 29
03-07 00:43:32.876 24737  3946 I VrApi   : OVR::Stats thread stopped
03-07 00:43:33.802 13334 13355 D VrApi   : targetSDKVersion 30
03-07 00:43:33.826 13334 13355 I VrApi   : OVR::Stats thread started
03-07 00:43:33.827 13334 13409 D VrApi   : targetSDKVersion 30
03-07 00:43:33.832 13334 13409 D VrApi   : VrApi::isWifiConnected exception: Make sure android.permission.ACCESS_NETWORK_STATE is set in the manifest.
03-07 00:43:35.009 13334 13409 I VrApi   : FPS=1/72,Prd=0ms,Tear=0,Early=0,Stale=4,Stale2/5/10/max=0/0/0/0,VSnc=0,Lat=-1,Fov=0,CPU4/GPU=4/4,1478/525MHz,OC=FF,TA=0/0/0,SP=N/N/N,Mem=2092MHz,Free=5115MB,PLS=0,Temp=30.7C/0.0C,TW=1.42ms,App=-110.70ms,GD=0.14ms,CPU&GPU=0.00ms,LCnt=2(DR71,LM2),GPU%=0.21,CPU%=0.02(W0.05),DSF=1.00,CFL=19.70/21.44,LD=0
03-07 00:43:36.004 13334 13409 I VrApi   : FPS=72/72,Prd=24ms,Tear=0,Early=0,Stale=8,Stale2/5/10/max=0/0/1/30,VSnc=0,Lat=-1,Fov=0,CPU4/GPU=4/4,1478/525MHz,OC=FF,TA=0/0/0,SP=N/N/N,Mem=1353MHz,Free=5115MB,PLS=0,Temp=30.7C/0.0C,TW=1.43ms,App=0.84ms,GD=0.12ms,CPU&GPU=2.24ms,LCnt=3(DR72,LM3),GPU%=0.20,CPU%=0.15(W0.17),DSF=1.00,CFL=19.61/21.52,LD=0
03-07 00:43:37.002 13334 13409 I VrApi   : FPS=72/72,Prd=24ms,Tear=0,Early=0,Stale=0,Stale2/5/10/max=0/0/0/0,VSnc=0,Lat=-1,Fov=0,CPU4/GPU=4/4,1478/525MHz,OC=FF,TA=0/0/0,SP=N/N/N,Mem=1353MHz,Free=5115MB,PLS=0,Temp=30.7C/0.0C,TW=1.43ms,App=0.88ms,GD=0.12ms,CPU&GPU=2.23ms,LCnt=3(DR72,LM3),GPU%=0.20,CPU%=0.03(W0.05),DSF=1.00,CFL=19.69/21.41,LD=0
"""
