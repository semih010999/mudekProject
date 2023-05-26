import sys
from PyQt5 import QtWidgets,QtCore
from PyQt5.QtWidgets import QFileDialog, QApplication, QMainWindow,QMessageBox
from PyQt5.uic import loadUi
import pyrebase
import json
import os
import logging
import res

firebaseConfig = {
  "apiKey": "AIzaSyAaB4aleIwvDTNwI3TH8ejS0P_u_n5VLzU",
  "authDomain": "yazilimmimarisi-948e6.firebaseapp.com",
  "databaseURL": "https://yazilimmimarisi-948e6-default-rtdb.firebaseio.com",
  "projectId": "yazilimmimarisi-948e6",
  "storageBucket": "yazilimmimarisi-948e6.appspot.com",
  "messagingSenderId": "492435203336",
  "appId": "1:492435203336:web:de113c8ee35dd52f67b8bd"
}

firebase = pyrebase.initialize_app(firebaseConfig)
db=firebase.database()
storage=firebase.storage()

class FirstScreen(QMainWindow):
    def __init__(self):
        super(FirstScreen,self).__init__()
        loadUi("ui/firstScreen.ui",self)
        self.btnQuit.clicked.connect(self.BtnQuit)
        self.btnOne.clicked.connect(self.academicianScreen)
        self.btnTwo.clicked.connect(self.coordinatorScreen)

    def BtnQuit(self):
        answer=QMessageBox.question(self,"Çıkış","Çıkmak istediğinize emin misiniz ?",\
                        QMessageBox.Yes | QMessageBox.No)
        if answer==QMessageBox.Yes:
            sys.exit(app.exec_())
        else:
            self.show()

    def academicianScreen(self):
        academicianScreen=AcademicianLoginScreen()
        widget.addWidget(academicianScreen)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def coordinatorScreen(self):
        coordinatorScreen=CoordinatorLoginScreen()
        widget.addWidget(coordinatorScreen)
        widget.setCurrentIndex(widget.currentIndex()+1)

class AcademicianLoginScreen(QMainWindow):
    def __init__(self):
        super(AcademicianLoginScreen,self).__init__()
        loadUi("ui/academicianScreen.ui",self)
        self.btnQuit.clicked.connect(self.BtnQuit)
        self.btnLogin.clicked.connect(self.loginFunction)

    def loginFunction(self):
        username = self.lineUsername.text()
        password = self.linePassword.text()
        academicians = db.child("academicians").get()
        for user in academicians.each():
            if user.val()["username"] == username and user.val()["password"] == password:
                userInfo = user.key()
                answer = QMessageBox.question(self, "GİRİŞ BAŞARILI", "Giriş Başarılı! Ana menüye Devam etmek İster misiniz?",\
                    QMessageBox.Yes | QMessageBox.No)
                if answer == QMessageBox.Yes:
                    self.mainScreen(username)
                else:
                    self.show()
                return userInfo
                
        QMessageBox.about(self, "GİRİŞ BAŞARISIZ", "Giriş Başarısız ya da Böyle Bir Kayıt Yok! Lütfen Tekrar Deneyin.")
        return None
    
    def mainScreen(self, Username):
        academicianMainScreen=AcademicianMainScreen()
        academicianMainScreen.firstFunction(Username)
        widget.addWidget(academicianMainScreen)
        widget.setCurrentIndex(widget.currentIndex()+1)


    def BtnQuit(self):
        answer=QMessageBox.question(self,"Çıkış","Çıkmak istediğinize emin misiniz ?",\
                        QMessageBox.Yes | QMessageBox.No)
        if answer==QMessageBox.Yes:
            sys.exit(app.exec_())
        else:
            self.show()

class CoordinatorLoginScreen(QMainWindow):
    def __init__(self):
        super(CoordinatorLoginScreen,self).__init__()
        loadUi("ui/coordinatorScreen.ui",self)
        self.btnQuit.clicked.connect(self.BtnQuit)
        self.btnLogin.clicked.connect(self.loginFunction)

    def loginFunction(self):
        username = self.lineUsername.text()
        password = self.linePassword.text()
        academicians = db.child("coordinator").get()
        for user in academicians.each():
            if user.val()["username"] == username and user.val()["password"] == password:
                userInfo = user.key()
                answer = QMessageBox.question(self, "GİRİŞ BAŞARILI", "Giriş Başarılı! Ana menüye Devam etmek İster misiniz?",\
                    QMessageBox.Yes | QMessageBox.No)
                if answer == QMessageBox.Yes:
                    self.mainScreen(username)
                else:
                    self.show()
                return userInfo
                
        QMessageBox.about(self, "GİRİŞ BAŞARISIZ", "Giriş Başarısız ya da Böyle Bir Kayıt Yok! Lütfen Tekrar Deneyin.")
        return None

    def mainScreen(self, Username):
        coordinatorMainScreen=CoordinatorMainScreen()
        coordinatorMainScreen.firstFunction(Username)
        widget.addWidget(coordinatorMainScreen)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def BtnQuit(self):
        answer=QMessageBox.question(self,"Çıkış","Çıkmak istediğinize emin misiniz ?",\
                        QMessageBox.Yes | QMessageBox.No)
        if answer==QMessageBox.Yes:
            sys.exit(app.exec_())
        else:
            self.show()

class CoordinatorMainScreen(QMainWindow):
    def __init__(self):
        super(CoordinatorMainScreen,self).__init__()
        loadUi("ui/coordinatorMainScreen.ui",self)
        self.btnQuit.clicked.connect(self.BtnQuit)
        self.btnAddUser.clicked.connect(self.createUser)
        

    def firstFunction(self,Username):
        self.titleUser.setText(Username)
        self.btnAddLessonPage.clicked.connect(lambda : self.lessonAddPage(Username))
        
        try:
            academicians = db.child("academicians").get()
            if academicians is not None:
                academicianKeys = []
                for academician in academicians.each():
                    academicianKeys.append(academician.val())

                data = "[{}]".format(",".join(json.dumps(key) for key in academicianKeys))
                academicianData = json.loads(data)

                info_text = ""
                for academician in academicianData:
                    if 'username' in academician:
                        username = academician['username']

                        academician_info_text = f"Ad Soyad : {username}"
                        
                        info_text += academician_info_text + "\n"
                    else:
                        logging.warning("Missing 'username' key in student: %s", academician)
                        
                self.listUsers.setText(info_text)
            else:
                self.listUsers.setText("Herhangi bir kayıt bulunamadı.")

        except Exception as e:
            logging.error("Error in firstFunction(): %s", e)
            self.listUsers.setText("Henüz bir kayıt eklenmemiş.")

    def createUser(self):
        username = self.lineUsername.text()
        password = self.linePassword.text()
        
        if not username or not password:
            QMessageBox.about(self, "Kayıt Başarısız", "Lütfen tüm alanları doldurun.")
            return
        
        data = {"username": username, "password": password}
        newUser = db.child("academicians").push(data)
        newUserId = newUser["name"]
        user_data = db.child("academicians").child(newUserId).get().val()
        
        if user_data["username"] == username and user_data["password"] == password:
            QMessageBox.about(self, "Kayıt Ekleme Başarılı", "Kayıt Ekleme Başarılı !")
        else:
            QMessageBox.about(self, "Kayıt Ekleme Başarısız", "Kayıt Ekleme Başarısız !")

        try:
            academicians = db.child("academicians").get()
            if academicians is not None:
                academicianKeys = []
                for academician in academicians.each():
                    academicianKeys.append(academician.val())

                data = "[{}]".format(",".join(json.dumps(key) for key in academicianKeys))
                academicianData = json.loads(data)

                info_text = ""
                for academician in academicianData:
                    if 'username' in academician:
                        username = academician['username']

                        academician_info_text = f"Ad Soyad : {username}"
                        
                        info_text += academician_info_text + "\n"
                    else:
                        logging.warning("Missing 'username' key in student: %s", academician)
                        
                self.listUsers.setText(info_text)
            else:
                self.listUsers.setText("Herhangi bir kayıt bulunamadı.")

        except Exception as e:
            logging.error("Error in firstFunction(): %s", e)
            self.listUsers.setText("Henüz bir kayıt eklenmemiş.")


    def BtnQuit(self):
        answer=QMessageBox.question(self,"Çıkış","Çıkmak istediğinize emin misiniz ?",\
                        QMessageBox.Yes | QMessageBox.No)
        if answer==QMessageBox.Yes:
            sys.exit(app.exec_())
        else:
            self.show()

    def lessonAddPage(self, Username):
        coordinatorMainScreenTwo=CoordinatorMainScreenTwo()
        coordinatorMainScreenTwo.firstFunction(Username)
        widget.addWidget(coordinatorMainScreenTwo)
        widget.setCurrentIndex(widget.currentIndex()+1)

class CoordinatorMainScreenTwo(QMainWindow):
    def __init__(self):
        super(CoordinatorMainScreenTwo,self).__init__()
        loadUi("ui/coordinatorMainScreenTwo.ui",self)
        self.btnQuit.clicked.connect(self.BtnQuit)
        self.btnAddLesson.clicked.connect(self.createLesson)

    def firstFunction(self,Username):
        self.titleUser.setText(Username)
        self.btnAddUserPage.clicked.connect(lambda : self.userAddPage(Username))

        try:
            lessons = db.child("lessons").get()
            if lessons is not None:
                lessonCodes = []
                for lessoN in lessons.each():
                    lessonCodes.append(lessoN.key())

                info_text = ""
                for LessonName in lessonCodes:
                    academicianLessons = db.child("lessons").child(LessonName).get()
                    if academicianLessons is not None:
                        lessonKeys = []
                        for lesson in academicianLessons.each():
                            lessonKeys.append(lesson.val())

                        data = "[{}]".format(",".join(json.dumps(key) for key in lessonKeys))
                        lessonData = json.loads(data)

                        for lessonn in lessonData:
                            if 'lessonName' in lessonn:
                                lessonnamE = lessonn['lessonName']
                                academicianName = lessonn['lessonAcademician']

                                lesson_info_text = f"{academicianName} - Ders adı : {lessonnamE}"
                                
                                info_text += lesson_info_text + "\n"
                            else:
                                logging.warning("Missing 'lessonname' key in lesson: %s", lessonn)
                    else:
                        logging.warning("No lessons found for academician: %s", academicianName)
                        
                if info_text:
                    self.listLessons.setText(info_text)
                else:
                    self.listLessons.setText("Herhangi bir kayıt bulunamadı.")
            else:
                self.listLessons.setText("Herhangi bir kayıt bulunamadı.")
        except Exception as e:
            logging.error("Error occurred while retrieving lesson data: %s", e)

    def createLesson(self):
        lessonName = self.lineLessonName.text()
        lessonCode = self.lineLessonCode.text()
        lessonYear = self.lineLessonYear.text()
        lessonAcademican = self.lineLessonAcademician.text()
        lessonBranch = self.lineLessonBranch.text()
        learnOutput = self.textEdit.toPlainText()
        lessonSubject = self.textEdit2.toPlainText()
        
        if not lessonName or not lessonCode or not lessonYear or not lessonAcademican or not lessonBranch or not learnOutput or not lessonSubject:
            QMessageBox.about(self, "Kayıt Başarısız", "Lütfen tüm alanları doldurun.")
            return
        
        data = {"lessonName": lessonName, "lessonCode": lessonCode, "lessonYear": lessonYear, "lessonAcademician": lessonAcademican, "lessonBranch": lessonBranch, "learnOutput": learnOutput, "lessonSubject": lessonSubject}
        newUser = db.child("lessons").child(lessonCode).push(data)
        newUserId = newUser["name"]
        lesson_data = db.child("lessons").child(lessonCode).child(newUserId).get().val()
        
        if lesson_data["lessonName"] == lessonName and lesson_data["lessonCode"] == lessonCode and lesson_data["lessonYear"] == lessonYear and lesson_data["lessonAcademician"] == lessonAcademican and lesson_data["lessonBranch"] == lessonBranch and lesson_data["learnOutput"] == learnOutput and lesson_data["lessonSubject"] == lessonSubject:
            QMessageBox.about(self, "Kayıt Ekleme Başarılı", "Kayıt Ekleme Başarılı !")
        else:
            QMessageBox.about(self, "Kayıt Ekleme Başarısız", "Kayıt Ekleme Başarısız !")

        try:
            lessons = db.child("lessons").get()
            if lessons is not None:
                lessonCodes = []
                for lessoN in lessons.each():
                    lessonCodes.append(lessoN.key())

                info_text = ""
                for LessonName in lessonCodes:
                    academicianLessons = db.child("lessons").child(LessonName).get()
                    if academicianLessons is not None:
                        lessonKeys = []
                        for lesson in academicianLessons.each():
                            lessonKeys.append(lesson.val())

                        data = "[{}]".format(",".join(json.dumps(key) for key in lessonKeys))
                        lessonData = json.loads(data)

                        for lessonn in lessonData:
                            if 'lessonName' in lessonn:
                                lessonnamE = lessonn['lessonName']
                                academicianName = lessonn['lessonAcademician']

                                lesson_info_text = f"{academicianName} - Ders adı : {lessonnamE}"
                                
                                info_text += lesson_info_text + "\n"
                            else:
                                logging.warning("Missing 'lessonname' key in lesson: %s", lessonn)
                    else:
                        logging.warning("No lessons found for academician: %s", academicianName)
                        
                if info_text:
                    self.listLessons.setText(info_text)
                else:
                    self.listLessons.setText("Herhangi bir kayıt bulunamadı.")
            else:
                self.listLessons.setText("Herhangi bir kayıt bulunamadı.")
        except Exception as e:
            logging.error("Error occurred while retrieving lesson data: %s", e)


    def BtnQuit(self):
        answer=QMessageBox.question(self,"Çıkış","Çıkmak istediğinize emin misiniz ?",\
                        QMessageBox.Yes | QMessageBox.No)
        if answer==QMessageBox.Yes:
            sys.exit(app.exec_())
        else:
            self.show()

    def userAddPage(self, Username):
        coordinatorMainScreen=CoordinatorMainScreen()
        coordinatorMainScreen.firstFunction(Username)
        widget.addWidget(coordinatorMainScreen)
        widget.setCurrentIndex(widget.currentIndex()+1)

class AcademicianMainScreen(QMainWindow):
    def __init__(self):
        super(AcademicianMainScreen,self).__init__()
        loadUi("ui/academicianMainScreen.ui",self)
        self.btnQuit.clicked.connect(self.BtnQuit)

    def firstFunction(self,Username):
        self.titleUser.setText(Username)
        self.btnAcademician.clicked.connect(lambda: self.checkLessonCodeAcademician(Username))
        self.btnMudekEmployee.clicked.connect(lambda: self.checkLessonCodeMudek(Username))

        try:
            lessons = db.child("lessons").get()
            if lessons is not None:
                lessonCodes = []
                for lessoN in lessons.each():
                    lessonCodes.append(lessoN.key())

                info_text = ""
                for LessonName in lessonCodes:
                    academicianLessons = db.child("lessons").child(LessonName).get()
                    if academicianLessons is not None:
                        lessonKeys = []
                        for lesson in academicianLessons.each():
                            lessonKeys.append(lesson.val())

                        data = "[{}]".format(",".join(json.dumps(key) for key in lessonKeys))
                        lessonData = json.loads(data)

                        for lessonn in lessonData:
                            if 'lessonName' in lessonn:
                                lessonnamE = lessonn['lessonName']
                                academicianName = lessonn['lessonAcademician']
                                LessonCode = lessonn['lessonCode']

                                lesson_info_text = f"{academicianName} - Ders adı : {lessonnamE} - Ders Kodu : {LessonCode}"
                                
                                info_text += lesson_info_text + "\n"
                            else:
                                logging.warning("Missing 'lessonname' key in lesson: %s", lessonn)
                    else:
                        logging.warning("No lessons found for academician: %s", academicianName)
                        
                if info_text:
                    self.listLessons.setText(info_text)
                else:
                    self.listLessons.setText("Herhangi bir kayıt bulunamadı.")
            else:
                self.listLessons.setText("Herhangi bir kayıt bulunamadı.")
        except Exception as e:
            logging.error("Error occurred while retrieving lesson data: %s", e)

    def checkLessonCodeAcademician(self, Username):
        lessonCode = self.lineLessonCode.text()
        if not lessonCode:
            QMessageBox.about(self, "Hata!", "Ders kodu boş bırakılamaz.")
        else:
            self.lessonDetailPage(Username, lessonCode)

    def checkLessonCodeMudek(self, Username):
        lessonCode = self.lineLessonCode.text()
        if not lessonCode:
            QMessageBox.about(self, "Hata!", "Ders kodu boş bırakılamaz.")
        else:
            self.mudekEmployeePage(Username, lessonCode)

    def lessonDetailPage(self, Username, LessonCode):
        lessonDetailPage=AcademicianMainScreenTwo()
        lessonDetailPage.firstFunction(Username, LessonCode)
        widget.addWidget(lessonDetailPage)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def mudekEmployeePage(self, Username, LessonCode):
        mudekEmployeePage=MudekEmployeeScreen()
        mudekEmployeePage.firstFunction(Username, LessonCode)
        widget.addWidget(mudekEmployeePage)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def BtnQuit(self):
        answer=QMessageBox.question(self,"Çıkış","Çıkmak istediğinize emin misiniz ?",\
                        QMessageBox.Yes | QMessageBox.No)
        if answer==QMessageBox.Yes:
            sys.exit(app.exec_())
        else:
            self.show()

class AcademicianMainScreenTwo(QMainWindow):
    def __init__(self):
        super(AcademicianMainScreenTwo,self).__init__()
        loadUi("ui/academicianMainScreenTwo.ui",self)
        self.btnQuit.clicked.connect(self.BtnQuit)
        self.btnAddFile.clicked.connect(self.addFile)
        self.btnAddLessonInfo.clicked.connect(self.createLessonNoteDetail)

    def firstFunction(self,Username,LessonCode):
        self.titleUser.setText(Username)
        self.titleLessonInfo.setText(LessonCode)

        try:
            fileNames = db.child("fileNames").get()
            if fileNames is not None:
                fileKeys = []
                for student in fileNames.each():
                    fileKeys.append(student.val())

                dataFile = "[{}]".format(",".join(json.dumps(key) for key in fileKeys))
                fileData = json.loads(dataFile)

                infoTextFile = "" 
                for file in fileData:
                    if 'fileName' in file:
                        fileName = file['fileName']
                        fileInfoText = f"Dosya Adı: {fileName}"
                        infoTextFile += fileInfoText + "\n"
                    else:
                        logging.warning("Missing 'fileName' key in file: %s", file)

                self.listFiles.setText(infoTextFile)
            else:
                self.listFiles.setText("Kayıt bulunamadı.")
        except Exception as e:
            logging.error("Error in setFileNames(): %s", e)
            self.listFiles.setText("Henüz doysa yüklenmemiş.")


    def addFile(self):
        fname, _ = QFileDialog.getOpenFileName(self, "Open File", "", "All Files (*);;PNG Files (*.png)")
        if not fname:
            QMessageBox.about(self,"Hata !","Dosya seçilmedi.")
            return
        QMessageBox.about(self,"Bekleyiniz !","İşlem tamamlanana kadar bekleyin internet hıznıza göre zaman alabilir. Tamamlanınca yeni bir uyarı göreceksiniz.")
        filename = str(fname)
        cloudfilename = self.lineFileName.text()
        if not cloudfilename:
            QMessageBox.about(self,"Hata !","Dosya adı girilmedi.")
            return
        firebase.storage().child(cloudfilename).put(filename)
        data={"fileName":cloudfilename}
        newFile=db.child("fileNames").push(data)
        newFileId = newFile["name"]
        file_data = db.child("fileNames").child(newFileId).get().val()
        if file_data["fileName"] == cloudfilename:
            QMessageBox.about(self,"Yükleme Başarılı !","Dosya Yükleme Başarılı")
        else:
            QMessageBox.about(self,"Yükleme Başarısız !","Dosya Yükleme Başarısız")

        try:
            fileNames = db.child("fileNames").get()
            if fileNames is not None:
                fileKeys = []
                for student in fileNames.each():
                    fileKeys.append(student.val())

                dataFile = "[{}]".format(",".join(json.dumps(key) for key in fileKeys))
                fileData = json.loads(dataFile)

                infoTextFile = "" 
                for file in fileData:
                    if 'fileName' in file:
                        fileName = file['fileName']
                        fileInfoText = f"Dosya Adı: {fileName}"
                        infoTextFile += fileInfoText + "\n"
                    else:
                        logging.warning("Missing 'fileName' key in file: %s", file)

                self.listFiles.setText(infoTextFile)
            else:
                self.listFiles.setText("Kayıt bulunamadı.")
        except Exception as e:
            logging.error("Error in setFileNames(): %s", e)
            self.listFiles.setText("Henüz doysa yüklenmemiş.")
    
    def createLessonNoteDetail(self):
        midterm = self.lineMidterm.text()
        final = self.lineFinal.text()
        homework = self.lineHomework.text()
        project = self.lineProject.text()
        activity = self.lineActivity.text()
        midtermNumber = self.lineMidterm2.text()
        finalNumber = self.lineFinal2.text()
        homeworkNumber = self.lineHomework2.text()
        projectNumber = self.lineProject2.text()
        activityNumber = self.lineActivity2.text()
        lessonCode = self.titleLessonInfo.text()
        
        if not midterm or not final or not homework or not project or not activity or not midtermNumber or not finalNumber or not homeworkNumber or not projectNumber or not activityNumber:
            QMessageBox.about(self, "Kayıt Başarısız", "Lütfen tüm alanları doldurun.")
            return
        
        data = {"midterm": midterm, "final": final, "homework": homework, "project": project, "activity": activity, "midtermNumber": midtermNumber, "finalNumber": finalNumber, "homeworkNumber": homeworkNumber, "projectNumber": projectNumber, "activityNumber": activityNumber}
        newUser = db.child("lessonsNoteInfo").child((lessonCode)).push(data)
        newUserId = newUser["name"]
        lesson_data = db.child("lessonsNoteInfo").child(lessonCode).child(newUserId).get().val()
        
        if lesson_data["midterm"] == midterm and lesson_data["final"] == final and lesson_data["homework"] == homework and lesson_data["project"] == project and lesson_data["activity"] == activity and lesson_data["midtermNumber"] == midtermNumber and lesson_data["finalNumber"] == finalNumber and lesson_data["homeworkNumber"] == homeworkNumber and lesson_data["projectNumber"] == projectNumber and lesson_data["activityNumber"] == activityNumber:
            QMessageBox.about(self, "Başarılı !", "Bilgi Ekleme Başarılı !")
        else:
            QMessageBox.about(self, "Başarısız !", "Bilgi Ekleme Başarısız !")

    def BtnQuit(self):
        answer=QMessageBox.question(self,"Çıkış","Çıkmak istediğinize emin misiniz ?",\
                        QMessageBox.Yes | QMessageBox.No)
        if answer==QMessageBox.Yes:
            sys.exit(app.exec_())
        else:
            self.show()

class MudekEmployeeScreen(QMainWindow):
    def __init__(self):
        super(MudekEmployeeScreen,self).__init__()
        loadUi("ui/mudekEmployeeScreen.ui",self)
        self.btnQuit.clicked.connect(self.BtnQuit)

    def firstFunction(self,Username,LessonCode):
        self.titleUser.setText(Username)
        self.titleLessonInfo.setText(LessonCode)

        #dosya isimlerini çekme ve yazdırma
        try:
            fileNames = db.child("fileNames").get()
            if fileNames is not None:
                fileKeys = []
                for student in fileNames.each():
                    fileKeys.append(student.val())

                dataFile = "[{}]".format(",".join(json.dumps(key) for key in fileKeys))
                fileData = json.loads(dataFile)

                infoTextFile = "" 
                for file in fileData:
                    if 'fileName' in file:
                        fileName = file['fileName']
                        fileInfoText = f"Dosya Adı: {fileName}"
                        infoTextFile += fileInfoText + "\n"
                    else:
                        logging.warning("Missing 'fileName' key in file: %s", file)

                self.listFiles.setText(infoTextFile)
            else:
                self.listFiles.setText("Kayıt bulunamadı.")
        except Exception as e:
            logging.error("Error in setFileNames(): %s", e)
            self.listFiles.setText("Henüz doysa yüklenmemiş.")

        #öğrenme çıktıları ve ders konularını çekme ve yazdırma
        try:
            lesson = db.child("lessons").child(LessonCode).get()
            if lesson is not None:
                lessonCodeKeys = []
                for lessonn in lesson.each():
                    lessonCodeKeys.append(lessonn.val())

                data = "[{}]".format(",".join(json.dumps(key) for key in lessonCodeKeys))
                lessonInfosData = json.loads(data)

                info_text = ""
                info_text_2 = ""
                for lessonInfos in lessonInfosData:
                    if 'lessonCode' in lessonInfos:
                        learnOutput = lessonInfos['learnOutput']
                        lessonSubject = lessonInfos['lessonSubject']

                        learnOutput_info_text = f"{learnOutput}"
                        lessonSubject_info_text = f"{lessonSubject}"

                        info_text += learnOutput_info_text + "\n"
                        info_text_2 += lessonSubject_info_text + "\n"

                    else:
                        logging.warning("Missing 'lessonname' key in lesson: %s", lessonInfos)

                if info_text:
                    self.listLearnOutput.setText(info_text)
                else:
                    self.listLearnOutput.setText("Herhangi bir kayıt bulunamadı.")

                if info_text_2:
                    self.listLessonSubject.setText(info_text_2)
                else:
                    self.listLessonSubject.setText("Herhangi bir kayıt bulunamadı.")
            else:
                self.listLearnOutput.setText("Herhangi bir kayıt bulunamadı.")
                self.listLessonSubject.setText("Herhangi bir kayıt bulunamadı.")
        except Exception as e:
            logging.error("Error occurred while retrieving lesson data: %s", e)

        #ders notlandırma bilgilerini çekme ve yazdırma
        try:
            lessonNotes = db.child("lessonsNoteInfo").child(LessonCode).get()
            if lessonNotes is not None:
                lessonKeys = []
                for lesson in lessonNotes.each():
                    lessonKeys.append(lesson.val())

                data = "[{}]".format(",".join(json.dumps(key) for key in lessonKeys))
                lessonNotesData = json.loads(data)

                info_text = ""
                row = ""
                for lessonn in lessonNotesData:
                    if 'midterm' in lessonn:
                        midterm = lessonn['midterm']
                        final = lessonn['final']
                        homework = lessonn['homework']
                        project = lessonn['project']
                        activity = lessonn['activity']
                        midtermNumber = lessonn['midtermNumber']
                        finalNumber = lessonn['finalNumber']
                        homeworkNumber = lessonn['homeworkNumber']
                        projectNumber = lessonn['projectNumber']
                        activityNumber = lessonn['activityNumber']
                        row1 = lessonn['row1']
                        row2 = lessonn['row2']
                        row3 = lessonn['row3']
                        row4 = lessonn['row4']
                        row5 = lessonn['row5'] 

                        lessonNote_info_text = f"Vize : {midterm} - {midtermNumber}\nFinal : {final} - {finalNumber}\nÖdev : {homework} - {homeworkNumber}\nProje : {project} - {projectNumber}\nUygulama : {activity} - {activityNumber}"
                        row_info_text = f"{row1}\n{row2}\n{row3}\n{row4}\n{row5}"

                        info_text += lessonNote_info_text + "\n"
                        row += row_info_text + "\n"
                    else:
                        logging.warning("Missing 'lessonname' key in lesson: %s", lessonn)

                if info_text:
                    self.listLessonNoteInfos.setText(info_text)
                else:
                    self.listLessonNoteInfos.setText("Herhangi bir kayıt bulunamadı.")
                    
                if row:
                    self.titleRow1.setText(row)
                else:
                    self.titleRow1.setText("Herhangi bir kayıt bulunamadı.")
            else:
                self.listLessonNoteInfos.setText("Herhangi bir kayıt bulunamadı.")
                self.titleRow1.setText("Herhangi bir kayıt bulunamadı.")
        except Exception as e:
            logging.error("Error occurred while retrieving lesson data: %s", e)


    def BtnQuit(self):
        answer=QMessageBox.question(self,"Çıkış","Çıkmak istediğinize emin misiniz ?",\
                        QMessageBox.Yes | QMessageBox.No)
        if answer==QMessageBox.Yes:
            sys.exit(app.exec_())
        else:
            self.show()

app=QApplication(sys.argv)
mainwindow=FirstScreen()
widget=QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.showFullScreen()
app.exec_()