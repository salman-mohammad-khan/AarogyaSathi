from app.core import websearch

r = websearch.search_health("what is dengue fever")
if r:
    print("SOURCE:", r["source"])
    print("URL:", r["url"])
    print("ANSWER:", r["answer"][:200])
else:
    print("NO RESULT (DuckDuckGo may be blocked or returned nothing)")
