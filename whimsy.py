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
        title1 = generate_figlet('CS50\nFinal Project :', 'standard')
        title2 = generate_figlet('Budgets App', 'banner')
        cowified = generate_cow('Welcome to my project!')
        return f'\n\n\n\n{title1}\n\n{title2}\n{cowified}'
    else:
        return "Welcome to the Budgets App"