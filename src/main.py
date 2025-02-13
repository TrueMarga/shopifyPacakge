from utils.api.shopify_client import ShopifySearch

def get_search_suggestions(search_client, query, min_chars=2):
    """
    Get search suggestions as user types
    """
    if len(query) < min_chars:
        return None
        
    try:
        # Perform predictive search
        results = search_client.search_products(query)
        return results
    except Exception as e:
        print(f"Error getting suggestions: {e}")
        return None

def main():
    try:
        # Initialize the search client
        search_client = ShopifySearch()
        
        while True:
            # Get search term from user
            search_term = input("\nStart typing to search (or 'quit' to exit): ").strip()
            
            if search_term.lower() == 'quit':
                print("Goodbye!")
                break
                
            if not search_term:
                print("Please enter a search term")
                continue
                
            # Show that we're doing predictive search
            print("\nShowing predictive results...")
            
            # Get predictive results
            results = get_search_suggestions(search_client, search_term)
            
            if results is None:
                print("An error occurred while searching")
                continue
                
            if not results.get('products'):
                print(f"No products found matching '{search_term}'")
                suggested_terms = [
                    search_term.replace('o', 'oo'),  # hoddie -> hoodie
                    search_term + 's',               # hoodie -> hoodies
                    search_term.replace('ie', 'y')   # hoodie -> hoody
                ]
                print("\nDid you mean:")
                for term in suggested_terms:
                    print(f"- {term}")
                continue
                
            # Print results with categories
            print("\nFound Products:")
            for i, product in enumerate(results['products'], 1):
                print(f"\n{i}. {product['title']}")
                if product.get('price'):
                    print(f"   💰 Price: {product['price']['amount']} {product['price']['currency']}")
                if product.get('description'):
                    print(f"   📝 Description: {product['description'][:100]}...")
                if product.get('image_url'):
                    print(f"   🖼️  Product Image: {product['image_url']}")
                print(f"   🔗 Handle: {product['handle']}")
                
            # Show related terms
            related_terms = [
                f"{search_term} sale",
                f"{search_term} new",
                f"{search_term} popular"
            ]
            print("\nRelated searches:")
            for term in related_terms:
                print(f"- {term}")
                
    except KeyboardInterrupt:
        print("\nSearch terminated by user")
    except Exception as e:
        print(f"Fatal error: {e}")

if __name__ == "__main__":
    main()
