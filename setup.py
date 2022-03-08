print("Here will be shown all the progress of installation.")
print("Здесь будет показан процесс установки.")
import os
eng = input("Choose your language (ru/en)\nВыберите язык (ru/en) - ") != "ru"
text = {
    "langselected": {
        "ru":"Язык выбран!",
        "en":"Language selected!"
    },
    "insconfirm": {
        "ru":"После нажатия Enter папка и программы будут установлены здесь. После установки прочитайте README.txt. Во время работы программы не редактируйте созданные файлы.",
        "en":"After pressing Enter, the folder and files will be created here. After installing read README.txt. Do not edit created files while installing."
    },
    "step1": {
        "ru":"DEBUG | Установка файлов.",
        "en":"DEBUG | Creating files."
    },
    "step2":{
        "ru":"DEBUG | Создаем show.py...",
        "en":"DEBUG | Creating show.py..."
    },
    "step3":{
        "ru":"DEBUG | Создаем hide.py...",
        "en":"DEBUG | Creating hide.py..."
    },
    "step4":{
        "ru":"DEBUG | Создаем contents.txt и присваиваем ему пароль...",
        "en":"DEBUG | Creating contents.txt and assigning it the password..."
    },
    "compiling": {
        "ru":"Почти готово. Компилируем hide.py, passchanger.py и show.py...",
        "en":"Almost ready. Compiling hide.py, passchanger.py and show.py..."
    },
    "ready":{
        "ru":"Готово! Теперь вы можете хранить файлы. \nИз-за бага с библиотеками, пожалуйста, перейдите по указанному в процессе компиляции пути и скопируйте оттуда файлы show.exe и hide.exe. (скорее всего 'Updating manifest in <нужный путь>')\nВы можете закрыть программу.",
        "en":"All done! Now you can store your files. \nBecause of a problem with libraries, you need to go to a path shown in the compiling log and copy the executables. (most probably 'Updating manifest in <the path you need>')\nYou can close this window."
    },
    "readme":{
        "ru":"Создаем README.txt...",
        "en":"Creating README.txt..."
    },
    "step3.5":{
        "ru":"DEBUG | Создаем passchanger.py...",
        "en":"DEBUG | Creating passchanger.py..."
    }
}
def printtext(t):
    global text,eng
    print(text[t]["en" if eng else "ru"])
printtext("langselected")
printtext("insconfirm")
input()
printtext("step1")
p = os.path.dirname(os.path.realpath(__file__))
if eng:     
    dirs = p+"\\Hidden files\\hidden folder"
    sdir = p+"\\Hidden files\\"
else:   
    dirs = p+"\\Скрытые файлы\\hidden folder"
    sdir = p+"\\Скрытые файлы\\"


os.makedirs(dirs)
printtext("step3.5")
with open(sdir+"passchanger.py", "w") as f:
    f.write(r"""
from ctypes import *

import sys, os
kernel32 = windll.kernel32

LPSTR     = c_wchar_p
DWORD     = c_ulong
LONG      = c_ulong
WCHAR     = c_wchar * 296
LONGLONG  = c_longlong

class LARGE_INTEGER_UNION(Structure):
    _fields_ = [
        ("LowPart", DWORD),
        ("HighPart", LONG),]

class LARGE_INTEGER(Union):
    _fields_ = [
        ("large1", LARGE_INTEGER_UNION),
        ("large2", LARGE_INTEGER_UNION),
        ("QuadPart",    LONGLONG),
    ]

class WIN32_FIND_STREAM_DATA(Structure):
    _fields_ = [
        ("StreamSize", LARGE_INTEGER),
        ("cStreamName", WCHAR),
    ]
    '''
    typedef struct _WIN32_FIND_STREAM_DATA {
      LARGE_INTEGER StreamSize;
      WCHAR         cStreamName[MAX_PATH + 36];
    } WIN32_FIND_STREAM_DATA, *PWIN32_FIND_STREAM_DATA;
    '''

class ADS():
    def __init__(self, filename):
        self.filename = filename
        self.streams = self.init_streams()

    def init_streams(self):
        file_infos = WIN32_FIND_STREAM_DATA()
        streamlist = list()

        findFirstStreamW = kernel32.FindFirstStreamW
        findFirstStreamW.restype = c_void_p

        myhandler = kernel32.FindFirstStreamW (LPSTR(self.filename), 0, byref(file_infos), 0)
        '''
        HANDLE WINAPI FindFirstStreamW(
          __in        LPCWSTR lpFileName,
          __in        STREAM_INFO_LEVELS InfoLevel, (0 standard, 1 max infos)
          __out       LPVOID lpFindStreamData, (return information about file in a WIN32_FIND_STREAM_DATA if 0 is given in infos_level
          __reserved  DWORD dwFlags (Reserved for future use. This parameter must be zero.) cf: doc
        );
        https://msdn.microsoft.com/en-us/library/aa364424(v=vs.85).aspx
        '''
        p = c_void_p(myhandler)

        if file_infos.cStreamName:
            streamname = file_infos.cStreamName.split(":")[1]
            if streamname: streamlist.append(streamname)

            while kernel32.FindNextStreamW(p, byref(file_infos)):
                streamlist.append(file_infos.cStreamName.split(":")[1])

        kernel32.FindClose(p)  # Close the handle

        return streamlist

    def __iter__(self):
        return iter(self.streams)

    def has_streams(self):
        return len(self.streams) > 0

    def full_filename(self, stream):
        return "%s:%s" % (self.filename, stream)

    def add_stream_from_file(self, filename):
        if os.path.exists(filename):
            with open(filename, "rb") as f:
                content = f.read()
            return self.add_stream_from_string(filename, content)
        else:
            print("Could not find file: {0}".format(filename))
            return False

    def add_stream_from_string(self, stream_name, string):
        fullname = self.full_filename(os.path.basename(stream_name))
        if os.path.exists(fullname):
            print("Stream name already exists")
            return False
        else:
            fd = open(fullname, "wb")
            fd.write(string)
            fd.close()
            self.streams.append(stream_name)
            return True

    def delete_stream(self, stream):
        try:
            os.remove(self.full_filename(stream))
            self.streams.remove(stream)
            return True
        except:
            return False

    def get_stream_content(self, stream):
        fd = open(self.full_filename(stream), "rb")
        content = fd.read()
        fd.close()
        return content


from os.path import dirname,realpath
from time import sleep
def main():
    p = dirname(realpath(__file__))
    a = ADS(p+"\\hidden folder\\contents.txt")
    if input("Password: ") != a.get_stream_content("streampass.txt").decode("utf-8"):   return "Wrong password!"
    a.delete_stream("streampass.txt")
    a.add_stream_from_string("streampass",input("New password: ").encode("utf-8"))
    return "Success!"
print(main())
sleep(5)

    """)
printtext("step2")
with open(sdir+"show.py", "w") as f:
    f.write(r"""
from ctypes import *

import sys, os
kernel32 = windll.kernel32

LPSTR     = c_wchar_p
DWORD     = c_ulong
LONG      = c_ulong
WCHAR     = c_wchar * 296
LONGLONG  = c_longlong

class LARGE_INTEGER_UNION(Structure):
    _fields_ = [
        ("LowPart", DWORD),
        ("HighPart", LONG),]

class LARGE_INTEGER(Union):
    _fields_ = [
        ("large1", LARGE_INTEGER_UNION),
        ("large2", LARGE_INTEGER_UNION),
        ("QuadPart",    LONGLONG),
    ]

class WIN32_FIND_STREAM_DATA(Structure):
    _fields_ = [
        ("StreamSize", LARGE_INTEGER),
        ("cStreamName", WCHAR),
    ]
    '''
    typedef struct _WIN32_FIND_STREAM_DATA {
      LARGE_INTEGER StreamSize;
      WCHAR         cStreamName[MAX_PATH + 36];
    } WIN32_FIND_STREAM_DATA, *PWIN32_FIND_STREAM_DATA;
    '''

class ADS():
    def __init__(self, filename):
        self.filename = filename
        self.streams = self.init_streams()

    def init_streams(self):
        file_infos = WIN32_FIND_STREAM_DATA()
        streamlist = list()

        findFirstStreamW = kernel32.FindFirstStreamW
        findFirstStreamW.restype = c_void_p

        myhandler = kernel32.FindFirstStreamW (LPSTR(self.filename), 0, byref(file_infos), 0)
        '''
        HANDLE WINAPI FindFirstStreamW(
          __in        LPCWSTR lpFileName,
          __in        STREAM_INFO_LEVELS InfoLevel, (0 standard, 1 max infos)
          __out       LPVOID lpFindStreamData, (return information about file in a WIN32_FIND_STREAM_DATA if 0 is given in infos_level
          __reserved  DWORD dwFlags (Reserved for future use. This parameter must be zero.) cf: doc
        );
        https://msdn.microsoft.com/en-us/library/aa364424(v=vs.85).aspx
        '''
        p = c_void_p(myhandler)

        if file_infos.cStreamName:
            streamname = file_infos.cStreamName.split(":")[1]
            if streamname: streamlist.append(streamname)

            while kernel32.FindNextStreamW(p, byref(file_infos)):
                streamlist.append(file_infos.cStreamName.split(":")[1])

        kernel32.FindClose(p)  # Close the handle

        return streamlist

    def __iter__(self):
        return iter(self.streams)

    def has_streams(self):
        return len(self.streams) > 0

    def full_filename(self, stream):
        return "%s:%s" % (self.filename, stream)

    def add_stream_from_file(self, filename):
        if os.path.exists(filename):
            with open(filename, "rb") as f:
                content = f.read()
            return self.add_stream_from_string(filename, content)
        else:
            print("Could not find file: {0}".format(filename))
            return False

    def add_stream_from_string(self, stream_name, string):
        fullname = self.full_filename(os.path.basename(stream_name))
        if os.path.exists(fullname):
            print("Stream name already exists")
            return False
        else:
            fd = open(fullname, "wb")
            fd.write(string)
            fd.close()
            self.streams.append(stream_name)
            return True

    def delete_stream(self, stream):
        try:
            os.remove(self.full_filename(stream))
            self.streams.remove(stream)
            return True
        except:
            return False

    def get_stream_content(self, stream):
        fd = open(self.full_filename(stream), "rb")
        content = fd.read()
        fd.close()
        return content


from os.path import dirname,realpath
from time import sleep
def main():
    p = dirname(realpath(__file__))
    a = ADS(p+"\\hidden folder\\contents.txt")
    if input("Password: ") != a.get_stream_content("streampass.txt").decode("utf-8"):   return "Wrong password!"
    for i in a.streams:
        if i == "streampass.txt":   continue
        print("Found stream: "+i)
        with open(p+"\\hidden folder\\"+i,"wb") as f:
            f.write(a.get_stream_content(i))
            a.delete_stream(i)
    return "Success!"
print(main())
sleep(5)

    """)
printtext("step3")
with open(sdir+"hide.py","w") as f:
    f.write(r"""
from ctypes import *

import sys, os
kernel32 = windll.kernel32

LPSTR     = c_wchar_p
DWORD     = c_ulong
LONG      = c_ulong
WCHAR     = c_wchar * 296
LONGLONG  = c_longlong

class LARGE_INTEGER_UNION(Structure):
    _fields_ = [
        ("LowPart", DWORD),
        ("HighPart", LONG),]

class LARGE_INTEGER(Union):
    _fields_ = [
        ("large1", LARGE_INTEGER_UNION),
        ("large2", LARGE_INTEGER_UNION),
        ("QuadPart",    LONGLONG),
    ]

class WIN32_FIND_STREAM_DATA(Structure):
    _fields_ = [
        ("StreamSize", LARGE_INTEGER),
        ("cStreamName", WCHAR),
    ]
    '''
    typedef struct _WIN32_FIND_STREAM_DATA {
      LARGE_INTEGER StreamSize;
      WCHAR         cStreamName[MAX_PATH + 36];
    } WIN32_FIND_STREAM_DATA, *PWIN32_FIND_STREAM_DATA;
    '''

class ADS():
    def __init__(self, filename):
        self.filename = filename
        self.streams = self.init_streams()

    def init_streams(self):
        file_infos = WIN32_FIND_STREAM_DATA()
        streamlist = list()

        findFirstStreamW = kernel32.FindFirstStreamW
        findFirstStreamW.restype = c_void_p

        myhandler = kernel32.FindFirstStreamW (LPSTR(self.filename), 0, byref(file_infos), 0)
        '''
        HANDLE WINAPI FindFirstStreamW(
          __in        LPCWSTR lpFileName,
          __in        STREAM_INFO_LEVELS InfoLevel, (0 standard, 1 max infos)
          __out       LPVOID lpFindStreamData, (return information about file in a WIN32_FIND_STREAM_DATA if 0 is given in infos_level
          __reserved  DWORD dwFlags (Reserved for future use. This parameter must be zero.) cf: doc
        );
        https://msdn.microsoft.com/en-us/library/aa364424(v=vs.85).aspx
        '''
        p = c_void_p(myhandler)

        if file_infos.cStreamName:
            streamname = file_infos.cStreamName.split(":")[1]
            if streamname: streamlist.append(streamname)

            while kernel32.FindNextStreamW(p, byref(file_infos)):
                streamlist.append(file_infos.cStreamName.split(":")[1])

        kernel32.FindClose(p)  # Close the handle

        return streamlist

    def __iter__(self):
        return iter(self.streams)

    def has_streams(self):
        return len(self.streams) > 0

    def full_filename(self, stream):
        return "%s:%s" % (self.filename, stream)

    def add_stream_from_file(self, filename):
        if os.path.exists(filename):
            with open(filename, "rb") as f:
                content = f.read()
            return self.add_stream_from_string(filename, content)
        else:
            print("Could not find file: {0}".format(filename))
            return False

    def add_stream_from_string(self, stream_name, string):
        fullname = self.full_filename(os.path.basename(stream_name))
        if os.path.exists(fullname):
            print("Stream name already exists")
            return False
        else:
            fd = open(fullname, "wb")
            fd.write(string)
            fd.close()
            self.streams.append(stream_name)
            return True

    def delete_stream(self, stream):
        try:
            os.remove(self.full_filename(stream))
            self.streams.remove(stream)
            return True
        except:
            return False

    def get_stream_content(self, stream):
        fd = open(self.full_filename(stream), "rb")
        content = fd.read()
        fd.close()
        return content

        
from os import listdir,fsencode,remove
from os.path import dirname,realpath
from time import sleep
p = dirname(realpath(__file__))"""+f"""
directory = fsencode(p+"\\hidden folder")
a = ADS(p+"\\hidden folder\\contents.txt")
"""+
r"""
for file in listdir(directory):
    if file == b"contents.txt":     continue
    file = file.decode("utf-8")
    a.add_stream_from_file(p+"\\hidden folder\\"+file)
    print(f"Hiding {file}...")
    remove(p+f"\\hidden folder\\{file}")
print("Hidden successfully!")
sleep(5)
    """)
printtext("step4")
with open(dirs+"\\contents.txt",'wt',encoding='utf8') as f:    
    f.write('There is nothing here, surprised?' if eng else 'Здесь ничего нет!')

from ctypes import *
kernel32 = windll.kernel32

LPSTR     = c_wchar_p
DWORD     = c_ulong
LONG      = c_ulong
WCHAR     = c_wchar * 296
LONGLONG  = c_longlong

class LARGE_INTEGER_UNION(Structure):
    _fields_ = [
        ("LowPart", DWORD),
        ("HighPart", LONG),]
class LARGE_INTEGER(Union):
    _fields_ = [
        ("large1", LARGE_INTEGER_UNION),
        ("large2", LARGE_INTEGER_UNION),
        ("QuadPart",    LONGLONG),
    ]
class WIN32_FIND_STREAM_DATA(Structure):
    _fields_ = [
        ("StreamSize", LARGE_INTEGER),
        ("cStreamName", WCHAR),
    ]
    '''
    typedef struct _WIN32_FIND_STREAM_DATA {
      LARGE_INTEGER StreamSize;
      WCHAR         cStreamName[MAX_PATH + 36];
    } WIN32_FIND_STREAM_DATA, *PWIN32_FIND_STREAM_DATA;
    '''
class ADS():
    def __init__(self, filename):
        self.filename = filename
        self.streams = self.init_streams()

    def init_streams(self):
        file_infos = WIN32_FIND_STREAM_DATA()
        streamlist = list()

        findFirstStreamW = kernel32.FindFirstStreamW
        findFirstStreamW.restype = c_void_p

        myhandler = kernel32.FindFirstStreamW (LPSTR(self.filename), 0, byref(file_infos), 0)
        '''
        HANDLE WINAPI FindFirstStreamW(
          __in        LPCWSTR lpFileName,
          __in        STREAM_INFO_LEVELS InfoLevel, (0 standard, 1 max infos)
          __out       LPVOID lpFindStreamData, (return information about file in a WIN32_FIND_STREAM_DATA if 0 is given in infos_level
          __reserved  DWORD dwFlags (Reserved for future use. This parameter must be zero.) cf: doc
        );
        https://msdn.microsoft.com/en-us/library/aa364424(v=vs.85).aspx
        '''
        p = c_void_p(myhandler)

        if file_infos.cStreamName:
            streamname = file_infos.cStreamName.split(":")[1]
            if streamname: streamlist.append(streamname)

            while kernel32.FindNextStreamW(p, byref(file_infos)):
                streamlist.append(file_infos.cStreamName.split(":")[1])

        kernel32.FindClose(p)  # Close the handle

        return streamlist


    def full_filename(self, stream):
        return "%s:%s" % (self.filename, stream)

    def add_stream_from_string(self, stream_name, string):
        fullname = self.full_filename(os.path.basename(stream_name))
        if os.path.exists(fullname):
            print("Stream name already exists")
            return False
        else:
            fd = open(fullname, "wb")
            fd.write(string)
            fd.close()
            self.streams.append(stream_name)
            return True
a = ADS(dirs+"\\contents.txt")
a.add_stream_from_string("streampass",input("Enter the password for files: " if eng else "Введите пароль для файлов: ").encode("utf-8"))
del a,ADS,WIN32_FIND_STREAM_DATA,LARGE_INTEGER,LARGE_INTEGER_UNION,LONG,LONGLONG,WCHAR,DWORD,LPSTR,kernel32
import PyInstaller.__main__
from time import sleep
printtext("readme")
with open(sdir+"README.txt","wt",encoding="utf8") as f:
    f.write("""
Hello! Glad you opened this.
contents.txt is storing all the files that are hidden with no security,
but the way it's hidden is pretty unknown to most people, so nobody will find the files.
It is still secure, since you can't have alternate data streams in an USB drive because it stores files differently.
Your files are safe, unless you have AlternateDataStreamView or something like that on your PC.
You can't change the names of the folders, that will make them inaccessible.
Ironically, you can change the content of contents.txt, but not its name.
You can delete this README file now.
""" if eng else """
Привет! Рад что ты это открыл.
contents.txt хранит все спрятанные файлы без всякой защиты,
но способ, которым спрятаны файлы неизвестен большинству людей, так что файлы никто не найдет.
Это все равно хорошая защита, тк USB флешки не могут хранить Alternate Data Streams, поскольку там файлы хранятся по другому.
Файлы в безопасности, если у вас нет AlternateDataStreamView или наподобие этого.
Вы не можете переименовывать папки, иначе они станут недоступными.
Вы можете менять текст в contents.txt, но не его название.
Вы можете удалить этот README.
    """)
printtext("compiling")
sleep(3)
PyInstaller.__main__.run([
    sdir+'hide.py',
    '--onefile'
])
PyInstaller.__main__.run([
    sdir+'show.py',
    '--onefile'
])
PyInstaller.__main__.run([
    sdir+'passchanger.py',
    '--onefile'
])
printtext("ready")
os.remove(sdir+'show.py')
os.remove(sdir+'hide.py')
while True:     pass