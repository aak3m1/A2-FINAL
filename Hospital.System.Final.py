from tkinter import *
from tkinter import ttk  # Import ttk for themed widgets
from tkcalendar import DateEntry
from datetime import datetime
from tkinter import StringVar
import sqlite3
import tkinter.messagebox
from tkinter import Label, Entry, Button, Toplevel, messagebox
from collections import deque


#system class
class System:
    def __init__(self, root):
        """
        this class represents the system object with the provided root (Tkinter Window)
        the root: Tk object
        the main window of the hospital management system
        """
        
        self.root = root #assigning the tkniter root window to the instance variable
        self.root.title("Welcome to Hospital Management System") #setting title
        self.root.geometry("450x300") #setting the frame
        self.root.configure
        self.conn = sqlite3.connect('Hospital.system.FINAL.db') #connect to the database for the Hospital Management
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                password TEXT
            )
        ''') #creating the employees table if it doesn't exist
        self.conn.commit()

        #login frame
        self.login_frame = Frame(self.root, bd=5, relief=RIDGE)
        self.login_frame.pack(pady=20)

        #username entering
        self.lblUsername = Label(self.login_frame, text="Username:")
        self.lblUsername.grid(row=0, column=0)
        self.entryUsername = Entry(self.login_frame)
        self.entryUsername.grid(row=0, column=1)

        #password entering
        self.lblPassword = Label(self.login_frame, text="Password:")
        self.lblPassword.grid(row=1, column=0)
        self.entryPassword = Entry(self.login_frame, show='*')
        self.entryPassword.grid(row=1, column=1)

        #login button
        self.btnLogin = Button(self.login_frame, text="Login", command=self.login)
        self.btnLogin.grid(row=2, column=0, columnspan=2)


    def login(self):
        username = self.entryUsername.get()
        password = self.entryPassword.get()

        self.cursor.execute('SELECT * FROM employees WHERE username = ? AND password = ?', (username, password))
        user = self.cursor.fetchone() #if the username and password match in the database

        if user:
            messagebox.showinfo("Login Successful", "Welcome to the Hospital Management System!")
            self.open_hospital_system()# Open the Hospital Management System window after successful login
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

    def open_hospital_system(self):# Open the hospital management system GUI here
        self.root.destroy()  # closing the login window
        root = Tk()
        application = Hospital(root)
        root.mainloop()


class Patient:
    """
        class represents the Patient object with the provided attributes
        patient ID
        patient Name
        appointment time
        is emergency
    """
    def __init__(self, patient_id, patient_name, appointment_time, is_emergency=False):
        self.patient_id = patient_id
        self.patient_name = patient_name
        self.appointment_time = appointment_time
        self.is_emergency = is_emergency
        self.doctor = None # Initially no doctor assigned
        self.medications = [] #list hold medications for patient


class Doctor:
    """
    this class to represent a doctor
    doctor ID
    doctor Name
    """
    def __init__(self, doctor_id, doctor_name):
        self.doctor_id = doctor_id
        self.doctor_name = doctor_name

class Hospital:
    """
    this class represents the hospital GUI
    """
    def __init__(self, root):
        self.root = root
        self.root.title("Hospital Management System")#setting  title of the window
        self.root.geometry("1200x600") #setting size of the window
        self.root.configure
        self.waiting_queue = deque()
        self.prescription_stack = []

        def add_patient_to_queue(self, patient):
            self.waiting_queue.append(patient)

        def remove_patient_from_queue(self):
            if self.waiting_queue:
                return self.waiting_queue.popleft()
            else:
                messagebox.showinfo("Info", "No patients in the waiting queue.")

        def add_prescription(self, prescription):
            self.prescription_stack.append(prescription)

        def get_last_prescription(self):
            if self.prescription_stack:
                return self.prescription_stack.pop()
            else:
                messagebox.showinfo("Info", "No prescriptions to show.")

        self.conn = sqlite3.connect('Hospital.system.db') #connecting to the database
        self.cursor = self.conn.cursor() #create a cursor for database operations

        self.emergency_checkbox_var = BooleanVar() #variables for GUI elements and patient information
        self.emergency_checkbox_var.set(False)

        self.waiting_list = [] #empty waiting list
        cmbNameTablets = StringVar()#variable for medication name dropdown
        Ref = StringVar()#patient reference number
        Dose = StringVar()#medication dose
        NumberTables = StringVar()#number of tablets
        AppointmentDate = StringVar() #appointment date
        HowtoUseMedication = StringVar() #HowtoUseMedication variable
        Medication = StringVar() #medication name
        PatientID = StringVar() #patient ID
        PatientName = StringVar()#patient name
        DateOfBirth = StringVar()#patient date of birth
        PatientAddress = StringVar() #patient address
        Prescription = StringVar() #prescription details
        DoctorName = StringVar() #doctor's name
        self.search_var = StringVar()#search functionality

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS patients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                reference_no TEXT,
                appointment_date TEXT,
                patient_id TEXT,
                patient_name TEXT,
                date_of_birth TEXT,
                patient_address TEXT,
                name_of_tablets TEXT,
                no_of_tablets TEXT,
                dose TEXT,
                use_medication_main TEXT,
                use_medication_details TEXT,
                doctor_name TEXT
            )
        ''') #creating the patients table in database if not exist

        self.cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_appointment_date
            ON patients (appointment_date)
        ''') #creating index on the 'appointment date'

        self.conn.commit() #changes to the database

        def openMedicationWindow(): #create a new window for medication details
            medication_window = Toplevel()
            medication_window.title("Medication Details") #window title
            medication_window.geometry("400x150")#window size

            #mediction labels and entry widgets in the new window
            lblNameTablet = Label(medication_window, text="Name of Tablets:")
            lblNameTablet.grid(row=0, column=0, sticky=W)
            cboNameTablet = ttk.Combobox(medication_window, textvariable=cmbNameTablets, state='readonly', width=23)
            cboNameTablet['values'] = ('', 'Ibuprofen', 'Panadol', 'Advil', 'Adole','Asprine','Feroglobin','Ativan','Amlodipine')
            cboNameTablet.current(0)
            cboNameTablet.grid(row=0, column=1, sticky=W)

            lblNoOfTablets = Label(medication_window, text="No. of Tablets:", padx=2 ,pady=2)
            lblNoOfTablets.grid(row=1, column=0, sticky=W)
            txtNoOfTablets = Entry(medication_window, textvariable=NumberTables, width=25)
            txtNoOfTablets.grid(row=1, column=1)

            lblDose = Label(medication_window,text="Dose:", padx=2 , pady=4)
            lblDose.grid(row=2, column=0, sticky=W)
            txtDose = Entry(medication_window, textvariable=Dose, width=25)
            txtDose.grid(row=2, column=1)

            lblUseMedication = Label(medication_window, text="Use Medication:", padx=2, pady=2)
            lblUseMedication.grid(row=3, column=0, sticky=W)
            txtUseMedication = Entry(medication_window, textvariable=HowtoUseMedication, width=25)
            txtUseMedication.grid(row=3, column=1)

            btnSaveMedication = Button(medication_window, text='Save Medication', width=24, bd=4, command=saveMedication)
            btnSaveMedication.grid(row=4, column=1)

        def saveMedication(): #retrieve medication details from entry widgets
            name_tablets = cmbNameTablets.get()
            no_of_tablets = NumberTables.get()
            dose = Dose.get()
            use_medication_details = HowtoUseMedication.get() #changing variable name

            self.cursor.execute('''
                INSERT INTO patients (name_of_tablets, no_of_tablets, dose, use_medication_details)
                VALUES (?, ?, ?, ?)
            ''', (name_tablets, no_of_tablets, dose, use_medication_details)) #inserting medication details into the database

            self.conn.commit() #commit changes to the database
            tkinter.messagebox.showinfo("Success", "Medication details saved successfully!")#show success message

        def iExit():
            iExit=tkinter.messagebox.askyesno("Hospital Managment System","Confirm if you want to exit")
            if iExit>0: #confirmation before exiting
                root.destroy()#destroy the root window
            return

        def Sort(): #fetch and sort appointments from the database
            self.cursor.execute('SELECT * FROM patients ORDER BY appointment_date ASC')
            sorted_appointments = self.cursor.fetchall()
            display_sorted_appointments(sorted_appointments) #display sorted appointments in a new window

        def display_sorted_appointments(sorted_appointments): #new window for displaying sorted appointments
            sorted_window = Toplevel(self.root)
            sorted_window.title("Sorted Appointments")
            sorted_window.geometry("800x400")

            tree = ttk.Treeview(sorted_window, columns=("Patient ID", "Patient Name", "Appointment Date"))
            tree.heading("#0", text="Index")
            tree.heading("Patient ID", text="Patient ID")
            tree.heading("Patient Name", text="Patient Name")
            tree.heading("Appointment Date", text="Appointment Date")
            tree.pack(expand=True, fill='both')

            for index, appointment in enumerate(sorted_appointments, start=1): #sorted appointments into the treeview
                tree.insert("", "end", text=str(index), values=(appointment[4], appointment[5], appointment[3]))

        def iPrescription(): #getting data from entry widgets
            reference_no = Ref.get() #Retrieve data from Ref
            appointment_date = AppointmentDate.get()#from AppointmentDate
            patient_id = PatientID.get()#from PatientID
            patient_name = PatientName.get() #from PatientName
            date_of_birth = DateOfBirth.get()  #from DateOfBirth
            patient_address = PatientAddress.get()  #from PatientAddress
            name_of_tablets = cmbNameTablets.get()  #from cmbNameTablets
            no_of_tablets = NumberTables.get()  #from NumberTables
            dose = Dose.get()  #Dose
            Howtossemedication = HowtoUseMedication.get()  # Changed variable name
            doctor_name = DoctorName.get()  #DoctorName
            use_medication_main=Medication.get() #from Medication

            self.cursor.execute('''
                INSERT INTO patients (
                    reference_no, appointment_date, patient_id, patient_name, date_of_birth,
                    patient_address, name_of_tablets, no_of_tablets, dose, use_medication_main, use_medication_details, doctor_name
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                reference_no, appointment_date, patient_id, patient_name, date_of_birth,
                patient_address, name_of_tablets, no_of_tablets, dose, use_medication_main, Howtossemedication,
                doctor_name
            ))#inseting data into the patients table in the database
            self.conn.commit() #commit changes to the database
            prescription_data = (
            f"Reference No: {reference_no}\n"
            f"Appointment Date: {appointment_date}\n"
            f"Patient ID: {patient_id}\n"
            f"Patient Name: {patient_name}\n"
            f"Date of Birth: {date_of_birth}\n"
            f"Patient Address: {patient_address}\n"
            f"Name of Tablets: {name_of_tablets}\n"
            f"No. of Tablets: {no_of_tablets}\n"
            f"Dose: {dose}\n"
            f"Medication: {Howtossemedication}\n"
            f"Doctor Name: {doctor_name}\n\n"
            ) #Create a formatted prescription

            self.textPrescription.insert(END, prescription_data) #inserting prescription data into textPrescription widget
            self.textFrameDetail.insert(END, f"\t{Medication.get()}\t\t\n") #inserting medication data into FrameDetail widget

        def iDelete(): #clearing the entry widgets and set StringVar variables to empty strings
            Ref.set("")
            DoctorName.set("")
            NumberTables.set("")
            Dose.set("")
            AppointmentDate.set("")
            PatientID.set("")
            PatientName.set("")
            DateOfBirth.set("")
            PatientAddress.set("")
            Prescription.set("")
            Medication.set("")
            HowtoUseMedication.set("")

            self.textPrescription.delete("1.0",END) #Clear the text widgets
            self.textFrameDetail.delete("1.0",END)
            return

        def iReset(): #similar to iDelete(), reset values and clear text widgets
            Ref.set("")
            DoctorName.set("")
            Dose.set("")
            NumberTables.set("")
            AppointmentDate.set("")
            PatientID.set("")
            PatientName.set("")
            DateOfBirth.set("")
            PatientAddress.set("")
            Prescription.set("")
            Medication.set("")
            HowtoUseMedication.set("")
            self.textPrescription.delete("1.0",END)
            self.textFrameDetail.delete("1.0",END)
            return

        def add_patient(): #getting data from entry widgets and checkbox
            patient_id = self.entryPatientID.get()
            patient_name = self.entryPatientName.get()
            appointment_time = self.entryAppointmentTime.get()
            is_emergency = self.emergency_checkbox_var.get()

            if patient_id and patient_name and appointment_time: #creating a new Patient object and add it to the waiting list
                new_patient = Patient(patient_id, patient_name, appointment_time, is_emergency=is_emergency)
                self.waiting_list.append(new_patient)
                messagebox.showinfo("Success", "Patient added to waiting list!")
            else:
                messagebox.showerror("Error", "Please fill in all fields.")
            return

        def remove_patient():
            if self.waiting_list: #removing the first patient from the waiting list and show a success message
                removed_patient = self.waiting_list.pop(0)
                messagebox.showinfo("Success", f"Patient {removed_patient.patient_name} removed from waiting list.")
            else:
                messagebox.showinfo("Info", "No patients in the waiting list.")
            return

        def OpenAddPatientWindow(): #opening a new window for adding a patient
            add_patient_window = Toplevel()
            add_patient_window.title("Add Patient")
            add_patient_window.geometry("400x200")
            lblTitle = Label(add_patient_window, text="Add New Patient")
            lblTitle.pack()
            lblPatientID = Label(add_patient_window, text="Patient ID:")
            lblPatientID.pack()
            self.entryPatientID = Entry(add_patient_window)
            self.entryPatientID.pack()

            lblPatientName = Label(add_patient_window, text="Patient Name:")
            lblPatientName.pack()
            self.entryPatientName = Entry(add_patient_window)
            self.entryPatientName.pack()

            lblAppointmentTime = Label(add_patient_window, text="Arrivel Time:")
            lblAppointmentTime.pack()
            self.entryAppointmentTime = Entry(add_patient_window)
            self.entryAppointmentTime.pack()

            emergency_checkbox = Checkbutton(add_patient_window, text="Emergency Patient",
                                            variable=self.emergency_checkbox_var, onvalue=True, offvalue=False)
            emergency_checkbox.pack() #checkbox for emergency status

            btnAdd = Button(add_patient_window, text="Add Patient", command=add_patient)
            btnAdd.pack()
            return

        def OpenWaitingRoom(): #new window for the waiting room list
            waiting_window = Toplevel()
            waiting_window.title("Waiting Room List")
            waiting_window.geometry("600x400")
            lblTitle = Label(waiting_window, text="Patients Waiting for Consultation")
            lblTitle.pack()

            lbl_header = Label(waiting_window, text="Patient ID | Name | Appointment Time | Emergency |  Doctor | ")
            lbl_header.pack()

            for idx, patient in enumerate(self.waiting_list, start=1):
                patient_info = f"{patient.patient_id} | {patient.patient_name} | {patient.appointment_time} | " \
                           f"{patient.is_emergency} | {patient.doctor.doctor_name if patient.doctor else 'Not assigned'} | "
                lbl_patient_info = Label(waiting_window, text=patient_info)
                lbl_patient_info.pack() #displaying patient information in the waiting room list
            btn_remove_patient = Button(waiting_window, text="Remove Patient", command=remove_patient)
            btn_remove_patient.pack()

        def OpenUpdateWindow(): #create a new window for updating patient details
            Update_window = Toplevel()
            Update_window.title("Update Details")
            Update_window.geometry("800x250")

            lblRef = Label(Update_window, text="Reference No:", padx=2 , pady=2) #labels and entry widgets for updating patient details
            lblRef.grid(row=0, column=0)
            txtRef = Entry(Update_window,textvariable=Ref, width=25)
            txtRef.grid(row=0, column=1)

            lblPatientID = Label(Update_window, text="Patient ID:", padx=2, pady=2)
            lblPatientID.grid(row=0, column=2)
            txtPatientID = Entry(Update_window, textvariable=PatientID, width=25)
            txtPatientID.grid(row=0, column=3)

            lblPatientName = Label(Update_window, text="Patient Name:", padx=2, pady=2)
            lblPatientName.grid(row=1, column=2)
            txtPatientName = Entry(Update_window ,textvariable=PatientName , width=25)
            txtPatientName.grid(row=1, column=3)

            lblDateOfBirth = Label(Update_window, text="Date Of Birth:", padx=2, pady=2)
            lblDateOfBirth.grid(row=2, column=0)
            txtDateOfBirth = DateEntry(Update_window, textvariable=DateOfBirth, width=23)
            txtDateOfBirth.grid(row=2, column=1)

            lblPatientAddress = Label(Update_window, text="Patient Address:", padx=2, pady=2)
            lblPatientAddress.grid(row=2, column=2)
            txtPatientAddress= Entry(Update_window, textvariable=PatientAddress , width=25)
            txtPatientAddress.grid(row=2, column=3)

            lblAppointmentDate = Label(Update_window, text="AppointmentDate", padx=2, pady=2)
            lblAppointmentDate.grid(row=3, column=2)
            txtAppointmentDate = DateEntry(Update_window, textvariable=AppointmentDate, width=23)
            txtAppointmentDate.grid(row=3, column=3)

            lblDoctorName= Label(Update_window, text="Doctor Name:", padx=2 ,pady=2)
            lblDoctorName.grid(row=4, column=0)
            txtDoctorName = Entry(Update_window,textvariable=DoctorName , width=25)
            txtDoctorName.grid(row=4, column=1)

            lblNameTablet = Label(Update_window, text="Name of Tablets:", padx=2, pady=2)
            lblNameTablet.grid(row=4, column=2, sticky=W)
            cboNameTablet = ttk.Combobox(Update_window, textvariable=cmbNameTablets, state='readonly', font=('arial', 12, 'bold'), width=23)
            cboNameTablet['values'] = ('', 'Ibuprofen', 'Panadol', 'Advil', 'Adole','Asprine','Feroglobin','Ativan','Amlodipine')
            cboNameTablet.current(0)
            cboNameTablet.grid(row=4, column=3, sticky=W)

            lblNoOfTablets = Label(Update_window, text="No. of Tablets:", padx=2 ,pady=2)
            lblNoOfTablets.grid(row=5, column=0, sticky=W)
            txtNoOfTablets = Entry(Update_window,textvariable=NumberTables, width=25)
            txtNoOfTablets.grid(row=5, column=1)

            lblDose = Label(Update_window, text="Dose:", padx=2 , pady=4)
            lblDose.grid(row=5, column=2, sticky=W)
            txtDose = Entry(Update_window, textvariable=Dose, width=25)
            txtDose.grid(row=5, column=3)

            lblUseMedication = Label(Update_window, text="Use Medication:", padx=2, pady=2)
            lblUseMedication.grid(row=6, column=0, sticky=W)
            txtUseMedication = Entry(Update_window, textvariable=HowtoUseMedication, width=25)
            txtUseMedication.grid(row=6, column=1)


            lblUseMedication = Label(Update_window, text="Use Medication:", padx=2, pady=2)
            lblUseMedication.grid(row=6, column=2)
            txtUseMedication = Entry(Update_window, textvariable=Medication , width=25)
            txtUseMedication.grid(row=6, column=3) # Set initial text for the text box

            btnUpdate = Button(Update_window, text='Update', width=24, bd=4, command=iUpdate)#button to update patient details
            btnUpdate.grid(row=10, column=1)
            return

        def iUpdate(): #getting updated data from entry widgets
            patient_id =PatientID.get()
            patient_name =PatientName.get()
            date_of_birth =DateOfBirth.get()
            patient_address = PatientAddress.get()
            name_of_tablets =cmbNameTablets.get()
            no_of_tablets = NumberTables.get()
            dose = Dose.get()
            use_medication_main = HowtoUseMedication.get()
            doctor_name = DoctorName.get()
            appointment_date = AppointmentDate.get()

            self.cursor.execute('SELECT * FROM patients WHERE patient_id = ?', (patient_id,)) #checking if patient_id exists
            existing_record = self.cursor.fetchone()
            if existing_record: #update the record
                self.cursor.execute('''
                    UPDATE patients SET
                    patient_name = ?,
                    date_of_birth = ?,
                    patient_address = ?,
                    name_of_tablets = ?,
                    no_of_tablets = ?,
                    dose = ?,
                    use_medication_main = ?,
                    doctor_name = ?,
                    appointment_date = ?
                    WHERE patient_id = ?
                ''', (patient_name, date_of_birth, patient_address, name_of_tablets,
                    no_of_tablets, dose, use_medication_main, doctor_name, appointment_date, patient_id))
                self.conn.commit()
                tkinter.messagebox.showinfo("Success", "Patient record updated successfully!")
            else:
                tkinter.messagebox.showerror("Error", "Patient ID not found!")
            return

        def search(): #responsible for creating a new window
            search_window = Toplevel()
            search_window.title("search Details")
            search_window.geometry("800x250")
            self.lblSearch = Label(search_window, text="Enter Patient ID:")
            self.lblSearch.pack()

            self.entrySearch = Entry(search_window, textvariable=self.search_var)
            self.entrySearch.pack()

            self.btnSearch = Button(search_window, text="Search", command=search_patient)
            self.btnSearch.pack()
            return

        def search_patient():#function is called when the user clicks the search button in the search window
            patient_id = self.search_var.get() #retrieves the patient ID entered by the user from the search_var.
            if not patient_id: #checking if patient ID is provided
                messagebox.showerror("Error", "Please enter a patient ID.")
                return
            self.cursor.execute('SELECT * FROM patients WHERE patient_id = ?', (patient_id,)) #Search for patient in the database
            patient_record = self.cursor.fetchone()

            if not patient_record: #display patient details in a new window
                messagebox.showinfo("Info", "Patient not found.")
                return
            display_patient_summary(patient_record)
            return

        def display_patient_summary(patient_record): #create a new window for displaying patient summary
            summary_window = Toplevel(self.root)
            summary_window.title("Patient Summary")
            summary_window.geometry("600x400")


            # with elements like patient ID, name, appointment time, etc.

            lblPatientID = Label(summary_window, text="Patient ID:") #display patient details using labels and entry widgets
            lblPatientID.grid(row=0, column=0)
            txtPatientID = Entry(summary_window)
            txtPatientID.insert(0, patient_record[4]) #assuming patient ID is at index 4

            txtPatientID.grid(row=0, column=1)

            lblPatientName = Label(summary_window, text="Patient Name:")
            lblPatientName.grid(row=1, column=0)
            txtPatientName = Entry(summary_window)
            txtPatientName.insert(0, patient_record[5])
            txtPatientName.grid(row=1, column=1)

            lblAppointmentTime = Label(summary_window, text="Appointment Time:")
            lblAppointmentTime.grid(row=2, column=0)
            txtAppointmentTime = Entry(summary_window)
            txtAppointmentTime.insert(0, patient_record[3])
            txtAppointmentTime.grid(row=2, column=1)

            lblDoctorName = Label(summary_window, text="Doctor Name:")
            lblDoctorName.grid(row=3, column=0)
            txtDoctorName = Entry(summary_window)
            txtDoctorName.insert(0, patient_record[14])
            txtDoctorName.grid(row=3, column=1)

            lblMedications = Label(summary_window, text="Medications:")
            lblMedications.grid(row=4, column=0)
            txtMedications = Text(summary_window, height=5, width=50)
            txtMedications.insert(END, patient_record[12])
            txtMedications.grid(row=4, column=1)

        MainFrame = Frame(self.root) #the main frame for the GUI application
        MainFrame.grid()
        TitleFrame = Frame(MainFrame, bd=20, width=1350, padx=20, relief=RIDGE) #creating the frame for the title at the top of the window
        TitleFrame.pack(side=TOP)
        self.lblTitle = Label(TitleFrame, text="Hospital Management System", padx=2)  #creating a label to display the title in the TitleFrame
        self.lblTitle.grid()
        FrameDetail = Frame(MainFrame, bd=20, width=1350, height=100, padx=20, relief=RIDGE) #creating a frame for detailed information at the bottom of the window

        FrameDetail.pack(side=BOTTOM)
        ButtonFrame = Frame(MainFrame, bd=20, width=1350, height=50, padx=20, relief=RIDGE) #creating a frame for buttons at the bottom of the window

        ButtonFrame.pack(side=BOTTOM)
        DataFrame = Frame(MainFrame, bd=20, width=1350, height=400, padx=20, relief=RIDGE) #crationg a frame for data display in the middle of the window

        DataFrame.pack(side=BOTTOM)
        DataFrameLEFT = LabelFrame(DataFrame, bd=10, width=800, height=300, padx=20, relief=RIDGE  #creating a left sub-frame in DataFrame for patient information

                              , font=('arial', 12, 'bold'), text="Patient Information:",)
        DataFrameLEFT.pack(side=LEFT) #create a right sub-frame in DataFrame for prescription information
        DataFrameRIGHT = LabelFrame(DataFrame, bd=10, width=450, height=300, padx=20, relief=RIDGE,text="Prescription:",)
        DataFrameRIGHT.pack(side=RIGHT)

        self.lblRef = Label(DataFrameLEFT, text="Reference No:", padx=2 , pady=2)#patient information in DataFrameLEFT
        self.lblRef.grid(row=0, column=0)
        self.txtRef = Entry(DataFrameLEFT,textvariable=Ref, width=25)
        self.txtRef.grid(row=0, column=1)

        self.lblAppointmentDate = Label(DataFrameLEFT, text="AppointmentDate", padx=2, pady=2)  #labels and entry widgets for doctor name and use medication in DataFrameLEFT
        self.lblAppointmentDate.grid(row=1, column=0)
        self.txtAppointmentDate = DateEntry(DataFrameLEFT, textvariable=AppointmentDate, width=23)
        self.txtAppointmentDate.grid(row=1, column=1)

        self.lblPatientID = Label(DataFrameLEFT, text="Patient ID:", padx=2, pady=2)
        self.lblPatientID.grid(row=1, column=2)
        self.txtPatientID = Entry(DataFrameLEFT,textvariable=PatientID , width=25)
        self.txtPatientID.grid(row=1, column=3)


        self.lblPatientName = Label(DataFrameLEFT, text="Patient Name:", padx=2, pady=2)
        self.lblPatientName.grid(row=2, column=0)
        self.txtPatientName = Entry(DataFrameLEFT, textvariable=PatientName , width=25)
        self.txtPatientName.grid(row=2, column=1)


        self.lblDateOfBirth = Label(DataFrameLEFT, text="Date Of Birth:", padx=2, pady=2)
        self.lblDateOfBirth.grid(row=2, column=2)
        self.txtDateOfBirth = DateEntry(DataFrameLEFT, textvariable=DateOfBirth, width=23)
        self.txtDateOfBirth.grid(row=2, column=3)


        self.lblPatientAddress = Label(DataFrameLEFT, text="Patient Address:", padx=2, pady=2)
        self.lblPatientAddress.grid(row=3, column=0)
        self.txtPatientAddress= Entry(DataFrameLEFT, textvariable=PatientAddress , width=25)
        self.txtPatientAddress.grid(row=3, column=1)

        self.lblUseMedication = Label(DataFrameLEFT, text="Use Medication:", padx=2, pady=2)
        self.lblUseMedication.grid(row=4, column=0)
        self.txtUseMedication = Entry(DataFrameLEFT,textvariable=Medication , width=25)
        self.txtUseMedication.grid(row=4, column=1)

        self.lblDoctorName= Label(DataFrameLEFT, text="  Doctor Name:", padx=2 ,pady=2)
        self.lblDoctorName.grid(row=4, column=2)
        self.txtDoctorName = Entry(DataFrameLEFT, textvariable=DoctorName , width=25)
        self.txtDoctorName.grid(row=4, column=3)

        self.textPrescription=Text(DataFrameRIGHT, width=43, height=14, padx=2, pady=2) # Text Widget for Prescription Display
        self.textPrescription.grid(row=0, column=0)

        self.btnPrescription=Button(ButtonFrame,text='Prescription',width=24 ,bd=4,command=iPrescription)  #Buttons in ButtonFrame
        self.btnPrescription.grid(row=0, column=0)

        self.btnPrescription=Button(ButtonFrame,text='Medication Details', width=24 ,bd=4, command=openMedicationWindow)
        self.btnPrescription.grid(row=0, column=1)

        self.btnDelete=Button(ButtonFrame,text='Delete',width=24 ,bd=4,command=iDelete)
        self.btnDelete.grid(row=0, column=2)

        self.btnReset=Button(ButtonFrame,text='Reset',width=24 ,bd=4,command=iReset)
        self.btnReset.grid(row=0, column=3)

        self.btnExit=Button(ButtonFrame,text='Exit', font=('arial', 12, 'bold'),width=24 ,bd=4,command=iExit)
        self.btnExit.grid(row=0, column=4)

        self.btnUpdate=Button(ButtonFrame,text='Update', width=24 ,bd=4,command=OpenUpdateWindow)
        self.btnUpdate.grid(row=1, column=0)

        self.btnAddPatient=Button(ButtonFrame,text='Add Patient', width=24 ,bd=4,command=OpenAddPatientWindow)
        self.btnAddPatient.grid(row=1, column=1)

        self.btnWaitingRoom=Button(ButtonFrame,text='WaitingRoom',width=24 ,bd=4,command=OpenWaitingRoom)
        self.btnWaitingRoom.grid(row=1, column=2)

        self.btnSearch = Button(ButtonFrame, text='Search for patient', width=24, bd=4,command=search)
        self.btnSearch.grid(row=1, column=3)

        self.btnSort = Button(ButtonFrame, text='appointments', width=24, bd=4,command=Sort)
        self.btnSort.grid(row=1, column=4)

        self.lblLabel = Label(FrameDetail, pady=4, padx=2,text="Type of medical condition/Does the patient use medications?")
        self.lblLabel.grid(row=0, column=0)

        self.textFrameDetail=Text(FrameDetail,width=141, height=4, padx=2, pady=4)
        self.textFrameDetail.insert(END, f"\t{Medication.get()}\t\t\n")
        self.textFrameDetail.grid(row=1, column=0)

if __name__ == '__main__':
    root = Tk()
    application = System(root)
    root.mainloop()
