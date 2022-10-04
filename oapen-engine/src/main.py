import data.oapen as oapen

def main():

    books_community = oapen.get_community(oapen.BOOKS_COMMUNITY_ID)
    print(books_community)
    books_collections = oapen.get_collections_from_community(oapen.BOOKS_COMMUNITY_ID)
    print(books_collections)
    books_items = oapen.get_items_from_collection("ea93f8f0-430f-4a03-b7e2-5b06053585b0")

    print(books_items)
    
    return


if __name__ == "__main__":
    main()
