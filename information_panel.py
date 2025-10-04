"""
Information panels for displaying model information and OOP explanations
"""

import tkinter as tk
from tkinter import ttk, scrolledtext
from gui_components import GUIComponentBase
from typing import Dict, Any

class InformationPanel(GUIComponentBase):
    """
    Information panel demonstrating Inheritance and displaying educational content
    """
    
    def __init__(self, parent):
        super().__init__(parent)
        self._notebook = None           # Encapsulated widget
        self._model_info_text = None    # Encapsulated widget
        self._oop_info_text = None      # Encapsulated widget
        self._setup_ui()
        self._populate_oop_explanation()
    
    def _setup_ui(self):
        """Private method to setup UI (Encapsulation)"""
        self.create_frame(padding="5", relief="solid", borderwidth=1)
        
        # Title
        title_label = ttk.Label(self._frame, text="Model Information & Explanation", 
                               font=('Arial', 10, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, sticky='w', pady=(0, 5))
        
        # Configure grid weights
        self._frame.grid_rowconfigure(1, weight=1)
        self._frame.grid_columnconfigure(0, weight=1)
        self._frame.grid_columnconfigure(1, weight=1)
        
        # Left side - Selected Model Info
        model_info_frame = ttk.Frame(self._frame, relief="solid", borderwidth=1)
        model_info_frame.grid(row=1, column=0, sticky='nsew', padx=(0, 2))
        model_info_frame.grid_rowconfigure(1, weight=1)
        model_info_frame.grid_columnconfigure(0, weight=1)
        
        ttk.Label(model_info_frame, text="Selected Model Info:", 
                 font=('Arial', 9, 'bold')).grid(row=0, column=0, sticky='w', padx=5, pady=2)
        
        self._model_info_text = tk.Text(
            model_info_frame, height=6, width=35, wrap=tk.WORD, font=('Arial', 8),
            bg='white', relief='flat', borderwidth=0
        )
        self._model_info_text.grid(row=1, column=0, sticky='nsew', padx=5, pady=2)
        
        # Right side - OOP Concepts Explanation
        oop_frame = ttk.Frame(self._frame, relief="solid", borderwidth=1)
        oop_frame.grid(row=1, column=1, sticky='nsew', padx=(2, 0))
        oop_frame.grid_rowconfigure(1, weight=1)
        oop_frame.grid_columnconfigure(0, weight=1)
        
        ttk.Label(oop_frame, text="OOP Concepts Explanation:", 
                 font=('Arial', 9, 'bold')).grid(row=0, column=0, sticky='w', padx=5, pady=2)
        
        self._oop_info_text = tk.Text(
            oop_frame, height=6, width=35, wrap=tk.WORD, font=('Arial', 8),
            bg='white', relief='flat', borderwidth=0
        )
        self._oop_info_text.grid(row=1, column=0, sticky='nsew', padx=5, pady=2)
    
    def _populate_oop_explanation(self):
        """Private method to populate OOP explanation (Encapsulation)"""
        oop_explanation = """
OOP CONCEPTS IMPLEMENTATION IN THIS APPLICATION

1. MULTIPLE INHERITANCE
   Where: TextClassificationModel and ImageClassificationModel classes
   Implementation: Both classes inherit from AIModelBase (abstract base class) and their respective Mixin classes
   
   Example:
   - TextClassificationModel inherits from AIModelBase + TextProcessorMixin
   - ImageClassificationModel inherits from AIModelBase + ImageProcessorMixin
   
   Why: This allows models to inherit core AI functionality from AIModelBase while gaining specialized 
   processing capabilities from Mixin classes, promoting code reuse and modularity.

2. MULTIPLE DECORATORS
   Where: @performance_monitor and @validate_input decorators
   Implementation: Applied to methods in AI model classes
   
   Examples:
   - @performance_monitor: Measures execution time of methods
   - @validate_input: Validates input data before processing
   
   Why: Decorators provide a clean way to add cross-cutting concerns (logging, validation, monitoring) 
   without modifying the core business logic, following the Single Responsibility Principle.

3. ENCAPSULATION
   Where: Throughout all classes using private attributes and property methods
   Implementation: Private attributes (prefixed with _) and public property methods
   
   Examples:
   - AIModelBase: _model_name, _category, _is_loaded (private attributes)
   - Property methods: model_name, category, is_loaded (controlled access)
   - GUI Components: _frame, _parent, _selected_model (private attributes)
   
   Why: Encapsulation hides internal implementation details and provides controlled access to object 
   state, ensuring data integrity and enabling easier maintenance.

4. POLYMORPHISM
   Where: AIModelBase abstract class and its implementations
   Implementation: Same interface (load_model, process_input) with different implementations
   
   Examples:
   - TextClassificationModel.process_input() handles text data
   - ImageClassificationModel.process_input() handles image data
   - Both can be used interchangeably through AIModelBase interface
   
   Why: Polymorphism allows different model types to be used through the same interface, making 
   the code more flexible and extensible.

5. METHOD OVERRIDING
   Where: Subclasses overriding parent class methods
   Implementation: Child classes provide specific implementations of parent methods
   
   Examples:
   - get_model_info() method overridden in both model classes
   - Abstract methods (load_model, process_input) implemented in subclasses
   - super() calls used to extend parent functionality
   
   Why: Method overriding allows subclasses to provide specialized behavior while maintaining 
   the same interface, enabling customization without breaking the contract.

ADDITIONAL OOP CONCEPTS:

6. ABSTRACTION
   Where: AIModelBase abstract class
   Implementation: Abstract methods that must be implemented by subclasses
   Why: Defines a contract that all AI models must follow, ensuring consistency.

7. COMPOSITION
   Where: GUI components containing other components
   Implementation: MainApplication contains multiple panel objects
   Why: Builds complex functionality by combining simpler components.

8. FACTORY PATTERN
   Where: ModelFactory class
   Implementation: Creates model instances based on type
   Why: Centralizes object creation and makes it easier to add new model types.

This application demonstrates practical use of OOP principles in a real-world scenario, 
showing how these concepts work together to create maintainable, extensible, and robust code.
        """
        
        # Match the exact format from the specifications
        short_explanation = """• Where Multiple Inheritance applied
• Why Encapsulation was applied
• How Polymorphism and Method Overriding are shown
• Where Multiple Decorators are applied"""
        
        self._oop_info_text.insert(tk.END, short_explanation.strip())
        self._oop_info_text.config(state='disabled')
    
    def update_model_info(self, model_info: Dict[str, Any]):
        """Public method to update model information (Encapsulation with controlled access)"""
        self._model_info_text.config(state='normal')
        self._model_info_text.delete(1.0, tk.END)
        
        # Format model information to match the image exactly
        formatted_info = "• Model Name\n• Category (Text, Vision, Audio)\n• Short Description"
        self._model_info_text.insert(tk.END, formatted_info)
        self._model_info_text.config(state='disabled')
    
    def _format_model_info(self, model_info: Dict[str, Any]) -> str:
        """Private method to format model information (Encapsulation)"""
        formatted = "• Model Name\n"
        formatted += f"  {model_info.get('name', 'N/A')}\n\n"
        
        formatted += "• Category (Text, Vision, Audio)\n"
        formatted += f"  {model_info.get('category', 'N/A')}\n\n"
        
        formatted += "• Short Description\n"
        formatted += f"  {model_info.get('description', 'N/A')}\n\n"
        
        formatted += "• Input Type\n"
        formatted += f"  {model_info.get('input_type', 'N/A')}\n\n"
        
        formatted += "• Output Type\n"
        formatted += f"  {model_info.get('output_type', 'N/A')}\n\n"
        
        formatted += "• Use Case\n"
        formatted += f"  {model_info.get('use_case', 'N/A')}"
        
        return formatted

class NotesPanel(GUIComponentBase):
    """
    Notes panel for additional information and references
    """
    
    def __init__(self, parent):
        super().__init__(parent)
        self._notes_text = None  # Encapsulated widget
        self._setup_ui()
        self._populate_notes()
    
    def _setup_ui(self):
        """Private method to setup UI (Encapsulation)"""
        self.create_frame(padding="2")
        
        # Notes text line
        content_label = ttk.Label(self._frame, text="Notes Extra notes, instructions, or references.", 
                               font=('Arial', 9))
        content_label.pack(anchor='w')
    
    def _populate_notes(self):
        """Private method to populate notes (Encapsulation)"""
        # Notes are now displayed in the title label, no separate text area needed
        pass
