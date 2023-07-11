import requests

# API endpoint URL
api_url = "https://www.europeana.eu/api/v2/search.json"

# Request parameters
params = {
    "query": "monet",
    "media:Type": "IMAGE",
    "rows": 10,
    "wskey": "loaplinf"
}

# Send the API request
response = requests.get(api_url, params=params)

# Check the response status code
if response.status_code == 200:
    # Parse the JSON response
    data = response.json()

    # Process the response data
    if "items" in data:
        for item in data["items"]:
            # Extract relevant information from the response
            title = item["title"]
            image_url = item["edmPreview"]

            # Do something with the extracted data
            print(f"Title: {title}")
            print(f"Image URL: {image_url}")
            print()
            print(item)

    # Total number of results
    total_results = data["totalResults"]
    print(f"Total Results: {total_results}")
else:
    print("Request failed. Status code:", response.status_code)
