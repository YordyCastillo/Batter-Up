import json

f = open('2-24.json', 'r')
db = json.load(f)
for ele in db[0:]:
    if (len(ele) < 3):
        db.remove(ele)
    with open('Mar_recipes.json', 'w') as file:
        json.dump(db, file, indent=4)
"""for ele in db[0:]:
   if (len(ele)<2)==True:
       db.remove(ele)
for Ingredients in 
with open('recipes_scraper/spiders/Feb_recipe.json', 'w') as file:
    json.dump(db,file,indent=4)
    
    """


#text in-between commans
#text after a number
#text before the opeing parentheses
#text after a the closing parentheses
#text after size i.e. small, medium, large