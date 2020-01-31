import TosStructure
def exportJob(path,job):
    with open(path+"/job_"+job.engname+".txt","w") as f:
        f.write
def exportJobTree(path,jobtree:TosStructure.JobTree):
    for job in jobtree.jobs:
        exportJob(path,job)