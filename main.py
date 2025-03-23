import warnings
from ui.gradio_ui import demo

# suppress deprecation warning for now
warnings.filterwarnings("ignore", category=DeprecationWarning)

if __name__ == "__main__":
    demo.launch()