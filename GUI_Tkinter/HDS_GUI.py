from Tkinter import *
import ttk
import tkMessageBox
import pandas.io.sql as sqlio          # Makes creation of dataframes/datasets from sql connection very easy
import numpy as np                     # Contains useful mathematical or matrix-related functions
import pyodbc
import base64

def getYrFacModelSys():
    """Method used to obtain unique model year, factory, names, and HDS system names.  Then, they will be used to populate
    the listboxes instead of hard-coding the values."""

    # Get password and "de-fuzzy" it
    pw_file = open(r'D:\webapps\_server\pyodbc\cmq.txt', 'r')
    pw = base64.b64decode(pw_file.read())
    userid = 'rb10'
    pw_file.close()
    cnxn_string = 'DSN=CMQ_PROD;UID=' + userid + ';PWD=' + pw

    con = pyodbc.connect(cnxn_string)

    sql_getYears = """
    select distinct
    mdl_yr

    from CMQ.V_DIM_MTO

    where
    mto_sk > 0

    order by
    mdl_yr desc"""

    sql_getFactory = """
    select distinct
    fctry_cd

    from CMQ.V_DIM_MTO

    where
    mto_sk > 0

    order by
    fctry_cd"""

    sql_getModels = """
    select distinct
    mdl_nm

    from CMQ.V_DIM_MTO

    where
    mto_sk > 0

    order by
    mdl_nm"""

    sql_getSysName = """
    select distinct
    sys_nm

    from CMQ.V_HDS_DTL"""
    

    df_years = sqlio.read_frame(sql_getYears, con)
    df_factory = sqlio.read_frame(sql_getFactory, con)
    df_models = sqlio.read_frame(sql_getModels, con)
    df_sysnames = sqlio.read_frame(sql_getSysName, con)

    con.close()

    years = df_years.values
    years = years[:16]  # Get just the last 16 most recent model years, no need to run data since 1987.

    factories = df_factory.values
    models = df_models.values
    sysnames = df_sysnames.values

    year_values = []
    for year in years:
        year_values.append(year[0])

    factory_values = []
    for factory in factories:
        if factory != 'UNKNOWN' and factory != 'CHAC':
            factory_values.append(factory[0])
        
    model_values = []
    for model in models:
        if model != 'UNKNOWN':
            model_values.append(model[0])

    sysnames_values = []
    for name in sysnames:
        if name != 'UNKNOWN':
            sysnames_values.append(name[0])

    return year_values, factory_values, model_values, sysnames_values


class GetHDSFreeze(Frame):
    def __init__(self, master):
        self.frame = Frame(master)
        self.frame.pack()

        years, factories, models, sysnames = getYrFacModelSys()

        ################################## Create labels ####################################
        self.lblYear = Label(self.frame, text="Model Year")
        self.lblYear.grid(row=0, column=0)

        self.lblFactory = Label(self.frame, text="Factory")
        self.lblFactory.grid(row=0, column=2)

        self.lblModel = Label(self.frame, text="Model Name")
        self.lblModel.grid(row=0, column=3)

        self.lblSysNames = Label(self.frame, text="System Name")
        self.lblSysNames.grid(row=0, column=5)

        ################################# Create listboxes and scrollbars ##############################
        # Year listbox and scrollbar
        self.yScroll_yr = Scrollbar(self.frame, orient=VERTICAL)
        self.yScroll_yr.grid(row=1, column=1, sticky=N+S)                
        self.year_values = StringVar()
        self.listYear = Listbox(self.frame, exportselection=0, activestyle='none', listvariable=self.year_values, selectmode=MULTIPLE, yscrollcommand=self.yScroll_yr.set)
        for year in years:
            self.listYear.insert(END, year)
        self.listYear.grid(row=1, column=0)
        self.yScroll_yr['command'] = self.listYear.yview

        # Factory listbox
        self.factory_values = StringVar()
        self.listFactory = Listbox(self.frame, exportselection=0, activestyle='none', listvariable=self.factory_values, selectmode=MULTIPLE)
        for factory in factories:
            self.listFactory.insert(END, factory)
        self.listFactory.grid(row=1, column=2)
        self.listFactory.grid_configure(padx=10)

        # Model listbox and scrollbar
        self.yScroll_model = Scrollbar(self.frame, orient=VERTICAL)
        self.yScroll_model.grid(row=1, column=4, sticky=N+S)                
        self.model_values = StringVar()
        self.listModel = Listbox(self.frame, exportselection=0, activestyle='none', listvariable=self.model_values, selectmode=MULTIPLE, yscrollcommand=self.yScroll_model.set)
        for model in models:
            self.listModel.insert(END, model)
        self.listModel.grid(row=1, column=3)
        self.yScroll_model['command'] = self.listModel.yview

        # System name listbox and scrollbar
        self.yScroll_sys = Scrollbar(self.frame, orient=VERTICAL)
        self.yScroll_sys.grid(row=1, column=6, sticky=N+S)
        self.sysname_values = StringVar()
        self.listSysName = Listbox(self.frame, exportselection=0, activestyle='none', listvariable=self.sysname_values, selectmode=MULTIPLE, yscrollcommand=self.yScroll_sys.set)
        for name in sysnames:
            self.listSysName.insert(END, name)
        self.listSysName.grid(row=1, column=5)
        self.yScroll_sys['command'] = self.listSysName.yview

        ############################# Create Buttons ################################
        self.btnPrintYrs = Button(self.frame, text="Print Years", command=self.printYears)
        self.btnPrintYrs.grid(row=2, column=0)

        self.btnPrintFac = Button(self.frame, text="Print Factories", command=self.printFactories)
        self.btnPrintFac.grid(row=2, column=2)

        self.btnPrintMdl = Button(self.frame, text="Print Models", command=self.printModels)
        self.btnPrintMdl.grid(row=2, column=3)

        self.btnSysName = Button(self.frame, text="Print System Name", command=self.printSystems)
        self.btnSysName.grid(row=2, column=5)        

        self.btnDelete = Button(self.frame, text="Next", command=self.buildSQL)
        self.btnDelete.grid(row=3, column=5)        

    def printYears(self):
        idx_selected = self.listYear.curselection()

        for year in idx_selected:
            print self.listYear.get(year)
            self.year_list.append(year)

    def printFactories(self):
        idx_selected = self.listFactory.curselection()

        for factory in idx_selected:
            print self.listFactory.get(factory)
            self.factory_list.append(factory)

    def printModels(self):
        idx_selected = self.listModel.curselection()

        for model in idx_selected:
            print self.listModel.get(model)
            self.model_list.append(model)

    def printSystems(self):
        idx_selected = self.listSysName.curselection()

        if idx_selected:
            for name in idx_selected:
                print self.listSysName.get(name)
        else:
            tkMessageBox.showerror('Missing system name','Please select at least 1 system name')

    def next1(self):
        for child in self.frame.winfo_children():
            child.destroy()

        self.btnTest = Button(self.frame, text="Test")
        self.btnTest.grid(row=0, column=0)

    def buildSQL(self):
        year_list    = []
        factory_list = []
        model_list   = []
        system_list  = []

        sql_begin = """
SELECT DISTINCT
HDS.MDL_YR,
HDS.FCTRY_CD,
HDS.MDL_NM,
VIN_NO,
SAE_CD || '--' || DTC_DESC,
"ENGINE CYLINDERS" AS ENG_CYL,
"ENGINE SERIES" AS ENG_SERIES,
TRANSMISSION

FROM CMQ.V_HDS_DTL HDS

LEFT JOIN CMQ.V_DIM_MTO_FEATURE_PIVOT FEATURES
ON HDS.MTO_MDL_CD = FEATURES.MTO_MDL_CD
AND HDS.MTO_TYP_CD = FEATURES.MTO_TYP_CD

LEFT JOIN CMQ.V_DIM_DTC_CD DTC
ON HDS.SAE_CD = DTC.DTC_CD

WHERE
HDS.MDL_YR IN("""
        idx_selected_year = self.listYear.curselection()
        idx_selected_factory = self.listFactory.curselection()
        idx_selected_model = self.listModel.curselection()
        idx_selected_system = self.listSysName.curselection()

        if idx_selected_year:
            for year in idx_selected_year:
                year_list.append(self.listYear.get(year))
        else:
            tkMessageBox.showerror('Error','You must select at least 1 year')

        if idx_selected_factory:
            for factory in idx_selected_factory:
                factory_list.append(self.listFactory.get(factory))
        else:
            tkMessageBox.showerror('Error','You must select at least 1 factory')

        if idx_selected_model:
            for model in idx_selected_model:
                model_list.append(self.listModel.get(model))
        else:
            tkMessageBox.showerror('Error','You must select at least 1 model')

        if idx_selected_system:
            for name in idx_selected_system:
                system_list.append(self.listSysName.get(name))
        else:
            tkMessageBox.showerror('Error','You must select at least 1 system name')

        year_string = ''
        for year in year_list:
            year_string = year_string + year + ","
        year_string = year_string[:-1]

        factory_string = ''
        for factory in factory_list:
            factory_string = factory_string + "'" + factory + "'" + ","
        factory_string = factory_string[:-1]

        model_string = ''
        for model in model_list:
            model_string = model_string + "'" + model + "'" + ","
        model_string = model_string[:-1]

        system_string = ''
        for system in system_list:
            system_string = system_string + "'" + system + "'" + ","
        system_string = system_string[:-1]

        sql_final = sql_begin + year_string + ")" + "\nAND HDS.FCTRY_CD IN(" + factory_string + ")" + "\nAND HDS.MDL_NM IN(" \
                + model_string + ")" + "\nAND HDS.SYS_NM IN(" + system_string + ")"

        print sql_final


if __name__ == "__main__":
    root = Tk()
    root.title("Get HDS/Freeze Tool")
    root.update()
    app = GetHDSFreeze(root)
    root.mainloop()
