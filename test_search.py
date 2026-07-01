from search import search_catalog

query = "Java developer backend APIs"

results = search_catalog(query)

for item in results:
    print(item)