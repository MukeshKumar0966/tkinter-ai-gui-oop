"""
GUI Components demonstrating OOP concepts and Tkinter widgets
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from typing import Dict, Any, Callable
from ai_models import ModelFactory, AIModelBase
import threading
import json

class GUIComponentBase:
    """
    Base class for GUI components demonstrating Encapsulation
    """
    
    def __init__(self, parent, **kwargs):
        self._parent = parent  # Encapsulated private attribute
        self._frame = None     # Encapsulated private attribute
        self._configure_style()
    
    def _configure_style(self):
        """Private method for style configuration (Encapsulation)"""
        self._style = ttk.Style()
        self._style.theme_use('default')  # Clean default theme
        
        # Configure clean, minimalistic styles
        self._style.configure('TFrame', background='#f0f0f0')
        self._style.configure('TLabel', background='#f0f0f0', foreground='black')
        self._style.configure('TButton', background='white', foreground='black')
        self._style.configure('TCombobox', fieldbackground='white')
        self._style.configure('TRadiobutton', background='#f0f0f0', foreground='black')
    
    @property
    def frame(self):
        """Getter for frame (Encapsulation)"""
        return self._frame
    
    def create_frame(self, **kwargs):
        """Create the main frame for this component"""
        self._frame = ttk.Frame(self._parent, **kwargs)
        return self._frame

class ModelSelectionPanel(GUIComponentBase):
    """
    Model selection panel demonstrating Inheritance and Encapsulation
    """
    
    def __init__(self, parent, on_model_change: Callable = None):
        super().__init__(parent)
        self._on_model_change = on_model_change  # Encapsulated callback
        self._selected_model = tk.StringVar()    # Encapsulated variable
        self._load_button = None                 # Encapsulated widget
        self._model_dropdown = None              # Encapsulated widget
        self._setup_ui()
    
    def _setup_ui(self):
        """Private method to setup UI (Encapsulation)"""
        self.create_frame(padding="5")
        
        # Model selection label and dropdown in one row
        ttk.Label(self._frame, text="Model Selection:", 
                 font=('Arial', 10)).grid(row=0, column=0, sticky='w', padx=(0, 5))
        
        self._model_dropdown = ttk.Combobox(
            self._frame, 
            textvariable=self._selected_model,
            values=ModelFactory.get_available_models(),
            state="readonly",
            width=15
        )
        self._model_dropdown.grid(row=0, column=1, sticky='w', padx=(0, 10))
        self._model_dropdown.bind('<<ComboboxSelected>>', self._on_model_selected)
        
        # Load button
        self._load_button = ttk.Button(
            self._frame, 
            text="Load Model", 
            command=self._load_model,
            state='disabled'
        )
        self._load_button.grid(row=0, column=2, sticky='w')
        
        # Set first model as default (after creating the button)
        available_models = ModelFactory.get_available_models()
        if available_models:
            self._selected_model.set(available_models[0])
            self._load_button.config(state='normal')
            # Delay the callback to ensure all components are initialized
            if self._on_model_change:
                self._frame.after(100, lambda: self._on_model_change(available_models[0]))
    
    def _on_model_selected(self, event=None):
        """Private callback for model selection (Encapsulation)"""
        self._load_button.config(state='normal')
        if self._on_model_change:
            self._on_model_change(self._selected_model.get())
    
    def _load_model(self):
        """Private method to load selected model (Encapsulation)"""
        model_type = self._selected_model.get()
        if model_type:
            # Disable button during loading
            self._load_button.config(state='disabled', text='Loading...')
            
            # Load model in separate thread to prevent GUI freezing
            def load_thread():
                try:
                    model = ModelFactory.create_model(model_type)
                    model.load_model()
                    
                    # Update GUI in main thread using the root window
                    root = self._frame.winfo_toplevel()
                    root.after(0, lambda: self._on_load_complete(model))
                except Exception as e:
                    root = self._frame.winfo_toplevel()
                    root.after(0, lambda: self._on_load_error(str(e)))
            
            threading.Thread(target=load_thread, daemon=True).start()
    
    def _on_load_complete(self, model: AIModelBase):
        """Private callback for successful model loading (Encapsulation)"""
        self._load_button.config(state='normal', text='Load Model')
        messagebox.showinfo("Success", f"Model {model.model_name} loaded successfully!")
        
        # Notify parent about loaded model
        if hasattr(self._parent, '_on_model_loaded'):
            self._parent._on_model_loaded(model)
    
    def _on_load_error(self, error_msg: str):
        """Private callback for model loading error (Encapsulation)"""
        self._load_button.config(state='normal', text='Load Model')
        messagebox.showerror("Error", f"Failed to load model: {error_msg}")

class InputPanel(GUIComponentBase):
    """
    Input panel demonstrating Inheritance and Polymorphism
    """
    
    def __init__(self, parent):
        super().__init__(parent)
        self._input_type = tk.StringVar(value="Text")  # Encapsulated variable
        self._input_text = tk.StringVar()              # Encapsulated variable
        self._input_file_path = tk.StringVar()         # Encapsulated variable
        self._text_entry = None                        # Encapsulated widget
        self._file_frame = None                        # Encapsulated widget
        self._setup_ui()
    
    def _setup_ui(self):
        """Private method to setup UI (Encapsulation)"""
        self.create_frame(padding="5", relief="solid", borderwidth=1)
        
        # Title
        title_label = ttk.Label(self._frame, text="User Input Section", 
                               font=('Arial', 10, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, sticky='w', pady=(0, 5))
        
        # Input type selection
        input_frame = ttk.Frame(self._frame)
        input_frame.grid(row=1, column=0, columnspan=3, sticky='w', pady=(0, 5))
        
        ttk.Radiobutton(input_frame, text="Text", variable=self._input_type, 
                       value="Text", command=self._on_input_type_change).pack(side='left', padx=(0, 15))
        ttk.Radiobutton(input_frame, text="Image", variable=self._input_type, 
                       value="Image", command=self._on_input_type_change).pack(side='left')
        
        # Browse button (for image mode)
        ttk.Button(input_frame, text="Browse", 
                  command=self._browse_file).pack(side='left', padx=(15, 0))
        
        # Text input area
        self._text_entry = tk.Text(self._frame, height=8, width=40, 
                                  bg='white', relief='solid', borderwidth=1)
        self._text_entry.grid(row=2, column=0, columnspan=3, sticky='ew', pady=(0, 5))
        
        # File input area (initially hidden)
        self._file_frame = ttk.Frame(self._frame)
        
        ttk.Label(self._file_frame, text="Selected file:").pack(side='left', padx=(0, 5))
        ttk.Label(self._file_frame, textvariable=self._input_file_path, 
                 foreground='blue').pack(side='left', padx=(0, 10))
        
        # Process buttons
        button_frame = ttk.Frame(self._frame)
        button_frame.grid(row=4, column=0, columnspan=3, pady=(5, 0))
        
        ttk.Button(button_frame, text="Run Model 1", 
                  command=lambda: self._process_input(1)).pack(side='left', padx=(0, 5))
        ttk.Button(button_frame, text="Run Model 2", 
                  command=lambda: self._process_input(2)).pack(side='left', padx=(0, 5))
        ttk.Button(button_frame, text="Cl", 
                  command=self._clear_input).pack(side='left')
    
    def _on_input_type_change(self):
        """Private method handling input type change (Encapsulation)"""
        if self._input_type.get() == "Text":
            self._text_entry.grid(row=2, column=0, columnspan=3, sticky='ew', pady=(0, 10))
            self._file_frame.grid_remove()
        else:
            self._text_entry.grid_remove()
            self._file_frame.grid(row=2, column=0, columnspan=3, sticky='w', pady=(0, 10))
    
    def _browse_file(self):
        """Private method for file browsing (Encapsulation)"""
        filetypes = [
            ("Image files", "*.jpg *.jpeg *.png *.bmp *.gif"),
            ("All files", "*.*")
        ]
        filename = filedialog.askopenfilename(filetypes=filetypes)
        if filename:
            self._input_file_path.set(filename)
    
    def _process_input(self, model_number: int):
        """Private method to process input (Encapsulation)"""
        if hasattr(self._parent, '_process_with_model'):
            input_data = self._get_input_data()
            if input_data:
                self._parent._process_with_model(input_data, model_number)
    
    def _get_input_data(self) -> Dict[str, Any]:
        """Private method to get current input data (Encapsulation)"""
        if self._input_type.get() == "Text":
            text = self._text_entry.get(1.0, tk.END).strip()
            if not text:
                messagebox.showwarning("Warning", "Please enter some text")
                return None
            return {"type": "text", "data": text}
        else:
            file_path = self._input_file_path.get()
            if not file_path:
                messagebox.showwarning("Warning", "Please select an image file")
                return None
            return {"type": "image", "data": file_path}
    
    def _clear_input(self):
        """Private method to clear input (Encapsulation)"""
        self._text_entry.delete(1.0, tk.END)
        self._input_file_path.set("")

class OutputPanel(GUIComponentBase):
    """
    Output panel demonstrating Inheritance
    """
    
    def __init__(self, parent):
        super().__init__(parent)
        self._output_text = None  # Encapsulated widget
        self._setup_ui()
    
    def _setup_ui(self):
        """Private method to setup UI (Encapsulation)"""
        self.create_frame(padding="5", relief="solid", borderwidth=1)
        
        # Title
        title_label = ttk.Label(self._frame, text="Model Output Section", 
                               font=('Arial', 10, 'bold'))
        title_label.grid(row=0, column=0, sticky='w', pady=(0, 5))
        
        # Output display
        ttk.Label(self._frame, text="Output Display:").grid(row=1, column=0, sticky='w', pady=(0, 5))
        
        self._output_text = tk.Text(self._frame, height=12, width=50, 
                                   bg='white', relief='solid', borderwidth=1,
                                   state='disabled')
        self._output_text.grid(row=2, column=0, sticky='nsew')
        
        # Configure grid weights
        self._frame.grid_rowconfigure(2, weight=1)
        self._frame.grid_columnconfigure(0, weight=1)
    
    def display_output(self, output_data: Dict[str, Any]):
        """Public method to display output (Encapsulation with controlled access)"""
        self._output_text.config(state='normal')
        self._output_text.delete(1.0, tk.END)
        
        # Format output nicely
        formatted_output = json.dumps(output_data, indent=2, ensure_ascii=False)
        self._output_text.insert(tk.END, formatted_output)
        
        self._output_text.config(state='disabled')
    
    def clear_output(self):
        """Public method to clear output (Encapsulation with controlled access)"""
        self._output_text.config(state='normal')
        self._output_text.delete(1.0, tk.END)
        self._output_text.config(state='disabled')
