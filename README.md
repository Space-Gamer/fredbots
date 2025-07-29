# FRedBots: Fundamental Reinforcement Learning Enabled Bots

## Introduction

**FRedBots** (Fundamental Reinforcement Learning Enabled Bots) is a multi-robot autonomous warehouse delivery system powered by **Q-learning** and the **Robot Operating System (ROS)**.

With the increasing demand for automation in logistics, our system tackles two of the most critical challenges in warehouse robotics:
- **Optimal path planning**
- **Efficient task coordination**

This project demonstrates how **reinforcement learning (RL)**—specifically Q-learning—can be used to:
- Enable autonomous mobile robots (AMRs) to navigate complex environments
- Avoid obstacles and deadlocks in real-time
- Efficiently schedule and distribute package delivery tasks across multiple agents

By integrating Q-learning with ROS in a simulated Gazebo environment, FRedBots showcases:
- Smart route learning via reward-based feedback
- A local controller to prevent collisions between agents
- A task scheduler that dynamically assigns jobs based on location and priority

> 🧠 In short, FRedBots presents a modular, scalable, and intelligent approach to warehouse automation using model-free reinforcement learning.

## Publication

This project was presented in the **ICCCR 2025: 5th International Conference on Computer, Control and Robotics**.  
[Read the paper here](https://doi.org/10.1109/ICCCR65461.2025.11072598)

## Authors

1. [Pradeep J](https://github.com/Space-Gamer)
2. [Ashvin Bhat](https://github.com/ashvinbhat)
3. [Amulya Marali](https://github.com/amulyamarali)
4. [Rohan Mahesh Rao](https://github.com/Rohanmrao)
5. [Sriram Radhakrishna](https://github.com/sr42-dev)
6. Rajasekar Mohan

## Demo

[![Watch the video](https://img.youtube.com/vi/HnlNoSQTMtw/0.jpg)](https://www.youtube.com/watch?v=HnlNoSQTMtw)


## Problem Statement

Design and implement a reinforcement learning algorithm for
task scheduling in a collaborative robotic
system, with a focus on package
transportation within warehouses. The goal is
to improve efficiency and reduce the number
of deadlocks, while operating in a
non-deterministic environment.

## Abstract

Autonomous systems have undergone a revolutionary transformation with the advent of artificial intelligence
and machine learning, namely reinforcement learning (RL).
This research investigates the use of Q-learning in warehouse
automation and autonomous mobile robot (AMR) navigation. It
uses the ROS (Robot Operating System) to tackle the problems of
job scheduling and deadlock avoidance, demonstrating the revolutionary power of RL in dynamic situations. We demonstrate
effective job coordination and obstacle avoidance by integrating
Q-learning with ROS, highlighting the potential for AI-driven
solutions to improve operational efficiency in warehouses which
includes optimized path planning strategies.

## Implementation

The **FRedBots** project integrates **Q-learning** and the **Robot Operating System (ROS)** to build an intelligent, multi-robot package delivery system designed for dynamic warehouse environments.


### 1. Robot Navigation Using Q-Learning

We model the warehouse as a `21×21` grid environment and use Q-learning to enable autonomous path planning.

- **States**: Each grid cell represents a unique state `(i, j)`.
- **Actions**: `{Up, Right, Down, Left}` corresponding to `{0, 1, 2, 3}`.
- **Rewards**:
  - `+100` for reaching the goal
  - `-100` for hitting an obstacle
  - `-1` for each move (to promote shorter paths)

The Q-values `Q(s, a)` are updated using the Bellman equation, and action selection is driven by an **epsilon-greedy policy** to balance exploration and exploitation.

A **negative Euclidean reward gradient** ensures the robot learns the most efficient routes, while harsh penalties deter obstacle collisions.

### 2. Real-Time Path Planning

When a new package is introduced:
- It is dynamically assigned to a free robot.
- The robot trains a Q-learning agent in real time to find the optimal delivery path.
- The learned `Q-table` is used to make navigation decisions based on maximizing cumulative rewards.

### 3. Collision & Deadlock Avoidance

To manage multi-robot coordination and prevent conflicts, we implement a ROS service called `local_controller`:

- Maintains a global **occupancy grid**.
- Each robot must request permission to move to a new cell.
- If the cell is occupied, the robot waits or selects an alternative route.
- This ensures no two robots occupy the same cell at any time, avoiding deadlocks and collisions.

### 4. Task Scheduling

A second ROS service, `tasker`, is responsible for assigning delivery tasks to robots efficiently:

- Robots request assignments dynamically.
- A **utility score** is calculated for each available task based on:
  - Distance to pickup location
  - Task priority
- The scheduler assigns the highest-utility task to the requesting robot.
- A user-friendly **GUI** and **CLI** allow real-time monitoring and task management.

### 5. ROS Integration

The entire system is built around ROS for modularity and scalability:

- **ROS Topics**:
  - Used for odometry updates and motion commands (`/cmd_vel`, etc.).
- **ROS Services**:
  - `local_controller`: Manages deadlock avoidance.
  - `tasker`: Handles intelligent task scheduling.

ROS enables asynchronous communication and easy integration of multiple nodes, making the FRedBots architecture extensible and simulation-friendly.

## Running the Project

### Requirements
- **Ubuntu 20.04** (or compatible version)
- **ROS Noetic** (or compatible version)
- **Gazebo** (for simulation)
- **Python 3** (for Q-learning implementation)

To run the FRedBots project, follow these steps:
1. Clone the repository in the `src` directory of your catkin workspace using the following command
```bash
git clone https://github.com/Space-Gamer/FRedBots.git
```
2. Navigate to the root of your catkin workspace and build the project using the following commands
```bash
catkin_make
source devel/setup.bash
```
3. Launch the Gazebo simulation environment with the following command
```bash
roslaunch fredbots final_ql.launch
```
---
Note: This project was developed as part of the [PES Innovation Lab](https://www.theinnovationlab.in/) Summer Internship 2023.
