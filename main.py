from frontend import *

if __name__ == "__main__":
    root = tk.Tk()
    app = TollPlazaGUI(root)
    app.registeration_forum()
    app.searchbar()
    app.show_data()
    app.configuration()
    root.mainloop()

