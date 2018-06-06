import requests
from bs4 import BeautifulSoup


def getResultsForProduct(url, productName):
	pageContent = requests.get(url + '/products?KW=' + productName)
	htmlContent = BeautifulSoup(pageContent.text, 'html.parser')
	return htmlContent

def getResultsForProductAndPageNumber(url, productName, pageNumber):
	pageContent = requests.get(url + '/' + productName + '/products~PG-'+ str(pageNumber) + '?KW=' + productName)
	htmlContent = BeautifulSoup(pageContent.text, 'html.parser')
	return htmlContent

def getProductsPerPage(url, productName):
	htmlResult = getResultsForProduct(url, productName)
	page_count = htmlResult.find(class_='numTotalResults')
	if page_count == None:
		return None
	for page in page_count:
		results_per_page = page.split(' ')[3]
	return int(results_per_page)

def getProductsOnLastPage(url, productName, pageNumber):
	last_page_html = getResultsForProductAndPageNumber(url, productName, pageNumber)
	last_page_count = last_page_html.find(class_='numTotalResults')
	for last_page in last_page_count:
		last_page_results = int(last_page.split(' ')[3].replace(',', '')) - int(last_page.split(' ')[1].replace(',', ''))
	return last_page_results

def getProductCount(url, productName):
	htmlContent = getResultsForProduct(url, productName)
	results_list = htmlContent.find(class_='paginationNew')
	if results_list == None:
		results = getProductsPerPage(url, productName)
		if results == None:
			print("No matching results found!")
			return 0
		return results
	results_list_items = results_list.findAll('a')
	maxVal = 0

	for results in results_list_items:
		names = results.contents
		for a in names:
			try:
				res = int(a.strip())
				if res > maxVal:
					maxVal = res
			except ValueError as verr:
				pass

	if maxVal > 0:
		products_on_last_page = getProductsOnLastPage(url, productName, maxVal)
	else:
		products_on_last_page = 0

	maxVal = (maxVal-1) * getProductsPerPage(url, productName) + products_on_last_page + 1
	return maxVal

def getProductCountLowAndHighPerPage(url, productName, pageNum):
	htmlResult = getResultsForProductAndPageNumber(url, productName, pageNum)
	page_count = htmlResult.find(class_='numTotalResults')
	if page_count == None:
		return None
	for page in page_count:
		results_per_page_low = page.split(' ')[1]
		results_per_page_high = page.split(' ')[3]
	result_pair = (int(results_per_page_low), int(results_per_page_high))
	return result_pair

def getSearchResults(url, productName, pageNum):
	pageContent = requests.get(url + '/products?KW=' + productName)
	htmlContent = BeautifulSoup(pageContent.text, 'html.parser')

	maxProductCount = getProductCountLowAndHighPerPage(url, productName, pageNum)
	if maxProductCount == None:
		print("No results found!")
		return 0

	searchResults = []

	searchResultsContainer = htmlContent.find(id='searchResultsContainer')
	product_count = 1
	product_id_prefix = "quickLookItem-"

	for count in range(1,(maxProductCount[1]-maxProductCount[0])):
		searchCell = searchResultsContainer.find(id=(product_id_prefix+str(count)))
		
		try:
			product = searchCell.find(class_='gridItemBtm').find(class_='productName').findAll('span')
			price = searchCell.find(class_='gridItemBtm').find(id=('priceQA'+str(count))).find(class_='productPrice').findAll('a')
		except AttributeError:
			continue

		productName = product[0]['title']
		productPrice = price[0].contents[0].strip('\n')

		searchResults.append({productName:productPrice})

	for pair in searchResults:
	 	print(pair)
			
	return searchResults




