

import datetime
from typing import Optional


class OrderEntity:
    def __init__(
            self, 
            id: Optional[int] = None, 
            order_date: datetime = None, 
            status: str = None, 
            total_amount: float = None
    ):
        self.id = id or None
        self.order_date = order_date
        self.status = status
        self.total_amount = total_amount



    