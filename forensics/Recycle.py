import os
import winreg


def getRecycleDir():
    dirs = ['C:\\Recycler\\', 'C:\\Recycled\\', 'C:\\$Recycle.Bin\\']
    for recycleDir in dirs:
        if os.path.isdir(recycleDir):
            return recycleDir

    return None


def sid2user(sid):
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                             "SOFTWARE\Microsoft\Windows NT\CurrentVersion\ProfileList\\" + sid)
        profileImagePath, _ = winreg.QueryValueEx(key, 'ProfileImagePath')
        user = profileImagePath.split('\\')[-1]
        return user
    except:
        return sid


if __name__ == '__main__':

    recycleDir = getRecycleDir()
    sidList = os.listdir(recycleDir)

    print(recycleDir)
    for sid in sidList:
        files = os.listdir(recycleDir + sid)
        user = sid2user(sid)
        print('\n[*] Listing Files For User:', str(user))
        for file in files:
            print('[+] Found file:', str(file))
