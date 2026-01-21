from datetime import datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.infrastructure.database import Base


class OrderORM(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, index=True)
    order_date = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default='pending')
    total_amount = Column(Float, nullable=False)

    order_items = relationship("OrderItemORM", back_populates="order")