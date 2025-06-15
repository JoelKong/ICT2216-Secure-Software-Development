from abc import ABC, abstractmethod
from typing import Dict, Tuple, Any, Optional

class IPaymentService(ABC):
    """Interface for payment service operations"""
    
    @abstractmethod
    def create_checkout_session(self, user_id: int) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        """Create a new checkout session"""
        pass
    
    @abstractmethod
    def verify_session(self, session_id: str) -> Tuple[bool, Optional[int], Optional[str]]:
        """Verify a completed session and update user membership"""
        pass