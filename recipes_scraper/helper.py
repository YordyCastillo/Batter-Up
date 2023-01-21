#import json
import configparser


class Helper:

    def __init__(self, recipes):
        self.recipes = recipes


        config = configparser.ConfigParser()
        config.read('config.ini')
        section_name = 'Helper'
        attributes = []

        if section_name in config:
            section_keys = ["recipename","ingredients","url"]
            for key in config[section_name]:
                if key in section_keys:
                    attributes.append(config[section_name][key])
            print(attributes)

            #print(config[section_name][''])


        # these should eventually be populated from a file
        #attributes = ['Recipe_Name', 'Ingredients', 'URL']

        bad_recipes = []
        good_recipes = []

        for recipe in self.recipes:
            recipeKeys = list(recipe)
            isFound = all(item in recipeKeys for item in attributes)
            if (isFound):
                good_recipes.append(recipe)
            else:
                bad_recipes.append(recipe)
        self.recipes = good_recipes
    #rint("Length of self.recipes: " + str(len(self.recipes)))
        #print("Length of bad_recipes: " + str(len(bad_recipes)))

        #print("Length of good_recipes: " + str(len(good_recipes)))



    def recipeList(self):
        recipeNames = []
        for recipe in self.recipes:
            recipeNames.append(recipe[u'Recipe_Name'])
        return recipeNames

    def retrieveIngredientsList(self, passedRecipe):
        for recipe in self.recipes:
            # change == to in if you want to match substring
            if recipe[u'Recipe_Name'] == passedRecipe:
                return recipe[u'Ingredients'], recipe[u'URL']

    def searchRecipesWithIngredient(self, passedIngredient):
        recipeNames = []
        for recipe in self.recipes:
            # print(recipe[u'Recipe_Name'])
            for ingredient in recipe[u'Ingredients']:
                if passedIngredient in ingredient:
                    recipeNames.append(recipe[u'Recipe_Name'])
                    break  # word might be in more than one ingredient
        return recipeNames

    def reset(self):
        self.__init__()