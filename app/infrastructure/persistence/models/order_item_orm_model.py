from datetime import datetime

from sqlalchemy import Column, Float, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.core.databases.database import Base


class OrderItemORM(Base):
    __tablename__ = 'order_items'

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)

    order = relationship("OrderORM", back_populates="order_items")
    product = relationship("ProductORM", back_populates="order_items")