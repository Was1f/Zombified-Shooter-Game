# 🧟‍♂️ Zombified - A 2D OpenGL Zombie Shooter Game

Zombified is a 2D top-down zombie shooter built entirely using OpenGL (PyOpenGL), with custom drawing done via the midpoint line and circle algorithms. The game uses no external assets — everything is rendered using raw `GL_POINTS`. Designed to demonstrate low-level graphics programming and algorithmic rendering in Python.

---

## 🎮 Gameplay Overview

- Fight waves of zombies (regular + special)
- Shoot bullets toward mouse click direction
- Rotate your player to aim in different directions
- Avoid zombies and keep your health up
- Blood splatter effects and scoring system
- Multiple difficulty levels and pause menu

---

## 🖼 Screenshot

> A glimpse of the gameplay below:

<p align="center">
  <img src="gameplayss.png" alt="Zombified Gameplay Screenshot" width="600">
</p>

---

## 🧪 Features

- 🔫 Shooting Mechanics with Rotation-based Aim
- 🧟 Randomly Spawning Zombies with AI Movement
- 🧠 Collision Detection (Player, Bullet, Zombie)
- 🩸 Dynamic Blood Splatter Effects
- 💡 No textures — all visuals created using midpoint line/circle algorithms
- ⏸ Pause Menu with Difficulty Toggle
- 🏠 Main Menu and Game Over Screens

---

## 🎮 Controls

| Action              | Key / Mouse      |
|---------------------|------------------|
| Move Up             | `W`              |
| Move Down           | `S`              |
| Move Left           | `A`              |
| Move Right          | `D`              |
| Rotate Gun CCW      | `J`              |
| Rotate Gun CW       | `K`              |
| Fire Bullet         | Left Mouse Click |

---

## 📦 Requirements

- Python 3.x
- PyOpenGL
- NumPy

### 🔧 Install dependencies:
```bash
pip install PyOpenGL PyOpenGL_accelerate numpy
```

---

## 🚀 Run the Game

```bash
python Zombified_main_game.py
```

---

## 📂 Project Structure

```text
📁 your-folder/
├── Zombified_main_game.py   # Main game code
└── gameplayss.png           # Screenshot (add yourself)
```

---

## ⚙️ Algorithms Used

- **Midpoint Line Drawing Algorithm**
- **Midpoint Circle Drawing Algorithm**
- **Zone-based Line Conversion**
- **Basic Vector Math for Rotation and Collision**

---

## 📌 Notes

- Built with educational purposes in mind
- No external art assets used
- No game engine — all logic done from scratch using Python and OpenGL

---

## 👨‍💻 Author

Developed by Wasif Khan  
BRAC University | Department of Computer Science and Engineering  
*Game coded manually using raw OpenGL & pixel-level control*

---

## 🧠 License

Feel free to use, modify, or expand this project. Attribution is appreciated!

---
