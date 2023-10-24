import wx
import sqlite3
import random


class NameGeneratorApp(wx.App):
    def OnInit(self):
        self.frame = MainFrame(None, title="Name Generator")
        self.frame.Show()
        return True


class MainFrame(wx.Frame):
    def __init__(self, parent, title):
        super(MainFrame, self).__init__(parent, title=title, size=(600, 400))
#        self.SetBackgroundColour(wx.Colour(255, 0, 0))

        self.notebook = wx.Notebook(self)
        self.tab_generate = NameGeneratorTab(self.notebook)
        self.tab_add = NameAddTab(self.notebook)
        self.tab_about = AboutTab(self.notebook)  # Add the "About" tab

        self.notebook.AddPage(self.tab_generate, "Generate Names")
        self.notebook.AddPage(self.tab_add, "Add Names")
        self.notebook.AddPage(self.tab_about, "About")  # Add the "About" tab

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.notebook, 1, wx.EXPAND)
        self.SetSizer(sizer)


class NameGeneratorTab(wx.Panel):
    def __init__(self, parent):
        super(NameGeneratorTab, self).__init__(parent)

        self.conn = sqlite3.connect('namegen_names.db')
        self.cursor = self.conn.cursor()

        self.gender_radio = wx.RadioBox(self, label="Select Gender", choices=["Male", "Female"],
                                        style=wx.RA_SPECIFY_COLS)

        self.generate_button = wx.Button(self, label="Generate")
        self.generated_name_label = wx.StaticText(self, label="Generated Name:")
        self.generated_name_text = wx.TextCtrl(self, style=wx.TE_READONLY)

        self.generate_button.Bind(wx.EVT_BUTTON, self.on_generate)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.gender_radio, flag=wx.EXPAND | wx.ALL, border=10)
        sizer.Add(self.generate_button, flag=wx.EXPAND | wx.ALL, border=10)
        sizer.Add(self.generated_name_label, flag=wx.EXPAND | wx.ALL, border=10)
        sizer.Add(self.generated_name_text, flag=wx.EXPAND | wx.ALL, border=10)

        self.SetSizer(sizer)

    def on_generate(self, event):
        gender = "male" if self.gender_radio.GetSelection() == 0 else "female"
        generated_name = self.generate_name(gender)
        self.generated_name_text.SetValue(generated_name)

    def generate_name(self, gender):
        table = 'male_firstnames' if gender == 'male' else 'female_firstnames'

        self.cursor.execute(f"SELECT name FROM {table} ORDER BY RANDOM() LIMIT 1")
        result = self.cursor.fetchone()

        self.cursor.execute("SELECT name FROM lastnames ORDER BY RANDOM() LIMIT 1")
        lastname_result = self.cursor.fetchone()

        return f"{result[0]} {lastname_result[0]}"


class NameAddTab(wx.Panel):
    def __init__(self, parent):
        super(NameAddTab, self).__init__(parent)

        self.conn = sqlite3.connect('namegen_names.db')
        self.cursor = self.conn.cursor()

        self.name_type_radio = wx.RadioBox(self, label="Name Type",
                                           choices=["Male Firstname", "Female Firstname", "Last Name"],
                                           style=wx.RA_SPECIFY_COLS)
        self.name_entry = wx.TextCtrl(self)
        self.add_button = wx.Button(self, label="Add Name")
        self.status_label = wx.StaticText(self, label="")

        self.add_button.Bind(wx.EVT_BUTTON, self.on_add)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.name_type_radio, flag=wx.EXPAND | wx.ALL, border=10)
        sizer.Add(self.name_entry, flag=wx.EXPAND | wx.ALL, border=10)
        sizer.Add(self.add_button, flag=wx.EXPAND | wx.ALL, border=10)
        sizer.Add(self.status_label, flag=wx.EXPAND | wx.ALL, border=10)

        self.SetSizer(sizer)

    def on_add(self, event):
        name_type = self.name_type_radio.GetStringSelection()
        name = self.name_entry.GetValue().strip()

        if not name:
            self.status_label.SetLabel("Please enter a name.")
            return

        table = None

        if name_type == "Male Firstname":
            table = "male_firstnames"
        elif name_type == "Female Firstname":
            table = "female_firstnames"
        elif name_type == "Last Name":
            table = "lastnames"

        if table:
            self.cursor.execute(f"SELECT name FROM {table} WHERE name=?", (name,))
            existing_name = self.cursor.fetchone()

            if existing_name:
                self.status_label.SetLabel("Name already exists.")
            else:
                self.cursor.execute(f"INSERT INTO {table} (name) VALUES (?)", (name,))
                self.conn.commit()
                self.status_label.SetLabel(f"{name} added to {name_type}s.")
                self.name_entry.SetValue("")
        else:
            self.status_label.SetLabel("Invalid name type.")


class AboutTab(wx.Panel):
    def __init__(self, parent):
        super(AboutTab, self).__init__(parent)

        about_text = """RPG Name Generator

Author: Kaotick Jay
GitHub: https://github.com/kaotickj

Description:
Generates random male or female names for all types of RPG uses. 


"""

        about_label = wx.StaticText(self, label=about_text, style=wx.ALIGN_CENTER)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(about_label, flag=wx.EXPAND | wx.ALL, border=10)

        self.SetSizerAndFit(sizer)


if __name__ == '__main__':
    app = NameGeneratorApp()
    app.MainLoop()
