# Importing all the necessary libraries
import re
import requests
from bs4 import BeautifulSoup
import pandas as pd
import lxml


# Defining header for requesting data
headers = {'User-Agent': "getbagsfinance@gmail.com"}

# METHOD 1
# mention the path to excel file containing the URL of SEC filing documents
df = pd.read_csv("/replace-with-path-to-file/")
# select the form type for which you need to scrap data, based on the excel document you have
selected_rows = df[df['column-name-that-has-form-types'] == 'form-type-in-column']
# selected_rows = selected_rows[30:60]

# METHOD 2
# Mention the URL of filing documents for which you need to scrap data.
links = [r'replace//with/URL/of/Webpage/',]

# Getting content of SEC filing
request = requests.get(url,headers=headers)
html_page=request.text
# Creating bs object
soup = BeautifulSoup(html_page,'lxml')
# Removing <img> tags as it slows down the process of webscraping
imageTags = soup.find_all("img")
for tag in imageTags:
    tag.extract()

# Removing tags that have no content, to make webscraping optimal
emptyElements = soup.findAll(True,string=re.compile(r'^(\n)*(\xa0)*$'))
for tag in emptyElements:
    tag.extract()


number = 0

# If using Method 1,uncomment below line of code
for index, row in selected_rows.iterrows():

# If using Method 2, uncomment below line of code
# for url in links:

# If using Method 2, comment below line of code
    url = row['URL']
    number = number+1
    print(number,url)

    footnotes={}
    try:
        # Retrieving tags that have the term 'side pocket'/'side-pocket'/'sidepocket' without case sensitivity.
        # Replace the regex with required term.
        target = soup.find_all(True, string=re.compile(r'.*side.*pocket.*', re.IGNORECASE|re.DOTALL))

        keys_to_delete = []
        value=[]
        targetLength = len(target)

        # Deleting the duplicate elements returned
        newTarget=[]
        addedStrings=[]
        if(targetLength>0):
            newTarget.append(target[0])
            addedStrings.append(target[0].string)
            if (targetLength>=2):
                for i in range(1, targetLength):
                    if target[i].string not in addedStrings:
                        newTarget.append(target[i])
                        addedStrings.append(target[i].string)

        for resultElement in newTarget:
            entireRow = resultElement.findParents('tr')
            for row in entireRow:
                cells = row.findChildren(recursive=False)
                i=0
                for cell in cells:
                    if cell.contents:
                        if i%2 == 0:
                            key=cell.text.replace(" ", "").replace("\xa0", "")
                            i = i+1
                        else:
                            value = cell.text
                            i=i+1
                pattern=re.compile(r'.*side.*pocket.*',re.IGNORECASE|re.DOTALL)

                if re.search(pattern,key) or re.search(pattern,value):
                    if len(key)<=7:
                        footnotes[key]=value
        print(footnotes)
        print(number,"added")
    except:
        print("Error : Error parsing HTML content. Ignoring the problematic content.")
        footnotes['Error'] = "Error parsing HTML content. Ignoring the problematic content."
        print(number,"added")

    # If using Method 2 : The below line of code adds a new column 'Footnotes- side pocket' and adds row values respective for each filing.
    df.loc[index, 'Footnotes- side pocket'] = [footnotes]

# If using Method 2: Save the updated DataFrame back to the CSV file
df.to_csv("file - footnotes.csv", index=False)
