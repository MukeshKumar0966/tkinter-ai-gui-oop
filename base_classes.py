"""
Base classes demonstrating OOP concepts: Inheritance, Encapsulation, Polymorphism
"""

from abc import ABC, abstractmethod
from typing import Any, Dict
import logging

# Decorator examples
def performance_monitor(func):
    """Decorator to monitor method performance"""
    def wrapper(self, *args, **kwargs):
        import time
        start_time = time.time()
        result = func(self, *args, **kwargs)
        end_time = time.time()
        print(f"Method {func.__name__} took {end_time - start_time:.4f} seconds")
        return result
    return wrapper

def validate_input(func):
    """Decorator to validate input data"""
    def wrapper(self, *args, **kwargs):
        if args and not args[0]:
            raise ValueError("Input cannot be empty")
        return func(self, *args, **kwargs)
    return wrapper

class AIModelBase(ABC):
    """
    Abstract base class demonstrating:
    - Encapsulation: Private attributes with getter/setter methods
    - Polymorphism: Abstract methods that must be implemented by subclasses
    """
    
    def __init__(self, model_name: str, category: str):
        self._model_name = model_name  # Encapsulated private attribute
        self._category = category      # Encapsulated private attribute
        self._is_loaded = False       # Encapsulated private attribute
        self._model = None           # Encapsulated private attribute
    
    # Encapsulation: Getter methods
    @property
    def model_name(self) -> str:
        return self._model_name
    
    @property
    def category(self) -> str:
        return self._category
    
    @property
    def is_loaded(self) -> bool:
        return self._is_loaded
    
    # Encapsulation: Setter methods with validation
    @model_name.setter
    def model_name(self, value: str):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Model name must be a non-empty string")
        self._model_name = value
    
    @abstractmethod
    def load_model(self) -> None:
        """Abstract method - must be implemented by subclasses (Polymorphism)"""
        pass
    
    @abstractmethod
    def process_input(self, input_data: Any) -> Any:
        """Abstract method - must be implemented by subclasses (Polymorphism)"""
        pass
    
    @performance_monitor
    def get_model_info(self) -> Dict[str, str]:
        """Method that can be overridden by subclasses (Method Overriding)"""
        return {
            "name": self._model_name,
            "category": self._category,
            "status": "Loaded" if self._is_loaded else "Not Loaded"
        }

class TextProcessorMixin:
    """
    Mixin class demonstrating Multiple Inheritance
    Provides text processing capabilities
    """
    
    def clean_text(self, text: str) -> str:
        """Clean and preprocess text"""
        if not isinstance(text, str):
            return str(text)
        return text.strip().replace('\n', ' ').replace('\t', ' ')
    
    def validate_text_length(self, text: str, max_length: int = 1000) -> bool:
        """Validate text length"""
        return len(text) <= max_length

class ImageProcessorMixin:
    """
    Mixin class demonstrating Multiple Inheritance
    Provides image processing capabilities
    """
    
    def validate_image_format(self, image_path: str) -> bool:
        """Validate image format"""
        valid_formats = ['.jpg', '.jpeg', '.png', '.bmp', '.gif']
        return any(image_path.lower().endswith(fmt) for fmt in valid_formats)
    
    def get_image_info(self, image_path: str) -> Dict[str, Any]:
        """Get basic image information"""
        try:
            from PIL import Image
            with Image.open(image_path) as img:
                return {
                    "format": img.format,
                    "mode": img.mode,
                    "size": img.size
                }
        except Exception as e:
            return {"error": str(e)}
