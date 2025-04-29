import tkinter as tk
from tkinter import ttk
from backend import *

class TollPlazaGUI:
    def __init__(self, master):
        self.plaza = TollPlaza()
        self.master = master
        self.master.title("Toll Plaza Management System")
        self.success = ""
        self.registrationframe = ttk.LabelFrame(self.master, text="Entry Forum")
        self.registrationframe.grid(row=0, column=0, padx=10, pady=5)
        self.show_data_frame = ttk.LabelFrame(self.master, text="Recent Entries")
        self.show_data_frame.grid(row=0, column=1, padx=10, pady=5)
        self.config_frame = ttk.LabelFrame(self.registrationframe, text="Config")
        self.config_frame.grid(row=5, column=0, columnspan=2, padx=2, pady=2)
        
        self.cols = ["Vehicle", "Number Plate", "Rate", "Date And Time"]
        self.treescroll = ttk.Scrollbar(self.show_data_frame)

        self.data_treeview = ttk.Treeview(self.show_data_frame, columns=self.cols, show="headings", height=13, yscrollcommand=self.treescroll.set)
        self.treescroll.config(command=self.data_treeview.yview)

        self.data_treeview.column("Number Plate", width=100)
        self.data_treeview.column("Rate", width=70)
        self.data_treeview.column("Vehicle", width=70)
        self.data_treeview.column("Date And Time", width=120)
        
        self.data_treeview.heading("Vehicle", text="Vehicle")
        self.data_treeview.heading("Number Plate", text="Number Plate")
        self.data_treeview.heading("Rate", text="Rate")
        self.data_treeview.heading("Date And Time", text="Date And Time")

    def clear_entry(self, entry):
        entry.delete(0, 'end')

    def registeration_forum(self):
        vehicle_label = ttk.Label(self.registrationframe, text="Vehicle: ")
        vehicle_label.grid(row=0, column=0, padx=2, pady=2, sticky='w')
        self.vehicle_combox = ttk.Combobox(self.registrationframe, values=[name[0] for name in self.plaza.all_vehicle()])
        self.vehicle_combox.grid(row=1, column=0, columnspan=2, padx=2, pady=2, sticky='nsew')

        number_plate_label = ttk.Label(self.registrationframe, text="Number Plate: ")
        number_plate_label.grid(row=2, column=0, padx=2, pady=2, sticky='w')
        self.number_plate_entry = ttk.Entry(self.registrationframe)
        self.number_plate_entry.grid(row=3, column=0, columnspan=2, padx=2, pady=2, sticky='nsew')
        
        registration_b = ttk.Button(self.registrationframe, text="Add Details", command=self.registration_button, width=30)
        registration_b.grid(row=4, column=0, columnspan=2, padx=2, pady=2, sticky='nsew')
        self.success_label = ttk.Label(self.registrationframe, text="")
        self.success_label.grid(row=7, column=0, columnspan=2, padx=2, pady=2)
    
    def registration_button(self):
        number_plate = self.number_plate_entry.get()
        vehicle = self.vehicle_combox.get()
        if not number_plate or not vehicle:
            self.success_label.config(text="Error: Vehicle/Number Plate Can't Be Empty")
        else:
            self.render_data()
            self.clear_entry(self.vehicle_combox)
            self.clear_entry(self.number_plate_entry)
            self.success = self.plaza.register_passage(vehicle, number_plate)
            self.success_label.config(text=self.success)
            self.render_data()

        self.master.after(5000, lambda: self.hide_error(self.success_label))

    def show_data(self):
        self.render_data()

    def render_data(self):
        item_ids = self.data_treeview.get_children()
        for item in item_ids:
            self.data_treeview.delete(item)
        passage_tuple = self.plaza.passage_data()
        for data_tuple in passage_tuple[0:]:
            self.data_treeview.insert('', tk.END, values=data_tuple)
        self.clear_search.config(state="disable")

    def hide_error(self, label):
        label.config(text="")

    def searchbutton(self):
        search_by = self.search_entry.get()
        if search_by == "":
            self.search_error_label.config(text="Error: Search Bar Can Not Be Empty")
            self.master.after(5000, lambda: self.hide_error(self.search_error_label))
        else:
            search_result = self.plaza.search_passenger_data(search_by)
            item_ids = self.data_treeview.get_children()
            for item in item_ids:
                self.data_treeview.delete(item)
            passage_tuple = search_result
            if search_result == "Passenger data not found":
                self.search_error_label.config(text="Error: No Results")
                self.master.after(5000, lambda: self.hide_error(self.search_error_label))
            else:
                for data_tuple in passage_tuple[0:]:
                    self.data_treeview.insert('', tk.END, values(data_tuple))
                self.clear_entry(self.search_entry)
            self.clear_search.config(state="enable")

    def searchbar(self):
        self.searchbar_frame = ttk.Frame(self.show_data_frame)
        self.searchbar_frame.pack()
        search_label = ttk.Label(self.searchbar_frame, text="Search: ")
        search_label.grid(row=0, column=0)
        self.search_entry = ttk.Entry(self.searchbar_frame)
        self.search_entry.grid(row=0, column=1)
        search_button = ttk.Button(self.searchbar_frame, text="Search", command=self.searchbutton)
        search_button.grid(row=0, column=2)
        self.clear_search = ttk.Button(self.searchbar_frame, text="Show All", command=self.render_data, state="disable")
        self.clear_search.grid(row=0, column=3)
        self.search_error_label = ttk.Label(self.searchbar_frame, text="")
        self.search_error_label.grid(row=1, columnspan=4, pady=2)
        self.treescroll.pack(side="right", fill="y")
        self.data_treeview.pack(padx=5, pady=10)

    def addvehicle(self):
        name = self.add_vehicle_entry.get()
        print(self.plaza.add_vehicle(name=name))
        if name == "":
            self.error_label.configure(text="Error: Can't Be Empty <Add Vehicle>")
            self.master.after(5000, lambda: self.hide_error(self.error_label))
        else:
            self.clear_entry(self.add_vehicle_entry)
            self.vehicle_combox.configure(values=[name[0] for name in self.plaza.all_vehicle()])
            self.update_vehicle_price.configure(values=[name[0] for name in self.plaza.all_vehicle()])

    def fun_update_vehicle_price(self):
        vehicle_name = self.update_vehicle_price.get()
        vehicle_price = self.update_vehicle_price_updated.get()
        if not vehicle_name or not vehicle_price:
            self.error_label.configure(text="Error: Can't Be Empty <Select Vehicle> <Updated Price>")
            self.master.after(5000, lambda: self.hide_error(self.error_label))
        else:
            self.plaza.add_or_update_vehicle_rate(vehicle_name, vehicle_price)
            self.clear_entry(self.update_vehicle_price)
            self.clear_entry(self.update_vehicle_price_updated)

    def configuration(self):
        add_vehicle_label = ttk.Label(self.config_frame, text="Add Vehicle: ")
        add_vehicle_label.grid(row=0, column=0, padx=2, pady=5, sticky='w')
        self.add_vehicle_entry = ttk.Entry(self.config_frame)
        self.add_vehicle_entry.grid(row=0, column=1, padx=2, pady=5, sticky='ew')
        add_vehicle_button = ttk.Button(self.config_frame, text="Apply", command=self.addvehicle)
        add_vehicle_button.grid(row=0, column=2, padx=2, pady=5, sticky='ew')

        seperator1 = ttk.Separator(self.config_frame, orient="horizontal")
        seperator1.grid(row=1, column=0, columnspan=3, padx=2, pady=2, sticky='ew')

        update_vehicle_price_label = ttk.Label(self.config_frame, text="Select Vehicle: ")
        update_vehicle_price_label.grid(row=2, column=0, padx=2, pady=5, sticky='w')
        self.update_vehicle_price = ttk.Combobox(self.config_frame, values=[name[0] for name in self.plaza.all_vehicle()])
        self.update_vehicle_price.grid(row=2, column=1, padx=2, pady=5, sticky='ew')
        update_vehicle_price_label = ttk.Label(self.config_frame, text="Updated Price: ")
        update_vehicle_price_label.grid(row=3, column=0, padx=2, pady=5, sticky='w')
        self.update_vehicle_price_updated = ttk.Entry(self.config_frame)
        self.update_vehicle_price_updated.grid(row=3, column=1, padx=2, pady=5, sticky='ew')
        update_vehicle_price_button = ttk.Button(self.config_frame, text="Apply", command=self.fun_update_vehicle_price)
        update_vehicle_price_button.grid(row=2, rowspan=2, column=2, sticky='ns')
        self.error_label = ttk.Label(self.config_frame, text="")
        self.error_label.grid(row=4, column=0, columnspan=3)
