import pandas as pd
import os
import io
from uuid import uuid4
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import ttkthemes
from PIL import Image, ImageTk
import base64

# Button icons in base64 format
ICONS = {
    'browse': 'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAAOxAAADsQBlSsOGwAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYXBlLm9yZ5vuPBoAAADzSURBVDiNpdMxS0JRGMbx/70XvYgfIBoiGhwaHCJoClrCj9AH6gu0tLu4NLREtDg4uToIgRB9AhehIQmiQcWhC3V1TO5V7z3nvA3nPc/v/M/7vkdhYqhggxTv2McN3vAXJ8YBznGEV2Q4xW2eOMUGVkM9wid6uEAfG3jBCc7whq2QBjlXGZ7xkJ+vI8VtaDRWGQBb6OAKx9jEHQZh0Q0S3OMSbfQxDOdiLMznVpIQ6WAXzxiF4EmccxznVmxk4QU3+Ik4PZ//ZioYF31xgkmRZBYK72Aa5m/TZeAlJGNcDAr//TfwuvBcAE5wj8+ZF/4DdiJ2tKPPwD4AAAAASUVORK5CYII=',
    'process': 'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAAOxAAADsQBlSsOGwAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYXBlLm9yZ5vuPBoAAAE1SURBVDiNpdO/S1ZhFMfx13tuN7QhCHFIbGkQEYeG/gFNbuLkEm1NEQ0KQUtDEEFDY4vo4OQfIDgJQkOIEIhLi0NDYBAIWkhD1xO9vee5D5zlfM73+z3nOed7TF3YwCu8xD1cS7xc4BtGeEg8hT6+4gUe4yOmqQEXWMJ7vMUhxrmLV9jHDg7wAuNE7OFz3E18C83kdvH9cmKc2IsbIc0dd7CS54Z4F7RZiX8r1QBDfMNNvMfvgNaHC433EtqPoJ9UT5C9Rf8aEEi4SwKOUr0nQUcZqQRm2E6xjN0Eu4u9RewkPMN2YAuJrWEtUs3wOGgrmOE0xXFcGmEe73M0gi3jQ14+xE/0gjUquEGiO/iEX7iVxG5iO7mTGUYoqpL8zQ/mOIl5owpewEZZPsCntrH/QTcF/gACXU5QfTivngAAAABJRU5ErkJggg==',
    'save': 'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAAOxAAADsQBlSsOGwAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYXBlLm9yZ5vuPBoAAADTSURBVDiNpdMxSkNBEMbx346PgJVYiI0HTxDsvIJ38ApWXkG8goV4AA8g2FjYiZVYpEgXxEIteot9hWGzb/Nh2WVmf99/Z3ZWUYxwjzd8YIp97PW5UyzxiVes93yBGywwxyPOcYgzPGCGd5wUJW7iE3fYam0OcIsF7rDdcQ/CXOIBBxVucFWkmuA4zDdY7WK1AozxHKP7OMJOAcY4wjAgnzjrQqkDHOO2Y3YKUOMrB6hgaowKjBpwDVNjjPdoGaY+6hLXeG7+wl+s8YTJX+z9kRqPXiLkDQ6UAAAAAElFTkSuQmCC',
    'clear': 'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAAOxAAADsQBlSsOGwAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYXBlLm9yZ5vuPBoAAADVSURBVDiNpdOxSgNBFIXh7yaIYGORKsYmta0vYCNoayPY+yaWvoKdT2AhmEKwsxOfwE4stLFJQBEEC8HGbHP3WuwKy7Kb3fXANPfO+WbmzgyFGGEPa9jAbaKv4wlneEe3cDWe8IoPXGAXU3xjHLpzrCfiFe7RySO4xD3O0UxEP0M7kJ+hG7EGPvGCJRR4wBo2sYL94LYSHV14oX6CfYINLKIfxSksJ7j03dNruEUbTxjgFqMkwSJ+sI2tEL5iBacYxoE6KDGOvWpL7v5VhP8q/wRwgxu8zfzwL34BlzxnVUr8KXIAAAAASUVORK5CYII=',
    'help': 'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAAOxAAADsQBlSsOGwAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYXBlLm9yZ5vuPBoAAAFKSURBVDiNldM9S1xBGIbh65yjIQREiCAWFhYWQbC0sBPyC/IDLAQrEStJZyH4C9JZip2lRZpUgpXYWPgDJKRJrAykSEBFjR5z9mRmdyYWZ4/r7ooHppnhfe6Z932fsalJC7/Qxhw+Rxb4hn7ksI1ZXKKLS4zH93ks4ARPeIffOMcGPkQGphN4DTeRtYQJfMQXfEcdy5hHDSdYxQgW8BOjyf/9FA00MYsdfEIVs5jCHs5iS7exgWV8wAU2sY4DtDCMkf+0XQA13CYmH2Mh3t/gCsdx/RN3yXx+4i0eYhvVgVc5wVLK+DWcJtdpnOECb1KkPOE9PmMe99hDJ1GXcJRYr2MvJXiJwUFBCa9QwS6uU+oU3qGJFr4m3x5wEO9f4z7+XklcXyTFCvayL3lSWcBqIkr0R2wnBtLB+7y9fvcMhB7uccCfBQbYP6cnPp3X7Xi7AAAAAElFTkSuQmCC'
}

class Toast:
    """Toast notification widget"""
    def __init__(self, master, message, type_='info'):
        self.master = master
        
        # Configure colors based on type
        colors = {
            'success': ('#107C10', '#E6F4E6'),  # Green
            'error': ('#E81123', '#FDE7E9'),    # Red
            'info': ('#0078D4', '#E5F1FB'),     # Blue
            'warning': ('#FFB900', '#FFF8E6')   # Orange
        }
        
        # Create toast window
        self.window = tk.Toplevel(master)
        self.window.overrideredirect(True)
        self.window.attributes('-topmost', True)
        
        # Calculate position (bottom right of main window)
        master_x = master.winfo_x()
        master_y = master.winfo_y()
        master_width = master.winfo_width()
        
        # Create and pack the message label
        self.frame = ttk.Frame(self.window, style='Toast.TFrame')
        self.frame.pack(expand=True, fill='both')
        
        # Configure toast frame style
        style = ttk.Style()
        style.configure('Toast.TFrame', background=colors[type_][1])
        style.configure('Toast.TLabel',
                       background=colors[type_][1],
                       foreground=colors[type_][0],
                       font=('Segoe UI', 9))
        
        self.label = ttk.Label(self.frame, text=message, style='Toast.TLabel', padding=(15, 10))
        self.label.pack(expand=True, fill='both')
        
        # Position the window
        self.window.update_idletasks()
        window_width = self.window.winfo_width()
        window_height = self.window.winfo_height()
        
        x = master_x + master_width - window_width - 20
        y = master_y + master.winfo_height() - window_height - 40
        
        self.window.geometry(f'+{x}+{y}')
        
        # Schedule destruction
        self.window.after(3000, self.destroy)
        
        # Add fade effect
        self.window.attributes('-alpha', 0.0)
        self.fade_in()
    
    def fade_in(self):
        """Fade in animation"""
        alpha = self.window.attributes('-alpha')
        if alpha < 1.0:
            alpha += 0.1
            self.window.attributes('-alpha', alpha)
            self.window.after(20, self.fade_in)
        else:
            self.window.after(2000, self.fade_out)
    
    def fade_out(self):
        """Fade out animation"""
        alpha = self.window.attributes('-alpha')
        if alpha > 0.0:
            alpha -= 0.1
            self.window.attributes('-alpha', alpha)
            self.window.after(20, self.fade_out)
        else:
            self.destroy()
    
    def destroy(self):
        """Destroy the toast window"""
        self.window.destroy()

class ButtonWithIcon(tk.Button):
    """Custom button class that supports icons"""
    def __init__(self, master, text, icon_data=None, **kwargs):
        style = kwargs.pop('style', 'Primary.TButton')
        if 'compound' not in kwargs:
            kwargs['compound'] = 'left'
            
        # Set colors based on style
        if style == 'Primary.TButton':
            bg = '#0078D4'  # Windows blue
        elif style == 'Success.TButton':
            bg = '#107C10'  # Windows green
        else:
            bg = '#0078D4'  # Default to blue
            
        kwargs.update({
            'background': bg,
            'foreground': 'white',
            'activebackground': bg,
            'activeforeground': 'white',
            'relief': 'raised',
            'font': ('Segoe UI', 9),
            'padx': 10,
            'pady': 4,
            'border': 1
        })
        
        super().__init__(master, text=text, **kwargs)
        
        if icon_data:
            try:
                # Decode and create the icon image
                icon_data = base64.b64decode(icon_data)
                icon = Image.open(io.BytesIO(icon_data))
                # Scale icon based on text size
                font = kwargs.get('font', ('Segoe UI', 9))
                if isinstance(font, str):
                    size = 16
                else:
                    size = max(16, int(font[1] * 1.5))
                icon = icon.resize((size, size), Image.LANCZOS)
                self.icon = ImageTk.PhotoImage(icon)
                self.configure(image=self.icon)
                
                # Add some padding between icon and text
                current_padding = self.cget('padding')
                if isinstance(current_padding, str):
                    padding = tuple(map(int, current_padding.split()))
                else:
                    padding = current_padding if current_padding else (0, 0, 0, 0)
                self.configure(padding=(padding[0] + 5, padding[1], padding[2], padding[3]))
            except Exception as e:
                print(f"Warning: Could not load icon: {e}")
                self.icon = None

class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None
        self.widget.bind('<Enter>', self.enter)
        self.widget.bind('<Leave>', self.leave)

    def enter(self, event=None):
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25
        
        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")
        
        style = ttk.Style()
        style.configure('ToolTip.TLabel',
                       background='#FFFFEA',
                       foreground='#000000',
                       font=('Segoe UI', 9))
        
        label = ttk.Label(self.tooltip, text=self.text, style='ToolTip.TLabel',
                         padding=(5, 3), relief='solid', borderwidth=1)
        label.pack()

    def leave(self, event=None):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None

class LoadingSpinner:
    """Loading spinner widget"""
    def __init__(self, master, size=20, width=3, color='#0078D4'):
        self.master = master
        self.size = size
        self.canvas = tk.Canvas(master, width=size, height=size, 
                              bg=master.cget('bg'), highlightthickness=0)
        self.angle = 0
        self.width = width
        self.color = color
        self._job = None
    
    def start(self):
        """Start the loading spinner animation"""
        def spin():
            self.angle = (self.angle + 10) % 360
            self.canvas.delete("spinner")
            start = self.angle
            extent = min(360 - start, 100)  # Arc length
            self.canvas.create_arc(self.width, self.width, 
                                 self.size - self.width, self.size - self.width,
                                 start=start, extent=extent,
                                 outline=self.color, width=self.width,
                                 style="arc", tags="spinner")
            self._job = self.canvas.after(20, spin)
        spin()
        return self.canvas
    
    def stop(self):
        """Stop the loading spinner animation"""
        if self._job is not None:
            self.canvas.after_cancel(self._job)
            self._job = None
            self.canvas.delete("spinner")
    
    def pack(self, **kwargs):
        """Pack the spinner canvas"""
        self.canvas.pack(**kwargs)
    
    def grid(self, **kwargs):
        """Grid the spinner canvas"""
        self.canvas.grid(**kwargs)
    
    def place(self, **kwargs):
        """Place the spinner canvas"""
        self.canvas.place(**kwargs)

class DataCleanerGUI:
    def __init__(self, root):
        """
        Initializes the DataCleanerGUI application.
        Sets up the main window, applies a theme, and initializes file path variables.
        """
        self.root = root
        self.root.title("SSS Data File Cleaner")
        self.root.geometry("1000x700")
        self.root.resizable(True, True)

        # Apply a modern theme using ttkthemes
        self.style = ttkthemes.ThemedStyle(self.root)
        self.style.set_theme("vista")  # Using vista theme for better Windows compatibility
        
        # Override button style to ensure background colors are visible
        self.style.configure('TButton', background=None)  # This is important for button colors to work

        # Custom color scheme for Windows
        self.colors = {
            'primary': '#0078D4',      # Windows blue
            'secondary': '#FFB900',    # Windows gold
            'success': '#107C10',      # Windows green
            'warning': '#FF8C00',      # Windows orange
            'error': '#E81123',        # Windows red
            'background': '#F9F9F9',   # Light background
            'surface': "#FFFFFF",      # White
            'text': '#000000',         # Black
            'text_secondary': '#666666' # Gray
        }

        # Configure custom styles
        self._configure_styles()        # File paths
        self.raw_file_path = tk.StringVar()
        self.upload_file_path = tk.StringVar()
        self.status_var = tk.StringVar(value="Ready")
        
        # Add loading spinner instance
        self.loading_spinner = None

        self._create_widgets()
        self._create_tooltips()
        self._create_keyboard_shortcuts()

    def _configure_styles(self):
        """Configure custom styles for widgets"""
        # Frame styles
        self.style.configure('Main.TFrame', 
                            background=self.colors['background'])
        self.style.configure('Card.TFrame', 
                            background=self.colors['surface'])        # Button styles
        self.style.configure('Primary.TButton', 
                           font=('Segoe UI', 9),
                           padding=(10, 4))

        self.style.map('Primary.TButton',
                      foreground=[('disabled', 'grey'),
                                ('!disabled', 'white')],
                      background=[('disabled', '#cccccc'),
                                ('!disabled', self.colors['primary'])],
                      relief=[('disabled', 'flat'),
                            ('!disabled', 'raised')])
                            
        self.style.configure('Success.TButton',
                           font=('Segoe UI', 9),
                           padding=(10, 4))
        
        self.style.map('Success.TButton',
                      foreground=[('disabled', 'grey'),
                                ('!disabled', 'white')],
                      background=[('disabled', "#cccccc"),
                                ('!disabled', self.colors['success'])],
                      relief=[('disabled', 'flat'),
                            ('!disabled', 'raised')])

        # Small button style
        self.style.configure('Small.Primary.TButton',
                            font=('Segoe UI', 9),
                            padding=(8, 2))

        # Label styles with Windows-specific fonts
        self.style.configure('Header.TLabel',
                            font=('Segoe UI Semibold', 16),
                            background=self.colors['background'],
                            foreground=self.colors['text'])

        self.style.configure('SubHeader.TLabel',
                            font=('Segoe UI', 11),
                            background=self.colors['background'],
                            foreground=self.colors['text_secondary'])

        self.style.configure('Card.TLabel',
                            font=('Segoe UI', 9),
                            background=self.colors['surface'],
                            foreground=self.colors['text'])

        # Configure entry style
        self.style.configure('TEntry',
                            fieldbackground=self.colors['surface'],
                            borderwidth=1,
                            relief='solid',
                            font=('Segoe UI', 9))

    def _create_keyboard_shortcuts(self):
        """Set up keyboard shortcuts"""
        self.root.bind('<Control-o>', lambda e: self._browse_raw_file())
        self.root.bind('<Control-u>', lambda e: self._browse_upload_file())
        self.root.bind('<Control-p>', lambda e: self._process_files())
        self.root.bind('<Control-s>', lambda e: self._save_log())
        self.root.bind('<F1>', lambda e: self._show_help())
        self.root.bind('<Control-f>', lambda e: self.filter_entry.focus())

    def _create_tooltips(self):
        """Create tooltips for widgets with keyboard shortcuts"""
        ToolTip(self.raw_file_entry, "Select the SSS Final File from the previous month\nKeyboard shortcut: Ctrl+O")
        ToolTip(self.upload_file_entry, "Select the SSS Upload File for the current month\nKeyboard shortcut: Ctrl+U")

        ToolTip(self.process_btn, "Start the validation and cleaning process\nKeyboard shortcut: Ctrl+P")
        ToolTip(self.save_log_btn, "Save the processing results to a log file\nKeyboard shortcut: Ctrl+S")
        ToolTip(self.raw_browse_btn, "Browse for the SSS Final File\nKeyboard shortcut: Ctrl+O")
        ToolTip(self.upload_browse_btn, "Browse for the SSS Upload File\nKeyboard shortcut: Ctrl+U")
        # Add tooltip for filter entry
        if hasattr(self, 'filter_entry'):
            ToolTip(self.filter_entry, "Filter the results by text\nKeyboard shortcut: Ctrl+F")

    def _show_help(self):
        """Show help dialog with keyboard shortcuts and usage instructions"""
        help_text = """
SSS Data File Cleaner Help

Keyboard Shortcuts:
• Ctrl+O: Open Raw File
• Ctrl+U: Open Upload File
• Ctrl+P: Process Files
• Ctrl+S: Save Log
• F1: Show This Help

Usage Instructions:
1. Select the SSS Final File from the previous month
2. Select the SSS Upload File for the current month
3. Click 'Validate & Clean' to process the files
4. Review the results in the output area
5. Save the log if needed

Note: Large files may take longer to process.
        """
        messagebox.showinfo("Help", help_text)

    def _create_widgets(self):
        """
        Creates and arranges all GUI widgets with modern styling.
        """
        # Main container
        main_frame = ttk.Frame(self.root, style='Main.TFrame', padding="20")
        main_frame.grid(row=0, column=0, sticky='nsew')
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # Header with icon
        header_frame = ttk.Frame(main_frame, style='Main.TFrame')
        header_frame.grid(row=0, column=0, columnspan=3, sticky='ew', pady=(0, 20))
        
        # App title and description
        title_frame = ttk.Frame(header_frame, style='Main.TFrame')
        title_frame.pack(side='left')
        ttk.Label(title_frame, text="SSS Data File Cleaner", style='Header.TLabel').pack(anchor='w')
        ttk.Label(title_frame, text="Clean and validate SSS data files efficiently", 
                 style='SubHeader.TLabel').pack(anchor='w')        # Help button in header
        help_btn = ButtonWithIcon(header_frame, text=" Help", 
                              icon_data=ICONS['help'],
                              style='Primary.TButton',
                              command=self._show_help)
        help_btn.pack(side='right', padx=10)

        # File selection card
        file_card = ttk.Frame(main_frame, style='Card.TFrame', padding="15")
        file_card.grid(row=1, column=0, columnspan=3, sticky='ew', pady=(0, 20))        # Raw file selection
        ttk.Label(file_card, text="SSS Final File (Previous Month):", style='Card.TLabel').grid(row=0, column=0, sticky='w', pady=5)
        self.raw_file_entry = ttk.Entry(file_card, textvariable=self.raw_file_path, width=70)
        self.raw_file_entry.grid(row=0, column=1, padx=5, sticky='ew')
        self.raw_browse_btn = ButtonWithIcon(file_card, text=" Browse", 
                                        icon_data=ICONS['browse'],
                                        command=self._browse_raw_file,
                                        width=10)
        self.raw_browse_btn.grid(row=0, column=2, padx=5)

        # Upload file selection
        ttk.Label(file_card, text="SSS Upload File (Current Month):", style='Card.TLabel').grid(row=1, column=0, sticky='w', pady=5)
        self.upload_file_entry = ttk.Entry(file_card, textvariable=self.upload_file_path, width=70)
        self.upload_file_entry.grid(row=1, column=1, padx=5, sticky='ew')
        self.upload_browse_btn = ButtonWithIcon(file_card, text=" Browse", 
                                           icon_data=ICONS['browse'],
                                           command=self._browse_upload_file,
                                           width=10)
        self.upload_browse_btn.grid(row=1, column=2, padx=5)

        file_card.grid_columnconfigure(1, weight=1)

        # Options and actions card
        options_card = ttk.Frame(main_frame, style='Card.TFrame', padding="15")
        options_card.grid(row=2, column=0, columnspan=3, sticky='ew', pady=(0, 20))

        # Options
        options_frame = ttk.Frame(options_card, style='Card.TFrame')
        options_frame.pack(fill='x', pady=(0, 10))        # Options frame is kept for future options# Action buttons with icons
        buttons_frame = ttk.Frame(options_card, style='Card.TFrame')
        buttons_frame.pack(fill='x')
        self.process_btn = ButtonWithIcon(buttons_frame, text=" Validate & Clean", 
                                      icon_data=ICONS['process'],
                                      command=self._process_files, 
                                      style='Success.TButton',
                                      width=15)
        self.process_btn.pack(side='left', padx=5)
        
        self.save_log_btn = ButtonWithIcon(buttons_frame, text=" Save Log", 
                                       icon_data=ICONS['save'],
                                       command=self._save_log, 
                                       style='Primary.TButton',
                                       width=10)
        self.save_log_btn.pack(side='left', padx=5)

        # Results area
        results_frame = ttk.Frame(main_frame, style='Card.TFrame', padding="15")
        results_frame.grid(row=3, column=0, columnspan=3, sticky='nsew', pady=(0, 20))
        results_frame.grid_columnconfigure(0, weight=1)
        results_frame.grid_rowconfigure(2, weight=1)  # Changed row weight to 2

        # Results header with filter and clear button
        results_header = ttk.Frame(results_frame, style='Card.TFrame')
        results_header.grid(row=0, column=0, columnspan=2, sticky='ew', pady=(0, 5))
        ttk.Label(results_header, text="Processing Results", style='Card.TLabel').pack(side='left')

        # Filter area
        filter_frame = ttk.Frame(results_frame, style='Card.TFrame')
        filter_frame.grid(row=1, column=0, columnspan=2, sticky='ew', pady=(0, 10))
        
        ttk.Label(filter_frame, text="Filter:", style='Card.TLabel').pack(side='left', padx=(0, 5))
        self.filter_var = tk.StringVar()
        self.filter_entry = ttk.Entry(filter_frame, textvariable=self.filter_var)
        self.filter_entry.pack(side='left', fill='x', expand=True, padx=(0, 5))
        self.filter_var.trace_add('write', self._filter_results)
        
        ButtonWithIcon(filter_frame, text=" Clear", 
                      icon_data=ICONS['clear'],
                      command=self._clear_results,
                      style='Primary.TButton',
                      width=8).pack(side='right', padx=5)

        # Results text area with custom styling
        self.results_text = tk.Text(results_frame, height=20,
                                  font=('Consolas', 10),
                                  bg=self.colors['surface'],
                                  fg=self.colors['text'],
                                  relief="flat",
                                  borderwidth=1,
                                  padx=10,
                                  pady=10)
        self.results_text.grid(row=2, column=0, sticky='nsew')  # Changed to row 2

        # Custom scrollbar
        scrollbar = ttk.Scrollbar(results_frame, orient=tk.VERTICAL, command=self.results_text.yview)
        scrollbar.grid(row=2, column=1, sticky='ns')  # Changed to row 2
        self.results_text.configure(yscrollcommand=scrollbar.set)

        # Configure grid weights
        results_frame.grid_columnconfigure(0, weight=1)

        # Configure main frame grid weights
        main_frame.grid_rowconfigure(3, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)

        # Status bar with progress indication
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, 
                             style='Card.TLabel', padding=(10, 5))
        status_bar.grid(row=4, column=0, columnspan=3, sticky='ew')

    def _update_status(self, message):
        """Update status bar message"""
        self.status_var.set(message)
        self.root.update_idletasks()

    def _browse_raw_file(self):
        """
        Opens file dialog for raw data file with improved error handling.
        """
        try:
            filename = filedialog.askopenfilename(
                title="Select Raw Data File",
                filetypes=[("Text files", "*.txt"), ("CSV files", "*.csv"), ("All files", "*")],
                initialdir=os.path.dirname(self.raw_file_path.get()) if self.raw_file_path.get() else None
            )
            if filename:
                self.raw_file_path.set(filename)
                Toast(self.root, f"Raw file selected: {os.path.basename(filename)}", type_='success')
                self._update_status(f"Raw file selected: {os.path.basename(filename)}")
        except Exception as e:
            Toast(self.root, f"Error selecting file: {str(e)}", type_='error')

    def _browse_upload_file(self):
        """
        Opens file dialog for upload file with improved error handling.
        """
        try:
            filename = filedialog.askopenfilename(
                title="Select Upload File",
                filetypes=[("Text files", "*.txt"), ("CSV files", "*.csv"), ("All files", "*")],
                initialdir=os.path.dirname(self.upload_file_path.get()) if self.upload_file_path.get() else None
            )
            if filename:
                self.upload_file_path.set(filename)
                Toast(self.root, f"Upload file selected: {os.path.basename(filename)}", type_='success')
                self._update_status(f"Upload file selected: {os.path.basename(filename)}")
        except Exception as e:
            Toast(self.root, f"Error selecting file: {str(e)}", type_='error')

    def _process_files(self):
        """
        Initiates data validation and cleaning with enhanced progress feedback.
        """
        if not self.raw_file_path.get() or not self.upload_file_path.get():
            Toast(self.root, "Please select both files first", type_='error')
            return

        try:
            # Warn for large files
            raw_size = os.path.getsize(self.raw_file_path.get()) / 1024 / 1024  # MB
            upload_size = os.path.getsize(self.upload_file_path.get()) / 1024 / 1024
            if raw_size + upload_size > 100:  # Warn for files > 100 MB
                if not messagebox.askyesno("Large Files", 
                    "Large files detected. Processing may take several minutes. Continue?"):
                    return

            # Show loading spinner
            self.loading_spinner = LoadingSpinner(self.root)
            self.loading_spinner.grid(row=2, column=0, padx=5, pady=5)
            self.loading_spinner.start()

            self._update_status("Processing files...")
            self.results_text.delete(1.0, tk.END)
            self.results_text.insert(tk.END, "Starting data validation and cleaning process...\n")
            self.root.update_idletasks()

            # Disable buttons during processing
            self.process_btn.configure(state='disabled')
            self.save_log_btn.configure(state='disabled')

            # Process files
            base_dir = os.path.dirname(self.upload_file_path.get())
            file_name = os.path.basename(self.upload_file_path.get())
            name, ext = os.path.splitext(file_name)
            cleaned_output_path = os.path.join(base_dir, f"{name}_cleaned{ext}")
            report_output_path = os.path.join(base_dir, "mismatch_report.csv")

            def custom_print(*args, **kwargs):
                message = " ".join(map(str, args))
                self.results_text.insert(tk.END, message + "\n")
                self.results_text.see(tk.END)
                # Update GUI every 100 lines to prevent lag
                if self.results_text.get('1.0', tk.END).count('\n') % 100 == 0:
                    self.root.update_idletasks()

            original_print = print
            try:
                globals()['print'] = custom_print
                main(
                    self.raw_file_path.get(),
                    self.upload_file_path.get(),
                    cleaned_output_path,
                    report_output_path
                )
                self._update_status("Processing completed successfully")
                Toast(self.root, "Processing completed successfully!", type_='success')
            except Exception as e:
                self.results_text.insert(tk.END, f"\nAn unexpected error occurred: {e}\n")
                self._update_status("Error during processing")
                Toast(self.root, f"Error during processing: {str(e)}", type_='error')
            finally:
                globals()['print'] = original_print
                # Stop and remove loading spinner
                if self.loading_spinner:
                    self.loading_spinner.stop()
                    self.loading_spinner.canvas.grid_forget()
                    self.loading_spinner = None

        except Exception as e:
            Toast(self.root, f"Error: {str(e)}", type_='error')
            self._update_status("Error during processing")
        finally:
            # Re-enable buttons
            self.process_btn.configure(state='normal')
            self.save_log_btn.configure(state='normal')

    def _save_log(self):
        """
        Saves the results text to a file with error handling.
        """
        try:
            log_content = self.results_text.get(1.0, tk.END).strip()
            if not log_content:
                Toast(self.root, "No content to save", type_='warning')
                return

            filename = filedialog.asksaveasfilename(
                title="Save Log File",
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*")],
                initialdir=os.path.dirname(self.upload_file_path.get()) if self.upload_file_path.get() else None
            )
            if filename:
                with open(filename, 'w') as f:
                    f.write(log_content)
                self.results_text.insert(tk.END, f"\nLog saved to: {filename}\n")
                Toast(self.root, f"Log saved: {os.path.basename(filename)}", type_='success')
                self._update_status(f"Log saved: {os.path.basename(filename)}")
        except Exception as e:
            Toast(self.root, f"Error saving log: {str(e)}", type_='error')
            self._update_status("Error saving log")

    def _filter_results(self, *args):
        """Filter results based on search text"""
        filter_text = self.filter_var.get().lower()
        
        # Store original text if not already stored
        if not hasattr(self, '_original_text'):
            self._original_text = self.results_text.get(1.0, tk.END)
        
        if not filter_text:
            # Show original text if filter is empty
            self.results_text.delete(1.0, tk.END)
            self.results_text.insert(1.0, self._original_text)
            return
        
        # Filter lines containing the search text
        filtered_lines = [line for line in self._original_text.splitlines() 
                         if filter_text in line.lower()]
        
        # Update display
        self.results_text.delete(1.0, tk.END)
        if filtered_lines:
            self.results_text.insert(1.0, '\n'.join(filtered_lines))
        else:
            self.results_text.insert(1.0, "No matching results found.")

    def _clear_results(self):
        """Clear results and filter"""
        self.filter_var.set('')
        self.results_text.delete(1.0, tk.END)
        if hasattr(self, '_original_text'):
            del self._original_text  # Clear stored original text
        Toast(self.root, "Results cleared", type_='info')

def read_data_file(file_path):
    """
    Reads a semicolon-separated text file into a DataFrame with strict null preservation.
    Uses chunking for large files and optimized dtypes.
    """
    try:
        # Check file structure
        with open(file_path, 'r') as f:
            first_line = f.readline()
            if len(first_line.split(';')) != 11:
                print(f"Error: File {file_path} does not have 11 columns.")
                return None

        columns = [
            'ID1', 'ID2', 'SSS_Number', 'Last_Name', 'First_Name',
            'Middle_Name', 'Code', 'Amount', 'Flag', 'Field10', 'Field11'
        ]
        dtypes = {
            'ID1': 'string', 'ID2': 'string', 'SSS_Number': 'string',
            'Last_Name': 'string', 'First_Name': 'string', 'Middle_Name': 'string',
            'Code': 'string', 'Amount': 'string', 'Flag': 'string',
            'Field10': 'string', 'Field11': 'string'
        }

        # Use chunking for large files (>100 MB)
        if os.path.getsize(file_path) > 100 * 1024 * 1024:
            df = pd.concat([chunk for chunk in pd.read_csv(file_path, sep=';', header=None, names=columns, 
                                                           dtype=dtypes, keep_default_na=False, na_values=['NULL'], 
                                                           chunksize=10000)], ignore_index=True)
        else:
            df = pd.read_csv(file_path, sep=';', header=None, names=columns, 
                             dtype=dtypes, keep_default_na=False, na_values=['NULL'])
        
        # Vectorized string stripping
        str_columns = df.select_dtypes(include=['string']).columns
        df[str_columns] = df[str_columns].apply(lambda x: x.str.strip() if x.notna().any() else x)
        
        # Validate SSS_Number uniqueness
        if df['SSS_Number'].duplicated().any():
            print(f"Error: Duplicate SSS Numbers found in {file_path}: {df[df['SSS_Number'].duplicated()]['SSS_Number'].tolist()}")
            return None

        # Validate Amount format (vectorized)
        mask = df['Amount'].str.match(r'^\d+(\.\d+)?$')
        if not mask.all():
            print(f"Error: Invalid Amount format in {file_path}: {df[~mask]['Amount'].tolist()}")
            return None

        return df
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return None

def compare_dataframes(raw_df, upload_df):
    """
    Compares raw and upload DataFrames using vectorized operations.
    """
    mismatch_report = []
    missing_records = list(set(raw_df['SSS_Number']) - set(upload_df['SSS_Number']))
    extra_records = list(set(upload_df['SSS_Number']) - set(raw_df['SSS_Number']))
    
    # Merge DataFrames on SSS_Number
    merged = raw_df.merge(upload_df, on='SSS_Number', how='inner', suffixes=('_raw', '_upload'))
    
    for col in raw_df.columns:
        if col != 'SSS_Number':
            raw_col = f"{col}_raw"
            upload_col = f"{col}_upload"
            mask = merged[raw_col].fillna('') != merged[upload_col].fillna('')
            if mask.any():
                mismatches = merged[mask][['SSS_Number', raw_col, upload_col]]
                for _, row in mismatches.iterrows():
                    mismatch_report.append({
                        'SSS_Number': row['SSS_Number'],
                        'Field': col,
                        'Raw_Value': row[raw_col],
                        'Upload_Value': row[upload_col],
                        'Mismatch_Type': 'Value Mismatch'
                    })
    
    return mismatch_report, missing_records, extra_records

def clean_upload_file(raw_df, upload_df, extra_records, output_path):
    """
    Cleans the upload DataFrame by aligning with raw data using SSS_Number.
    """
    # Remove extra records
    cleaned_df = upload_df[~upload_df['SSS_Number'].isin(extra_records)].copy()
    if extra_records:
        print(f"Removed {len(extra_records)} extra records from upload file.")

    if cleaned_df.empty:
        print("No common records to clean after removing extra records.")
        return

    # Merge with raw_df to update fields
    raw_df_subset = raw_df.set_index('SSS_Number')
    cleaned_df = cleaned_df.set_index('SSS_Number')
    for col in raw_df.columns:
        if col != 'SSS_Number':
            cleaned_df[col] = raw_df_subset[col].reindex(cleaned_df.index).combine_first(cleaned_df[col])

    # Reset index and restore column order
    cleaned_df = cleaned_df.reset_index()[raw_df.columns]

    try:
        cleaned_df.to_csv(output_path, sep=';', index=False, header=False, na_rep='NULL')
        print(f"Cleaned upload file saved to: {output_path}")
    except Exception as e:
        print(f"Error saving cleaned file to {output_path}: {e}")

def save_mismatch_report(mismatch_report, missing_records, extra_records, report_path):
    """
    Saves the mismatch report to a CSV file.
    """
    report_df = pd.DataFrame(mismatch_report)
    missing_data = [{'SSS_Number': sss, 'Field': 'N/A', 'Raw_Value': 'N/A', 'Upload_Value': 'N/A', 'Mismatch_Type': 'Missing Record (in upload)'} for sss in missing_records]
    extra_data = [{'SSS_Number': sss, 'Field': 'N/A', 'Raw_Value': 'N/A', 'Upload_Value': 'N/A', 'Mismatch_Type': 'Extra Record (in upload)'} for sss in extra_records]
    final_report_df = pd.concat([report_df, pd.DataFrame(missing_data), pd.DataFrame(extra_data)], ignore_index=True)

    try:
        final_report_df.to_csv(report_path, index=False)
        print(f"Mismatch report saved to: {report_path}")
    except Exception as e:
        print(f"Error saving mismatch report to {report_path}: {e}")

def main(raw_file_path, upload_file_path, cleaned_output_path, report_output_path):
    """
    Orchestrates data validation and cleaning.
    """
    print("Starting data validation and cleaning process...")

    raw_df = read_data_file(raw_file_path)
    upload_df = read_data_file(upload_file_path)

    if raw_df is None or upload_df is None:
        print("Exiting due to file reading errors.")
        return

    print(f"Successfully read raw data file with {len(raw_df)} records.")
    print(f"Successfully read upload file with {len(upload_df)} records.")

    mismatch_report, missing_records, extra_records = compare_dataframes(raw_df, upload_df)

    print("\n--- Validation Summary ---")
    print(f"Total records in raw data: {len(raw_df)}")
    print(f"Total records in upload file: {len(upload_df)}")
    print(f"Number of records missing from upload file: {len(missing_records)}")
    print(f"Number of extra records in upload file: {len(extra_records)}")
    print(f"Number of value mismatches for common records: {len(mismatch_report)}")

    if mismatch_report:
        print("\n--- Detailed Value Mismatches ---")
        if len(mismatch_report) > 1000:
            print(f"Showing first 1000 mismatches (total: {len(mismatch_report)}). Full details in report.")
            for mismatch in mismatch_report[:1000]:
                print(f"SSS: {mismatch['SSS_Number']}, Field: {mismatch['Field']}, "
                      f"Raw: '{mismatch['Raw_Value']}', Upload: '{mismatch['Upload_Value']}'")
        else:
            for mismatch in mismatch_report:
                print(f"SSS: {mismatch['SSS_Number']}, Field: {mismatch['Field']}, "
                      f"Raw: '{mismatch['Raw_Value']}', Upload: '{mismatch['Upload_Value']}'")

    if missing_records:
        print(f"\n--- Missing Records (in raw, but not in upload) ---")
        print(f"SSS Numbers: {', '.join(missing_records)}")

    if extra_records:
        print(f"\n--- Extra Records (in upload, but not in raw) ---")
        print(f"SSS Numbers: {', '.join(extra_records)}")

    save_mismatch_report(mismatch_report, missing_records, extra_records, report_output_path)
    clean_upload_file(raw_df, upload_df, extra_records, cleaned_output_path)

    print("\n--- Process Completed ---")
    print("Check the mismatch report and cleaned file for details.")

if __name__ == "__main__":
    root = tk.Tk()
    app = DataCleanerGUI(root)
    root.mainloop()
