import wx
import json
from helper import *
import webbrowser
import wx.lib.agw.ultimatelistctrl as ULC

class MainWindow(wx.Frame):

    def __init__(self, parent, title):
        """
        Initialize the main window for the recipe application.

        :param parent: Parent widget for the main window.
        :type parent: wx.Window
        :param title: Title for the main window.
        :type title: str
        """
        super(MainWindow, self).__init__(parent, title=title, size=(600, 500))
        self.Centre()
        self.CreateStatusBar()
        self.createMenu()
        self.panel = RecipePanel(self)


    def createMenu(self):
        """
        Create the menu for the main window.
        """
        # MENUS
        menu = wx.Menu()
        menuLoad = menu.Append(wx.ID_FILE, "Load", "Load File")
        menuSearch = menu.Append(wx.ID_FIND, "Search", "Search for Recipe")
        menuExit = menu.Append(wx.ID_EXIT)

        # MENUBAR
        menuBar = wx.MenuBar()
        menuBar.Append(menu, "&File")  # Adding the 'File' to the MenuBar
        self.SetMenuBar(menuBar)  # Adding the MenuBar to the Frame content.

        # Binding Menu Events
        self.Bind(wx.EVT_MENU, self.OnLoad, menuLoad)
        self.Bind(wx.EVT_MENU, self.OnExit, menuExit)

    def OnLoad(self, event):
        """
        Event handler for when the "Load" menu item is clicked. Opens a file dialog
        to allow the user to select a file to load, and then loads the selected
        file and updates the panel with the contents of the file.
        """
        self.frame = wx.Frame(None, -1, 'window.py')
        self.frame.SetSize(0, 0, 200, 50)

        self.openFileDialog = wx.FileDialog(self.frame, "Open", "",
                                            "", "JSON files (*.json)|*.json",
                                            wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)

        if self.openFileDialog.ShowModal() == wx.ID_CANCEL:
            return  # user canceled loading file

        fileName = self.openFileDialog.GetPath()

        recipes = ""
        try:
            recipesFile = open(fileName, 'r')
            recipes = json.load(recipesFile)
        except FileNotFoundError as ex:
            print(ex)
            wx.MessageBox("The file could not be found.",
                          caption="Error")
        except json.JSONDecodeError as ex1:
            print(ex1)
            wx.MessageBox("The file provided does not seem to be JSON.",
                          caption="Error")

        self.JSONHelper = Helper(recipes)

        self.panel.RecipeSourceFile(self.JSONHelper)

    def OnSearch(self, event):
        """
        Event handler for when the search bar is used. Filters the recipes displayed
        in the panel based on the search query.
        """
        query = event.GetString()
        self.panel.FilterRecipes(query)

    def OnExit(self, event):
        """
        Event handler for when the "Exit" menu item is clicked. Closes the main window.
        """
        self.Close(True)





class RecipePanel(wx.Panel):
    def __init__(self, parent):
        """
        Initialize the panel for displaying recipes.

        :param parent: Parent widget for the panel.
        :type parent: wx.Window
        """
        wx.Panel.__init__(self, parent)
        self.SetBackgroundColour('gray')

        self.Recipe_list = wx.ListCtrl(self, style=wx.LC_REPORT)
        self.Recipe_list.InsertColumn(0, 'Recipe Name', width=200)
        self.Recipe_list.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnRecipeSelected)

        # Used a UtimateListCtrl over regular ListCtrl more info about it at https://docs.wxpython.org/wx.lib.agw.ultimatelistctrl.UltimateListCtrl.html
        self.Ingredients_URL_COLS = ULC.UltimateListCtrl(
            self,
            agwStyle=ULC.ULC_REPORT | ULC.ULC_HAS_VARIABLE_ROW_HEIGHT

        )

        self.Ingredients_URL_COLS.InsertColumn(0, 'Ingredients', width=200)
        self.Ingredients_URL_COLS.InsertColumn(1, 'URL', width=200)

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.Recipe_list, 0, wx.ALL | wx.EXPAND)
        sizer.Add(self.Ingredients_URL_COLS, 1, wx.ALL | wx.EXPAND)
        self.SetSizer(sizer)

        # self.RecipeSourceFile()

        # More bind events
        self.Recipe_list.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnRecipeSelected)
        self.Ingredients_URL_COLS.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnLinkSelected)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnRecipeSelected)

    def OnPaint(self, evt):
        """
        Event handler for when the panel needs to be repainted. Resizes the columns
        in the ingredients list control to evenly divide the width of the control.

        :param evt: Paint event.
        :type evt: wx.PaintEvent
        """
        width, height = self.Ingredients_URL_COLS.GetSize()
        for i in range(2):
            self.Ingredients_URL_COLS.SetColumnWidth(i, int(width / 2))
        evt.Skip()

    def OnRecipeSelected(self, event,source):
        """
        Event handler for when a recipe is selected in the recipe list control.
        Clears the ingredients list control and populates it with the ingredients
        and URLs for the selected recipe.

        :param event: Selection event for the recipe list control.
        :type event: wx.ListEvent
        """
        source = event.GetText()
        #print(source)
        self.Ingredients_URL_COLS.DeleteAllItems()
        self.Recipe_Ingr_URL(source)

    def OnLinkSelected(self, event):
        """
        Event handler for when an ingredient URL is selected in the ingredients list
        control. Opens the URL in the default web browser.

        :param event: Selection event for the ingredients list control.
        :type event: wx.ListEvent
        """
        webbrowser.open(event.GetText())

    def RecipeSourceFile(self, helper):
        recipeNames = helper.recipeList()
        self.Recipe_list.DeleteAllItems()
        for recipe in recipeNames:
            self.Recipe_list.Append([recipe])

    def Recipe_Ingr_URL(self,helper,source):
        ings, url = helper.retrieveIngredientsList(source)
        #ingr_string = ""
        #for ingr in ings:
        #    ingr_string += ingr
        #return ingr_string, url
            # change == to in if you want to match substring
            #if recipe[u'Recipe_Name'] == source:
            #    return ing, url
        index = 0
        self.Ingredients_URL_COLS.InsertStringItem(0, "\n".join(ings))
        self.Ingredients_URL_COLS.SetStringItem(index, 1, url)


        """for ele in self.file:
           if source in ele['Recipe_Name']:
                index = 0
                self.Ingredients_URL_COLS.InsertStringItem(0, "\n".join(ele['Ingredients']))
                self.Ingredients_URL_COLS.SetStringItem(index, 1, ele["URL"])"""

        """for recipe in self.recipes:
                # change == to in if you want to match substring
                if recipe[u'Recipe_Name'] == passedRecipe:
                    return recipe[u'Ingredients'], recipe[u'URL']"""



        # path = '/Users/Yordy/recipes_scraper/Mar_recipes.json'
        # with open(path, 'r') as j:
        # data = json.loads(j.read())
        # for ele in data[0:]:
        # self.Recipe_list.InsertItem(0, ele['Recipe_Name'])


def main():
    """
    Main entry point for the recipe application.
    """
    app = wx.App()
    window = MainWindow(None, "Batter Up!")
    window.Show()
    app.MainLoop()

if __name__ == '__main__':
    main()
