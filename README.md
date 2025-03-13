# Randomize Project

[![GitHub stars](https://img.shields.io/github/stars/eyver0day/randomize-project?style=social)](https://github.com/eyver0day/randomize-project/stargazers)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Randomize Project is a versatile tool designed to generate random project structures tailored for penetration testers, red teamers, and cybersecurity professionals. This tool helps you quickly create unpredictable directory templates that simulate real-world project environments, sparking creative solutions for security testing and development.

---

## Overview

In the dynamic field of cybersecurity, predictable project structures can limit creativity and hinder realistic simulations. Randomize Project allows you to generate a randomized directory tree with customizable parameters, enabling you to test, develop, and audit security solutions in environments that mimic the chaos of real-world scenarios.

Whether you need to create a randomized template for a new pentesting engagement or simply want to experiment with diverse project setups, Randomize Project streamlines the process, so you can focus on the critical challenges.

---

## Features

- **Randomized Directory Structures**  
  Generate unpredictable folder hierarchies to simulate various project environments.
- **Customizable Templates**  
  Configure parameters like maximum depth and the number of folders per level to tailor the output.
- **Seamless Integration**  
  Easily integrate the generated structure into your pentesting and red teaming workflows.
- **Lightweight & Fast**  
  Optimized for speed and efficiency without unnecessary overhead.
- **Open-Source & Community Driven**  
  Collaborate, contribute, and customize the project to fit your needs.

---

## Installation

### Prerequisites
- Python 3.8 or higher

### Steps
1. **Clone the repository:**
    ```bash
    git clone https://github.com/eyver0day/randomize-project.git
    cd randomize-project
    ```
2. **(Optional) Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    # On Windows:
    venv\Scripts\activate
    # On macOS/Linux:
    source venv/bin/activate
    ```
3. **Install required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

---

## Usage

Run the tool from the command line:
```bash
python randomize.py [options]
```

## Options

- `--depth <n>`: Set the maximum depth of the directory structure.
- `--max-folders <n>`: Limit the maximum number of folders per level.
- `--seed <value>`: Provide a seed for reproducible randomization (optional).

**Example:**
```bash
python randomize.py --depth 4 --max-folders 3
```

This command generates a random project structure with a maximum depth of 4 and up to 3 folders per level.


## Download

The latest version of Randomize Project is available for download:

📥 **[Download the Installer](https://mega.nz/folder/IMwVUC6R#hi-229UW1S7b69AM3dlhmg)**  
💾 **Alternative:** [Google Drive](https://drive.google.com/file/d/1MrCQx06nljgQ1o69NM3kukMPl2J7Qjx0/view?usp=sharing)  

For manual installation, follow the steps in the [Installation](#installation) section.


## Documentation

For comprehensive documentation, check out our [Wiki](https://github.com/eyver0day/randomize-project/wiki) or refer to the `docs/` directory, where you’ll find detailed guides, examples, and customization instructions.

## Contributing

Contributions are welcome! If you have ideas for improvements, want to fix a bug, or add a new feature, please follow our contribution guidelines:

- **Submit Issues:** Report bugs or feature requests on our [Issues page](https://github.com/eyver0day/randomize-project/issues).
- **Pull Requests:** We appreciate clean and well-documented pull requests. See [CONTRIBUTING.md](CONTRIBUTING.md) for more details.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

- **GitHub:** [@eyver0day](https://github.com/eyver0day)
- **Email:** 59qgj458@anonaddy.me

> **Note:**  
> Whether you're a seasoned pentester or just starting out in cybersecurity, Randomize Project empowers you to break away from predictable setups and explore creative, realistic environments for testing and development.  
> If you find this project useful, please give it a star ⭐ and share it with your network. Your support helps drive innovation and continuous improvement in the cybersecurity community.

*Optimized for efficiency, creativity, and community collaboration — because in cybersecurity, innovation is key!*
