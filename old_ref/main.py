#from PyQt5 import QtCore, QtGui, QtWidgets
#from newUser import Ui_MainWindow
import sys , os, openpyxl, csv
#инициализация


#переменные
melle = 1
HEAD_PROTOCOL = []
MESTO_GROOPPE_V_SPISKE = 3
LIST_GROOP = ["мальчики 2011-2013" ,"девочки 2011-2013" ,"мальчики 2007-2010","девочки 2007-2010","мальчики 2014-2016" , "девочки 2014-2016" ]
#
def cvalific_callV3(pat):#считает результаты окончательно, оно работает на волшебном дыме
    listMain = []
    prwd = openpyxl.load_workbook(pat)
    final = openpyxl.Workbook()
    for i in LIST_GROOP:
        final.create_sheet(i)
        finalList = final[i]
        listMain = []
        prws  = prwd[i]
        listcalc = [2, 4,5 ,9,10,11,12]
        for iV in range(2, none(prws , "v")):# перебор по вертикали/строкам
            list1 =[]
            for iG in listcalc :# перебор по горизонтали/колонкам
                apend = prws.cell(row=iV, column=iG).value
                list1.append(apend)
            listMain.append(list1)
        try:
            list2 = sorted(listMain, key=lambda point: (-point[3],point[4],-point[5], point[6]))
        except:
            pass
        print(list2)
        c=1
        for i in list2:  
            i.insert(0 ,c )  
            finalList.append(i)
            c +=1
        
        final.save(pat + ".xlsx")
    prwd.close#закрытие файла
    final.close
    return(listMain)

def cvalific_call2(pat):#считает результаты окончательно
    listMain = []
    prwd = openpyxl.load_workbook(pat)
    final = openpyxl.Workbook()
    for i in LIST_GROOP:
        final.create_sheet(i)
        finalList = final[i]
        listMain = []
        prws  = prwd[i]
        for iV in range(1, none(prws , "v")):# перебор по вертикали/строкам
            list1 =[]
            for iG in range(1, none(prws , "g")) :# перебор по горизонтали/колонкам
                apend = prws.cell(row=iV, column=iG).value
                list1.append(apend)
                print(apend)
            listMain.append(list1)
        list2 = sorted(listMain, key=lambda point: (-point[2],point[3],-point[4], point[5]))
        print(list2)
        c=1
        for i in list2:  
            i.insert(0 ,c )  
            finalList.append(i)
            c +=1
        final.save("end" + pat)
    prwd.close#закрытие файла
    final.close
    return(listMain)

def fromItogPrtocol(endCval, endFin, itogprotacol,csv1 ):
    Fin = openpyxl.load_workbook(endFin)
    Cval = openpyxl.load_workbook(endCval)
    itog = openpyxl.load_workbook(itogprotacol)
    obj = open(csv1 , encoding="utf-8")
    for ls in LIST_GROOP:
        lFin = Fin[ls]
        iCval = Cval[ls]
        litog = itog[ls]
        for iV in range(1, none(lFin, "v")): # считаем финалы
            stroka = []
            obj = open(csv1 , encoding="utf-8")
            file_reader1 = csv.reader(obj, delimiter = ",")
            print ( " csv ligin")
            for iG in range(1, none(lFin , "g")):
                stroka.append(lFin.cell(row=iV, column=iG).value)
            name = stroka[1]
            for icsv in file_reader1:
                if name == icsv[1]:
                    stroka.insert(2 , icsv[2][:4])# ГОД РОЖДЕНИЯ # здесь МОЖЕТ БЫТЬ ОШИБКА!!!!!
                    stroka.insert(3 , icsv[3])#РАЗРЯД
                    #stroka.insert(4 , icsv[4])#город
                    for i in range(1, none(iCval, "v")):
                        if iCval.cell(row = i, column = 2 ).value == name:
                            stroka.insert(5 , iCval.cell(row = i, column = 8 ).value )# top
                            stroka.insert(5 , iCval.cell(row = i, column = 7 ).value )#popitki top 
                            stroka.insert(5 , iCval.cell(row = i, column = 6 ).value )#zone 
                            stroka.insert(5 , iCval.cell(row = i, column = 5 ).value )#popitki Zone
            litog.append(stroka)
            print (stroka)
        print ("cvalific")    
        for iV in range(6, none(iCval, "v")): # считаем квалификацию
            stroka = []
            obj = open(csv1 , encoding="utf-8")
            file_reader1 = csv.reader(obj, delimiter = ",")
            print ( " csv ligin")
            for iG in range(1, none(iCval , "g")):
                stroka.append(iCval.cell(row=iV, column=iG).value)
            name = stroka[1]
            for icsv in file_reader1:
                if name == icsv[1]:
                    stroka.insert(2 , icsv[2][:4])# ГОД РОЖДЕНИЯ # здесь МОЖЕТ БЫТЬ ОШИБКА!!!!!
                    #stroka.insert(4 , icsv[4])#город
            litog.append(stroka)
            print (stroka)
        
        itog.save("itogprotacol.xlsx")

def cvalific_call(pat):#считает результаты окончательно, оно работает на волшебном дыме
    listMain = []
    prwd = openpyxl.load_workbook(pat)
    final = openpyxl.Workbook()
    for i in LIST_GROOP:
        final.create_sheet(i)
        finalList = final[i]
        listMain = []
        prws  = prwd[i]
        for iV in range(1, none(prws , "v")):# перебор по вертикали/строкам
            list1 =[]
            for iG in range(1, none(prws , "g")) :# перебор по горизонтали/колонкам
                apend = prws.cell(row=iV, column=iG).value
                list1.append(apend)
            listMain.append(list1)
        try:
            list2 = sorted(listMain, key=lambda point: (-point[3],point[4],-point[5], point[6]))
        except:
            pass
        print(list2)
        c=1
        for i in list2:  
            i.insert(0 ,c )  
            finalList.append(i)
            c +=1
        
        final.save(pat + ".xlsx")
    prwd.close#закрытие файла
    final.close
    return(listMain)

def startSort( pat , pat2):# делаем стартовый протокол и распределяем по группам
    wb= openpyxl.Workbook() 
    coi = 0
    for i3 in LIST_GROOP :# создаём листы для стартовых протоколов
        wb.create_sheet(i3)
        ws = wb[i3]
        tB= ["время предрегистрации" , "Ф.И.О", "дата рождения", "разряд", "город", "команда", "тренер", "Группа"]
        for rang in range(1, 30):
                    tB.append("Т-"+str(rang))
                    tB.append("Б-"+str(rang))
        ws.append(tB)
        print(i3)
        obj = open(pat2 , encoding="utf-8")
        file_reader1 = csv.reader(obj, delimiter = ",")
        for i in file_reader1:# тут мы тырим из массива 1 строку
            print(coi)
            if i[7] == i3:# 7 это столбец группы
                ws.append(i)# добавляем стороку в xlsx файл
        coi += 1
    wb.save(pat)
    return(i)

def res(bol):#возвращает реверсивный булиан
    if bol== True:
        bol = False
    elif bol == False:
        bol= True
    return(bol)

def Cvalific(pat, pat2):# считаем и записымаем в отдельный файл результаты квалификации
    listMain = []
    result = openpyxl.load_workbook(pat)
    wb= openpyxl.Workbook() 
    for i3 in LIST_GROOP :# создаём листы для результаов квалификации
        wb.create_sheet(i3)
        
    for sheet in LIST_GROOP :
        results  = result[sheet]
        ws = wb[sheet]
        for iV in range(2, none(results , "v")): # перебор строк вертикально
            t_b= True
            list1 =[]
            print (results.cell(row=iV, column=2).value + " next user") # логи))
            top = 0
            zone = 0
            topP= 0 
            zoneP = 0
            for iG in range(9, none(results , "g")): # перебор столбцов в строке  горизонтально
                apend = results.cell(row=iV, column=iG).value
                #print(apend , type(apend))
                if not apend:
                    pass
                elif t_b:
                    #print("это топы ")
                    top +=1
                    topP += apend
                elif t_b != True:
                    #print("это бонусы")
                    zone  +=1
                    zoneP += apend
                t_b = res(t_b)
            print( " топов" , top , "попыток", topP, "зон", zone, "попыток зон" , zoneP)# тоже лог)))
            listMain=[results.cell(row=iV, column=2).value ,results.cell(row=iV, column=4).value ,results.cell(row=iV, column=5).value , top , topP,zone,zoneP ] # добавляем строку в xlsx файл
            ws.append(listMain)
    wb.save(pat2)
    #cvalific_call(pat2)
def Cvalific2(pat, pat2):# считаем и записымаем в отдельный файл результаты квалификации
    listMain = []
    result = openpyxl.load_workbook(pat)
    wb= openpyxl.Workbook() 
    for i3 in LIST_GROOP :# создаём листы для результаов квалификации
        wb.create_sheet(i3)
        
    for sheet in LIST_GROOP :
        results  = result[sheet]
        ws = wb[sheet]
        for iV in range(2, none(results , "v")): # перебор строк вертикально
            t_b= True
            list1 =[]
            print (results.cell(row=iV, column=2).value + " next user")
            top = 0
            zone = 0
            topP= 0 
            zoneP = 0
            for iG in range(5, none(results , "g")):
                apend = results.cell(row=iV, column=iG).value
                #print(apend , type(apend))
                if not apend:
                    pass
                elif t_b:
                    #print("это топы ")
                    top +=1
                    topP += apend
                elif t_b != True:
                    #print("это бонусы")
                    zone  +=1
                    zoneP += apend
                t_b = res(t_b)
            print( " топов" , top , "попыток", topP, "зон", zone, "попыток зон" , zoneP)
            listMain=[results.cell(row=iV, column=2).value ,results.cell(row=iV, column=4).value  , top , topP,zone,zoneP ]
            ws.append(listMain)
            print(results.cell(row=iV, column=5))
    wb.save(pat2)
    cvalific_call2(pat2)
def none( ws , type ):#возвращает крайние свободные ячейки
    val = 1
    i = 0
    while val != None: 
        i = i +1
        if type == "v":
            val =ws.cell(row=i, column=1).value
        if type == "g":
            val =ws.cell(row=1, column=i).value
    return(i)   

def formFinal(pat , pat2):
    listMain = []
    tB = ["Место" ,"Ф.И.О." , "разряд", "город"]
    prwd = openpyxl.load_workbook(pat)
    ff = openpyxl.Workbook()
    for rang in range(1, 5):
                    tB.append("Т-"+str(rang))
                    tB.append("Б-"+str(rang))
    for i in LIST_GROOP:
        ff.create_sheet(i)
        fflList = ff[i]
        listMain = []
        prws  = prwd[i]
        fflList.append(tB)
        for iV in range(1, 7):# перебор по вертикали/строкам
            list1 =[]
            for iG in range(1, 5) :# перебор по горизонтали/колонкам
                apend = prws.cell(row=iV, column=iG).value
                list1.append(apend)
                
            list1.insert(0 , iV)
            list1.pop()
            listMain.append(list1)

            
        for i in listMain:
            fflList.append(i)
            print(type(i[1]))   
    ff.save(pat2) 
def formStart( path1,  csv1 ):
    wb= openpyxl.Workbook() 
    coi = 0
    for i3 in LIST_GROOP :# создаём листы для стартовых протоколов
        wb.create_sheet(i3)
        ws = wb[i3]
        tB= ["время предрегистрации" , "Ф.И.О", "дата рождения", "разряд", "город", "команда", "тренер", "Группа", "Top", "PTop", "Zone", "PZone"]
        ws.append(tB)
        print(i3)
        obj = open(csv1 , encoding="utf-8")
        file_reader1 = csv.reader(obj, delimiter = ",")# возвращяет массив который можно итерировать только один раз, после использования вызывать сначала open()
        for i in file_reader1:# тут мы тырим из массива 1 строку
            print(coi)
            if i[7] == i3:# 7 это столбец группы
                ws.append(i)# добавляем стороку в xlsx файл
        coi += 1
    wb.save(path1)
    return(i)


while True:
    inp = input("введите комfнду")
    if inp == "exit": 
        break
    elif inp == "formItogProtacol":
        fromItogPrtocol(input("введите путь к файлу с результатами квалификации") , input("введите путь к файлу с подщитаными результатами финала"), input("введите название файла для итогового протакола"), input("введите путь с CSV файлу"))
    elif inp == "import":
        startSort(input("введите путь сейва") , input("введите путь с CSV файлу") )
    elif inp == "calcCvalific":
        Cvalific(input("введите путь к файлу с результатами квалификации") , input("введите название файла подщитанных результатов квалификации"))
    elif inp == "formFinal":
        formFinal(input("введите путь к файлу подщётов результатов квалификации"), input("введите путь сохнанения стартовых протоколов финалов "  )  )
    elif inp == "calcFinal":
        Cvalific2(input("введите путь к файлу с результатами финала") , input("введите желаемый путь к сейву подщитанных результатов финала"))
    elif inp == "formStart": # замена import
        formStart(input("введите путь сейва") , input("введите путь с CSV файлу") )
    elif inp == "calcStart":
        cvalific_callV3(input("введите путь к файлу с результатами квалификации"))
    elif inp == "formInput":
        print ("lol no working")
        cvalific_call(input("введите путь к файлу с результатами квалификации"))
    elif inp == "help":
        print("""
        elif inp == "formItogProtacol": # это фунция делает итоговый протакол на основе всех результатов
        elif inp == "import":       #НЕ ИСПОЛЬЗУЕТСЯ , формирует стартовый протокол с местом для попыток каждой трассы.
        elif inp == "calcCvalific": #НЕ ИСПОЛЬЗУЕТСЯ, считает квалификацию , используется вместе с import, с другими не использовать.
        elif inp == "formFinal": #формирование стартового протакола финалов,
        elif inp == "calcFinal": #подсчёт финалов
        elif inp == "formStart": # замена import
        elif inp == "calcStart": #подсчёт квалификации, использовать вместе с formStart()
        """)