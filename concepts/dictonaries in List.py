travel_log = [
    {
        "country" : "France",
        "Visits" : 12,
        "Cities" : ["Paries" ,"Lillie","Dijion"],
    },
    {
      "country" : "Germany",
        "Visits" : 5,
        "Cities" : ["Berlin" ,"Tamil nadu","Sri lanka"],
    } ,  
    
]
def add_new_country(country_visited ,times_visted,cities_visited):
  new_country = {}  
  new_country["country"] = country_visited
  new_country["Visits"] = times_visted
  new_country["Cities"] = cities_visited
  travel_log.append(new_country)

    

add_new_country("Russia" ,2,["moscow","Sain paul","Amazaon"])
print(travel_log)