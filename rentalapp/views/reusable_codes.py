import requests
url = "https://restcountries.com/v3.1/all"
data = requests.get(url).json()

for i in range(len(data)):
    try:
        country_list = data[i]['name']['common']
        language_list = list(data[i]['languages'].values())
        language_list = ', '.join(language_list)
        flags_list = list(data[i]['flags'].values())[1]
        capital_country = data[i]['capital'][0]
        country_region = data[i]['region']
        country_sub_region = data[i]['subregion']
        country_maps = data[i]['maps']['googleMaps']
        country_timezones = data[i]['timezones'][0]
        country_currency = list(data[i]['currencies'])[0]
        country_symbol = list(data[i]['currencies'][country_currency])[1]
        country_currency = list(data[i]['currencies'][country_currency][country_symbol])[0]
        population = data[i]['population']
            
            # Create and save a new Country instance
        # country_instance = Country(
        #     name=country_list, 
        #     flag=flags_list,
        #     capital=capital_country,
        #     languages=language_list,
        #     region=country_region,
        #     subregion=country_sub_region,
        #     maps=country_maps,
        #     population=population,
        #     timezones=country_timezones,
        #     currencies=country_currency
        # )
        # country_instance.save()

    except Exception as e:
        print(e)


url = "KUb4SScJeAD6tiWLWjvv0xaF9NkDrLujOd8x568lPrIVG0ffrTgsiPxRuh7s"