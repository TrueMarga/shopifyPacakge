# src/shopify_search/models.py
from pydantic import BaseModel
from typing import List, Optional

class Price(BaseModel):
    amount: float
    currency_code: str

class Product(BaseModel):
    id: str
    title: str
    handle: str
    description: Optional[str]
    price: Optional[Price]
    image_url: Optional[str]

class Collection(BaseModel):
    id: str
    title: str
    handle: str

class Page(BaseModel):
    id: str
    title: str
    handle: str

class SearchResults(BaseModel):
    products: List[Product]
    collections: List[Collection]
    pages: List[Page]
