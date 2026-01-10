import os
import re
# SCONSTRUCT file interesting lines
# config.version = Version(
# major=15,
# minor=0,
# point=6,
# patch=0
#)
def updateSconstruct():
    "Update the build number in the SConstruct file"
    os.chmod(os.path.join(os.environ["SourcePath"],"develop","global","src","SConstruct"), int(755))
    fin = open(os.path.join(os.environ["SourcePath"],"develop","global","src","SConstruct"), 'r')
    fout = open(os.path.join(os.environ["SourcePath"],"develop","global","src","SConstruct1"), 'w')
    for line in fin:
        line=re.sub("point\'=[\'d]+","point="+os.environ["BuildNum"],line)
        fout.write(line)
    fin.close()
    fout.close()
    os.remove(os.path.join(os.environ["SourcePath"],"develop","global","src","SConstruct"))
    os.rename(os.path.join(os.environ["SourcePath"],"develop","global","src","SConstruct1"),
        os.path.join(os.environ["SourcePath"],"develop","global","src","SConstruct"))

# VERSION file interesting line
# ADLMSDK_VERSION_POINT=6
def updateVersion():
    "Update the build number in the VERSION file"
    os.chmod(os.path.join(os.environ["SourcePath"],"develop","global","src","VERSION"), int(755))
    fin = open(os.path.join(os.environ["SourcePath"],"develop","global","src","VERSION"), 'r')
    fout = open(os.path.join(os.environ["SourcePath"],"develop","global","src","VERSION1"), 'w')
    for line in fin:
        line=re.sub("ADLMSDK_VERSION_POINT=[\'d]+","ADLMSDK_VERSION_POINT="+os.environ["BuildNum"],line)
        fout.write(line)
    fin.close()
    fout.close()
    os.remove(os.path.join(os.environ["SourcePath"],"develop","global","src","VERSION"))
    os.rename(os.path.join(os.environ["SourcePath"],"develop","global","src","VERSION1"),
        os.path.join(os.environ["SourcePath"],"develop","global","src","VERSION"))

def main():
    updateSconstruct()
    updateVersion()

main()
