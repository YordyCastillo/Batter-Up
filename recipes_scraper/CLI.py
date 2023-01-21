import json
from helper import *


def main():
    """
    The main function for the Batter-up CLI interface. It prompts the user to enter the filename of a JSON file to load,
    loads the file and initializes a Helper object with the contents of the file. It then enters a loop in which it
    prompts the user to select a task and performs the selected task. The tasks include: listing known recipes, searching
    for recipes containing a given ingredient, listing the ingredients for a given recipe, and exiting the program.
    """
    print("Welcome to the Batter-up CLI interface!\n")

    while True:
        fileName = input("Type in the filename of the JSON data to use: ")
        try:
            recipesFile = open(fileName, 'r')
            recipes = json.load(recipesFile)
            break
        except FileNotFoundError as ex:
            print(ex)
            ask = input("The file could not be found."
                        " Would you like to try a different JSON file?"
                        " Y for Yes, N for No\n")
            if ask.lower() != 'y':
                print("OK GoodBye")
                exit(1)
        except json.JSONDecodeError as ex1:
            print(ex1)
            ask = input("The file provided does not seem to be JSON."
                        " Would you like to try a different JSON file?"
                        " Y for Yes, N for No\n")
            if ask.lower() != 'y':
                print("OK GoodBye")
                exit(1)

    JSONHelper = Helper(recipes)

    # if (len(fileName) == 0):
    # response = (input("\nYou provided an empty file ... would you like to try a diffrent JSON file? Y for Yes , N for No\n"))
    # if response =='y' or response == 'Y':
    # main()
    # else:
    # exit(1)
    # else:

    while True:
        print("\nPlease select a task from the following:\n\n"
              " 1. List known recipes\n"
              " 2. Search for recipes containing ingredient\n"
              " 3. List ingredients for given recipe\n"
              " 4. Exit the program\n")
        command = input("Task number: ")
        if command == "1":
            recipeNames = JSONHelper.recipeList()
            print("")
            for recipe in recipeNames:
                print("-" + recipe)
        if command == "2":
            ingredient = input("Type in ingredient: ")
            recipesWithIngredient = JSONHelper.searchRecipesWithIngredient(ingredient)
            print("")
            if (len(recipesWithIngredient) == 0):
                print("No recipes with that ingredient found!")
            else:
                for recipe in recipesWithIngredient:
                    print("-" + recipe)
        if command == "3":
            recipe = input("Type in recipe: ")
            try:
                ingredients, URL = JSONHelper.retrieveIngredientsList(recipe)
                print("")
                ingredient_string = ""
                for ingredient in ingredients:
                    ingredient_string += ingredient
                print("-" + ingredient_string)
                print("\nFor more information, visit the following URL: " + URL)
            except:
                print("That recipe was not found!")
        if command == "4":
            exit(0)


if __name__ == "__main__":
    main()