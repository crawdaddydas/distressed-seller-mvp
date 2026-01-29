"""Database models for property tracking"""
from sqlalchemy import create_engine, Column, String, Integer, Decimal, Date, Text, TIMESTAMP, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from config import DATABASE_URL

Base = declarative_base()
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)


class Property(Base):
    """Property model for tracking listings"""
    __tablename__ = 'properties'

    property_id = Column(String(50), primary_key=True)
    address = Column(Text, nullable=False)
    city = Column(String(100), default='St. Petersburg')
    state = Column(String(2), default='FL')
    zip_code = Column(String(10))
    property_type = Column(String(50))

    # Current listing
    current_price = Column(Decimal(12, 2))
    listing_date = Column(Date)
    listing_days = Column(Integer)
    status = Column(String(20))

    # Agent contact
    agent_name = Column(String(200))
    agent_phone = Column(String(20))
    agent_email = Column(String(200))

    # Property details
    bedrooms = Column(Integer)
    bathrooms = Column(Decimal(3, 1))
    sqft = Column(Integer)
    year_built = Column(Integer)

    # Engagement
    views = Column(Integer, default=0)
    favorites = Column(Integer, default=0)

    # Valuations
    estimated_value = Column(Decimal(12, 2))
    last_sold_price = Column(Decimal(12, 2))
    last_sold_date = Column(Date)

    # Metadata
    first_seen = Column(TIMESTAMP, default=datetime.utcnow)
    last_updated = Column(TIMESTAMP, default=datetime.utcnow)

    __table_args__ = (
        Index('idx_zip_code', 'zip_code'),
        Index('idx_listing_days', 'listing_days'),
        Index('idx_status', 'status'),
    )


class PriceHistory(Base):
    """Price history tracking"""
    __tablename__ = 'price_history'

    id = Column(Integer, primary_key=True, autoincrement=True)
    property_id = Column(String(50), nullable=False)
    price = Column(Decimal(12, 2), nullable=False)
    changed_date = Column(Date, nullable=False)
    event_type = Column(String(20))  # 'listed', 'reduced', 'increased'

    __table_args__ = (
        Index('idx_property_date', 'property_id', 'changed_date'),
    )


class DistressScore(Base):
    """Distress scores with breakdown"""
    __tablename__ = 'distress_scores'

    property_id = Column(String(50), nullable=False)
    score = Column(Integer, nullable=False)
    score_date = Column(Date, nullable=False)

    # Score components
    dom_points = Column(Integer)
    reduction_points = Column(Integer)
    drop_count_points = Column(Integer)
    below_estimate_points = Column(Integer)
    engagement_points = Column(Integer)
    market_context_points = Column(Integer)

    __table_args__ = (
        Index('idx_distress_score', 'score'),
        Index('idx_property_score_date', 'property_id', 'score_date'),
    )


def init_db():
    """Initialize the database schema"""
    Base.metadata.create_all(engine)
    print("✅ Database initialized")


if __name__ == '__main__':
    init_db()