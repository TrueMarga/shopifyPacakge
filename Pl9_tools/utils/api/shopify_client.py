import os
from dotenv import load_dotenv
import requests
import json

# Load environment variables
load_dotenv()

class ShopifySearch:
    def __init__(self):
        self.store_url = os.getenv('SHOPIFY_STORE_URL')
        self.storefront_token = os.getenv('SHOPIFY_STOREFRONT_TOKEN')
        
        if not self.store_url or not self.storefront_token:
            raise ValueError("Missing required environment variables. Please check your .env file")
            
        self.endpoint = f"https://{self.store_url}/api/2024-01/graphql.json"
        self.headers = {
            "X-Shopify-Storefront-Access-Token": self.storefront_token,
            "Content-Type": "application/json",
        }

    def search_products(self, query: str, limit: int = 10):
        """Perform predictive search for products"""
        graphql_query = """
        query predictiveSearch($query: String!, $limit: Int!) {
            predictiveSearch(query: $query, limit: $limit) {
                products {
                    id
                    title
                    handle
                    description
                    priceRange {
                        minVariantPrice {
                            amount
                            currencyCode
                        }
                    }
                    images(first: 1) {
                        edges {
                            node {
                                url
                            }
                        }
                    }
                }
            }
        }
        """

        try:
            print(f"Searching for '{query}'...")
            
            response = requests.post(
                self.endpoint,
                headers=self.headers,
                json={
                    "query": graphql_query,
                    "variables": {
                        "query": query,
                        "limit": limit
                    }
                },
                timeout=10
            )
            response.raise_for_status()
            
            data = response.json()
            
            # Check for errors in the GraphQL response
            if 'errors' in data:
                print(f"GraphQL Error: {data['errors']}")
                return None
                
            # Safely access the predictive search results
            search_results = data.get('data', {}).get('predictiveSearch', {})
            
            # Check if we have any products
            if not search_results or not search_results.get('products'):
                print(f"No products found matching '{query}'")
                return {'products': []}
                
            return self.format_results(search_results)
            
        except requests.exceptions.RequestException as e:
            print(f"Network or API Error: {e}")
            return None
        except json.JSONDecodeError:
            print("Error: Invalid JSON response from API")
            return None
        except Exception as e:
            print(f"Unexpected error: {e}")
            return None

    def format_results(self, search_data):
        """Format the search results"""
        products = []
        
        if not search_data or 'products' not in search_data:
            return {'products': []}
            
        for product in search_data['products']:
            # Safely get price information
            price_range = product.get('priceRange', {})
            min_variant_price = price_range.get('minVariantPrice', {}) if price_range else {}
            
            # Safely get image information
            images = product.get('images', {})
            edges = images.get('edges', []) if images else []
            image_url = edges[0].get('node', {}).get('url') if edges else None
            
            products.append({
                'title': product.get('title', 'No Title'),
                'handle': product.get('handle', ''),
                'description': product.get('description', ''),
                'price': {
                    'amount': min_variant_price.get('amount', '0.00'),
                    'currency': min_variant_price.get('currencyCode', 'USD')
                },
                'image_url': image_url
            })
            
        return {'products': products}

