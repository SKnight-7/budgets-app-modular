"""
Whimsy module — a small launch flourish for the app.

Provides an ASCII-art (FIGlet) title and a cowsay greeting that display once
when the app starts. It's pure character/UX, not functionality, but adds a bit
of warmth to what would otherwise be a cold CLI startup.
"""
from pyfiglet import Figlet, FigletError
import cowsay

def generate_figlet(phrase, user_font):
    """
    Generates a FIGlet text art representation of a given phrase using the specified font.

    Args:
        phrase (str): The phrase to be converted into FIGlet text art.
        user_font (str): The name of the FIGlet font to be used.

    Returns:
        str: The FIGlet text art representation of the phrase if the font is valid.
        str: "Invalid Font" if the specified font is not available or invalid.
    """
    try:
        figlet = Figlet(font=user_font)
        return figlet.renderText(phrase)
    except FigletError:
        return f"Invalid Font"

def generate_cow(phrase):
    """
    Generates a cowsay representation of a given phrase.

    Args:
        phrase (str): The phrase to be displayed in the cowsay output.

    Returns:
        str: The cowsay representation of the phrase.
    """
    return cowsay.get_output_string('cow', phrase)

def apply_whimsy(enable_whimsy=True):
    if enable_whimsy:
        title = generate_figlet('Budgets App', 'banner')
        cowified = generate_cow('Let\'s see how these finances are moooooving!')
        return f'\n\n\n\n{title}\n{cowified}'
    else:
        return "Welcome to the Budgets App"