from lxml import etree
import requests
import json
import sys

arguments = sys.argv[1:]
data = []

for  arg in arguments:
    product_url = arg

    response = requests.get(product_url)

    if response.status_code == 200:
        dom = etree.HTML(response.text)
        title = "Not Found"
        titles = dom.xpath("//h1")
        if titles:
            title = titles[0].text.strip()

        elements = dom.xpath("//div[contains(@class, 'row-price')]/span")
        
        if elements:    
            prices = []
            for el in elements:
                p = el.text.replace("RON", "")
                p = p.replace(" ", "")
                p = p.replace(",", ".")
                p = float(p)
                prices.append(p)
            
            min_price = min(prices);
            max_price = max(prices)
            print(title, max_price, min_price, len(elements))


            data.append({"title": title, "max_price": max_price, "min_price":min_price, "nr_offers":len(elements)})
        else:
            print("Elements not found")
    else:
        print("Failed to fetch the webpage.")

if(len(data)):
        with open("product.json", "w") as json_file:
                json.dump(data, json_file, indent=4)