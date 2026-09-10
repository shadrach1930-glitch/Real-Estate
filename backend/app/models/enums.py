"""
Shared enumerations used across the data model.
Values match the Database Design & Data Model Specification.
"""

import enum


class Intent(str, enum.Enum):
    BUY = "BUY"
    RENT = "RENT"
    SELL = "SELL"
    LAND = "LAND"
    PROPERTY_ENQUIRY = "PROPERTY_ENQUIRY"
    GENERAL_ENQUIRY = "GENERAL_ENQUIRY"
    HUMAN_REQUEST = "HUMAN_REQUEST"
    OTHER = "OTHER"


class TransactionType(str, enum.Enum):
    BUY = "BUY"
    RENT = "RENT"
    SELL = "SELL"
    UNKNOWN = "UNKNOWN"


class PropertyType(str, enum.Enum):
    APARTMENT = "APARTMENT"
    HOUSE = "HOUSE"
    DUPLEX = "DUPLEX"
    VILLA = "VILLA"
    LAND = "LAND"
    OFFICE = "OFFICE"
    SHOP = "SHOP"
    COMMERCIAL = "COMMERCIAL"
    OTHER = "OTHER"
    UNKNOWN = "UNKNOWN"


class Timeline(str, enum.Enum):
    IMMEDIATE = "IMMEDIATE"
    WITHIN_1_MONTH = "WITHIN_1_MONTH"
    WITHIN_3_MONTHS = "WITHIN_3_MONTHS"
    WITHIN_6_MONTHS = "WITHIN_6_MONTHS"
    RESEARCHING = "RESEARCHING"
    UNKNOWN = "UNKNOWN"


class LeadStatus(str, enum.Enum):
    NEW = "NEW"
    QUALIFIED = "QUALIFIED"
    ASSIGNED = "ASSIGNED"
    CONTACTED = "CONTACTED"
    FOLLOW_UP = "FOLLOW_UP"
    NEGOTIATION = "NEGOTIATION"
    CONVERTED = "CONVERTED"
    UNQUALIFIED = "UNQUALIFIED"
    LOST = "LOST"
    CLOSED = "CLOSED"


class LeadTemperature(str, enum.Enum):
    HOT = "HOT"
    WARM = "WARM"
    COLD = "COLD"


class Channel(str, enum.Enum):
    WEB = "WEB"
    WHATSAPP = "WHATSAPP"
    INSTAGRAM = "INSTAGRAM"
    EMAIL = "EMAIL"
    OTHER = "OTHER"


class SenderType(str, enum.Enum):
    CUSTOMER = "CUSTOMER"
    BOT = "BOT"
    SALES_REP = "SALES_REP"
    SYSTEM = "SYSTEM"


class FollowUpStatus(str, enum.Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"
    OVERDUE = "OVERDUE"
