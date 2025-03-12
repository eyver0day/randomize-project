# =============================================================================
# Hide Console Window on Startup
# =============================================================================
import sys
if sys.platform == "win32":
    import ctypes
    kernel32 = ctypes.windll.kernel32
    hwnd = kernel32.GetConsoleWindow()
    if hwnd:
        ctypes.windll.user32.ShowWindow(hwnd, 0)

#!/usr/bin/env python
# =============================================================================
# Import Standard Libraries and Third-Party Modules
# =============================================================================
import sys, random, string, secrets, os, math, requests
from datetime import date

# Import PyQt6 modules for the graphical user interface (GUI)
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QGroupBox, QLabel, QSpinBox, QComboBox, QSlider, QPushButton,
    QTextEdit, QProgressBar, QMessageBox, QFileDialog, QDialog, QSizePolicy
)
from PyQt6.QtCore import Qt, QTimer, QRect, QUrl, QObject, pyqtSlot, pyqtSignal
from PyQt6.QtGui import QFont, QPixmap, QPainter, QDesktopServices, QIcon
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebChannel import QWebChannel
from faker import Faker

# =============================================================================
# Resource Path Resolution Function
# =============================================================================
def resource_path(relative_path):
    """
    Returns the absolute path to a resource file.
    
    This function is designed to work in both development mode and when packaged 
    (e.g., with PyInstaller). It first tries to locate the file directly in the base 
    directory. If the file is not found there, it searches recursively within all 
    subdirectories of the base directory where the script (randomize.pyw) is located.
    
    :param relative_path: The filename or relative path of the resource.
    :return: The absolute path to the resource if found, or a candidate path otherwise.
    """
    try:
        # In a packaged environment, sys._MEIPASS points to the temporary folder
        base_path = sys._MEIPASS  
    except Exception:
        # In development mode, use the current working directory
        base_path = os.path.abspath(".")
    
    # Check if the resource exists directly in the base directory.
    candidate = os.path.join(base_path, relative_path)
    if os.path.exists(candidate):
        return candidate

    # If not found, walk through all subdirectories within the base directory.
    for root, dirs, files in os.walk(base_path):
        if relative_path in files:
            return os.path.join(root, relative_path)
    
    # If the resource is not found, return the candidate path (which may not exist)
    return candidate

# =============================================================================
# Global Variables for Simulated Email and Username Tracking
# =============================================================================
used_emails = set()
used_usernames = {}

# =============================================================================
# Translations Dictionary for Multilingual Support (Spanish and English)
# =============================================================================
translations = {
    "ES": {
         "window_title": "Identidades Random - PyQt6",
         "options_group": "Opciones de Generación",
         "cantidad": "Cantidad:",
         "genero": "Género:",
         "porcentaje_hombres": "Porcentaje de Hombres:",
         "nacionalidad": "Nacionalidad:",
         "nombres": "Nombres:",
         "apellidos": "Apellidos:",
         "radio": "Radio de variación (km):",
         "import_nombres": "Importar Nombres",
         "import_apellidos": "Importar Apellidos",
         "generar": "Generar Personas",
         "copiar": "Copiar Datos",
         "nueva_generacion": "Borrar",
         "cerrar": "Cerrar",
         "ayuda": "Ayuda",
         "help_header": "RANDOMIZE",
         "help_subheader": "Created by eyver0day",
         "help_description": ("Esta aplicación genera identidades aleatorias de forma dinámica. Permite configurar parámetros como la cantidad, el género, "
                              "la nacionalidad y la importación de diccionarios personalizados para nombres y apellidos. Ha sido desarrollada con PyQt6 y otras librerías, "
                              "ofreciendo una experiencia sencilla y robusta. Para mayor información o reportar errores, visite nuestro GitHub."),
         "help_github": "GitHub: <a href='https://github.com/eyver0day'>https://github.com/eyver0day</a>",
         "gender_items": ["Masculino", "Femenino", "Aleatorio"]
    },
    "EN": {
         "window_title": "Random Identities - PyQt6",
         "options_group": "Generation Options",
         "cantidad": "Quantity:",
         "genero": "Gender:",
         "porcentaje_hombres": "Male Percentage:",
         "nacionalidad": "Nationality:",
         "nombres": "Names:",
         "apellidos": "Surnames:",
         "radio": "Variation Radius (km):",
         "import_nombres": "Import Names",
         "import_apellidos": "Import Surnames",
         "generar": "Generate Persons",
         "copiar": "Copy Data",
         "nueva_generacion": "Delete",
         "cerrar": "Close",
         "ayuda": "Help",
         "help_header": "RANDOMIZE",
         "help_subheader": "Created by eyver0day",
         "help_description": ("This application dynamically generates random identities. It allows you to configure various parameters such as quantity, gender, "
                              "nationality and the import of custom dictionaries for first and last names. Developed using PyQt6 and other libraries, "
                              "it provides a simple yet robust experience. For more information or to report issues, please visit our GitHub."),
         "help_github": "GitHub: <a href='https://github.com/eyver0day'>https://github.com/eyver0day</a>",
         "gender_items": ["Male", "Female", "Random"]
    }
}

# =============================================================================
# Auxiliary Functions for Data Generation and Formatting
# =============================================================================
def reverse_geocode(lat, lon):
    """
    Performs a reverse geocoding lookup using OpenStreetMap's Nominatim API.
    
    Given latitude and longitude coordinates, this function returns a human-readable 
    address. If the request fails or no address is found, a default message is returned.
    
    :param lat: Latitude value.
    :param lon: Longitude value.
    :return: A string containing the address or a default message if unavailable.
    """
    url = f"https://nominatim.openstreetmap.org/reverse?format=jsonv2&lat={lat}&lon={lon}"
    headers = {"User-Agent": "random-person-generator/1.0"}
    try:
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            data = response.json()
            return data.get("display_name", "Ubicación desconocida")
    except Exception:
        return "Ubicación desconocida"
    return "Ubicación desconocida"

# Mapping between nationalities and Faker locales
nationality_locales = {
    "United States": "en_US",
    "Spain": "es_ES",
    "United Kingdom": "en_GB",
    "Germany": "de_DE",
    "France": "fr_FR",
    "Italy": "it_IT"
}

def get_available_email(fake):
    """
    Generates an email address that has not been used before.
    
    This function uses the Faker library to create a username, appends a randomly 
    selected domain, and ensures the email is unique within the used_emails set.
    
    :param fake: A Faker instance.
    :return: A unique email address.
    """
    domain_list = ["gmail.com", "hotmail.com", "outlook.com", "yahoo.com", "icloud.com"]
    while True:
        email_username = fake.user_name()
        domain = random.choice(domain_list)
        email = f"{email_username}@{domain}"
        if email not in used_emails:
            used_emails.add(email)
            return email

def get_available_username(fake, first_name, last_name):
    """
    Generates a username based on the provided first and last names.
    
    The function attempts to append a random number to the concatenated names until 
    a unique username is found or a maximum number of attempts is reached.
    
    :param fake: A Faker instance.
    :param first_name: The first name of the person.
    :param last_name: The last name of the person.
    :return: A unique username.
    """
    base = (first_name + last_name).lower()
    for _ in range(100):
        candidate = base + str(random.randint(1, 999))
        if used_usernames.get(candidate, 0) < 5:
            used_usernames[candidate] = used_usernames.get(candidate, 0) + 1
            return candidate
    return fake.user_name()

def get_random_coordinate(center, radius_km):
    """
    Calculates a random geographical coordinate within a specified radius.
    
    Given a central coordinate and a radius (in kilometers), this function computes 
    a random latitude and longitude offset based on a uniform distribution.
    
    :param center: A tuple (latitude, longitude) representing the center.
    :param radius_km: The radius in kilometers.
    :return: A tuple (new_latitude, new_longitude) within the specified radius.
    """
    lat0, lon0 = center
    radius_deg = radius_km / 111  # Approximation: 1° ≈ 111 km
    u = random.random()
    v = random.random()
    w = radius_deg * math.sqrt(u)
    t = 2 * math.pi * v
    dlat = w * math.cos(t)
    dlon = w * math.sin(t) / math.cos(math.radians(lat0))
    return lat0 + dlat, lon0 + dlon

def generate_person(fake, gender, center_coords=None, radius_km=None, names_list=None, surnames_list=None, num_first_names=1, num_last_names=2):
    """
    Generates a single random person with various attributes.
    
    Based on the selected gender and provided optional name/surname lists, the function 
    generates first names, last names, date of birth, age, email, username, password, 
    and an address (which can be geocoded based on coordinates).
    
    :param fake: A Faker instance.
    :param gender: The desired gender for the person.
    :param center_coords: Optional tuple (lat, lon) for location-based address generation.
    :param radius_km: Optional radius in kilometers to vary the address.
    :param names_list: Optional list of names to choose from.
    :param surnames_list: Optional list of surnames to choose from.
    :param num_first_names: Number of first names to generate.
    :param num_last_names: Number of last names to generate.
    :return: A dictionary containing the generated person's details.
    """
    if gender in ["Masculino", "Male"]:
        if names_list:
            first_names = [random.choice(names_list) for _ in range(num_first_names)]
        else:
            try:
                first_names = [fake.first_name_male() for _ in range(num_first_names)]
            except AttributeError:
                first_names = [fake.first_name() for _ in range(num_first_names)]
        if surnames_list:
            last_names = [random.choice(surnames_list) for _ in range(num_last_names)]
        else:
            try:
                last_names = [fake.last_name_male() for _ in range(num_last_names)]
            except AttributeError:
                last_names = [fake.last_name() for _ in range(num_first_names)]
        gender_val = "Masculino" if gender=="Masculino" else "Male"
    elif gender in ["Femenino", "Female"]:
        if names_list:
            first_names = [random.choice(names_list) for _ in range(num_first_names)]
        else:
            try:
                first_names = [fake.first_name_female() for _ in range(num_first_names)]
            except AttributeError:
                first_names = [fake.first_name() for _ in range(num_first_names)]
        if surnames_list:
            last_names = [random.choice(surnames_list) for _ in range(num_last_names)]
        else:
            try:
                last_names = [fake.last_name_female() for _ in range(num_last_names)]
            except AttributeError:
                last_names = [fake.last_name() for _ in range(num_first_names)]
        gender_val = "Femenino" if gender=="Femenino" else "Female"
    else:
        if names_list:
            first_names = [random.choice(names_list) for _ in range(num_first_names)]
        else:
            first_names = [fake.first_name() for _ in range(num_first_names)]
        if surnames_list:
            last_names = [random.choice(surnames_list) for _ in range(num_last_names)]
        else:
            last_names = [fake.last_name() for _ in range(num_last_names)]
        gender_val = "Aleatorio" if gender=="Aleatorio" else "Random"
    full_name = " ".join(first_names) + " " + " ".join(last_names)
    
    # Generate date of birth and calculate age
    dob = fake.date_of_birth(minimum_age=18, maximum_age=80)
    age = (date.today().year - dob.year) - ((date.today().month, date.today().day) < (dob.month, dob.day))
    
    # Generate unique email and username
    email = get_available_email(fake)
    username = get_available_username(fake, first_names[0], last_names[0])
    
    # Generate a random password
    password = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(12))
    
    # Determine the address, optionally using geocoded coordinates
    if center_coords and radius_km and radius_km > 0:
        new_coords = get_random_coordinate(center_coords, radius_km)
        address = reverse_geocode(new_coords[0], new_coords[1])
    else:
        address = fake.address().replace("\n", ", ")
    
    return {
        "Nombre": full_name,
        "Género": gender_val,
        "Fecha de Nacimiento": dob.strftime("%d-%m-%Y"),
        "Edad": age,
        "Dirección": address,
        "Email": email,
        "Username": username,
        "Password": password
    }

def generate_persons(n, nationality, gender, center_coords, male_percentage=50, radius_km=None, names_list=None, surnames_list=None, num_first_names=1, num_last_names=2):
    """
    Generates a list of random persons based on the specified criteria.
    
    This function selects a Faker locale based on the nationality input, iterates 
    to create multiple person entries, and adjusts gender based on the male percentage 
    when the gender is set to random.
    
    :param n: The number of persons to generate.
    :param nationality: The nationality for the generated persons.
    :param gender: The desired gender or randomness indicator.
    :param center_coords: Optional coordinate tuple for location-based generation.
    :param male_percentage: Percentage chance for male when gender is random.
    :param radius_km: Optional radius for geographic variation.
    :param names_list: Optional custom list of first names.
    :param surnames_list: Optional custom list of surnames.
    :param num_first_names: Number of first names per person.
    :param num_last_names: Number of last names per person.
    :return: A list of dictionaries containing person details.
    """
    if nationality == "Random":
        locale = random.choice(list(nationality_locales.values()))
    else:
        locale = nationality_locales.get(nationality, "en_US")
    fake = Faker(locale)
    persons = []
    for i in range(n):
        effective_gender = gender
        if gender in ["Aleatorio", "Random"]:
            effective_gender = "Masculino" if random.random() * 100 < male_percentage else "Femenino"
            if nationality == "en_US":
                effective_gender = "Random"
        persons.append(generate_person(fake, effective_gender, center_coords, radius_km, names_list, surnames_list, num_first_names, num_last_names))
    return persons

def format_persons(persons, lang="ES"):
    """
    Formats the list of generated persons into a human-readable string.
    
    Depending on the language selected, the function maps the labels to the 
    corresponding translations and appends a warning message regarding the use 
    of the tool.
    
    :param persons: A list of dictionaries containing person details.
    :param lang: The language code ('ES' or 'EN').
    :return: A formatted string representing all generated persons.
    """
    if lang == "EN":
        labels = {
            "Nombre": "Name",
            "Género": "Gender",
            "Fecha de Nacimiento": "Date of Birth",
            "Edad": "Age",
            "Dirección": "Address",
            "Email": "Email",
            "Username": "User",
            "Password": "Password"
        }
        warning = "\n⚠WARNING:\nThis script has been developed exclusively for educational purposes. I am not responsible for any misuse or malicious use of this tool. It is recommended to use it ethically and responsibly."
    else:
        labels = {
            "Nombre": "Nombre",
            "Género": "Género",
            "Fecha de Nacimiento": "Fecha de Nacimiento",
            "Edad": "Edad",
            "Dirección": "Dirección",
            "Email": "Email",
            "Username": "Usuario",
            "Password": "Contraseña"
        }
        warning = "\n⚠ADVERTENCIA:\nEste script ha sido desarrollado exclusivamente con fines educativos. No me hago responsable por cualquier uso indebido o malintencionado de esta herramienta. Se recomienda utilizarla de manera ética y responsable."
    output = ""
    for p in persons:
        output += (
            f"{labels['Nombre']}: {p['Nombre']}\n"
            f"{labels['Género']}: {p['Género']}\n"
            f"{labels['Fecha de Nacimiento']}: {p['Fecha de Nacimiento']}\n"
            f"{labels['Edad']}: {p['Edad']}\n"
            f"{labels['Dirección']}: {p['Dirección']}\n"
            f"{labels['Email']}: {p['Email']}\n"
            f"{labels['Username']}: {p['Username']}\n"
            f"{labels['Password']}: {p['Password']}\n"
            "----------------------------------------\n"
        )
    output += warning
    return output

# =============================================================================
# Custom Widgets and Classes for the Graphical Interface
# =============================================================================
class DraggableTextEdit(QTextEdit):
    """
    A QTextEdit subclass that supports drag-and-drop file loading.
    
    When a file is dragged onto the widget, its contents are loaded and displayed.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.loaded_file_path = None

    def dragEnterEvent(self, event):
        # Accept drag if URLs (files) are provided.
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            super().dragEnterEvent(event)

    def dropEvent(self, event):
        # Handle file drop events to load file content.
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            if urls:
                file_path = urls[0].toLocalFile()
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    self.setPlainText(content)
                    self.loaded_file_path = file_path
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Could not load the file: {e}")
        else:
            super().dropEvent(event)

class ImportButton(QPushButton):
    """
    A QPushButton subclass that supports drag-and-drop for importing dictionary files.
    
    When a file is dropped on the button, it reads the content and invokes the specified 
    callback function to handle the import.
    """
    def __init__(self, text, import_callback, parent=None):
        super().__init__(text, parent)
        self.setAcceptDrops(True)
        self.import_callback = import_callback

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            super().dragEnterEvent(event)

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            if urls:
                file_path = urls[0].toLocalFile()
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    self.import_callback(content, file_path)
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Could not load the file: {e}")
        else:
            super().dropEvent(event)

class MapBridge(QObject):
    """
    A QObject subclass used to bridge communication between the embedded map (in a QWebEngineView) 
    and the PyQt application.
    
    It defines a signal to send received coordinates from the map.
    """
    coordinatesReceived = pyqtSignal(float, float)
    
    @pyqtSlot(float, float)
    def sendCoordinates(self, lat, lon):
        self.coordinatesReceived.emit(lat, lon)

class HelpDialog(QDialog):
    """
    A dialog window that displays help information.
    
    The content includes a header, subheader, description, and a link to the GitHub repository.
    """
    def __init__(self, lang="ES", parent=None):
        super().__init__(parent)
        self.setWindowTitle(translations[lang]["ayuda"])
        self.setWindowIcon(QIcon(resource_path("help.ico")))
        self.resize(500, 400)
        layout = QVBoxLayout(self)
        
        # Display an image in the help dialog
        image_label = QLabel()
        pix = QPixmap(resource_path("help.png"))
        if not pix.isNull():
            pix = pix.scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            image_label.setPixmap(pix)
            image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(image_label)
        
        # Help text in HTML format for rich text display
        help_text = f"""
        <div style="text-align:center;">
          <span style="font-family:Impact; font-size:48pt;">{translations[lang]["help_header"]}</span><br>
          <span style="font-size:14pt;">{translations[lang]["help_subheader"]}</span>
        </div>
        <p style="text-align:justify; margin-top:20px;">
          {translations[lang]["help_description"]}
        </p>
        <p style="text-align:center; margin-top:20px;">
          {translations[lang]["help_github"]}
        </p>
        """
        help_label = QLabel(help_text)
        help_label.setTextFormat(Qt.TextFormat.RichText)
        help_label.setOpenExternalLinks(True)
        help_label.setWordWrap(True)
        layout.addWidget(help_label)
        
        # Layout for the buttons at the bottom of the dialog
        button_layout = QHBoxLayout()
        buy_button = QPushButton("Buy me a coffe")
        buy_button.setIcon(QIcon(resource_path("kofi.ico")))
        buy_button.clicked.connect(lambda: QDesktopServices.openUrl(QUrl("https://ko-fi.com/eyver0day")))
        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.accept)
        button_layout.addWidget(buy_button)
        button_layout.addStretch()
        button_layout.addWidget(ok_button)
        layout.addLayout(button_layout)

class SplashScreen(QDialog):
    """
    A splash screen that displays a loading image, title, subtitle, and a progress bar.
    
    The progress bar simulates loading for a few seconds before the main application window is shown.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        # Set window flags for a frameless, always-on-top window.
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setFixedSize(400, 350)
        self.setStyleSheet("background-color: white;")
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        # Splash image
        self.image_label = QLabel(self)
        duck_image = QPixmap(resource_path("rubber_ducky.png"))
        if not duck_image.isNull():
            duck_image = duck_image.scaled(150, 150, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.image_label.setPixmap(duck_image)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.image_label)
        
        # Title label
        self.title_label = QLabel("RANDOMIZE", self)
        font = QFont("Impact", 48)
        self.title_label.setFont(font)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.title_label)
        
        # Subtitle label
        self.subtitle_label = QLabel("Created by eyver0day", self)
        font_sub = QFont("Arial", 12)
        self.subtitle_label.setFont(font_sub)
        self.subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.subtitle_label)
        
        # Progress bar setup
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setTextVisible(False)
        layout.addWidget(self.progress_bar)
        
        self.progress_value = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_progress)
        # Update the progress every 50ms to simulate a 5-second load time
        self.timer.start(50)
    
    def update_progress(self):
        """
        Increments the progress bar value and closes the splash screen when complete.
        """
        self.progress_value += 1
        self.progress_bar.setValue(self.progress_value)
        if self.progress_value >= 100:
            self.timer.stop()
            self.accept()  # Close the splash screen and continue with the application

class MainWindow(QMainWindow):
    """
    The main window class for the application.
    
    This class sets up the primary user interface, including options for generating random identities,
    a map view for location selection, and output display.
    """
    def __init__(self):
        super().__init__()
        # Remove the default window frame.
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.current_language = "ES"
        self.setWindowTitle(translations[self.current_language]["window_title"])
        self.resize(700, 500)
        self.center_coords = None
        self.generated_output = ""
        self.names_dictionary = None
        self.surnames_dictionary = None
        self._drag_pos = None
        self.init_ui()
    
    def init_ui(self):
        """
        Initializes the user interface components and layouts.
        """
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_vlayout = QVBoxLayout(central_widget)
        main_vlayout.setContentsMargins(5, 5, 5, 5)
        main_vlayout.setSpacing(5)
        
        # Top bar: language selector and help button
        top_bar = QHBoxLayout()
        self.language_label = QLabel("Idioma:")
        top_bar.addWidget(self.language_label)
        self.lang_cb = QComboBox()
        self.lang_cb.addItems(["ES", "EN"])
        self.lang_cb.setCurrentText(self.current_language)
        self.lang_cb.currentTextChanged.connect(self.change_language)
        top_bar.addWidget(self.lang_cb)
        top_bar.addStretch()
        self.help_btn = QPushButton(translations[self.current_language]["ayuda"])
        self.help_btn.clicked.connect(self.show_help)
        top_bar.addWidget(self.help_btn)
        main_vlayout.addLayout(top_bar)
        
        # Main horizontal layout: options and map view
        main_hlayout = QHBoxLayout()
        main_vlayout.addLayout(main_hlayout)
        
        # Left panel: generation options and output area
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(5, 5, 5, 5)
        left_layout.setSpacing(5)
        
        self.options_group = QGroupBox(translations[self.current_language]["options_group"])
        options_layout = QVBoxLayout(self.options_group)
        options_layout.setSpacing(5)
        
        # Quantity selection
        qty_layout = QHBoxLayout()
        self.qty_label = QLabel(translations[self.current_language]["cantidad"])
        self.qty_spin = QSpinBox()
        self.qty_spin.setRange(1, 100)
        self.qty_spin.setValue(10)
        qty_layout.addWidget(self.qty_label)
        qty_layout.addWidget(self.qty_spin)
        options_layout.addLayout(qty_layout)
        
        # Gender selection
        gender_layout = QHBoxLayout()
        self.gender_label = QLabel(translations[self.current_language]["genero"])
        self.gender_cb = QComboBox()
        self.update_gender_items()
        self.gender_cb.currentIndexChanged.connect(self.on_gender_change)
        gender_layout.addWidget(self.gender_label)
        gender_layout.addWidget(self.gender_cb)
        options_layout.addLayout(gender_layout)
        
        # Slider for male percentage (only visible for random gender)
        self.male_slider_label = QLabel(translations[self.current_language]["porcentaje_hombres"])
        self.male_slider = QSlider(Qt.Orientation.Horizontal)
        self.male_slider.setRange(0, 100)
        self.male_slider.setValue(50)
        options_layout.addWidget(self.male_slider_label)
        options_layout.addWidget(self.male_slider)
        
        # Nationality selection
        nat_layout = QHBoxLayout()
        self.nat_label = QLabel(translations[self.current_language]["nacionalidad"])
        self.nat_cb = QComboBox()
        if self.current_language == "ES":
            self.nat_cb.addItems(["United States", "Spain", "United Kingdom", "Germany", "France", "Italy", "Aleatorio"])
        else:
            self.nat_cb.addItems(["United States", "Spain", "United Kingdom", "Germany", "France", "Italy", "Random"])
        self.nat_cb.setCurrentText("Aleatorio" if self.current_language=="ES" else "Random")
        self.nat_cb.currentIndexChanged.connect(self.on_nationality_change)
        nat_layout.addWidget(self.nat_label)
        nat_layout.addWidget(self.nat_cb)
        options_layout.addLayout(nat_layout)
        
        # Selection of the number of first names and surnames
        names_layout = QHBoxLayout()
        self.names_label = QLabel(translations[self.current_language]["nombres"])
        self.first_names_cb = QComboBox()
        self.first_names_cb.addItems(["1", "2"])
        self.first_names_cb.setFixedWidth(50)
        
        self.surnames_label = QLabel(translations[self.current_language]["apellidos"])
        self.last_names_cb = QComboBox()
        self.last_names_cb.addItems(["1", "2"])
        self.last_names_cb.setFixedWidth(50)
        
        names_layout.addWidget(self.names_label)
        names_layout.addWidget(self.first_names_cb)
        names_layout.addWidget(self.surnames_label)
        names_layout.addWidget(self.last_names_cb)
        options_layout.addLayout(names_layout)
        
        # Variation radius slider (for geographic variation)
        radio_layout = QVBoxLayout()
        self.radius_label = QLabel(translations[self.current_language]["radio"])
        self.radius_slider = QSlider(Qt.Orientation.Horizontal)
        self.radius_slider.setRange(0, 50)
        self.radius_slider.setValue(2)
        radio_layout.addWidget(self.radius_label)
        radio_layout.addWidget(self.radius_slider)
        options_layout.addLayout(radio_layout)
        
        # Buttons to import custom name and surname dictionaries
        dict_group = QGroupBox()
        dict_layout = QHBoxLayout(dict_group)
        self.import_names_btn = ImportButton(translations[self.current_language]["import_nombres"], self.import_names)
        self.import_names_btn.clicked.connect(self.open_names_file)
        self.import_surnames_btn = ImportButton(translations[self.current_language]["import_apellidos"], self.import_surnames)
        self.import_surnames_btn.clicked.connect(self.open_surnames_file)
        dict_layout.addWidget(self.import_names_btn)
        dict_layout.addWidget(self.import_surnames_btn)
        options_layout.addWidget(dict_group)
        
        # Button to generate identities
        self.generate_btn = QPushButton(translations[self.current_language]["generar"])
        self.generate_btn.clicked.connect(self.generate)
        options_layout.addWidget(self.generate_btn)
        
        left_layout.addWidget(self.options_group)
        
        # Output display area (read-only text area with drag-and-drop support)
        self.output_text = DraggableTextEdit()
        self.output_text.setReadOnly(True)
        left_layout.addWidget(self.output_text, stretch=1)
        
        # Progress bar for the generation process (hidden by default)
        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximum(100)
        self.progress_bar.setVisible(False)
        self.progress_bar.setStyleSheet("QProgressBar::chunk { background: #115190; }")
        self.progress_bar.setTextVisible(False)
        left_layout.addWidget(self.progress_bar)
        
        # Buttons for copying, resetting, and closing the application
        btn_layout = QHBoxLayout()
        self.copy_btn = QPushButton(translations[self.current_language]["copiar"])
        self.copy_btn.clicked.connect(self.copy_output)
        self.new_btn = QPushButton(translations[self.current_language]["nueva_generacion"])
        self.new_btn.clicked.connect(self.reset)
        self.exit_btn = QPushButton(translations[self.current_language]["cerrar"])
        self.exit_btn.clicked.connect(self.close)
        btn_layout.addWidget(self.copy_btn)
        btn_layout.addWidget(self.new_btn)
        btn_layout.addWidget(self.exit_btn)
        left_layout.addLayout(btn_layout)
        
        main_hlayout.addWidget(left_widget, stretch=1)
        
        # Right panel: Map view and address display
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(5, 5, 5, 5)
        right_layout.setSpacing(5)
        self.map_view = QWebEngineView()
        self.map_view.setHtml(self.get_map_html())
        self.map_view.setFixedWidth(300)
        self.map_view.setMinimumHeight(300)
        right_layout.addWidget(self.map_view)
        self.map_address_label = QLabel("No se ha seleccionado ubicación")
        self.map_address_label.setWordWrap(True)
        self.map_address_label.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        right_layout.addWidget(self.map_address_label)
        main_hlayout.addWidget(right_widget)
        
        # Configure QWebChannel to connect the map with the application
        self.map_bridge = MapBridge()
        channel = QWebChannel(self.map_view.page())
        channel.registerObject('mapBridge', self.map_bridge)
        self.map_view.page().setWebChannel(channel)
        self.map_bridge.coordinatesReceived.connect(self.handle_map_coordinates)
        
        self.on_gender_change()
    
    def get_map_html(self):
        """
        Returns the HTML content for the embedded map view.
        
        The HTML includes the necessary Leaflet libraries and sets up a basic map.
        Double-clicking on the map sends the coordinates back to the application.
        """
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8" />
            <title>Map</title>
            <link rel="stylesheet" href="https://unpkg.com/leaflet/dist/leaflet.css"/>
            <script src="https://unpkg.com/leaflet/dist/leaflet.js"></script>
            <script src="qrc:///qtwebchannel/qwebchannel.js"></script>
            <style>
              html, body, #map { width: 100%; height: 100%; margin: 0; padding: 0; }
            </style>
        </head>
        <body>
        <div id="map"></div>
        <script>
          new QWebChannel(qt.webChannelTransport, function(channel) {
            window.mapBridge = channel.objects.mapBridge;
          });
          var map = L.map('map').setView([40.7128, -74.0060], 5);
          L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', { maxZoom: 19 }).addTo(map);
          map.on('dblclick', function(e) {
            var lat = e.latlng.lat;
            var lon = e.latlng.lng;
            if (window.mapBridge) {
                window.mapBridge.sendCoordinates(lat, lon);
            }
          });
        </script>
        </body>
        </html>
        """
        return html
    
    def handle_map_coordinates(self, lat, lon):
        """
        Receives coordinates from the map view and updates the address label.
        
        :param lat: Latitude received from the map.
        :param lon: Longitude received from the map.
        """
        address = reverse_geocode(lat, lon)
        self.update_map_address(address, lat, lon)
    
    def update_map_address(self, address, lat, lon):
        """
        Updates the map address label and stores the center coordinates.
        
        :param address: The human-readable address.
        :param lat: Latitude value.
        :param lon: Longitude value.
        """
        self.map_address_label.setText("Centro: " + address)
        self.center_coords = (lat, lon)
    
    def on_gender_change(self):
        """
        Adjusts the visibility of certain controls based on the selected gender.
        
        If the gender is set to 'random', the male percentage slider is shown;
        otherwise, import buttons for custom dictionaries are displayed.
        """
        if self.gender_cb.currentText().lower() in ["aleatorio", "random"]:
            self.male_slider_label.setVisible(True)
            self.male_slider.setVisible(True)
            self.import_names_btn.hide()
            self.import_surnames_btn.hide()
        else:
            self.male_slider_label.setVisible(False)
            self.male_slider.setVisible(False)
            self.import_names_btn.show()
            self.import_surnames_btn.show()
    
    def on_nationality_change(self):
        """
        Changes the view of the map based on the selected nationality.
        
        Centers the map on predefined coordinates corresponding to the chosen country.
        """
        nationality = self.nat_cb.currentText()
        country_coords = {
            "United States": [39.8283, -98.5795],
            "Spain": [40.0, -4.0],
            "United Kingdom": [55.3781, -3.4360],
            "Germany": [51.1657, 10.4515],
            "France": [46.6034, 1.8883],
            "Italy": [41.8719, 12.5674]
        }
        if nationality in country_coords:
            lat, lon = country_coords[nationality]
            js_code = f"map.setView([{lat}, {lon}], 5);"
            self.map_view.page().runJavaScript(js_code)
    
    def generate(self):
        """
        Gathers the parameters from the user interface and generates random person identities.
        
        The output is formatted and either appended to a loaded file or auto-saved.
        """
        qty = self.qty_spin.value()
        gender = self.gender_cb.currentText()
        nationality = self.nat_cb.currentText()
        male_percentage = self.male_slider.value() if gender.lower() in ["aleatorio", "random"] else 50
        radius_km = self.radius_slider.value() if self.center_coords is not None else None
        num_first_names = int(self.first_names_cb.currentText())
        num_last_names = int(self.last_names_cb.currentText())
        persons = generate_persons(qty, nationality, gender, self.center_coords, male_percentage, radius_km,
                                   self.names_dictionary, self.surnames_dictionary, num_first_names, num_last_names)
        output = format_persons(persons, self.current_language)
        self.generated_output = output
        self.run_progress(self.after_progress_complete)
    
    def run_progress(self, callback):
        """
        Initiates a progress bar animation and calls the specified callback when complete.
        
        :param callback: A function to execute after the progress completes.
        """
        self.output_text.setVisible(False)
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(True)
        self.progress_value = 0
        self.timer = QTimer()
        self.timer.timeout.connect(lambda: self.update_progress(callback))
        self.timer.start(100)
    
    def update_progress(self, callback):
        """
        Updates the progress bar. Once it reaches 100%, stops the timer and executes the callback.
        
        :param callback: The function to call after completion.
        """
        self.progress_value += 5
        if self.progress_value > 100:
            self.timer.stop()
            self.progress_bar.setVisible(False)
            self.output_text.setVisible(True)
            callback()
        else:
            self.progress_bar.setValue(self.progress_value)
    
    def after_progress_complete(self):
        """
        Called after the progress bar completes to display the generated output.
        
        If a file was previously loaded, the new data is appended; otherwise, the output is auto-saved.
        """
        self.output_text.setPlainText(self.generated_output)
        if self.output_text.loaded_file_path:
            self.append_to_loaded_file()
        else:
            self.auto_save()
    
    def append_to_loaded_file(self):
        """
        Appends the generated data to the file that was previously loaded into the text area.
        """
        try:
            file_path = self.output_text.loaded_file_path
            with open(file_path, 'r', encoding='utf-8') as f:
                old_content = f.read()
            new_content = old_content.strip() + "\n" + self.generated_output
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            QMessageBox.information(self, "Archivo Actualizado", f"Datos actualizados en:\n{file_path}")
            self.output_text.setPlainText(new_content)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo actualizar el archivo:\n{e}")
    
    def auto_save(self):
        """
        Prompts the user to select a location and saves the generated output to a text file.
        """
        file_path, _ = QFileDialog.getSaveFileName(self, "Guardar datos", os.getcwd(), "Archivos de texto (*.txt)")
        if file_path:
            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(self.generated_output)
                QMessageBox.information(self, "Guardado", f"Datos guardados en:\n{file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo guardar el archivo:\n{e}")
    
    def copy_output(self):
        """
        Copies the generated output from the text area to the clipboard.
        """
        output = self.output_text.toPlainText().strip()
        if output:
            clipboard = QApplication.clipboard()
            clipboard.setText(output)
            QMessageBox.information(self, "Copiado", "Datos copiados.")
        else:
            QMessageBox.warning(self, "Sin datos", "No hay datos para copiar.")
    
    def reset(self):
        """
        Resets the user interface to its default state, clearing all inputs and outputs.
        """
        self.qty_spin.setValue(10)
        if self.current_language == "ES":
            self.gender_cb.setCurrentText("Aleatorio")
        else:
            self.gender_cb.setCurrentText("Random")
        self.on_gender_change()
        self.nat_cb.setCurrentText("Aleatorio" if self.current_language=="ES" else "Random")
        self.map_address_label.setText("No se ha seleccionado ubicación")
        self.center_coords = None
        self.output_text.clear()
        self.output_text.loaded_file_path = None
        self.map_view.page().runJavaScript("map.setView([40.7128, -74.0060], 5);")
    
    def import_names(self, content, file_path):
        """
        Imports a custom dictionary of first names from a text file.
        
        :param content: The file content as a string.
        :param file_path: The path of the file.
        """
        self.names_dictionary = [line.strip() for line in content.splitlines() if line.strip()]
        QMessageBox.information(self, "Importación", f"Diccionario de nombres importado desde:\n{file_path}")
    
    def import_surnames(self, content, file_path):
        """
        Imports a custom dictionary of surnames from a text file.
        
        :param content: The file content as a string.
        :param file_path: The path of the file.
        """
        self.surnames_dictionary = [line.strip() for line in content.splitlines() if line.strip()]
        QMessageBox.information(self, "Importación", f"Diccionario de apellidos importado desde:\n{file_path}")
    
    def open_names_file(self):
        """
        Opens a file dialog to allow the user to select a text file containing first names.
        """
        file_path, _ = QFileDialog.getOpenFileName(self, "Importar Diccionario de Nombres", os.getcwd(), "Archivos de texto (*.txt)")
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                self.import_names(content, file_path)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo cargar el archivo:\n{e}")
    
    def open_surnames_file(self):
        """
        Opens a file dialog to allow the user to select a text file containing surnames.
        """
        file_path, _ = QFileDialog.getOpenFileName(self, "Importar Diccionario de Apellidos", os.getcwd(), "Archivos de texto (*.txt)")
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                self.import_surnames(content, file_path)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo cargar el archivo:\n{e}")
    
    def change_language(self, lang):
        """
        Changes the language of the interface and updates all text labels accordingly.
        
        :param lang: The language code ('ES' or 'EN').
        """
        self.current_language = lang
        self.update_translations()
    
    def update_translations(self):
        """
        Updates the text of all user interface elements based on the selected language.
        """
        t = translations[self.current_language]
        self.setWindowTitle(t["window_title"])
        self.options_group.setTitle(t["options_group"])
        self.qty_label.setText(t["cantidad"])
        self.gender_label.setText(t["genero"])
        self.male_slider_label.setText(t["porcentaje_hombres"])
        self.nat_label.setText(t["nacionalidad"])
        self.names_label.setText(t["nombres"])
        self.surnames_label.setText(t["apellidos"])
        self.radius_label.setText(t["radio"])
        self.import_names_btn.setText(t["import_nombres"])
        self.import_surnames_btn.setText(t["import_apellidos"])
        self.generate_btn.setText(t["generar"])
        self.copy_btn.setText(t["copiar"])
        self.new_btn.setText(t["nueva_generacion"])
        self.exit_btn.setText(t["cerrar"])
        if self.current_language == "EN":
            self.language_label.setText("Language:")
        else:
            self.language_label.setText("Idioma:")
        self.nat_cb.clear()
        if self.current_language == "ES":
            self.nat_cb.addItems(["United States", "Spain", "United Kingdom", "Germany", "France", "Italy", "Aleatorio"])
            self.nat_cb.setCurrentText("Aleatorio")
        else:
            self.nat_cb.addItems(["United States", "Spain", "United Kingdom", "Germany", "France", "Italy", "Random"])
            self.nat_cb.setCurrentText("Random")
        self.update_gender_items()
    
    def update_gender_items(self):
        """
        Updates the gender selection combo box based on the current language.
        """
        current = self.gender_cb.currentText().lower()
        self.gender_cb.clear()
        self.gender_cb.addItems(translations[self.current_language]["gender_items"])
        if "masculino" in current or "male" in current:
            self.gender_cb.setCurrentIndex(0)
        elif "femenino" in current or "female" in current:
            self.gender_cb.setCurrentIndex(1)
        else:
            self.gender_cb.setCurrentIndex(2)
    
    def show_help(self):
        """
        Opens the help dialog to display usage information.
        """
        help_dialog = HelpDialog(self.current_language, self)
        help_dialog.exec()
    
    def mousePressEvent(self, event):
        """
        Captures the mouse press event to allow the window to be draggable.
        """
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()
    
    def mouseMoveEvent(self, event):
        """
        Updates the window position based on mouse movement while dragging.
        """
        if event.buttons() == Qt.MouseButton.LeftButton and self._drag_pos:
            self.move(event.globalPosition().toPoint() - self._drag_pos)
            event.accept()

# =============================================================================
# Main Execution Block
# =============================================================================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(resource_path("rubber_ducky.ico")))
    # Display the splash screen with a progress bar
    splash = SplashScreen()
    splash.exec()  # Wait until the splash screen is closed
    global app_window
    app_window = MainWindow()
    app_window.setWindowIcon(QIcon(resource_path("rubber_ducky.ico")))
    app_window.show()
    sys.exit(app.exec())
