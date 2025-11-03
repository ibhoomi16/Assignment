# AI-Powered Gantt Charts Assistant

Simpler, faster, and more reliable Gantt charts — powered by AI.

## Overview

This project is an AI-driven assistant to help you plan projects and visualize timelines using Gantt charts. Describe your project in natural language, and the assistant automatically generates and visualizes Gantt charts. Powered by [agno](https://github.com/your-link-to-agno) for LLM interaction and [matplotlib](https://matplotlib.org/) for chart rendering.

## Features

- 🧠 AI agent that understands project timelines described in natural language.
- 📊 Automatic Gantt chart generation with customizable durations (days/weeks/months).
- 💾 Persistent conversation history across sessions.
- 🧾 Custom tool integration for planning and visualization.
- 🖼️ Export charts as PNG files for easy sharing.

## Installation

1. Clone this repository:
   ```sh
   git clone https://github.com/ibhoomi16/Assignment.git
   cd Assignment
   ```

2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   # Or install agno and matplotlib directly
   pip install agno matplotlib
   ```

## Usage

1. Run the assistant:
   ```sh
   python app.py
   ```

2. Describe your project (e.g.):
   ```
   "Create a website in a week"
   ```

3. The assistant will generate a Gantt chart visualization and save it as a PNG file.

