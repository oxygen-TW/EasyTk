import functools
import inspect

def on_click(widget, *args):
    """A decorator to bind a function to a specific Tkinter event."""
    def decorator(func):
        sig = inspect.signature(func)
        
        @functools.wraps(func)
        def wrapper(event=None):
            # Check how many parameters the function expects
            num_params = len(sig.parameters)
            
            if num_params == 0:
                return func()
            elif len(args) > 0:
                # Arguments provided, pass them to the function
                return func(*args)
            else:
                # No arguments provided, pass event if function expects 1 param
                if num_params >= 1:
                    return func(event)
                else:
                    return func()
        
        # Bind the wrapper function to the widget and event
        widget.bind("<Button-1>", wrapper)
        return wrapper
    return decorator