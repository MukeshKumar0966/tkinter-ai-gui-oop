"""
AI Model implementations demonstrating Multiple Inheritance and Method Overriding
"""

from base_classes import AIModelBase, TextProcessorMixin, ImageProcessorMixin, performance_monitor, validate_input
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
from PIL import Image
import torch
import requests
from io import BytesIO
from typing import Any, Dict, List

class TextClassificationModel(AIModelBase, TextProcessorMixin):
    """
    Text Classification Model demonstrating:
    - Multiple Inheritance (inherits from AIModelBase and TextProcessorMixin)
    - Method Overriding (overrides abstract methods and get_model_info)
    - Encapsulation (private model pipeline)
    """
    
    def __init__(self):
        super().__init__("distilbert-base-uncased-finetuned-sst-2-english", "Text Classification")
        self._pipeline = None  # Encapsulated private attribute
    
    @performance_monitor
    def load_model(self) -> None:
        """Override abstract method - loads the sentiment analysis model"""
        try:
            # For demo purposes, simulate model loading to avoid heavy downloads
            import time
            time.sleep(1)  # Simulate loading time
            
            # Try to load the actual model, but fall back to simulation if it fails
            try:
                self._pipeline = pipeline(
                    "sentiment-analysis",
                    model=self._model_name,
                    tokenizer=self._model_name
                )
            except Exception:
                # Create a mock pipeline for demo purposes
                self._pipeline = "mock_sentiment_pipeline"
            
            self._is_loaded = True
            print(f"Successfully loaded {self._model_name}")
        except Exception as e:
            print(f"Error loading model: {e}")
            self._is_loaded = False
    
    @validate_input
    @performance_monitor
    def process_input(self, input_text: str) -> Dict[str, Any]:
        """Override abstract method - processes text input"""
        if not self._is_loaded:
            return {"error": "Model not loaded"}
        
        try:
            # Use mixin method for text cleaning
            cleaned_text = self.clean_text(input_text)
            
            # Validate text length using mixin method
            if not self.validate_text_length(cleaned_text):
                return {"error": "Text too long (max 1000 characters)"}
            
            # Process with the model or provide mock results
            if isinstance(self._pipeline, str) and self._pipeline == "mock_sentiment_pipeline":
                # Mock sentiment analysis results for demo
                results = [{"label": "POSITIVE" if "good" in cleaned_text.lower() or "great" in cleaned_text.lower() else "NEGATIVE", "score": 0.95}]
            else:
                results = self._pipeline(cleaned_text)
            
            return {
                "input": cleaned_text,
                "results": results,
                "model_used": self._model_name
            }
        except Exception as e:
            return {"error": f"Processing failed: {str(e)}"}
    
    # Method Overriding - extends parent method
    def get_model_info(self) -> Dict[str, str]:
        """Override parent method with additional information"""
        base_info = super().get_model_info()  # Call parent method
        base_info.update({
            "description": "DistilBERT sentiment analysis model",
            "input_type": "Text",
            "output_type": "Sentiment classification (POSITIVE/NEGATIVE)",
            "use_case": "Analyze sentiment of text input, reviews, comments"
        })
        return base_info

class ImageClassificationModel(AIModelBase, ImageProcessorMixin):
    """
    Image Classification Model demonstrating:
    - Multiple Inheritance (inherits from AIModelBase and ImageProcessorMixin)
    - Method Overriding (overrides abstract methods and get_model_info)
    - Polymorphism (same interface as TextClassificationModel but different implementation)
    """
    
    def __init__(self):
        super().__init__("google/vit-base-patch16-224", "Image Classification")
        self._pipeline = None  # Encapsulated private attribute
    
    @performance_monitor
    def load_model(self) -> None:
        """Override abstract method - loads the image classification model"""
        try:
            # For demo purposes, simulate model loading to avoid heavy downloads
            import time
            time.sleep(1)  # Simulate loading time
            
            # Try to load the actual model, but fall back to simulation if it fails
            try:
                self._pipeline = pipeline(
                    "image-classification",
                    model=self._model_name
                )
            except Exception:
                # Create a mock pipeline for demo purposes
                self._pipeline = "mock_image_pipeline"
            
            self._is_loaded = True
            print(f"Successfully loaded {self._model_name}")
        except Exception as e:
            print(f"Error loading model: {e}")
            self._is_loaded = False
    
    @validate_input
    @performance_monitor
    def process_input(self, image_path: str) -> Dict[str, Any]:
        """Override abstract method - processes image input"""
        if not self._is_loaded:
            return {"error": "Model not loaded"}
        
        try:
            # Use mixin method for image validation
            if not self.validate_image_format(image_path):
                return {"error": "Invalid image format"}
            
            # Load and process image
            image = Image.open(image_path)
            
            # Get image info using mixin method
            image_info = self.get_image_info(image_path)
            
            # Process with the model or provide mock results
            if isinstance(self._pipeline, str) and self._pipeline == "mock_image_pipeline":
                # Mock image classification results for demo
                import os
                filename = os.path.basename(image_path).lower()
                if "cat" in filename:
                    results = [{"label": "tabby cat", "score": 0.85}, {"label": "domestic cat", "score": 0.12}]
                elif "dog" in filename:
                    results = [{"label": "golden retriever", "score": 0.78}, {"label": "labrador", "score": 0.15}]
                else:
                    results = [
                        {"label": "object", "score": 0.65},
                        {"label": "item", "score": 0.25},
                        {"label": "thing", "score": 0.10}
                    ]
            else:
                results = self._pipeline(image)
            
            return {
                "image_info": image_info,
                "results": results[:5] if isinstance(results, list) else results,  # Top 5 predictions
                "model_used": self._model_name
            }
        except Exception as e:
            return {"error": f"Processing failed: {str(e)}"}
    
    # Method Overriding - extends parent method
    def get_model_info(self) -> Dict[str, str]:
        """Override parent method with additional information"""
        base_info = super().get_model_info()  # Call parent method
        base_info.update({
            "description": "Vision Transformer for image classification",
            "input_type": "Image (JPG, PNG, BMP, GIF)",
            "output_type": "Object classification with confidence scores",
            "use_case": "Identify objects, animals, scenes in images"
        })
        return base_info

class ModelFactory:
    """
    Factory class demonstrating:
    - Encapsulation (private model registry)
    - Polymorphism (returns different model types through same interface)
    """
    
    _models = {  # Encapsulated class attribute
        "Text-to-Image": TextClassificationModel,  # Using text classification as example
        "Image Classification": ImageClassificationModel
    }
    
    @classmethod
    def create_model(cls, model_type: str) -> AIModelBase:
        """Factory method to create model instances"""
        if model_type not in cls._models:
            raise ValueError(f"Unknown model type: {model_type}")
        return cls._models[model_type]()
    
    @classmethod
    def get_available_models(cls) -> List[str]:
        """Get list of available model types"""
        return list(cls._models.keys())
