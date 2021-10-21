import json

f = open('recipes_1014.json','r')
db=json.load(f)
for ele in db[0:]:
   if (len(ele)<2)==True:
       db.remove(ele)
with open('new_recipe.json','w') as file:
    json.dump(db,file,indent=4)


#text in-between commans
#text after a number
#text before the opeing parentheses
#text after a the closing parentheses
#text after size i.e. small, medium, large