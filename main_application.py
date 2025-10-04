"""
Main Application demonstrating comprehensive OOP concepts integration
"""

import tkinter as tk
from tkinter import ttk, messagebox
from gui_components import ModelSelectionPanel, InputPanel, OutputPanel
from information_panel import InformationPanel, NotesPanel
from ai_models import ModelFactory, AIModelBase
from typing import Dict, Any, Optional
import sys
import os

class MainApplication:
    """
    Main Application class demonstrating:
    - Composition (contains multiple GUI components)
    - Encapsulation (private methods and attributes)
    - Coordination between different components
    """
    
    def __init__(self):
        self._root = None                    # Encapsulated private attribute
        self._current_model = None           # Encapsulated private attribute
        self._model_selection_panel = None   # Encapsulated private attribute
        self._input_panel = None             # Encapsulated private attribute
        self._output_panel = None            # Encapsulated private attribute
        self._info_panel = None              # Encapsulated private attribute
        self._notes_panel = None             # Encapsulated private attribute
        self._setup_application()
    
    def _setup_application(self):
        """Private method to setup the main application (Encapsulation)"""
        self._create_main_window()
        self._create_menu()
        self._create_gui_components()
        self._arrange_layout()
    
    def _create_main_window(self):
        """Private method to create main window (Encapsulation)"""
        self._root = tk.Tk()
        self._root.title("Tkinter AI GUI")
        self._root.geometry("1000x700")
        self._root.minsize(900, 650)
        self._root.configure(bg='#f0f0f0')  # Light gray background
        
        # Configure grid weights for responsive design
        self._root.grid_rowconfigure(0, weight=1)
        self._root.grid_columnconfigure(0, weight=1)
        
        # Set application icon (if available)
        try:
            self._root.iconbitmap("icon.ico")
        except:
            pass  # Icon file not found, continue without it
    
    def _create_menu(self):
        """Private method to create application menu (Encapsulation)"""
        menubar = tk.Menu(self._root)
        self._root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Clear All", command=self._clear_all)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self._on_closing)
        
        # Models menu
        models_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Models", menu=models_menu)
        for model_type in ModelFactory.get_available_models():
            models_menu.add_command(
                label=f"Load {model_type}", 
                command=lambda mt=model_type: self._load_model_from_menu(mt)
            )
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self._show_about)
    
    def _create_gui_components(self):
        """Private method to create GUI components (Encapsulation)"""
        # Create main container
        main_container = ttk.Frame(self._root)
        main_container.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)
        main_container.grid_rowconfigure(1, weight=1)
        main_container.grid_columnconfigure(1, weight=1)
        
        # Create components with dependency injection
        self._model_selection_panel = ModelSelectionPanel(
            main_container, 
            on_model_change=self._on_model_type_selected
        )
        
        self._input_panel = InputPanel(main_container)
        self._output_panel = OutputPanel(main_container)
        self._info_panel = InformationPanel(main_container)
        self._notes_panel = NotesPanel(main_container)
        
        # Store reference to self in panels for callback access
        self._input_panel._parent = self
        self._model_selection_panel._parent = self
    
    def _arrange_layout(self):
        """Private method to arrange component layout (Encapsulation)"""
        # Configure main container grid weights
        main_container = self._model_selection_panel.frame.master
        main_container.grid_rowconfigure(0, weight=0)  # Model selection - fixed height
        main_container.grid_rowconfigure(1, weight=2)  # Input/Output - more space
        main_container.grid_rowconfigure(2, weight=1)  # Info section - less space but visible
        main_container.grid_rowconfigure(3, weight=0)  # Notes section - fixed height
        main_container.grid_columnconfigure(0, weight=1)
        main_container.grid_columnconfigure(1, weight=1)
        
        # Top row - Model selection
        self._model_selection_panel.frame.grid(
            row=0, column=0, columnspan=2, sticky='ew', pady=(0, 5)
        )
        
        # Middle row - Input and Output panels side by side
        self._input_panel.frame.grid(
            row=1, column=0, sticky='nsew', padx=(0, 2)
        )
        self._output_panel.frame.grid(
            row=1, column=1, sticky='nsew', padx=(2, 0)
        )
        
        # Bottom row - Information section (directly in main container)
        self._info_panel.frame.grid(
            row=2, column=0, columnspan=2, sticky='nsew', pady=(5, 0)
        )
        
        # Notes section at the very bottom
        self._notes_panel.frame.grid(
            row=3, column=0, columnspan=2, sticky='ew', pady=(2, 0)
        )
    
    def _on_model_type_selected(self, model_type: str):
        """Private callback for model type selection (Encapsulation)"""
        try:
            # Check if info panel is initialized
            if not hasattr(self, '_info_panel') or self._info_panel is None:
                return
            
            # Create model instance to get info (without loading)
            temp_model = ModelFactory.create_model(model_type)
            model_info = temp_model.get_model_info()
            self._info_panel.update_model_info(model_info)
        except Exception as e:
            print(f"Warning: Failed to get model info: {str(e)}")  # Use print instead of messagebox during initialization
    
    def _on_model_loaded(self, model: AIModelBase):
        """Private callback for successful model loading (Encapsulation)"""
        self._current_model = model
        model_info = model.get_model_info()
        self._info_panel.update_model_info(model_info)
    
    def _process_with_model(self, input_data: Dict[str, Any], model_number: int):
        """Private method to process input with loaded model (Encapsulation)"""
        if not self._current_model:
            messagebox.showwarning("Warning", "Please load a model first")
            return
        
        if not self._current_model.is_loaded:
            messagebox.showwarning("Warning", "Model is not loaded")
            return
        
        try:
            # Validate input type matches model capability
            if not self._validate_input_compatibility(input_data):
                return
            
            # Process input
            if input_data["type"] == "text":
                result = self._current_model.process_input(input_data["data"])
            elif input_data["type"] == "image":
                result = self._current_model.process_input(input_data["data"])
            else:
                messagebox.showerror("Error", "Unsupported input type")
                return
            
            # Display result
            output_with_metadata = {
                "model_number": model_number,
                "input_type": input_data["type"],
                "model_name": self._current_model.model_name,
                "result": result
            }
            
            self._output_panel.display_output(output_with_metadata)
            
        except Exception as e:
            error_output = {
                "error": str(e),
                "model_name": self._current_model.model_name if self._current_model else "Unknown"
            }
            self._output_panel.display_output(error_output)
    
    def _validate_input_compatibility(self, input_data: Dict[str, Any]) -> bool:
        """Private method to validate input compatibility (Encapsulation)"""
        model_info = self._current_model.get_model_info()
        model_category = model_info.get("category", "").lower()
        
        # Check compatibility based on model category and input type
        if input_data["type"] == "text" and "text" not in model_category:
            messagebox.showerror("Error", "Current model doesn't support text input. Please select 'Text-to-Image' model.")
            return False
        elif input_data["type"] == "image" and "image" not in model_category:
            messagebox.showerror("Error", "Current model doesn't support image input. Please select 'Image Classification' model.")
            return False
        
        return True
    
    def _load_model_from_menu(self, model_type: str):
        """Private method to load model from menu (Encapsulation)"""
        # Update dropdown selection
        self._model_selection_panel._selected_model.set(model_type)
        self._model_selection_panel._load_model()
    
    def _clear_all(self):
        """Private method to clear all data (Encapsulation)"""
        self._output_panel.clear_output()
        self._input_panel._clear_input()
        messagebox.showinfo("Info", "All data cleared")
    
    def _show_about(self):
        """Private method to show about dialog (Encapsulation)"""
        about_text = """
Tkinter AI GUI - OOP Demonstration

This application demonstrates comprehensive Object-Oriented Programming concepts:
• Multiple Inheritance
• Multiple Decorators  
• Encapsulation
• Polymorphism
• Method Overriding

Features:
• Integration with Hugging Face AI models
• Text and Image processing capabilities
• Modern GUI with educational content
• Modular code organization

Developed for HIT137 Assignment 3
        """
        messagebox.showinfo("About", about_text.strip())
    
    def _on_closing(self):
        """Private method to handle application closing (Encapsulation)"""
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self._root.quit()
            self._root.destroy()
    
    def run(self):
        """Public method to run the application"""
        self._root.protocol("WM_DELETE_WINDOW", self._on_closing)
        self._root.mainloop()

def main():
    """Main function to start the application"""
    try:
        app = MainApplication()
        app.run()
    except Exception as e:
        print(f"Application error: {e}")
        messagebox.showerror("Critical Error", f"Application failed to start: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
