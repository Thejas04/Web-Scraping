'''Importing modules needed in the code, If some of them missing you can install it in on your environment'''
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
import time
import requests

'''Feel Free to use other method or modules as you see fit'''

start_time = datetime.now()
'''Declaration of the columns that will be exported in excel file'''
columns_list = ["url", "product_title", "size", "price", "variation_id"]
result = pd.DataFrame(columns=columns_list)

'''Define the path to your input file'''
Links = pd.read_excel(r'/Users/thejas/Downloads/Mister_Sandman_Python_Test/input.xlsx')

candidates = input("Please input your name here : ")

'''Function to extract different informations of the product'''


def do_task(iteration):
    url = Links.iloc[iteration, 0]

    '''You can either use Selenium to scrape or use Beautifulsoup'''

    '''Try to fulfill the output required by fetching the data and save it in a variable'''
    output = []
    print(url)
    page = requests.get(url)
    variant = ''
    dim_flag = 0
    ## validating if varinat is present in the url link else variant is blank
    if len(url.split("=")) == 2:
        variant = url.split("=")[1]
    else:
        # if varaint id is not present then dimension is present in the url
        dim = url.split("-")[-1]
        dim_flag = 1
    output.append(variant)
    soup = BeautifulSoup(page.content, "html.parser")
    #print(soup)
    a = soup.find_all("div", {"class": "product-main"})
    title = ""
    # Getting Title from the html
    for i in soup.find_all("div", {"class": "product-details"}):
        #print("TITLE")
        title = i.find(class_="product-title").text
        for val in title.split("\n"):
            if not val.strip() == "":
                title = val
    output.append(url)
    output.append(title.strip())
    if not dim_flag:
        # handling scenario where 404 error is returned for some of the website links
        dim_tree = soup.find_all(class_="form-field-input form-field-select")
        if not (len(dim_tree)):
            dim = ""
        else:
            # getting dimension from the html
            dim = dim_tree[0].find_all("option", selected=True)[0].text
        output.append(dim.strip().strip("\n"))
    else:
        output.append(dim)
    if not len(a):
        money = ""
        output.append(money)
    else:
        # getting tags for price
        for tag in a[0]('span'):

            money = tag.find(class_="money")
            if money:
                money = money.text
                output.append(money)
                break
    return output


'''Use the function above to crawl for all links'''
# initialising empty dataframe
results = pd.DataFrame()
variant = []
url_list = []
title_list = []
dim_list = []
price_list = []
index = 0
for iteration in range(len(Links)):
    print('on the {} link (total: {})'.format(iteration + 1, len(Links)))
    output = do_task(iteration)
    variant.append(output[0])
    url_list.append(output[1])
    title_list.append(output[2])
    dim_list.append(output[3])
    price_list.append(output[4])

# adding values in the dataframe

results['url'] = url_list
results['product_title'] = title_list
results['size'] = dim_list
results['price'] = price_list
results['variant'] = variant

# '''Exporting result to target folder'''
end_time = datetime.now()
timestr = time.strftime("%d.%m.%Y-%H%M%S")
print('Duration: {}'.format(end_time - start_time))
name = "Webshop_" + timestr + "_" + candidates
results.to_excel(r'{}.xlsx'.format(name), index=False)
