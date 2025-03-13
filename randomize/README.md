# Randomize

**Randomize** is a powerful tool designed to create unpredictable, randomized directory structures for penetration testing, red teaming, and dynamic project simulations. Perfect for cybersecurity professionals and creative developers who need to emulate real-world scenarios with varied project layouts.

## Overview

Randomize leverages randomness to generate folder hierarchies that simulate the complexity and unpredictability of actual systems. With a focus on flexibility and performance, it can be seamlessly integrated into your workflow to test and develop security solutions or simply to experiment with creative directory structures.

## Features

- **Customizable Randomization:** Configure maximum depth, the number of folders per level, and even a seed for reproducible results.
- **Effortless Integration:** Designed as a modular component, Randomize can easily be incorporated into larger projects or automated pipelines.
- **High Performance:** Optimized for speed and efficiency, even when generating complex structures.
- **Cross-Platform Compatibility:** Works on Windows, macOS, and Linux.
- **Modular Design:** Easily extendable for advanced customization and integration into your existing tools.

## Usage

Integrate Randomize into your workflow with minimal setup:

1. **Run the Script:**  
   Execute the module from the command line:
   ```bash
   python randomize.py --depth 4 --max-folders 3 
   ```
   
2. ```--depth``` <n>: Maximum directory depth.<br>
```--max-folders``` <n>: Maximum folders per level.<br>
```--seed <value>:``` (Optional) Seed for reproducible results.

3. Programmatic Integration:<br> Import the module into your own scripts to generate random directory trees dynamically.

## Examples

Generate a structure with a maximum depth of 5 and up to 4 folders per level:
 ```bash
python randomize.py --depth 5 --max-folders 4
```
This command produces a unique directory layout every time (or reproducible if a seed is provided).
