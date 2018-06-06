import web_crawler as wc

if __name__ == "__main__":	
	searchResults = wc.getSearchResults('http://shopping.com', 'mobile', 3)
	for pair in searchResults:
	 	print(pair)

	result = wc.getProductCount('http://shopping.com', 'mobile')
	print(result)