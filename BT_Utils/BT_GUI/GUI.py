import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

tree_list = [('jbl', '34:43', 'zebbi'), ('akuna', '34:4w', 'zebbi'), ('patume', '3erew', 'zebbi')]

# Conert data to ListStore(list Treeview can display)
list_store = Gtk.ListStore(str, str, str)
for el in tree_list:
    list_store.append(list(el))

class myGUI(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title='BT_A2DP_Manager')

        # Setting default icon and window size
        self.set_default_icon_from_file('/home/spucis/Pictures/Screenshot from 2020-01-14 23-06-40.png')
        self.set_default_size(1024, 512)

        self.Grid_1 = Gtk.Grid()
        self.add(self.Grid_1)

        # Center Grid
        self.Grid_Center = Gtk.Grid()

        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=256)
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=100)
                
        self.Scan = Gtk.Button(label='Start Scan')
        self.Scan.connect("clicked", self.on_button_clicked)

        self.A2DP = Gtk.ComboBoxText()
        self.A2DP.append_text("Scelta1")
        self.A2DP.append_text("Scelta2")
        self.A2DP.set_active(0)
        # self.A2DP.connect("func", data direi)

        self.button3 = Gtk.Button(label='Start scan')
        self.button3.connect("clicked", self.on_button_clicked)

        self.B = Gtk.Label("Bottom")
        
        # TreeView is the item that is displayed
        self.tree = Gtk.TreeView(list_store)

        for i, col_title in enumerate(["Col_1", "Col_2", "Col_3"]):
            # Render explains how to draw the data
            renderer = Gtk.CellRendererText()

            # Creating columns ang givinf number identifier
            column = Gtk.TreeViewColumn(col_title, renderer, text=i)
            self.tree.append_column(column)

        hbox.pack_start(vbox, True, True, 0)

        vbox.pack_start(self.Scan, True, True, 0)
        hbox.pack_start(self.Grid_Center, True, True, 0)
        self.Grid_Center.add(self.A2DP)
        hbox.pack_start(self.button3, True, True, 0)
        vbox.pack_end(self.B, True, True, 0)
        vbox.pack_end(self.tree, True, True, 0)

        self.Grid_1.add(hbox)

        self.connect("destroy", Gtk.main_quit)
        self.show_all()
        Gtk.main()

    def on_button_clicked(self, widget):
        print("Ciao Allegro")