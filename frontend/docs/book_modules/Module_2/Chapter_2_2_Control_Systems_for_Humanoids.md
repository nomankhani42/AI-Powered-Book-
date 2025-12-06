---
week: 2
sidebar_position: 2
---

# Chapter 2.2: Control Systems for Humanoids

## The Challenge of Humanoid Control

Controlling humanoid robots is a complex task due to their high degrees of freedom, inherent instability (especially during bipedal locomotion), and the need for dynamic interaction with diverse environments.

## Hierarchical Control Architectures

Most humanoid control systems employ a hierarchical structure:

1.  **High-Level Planning**: Deals with long-term goals, task sequencing, and path planning (e.g., "walk to the door," "pick up the object").
2.  **Mid-Level Control (Motion Generation)**: Translates high-level plans into desired trajectories for the robot's center of mass, foot placements, and joint angles. This often involves:
    *   **Zero Moment Point (ZMP)**: A concept used to maintain dynamic balance during walking.
    *   **Whole-Body Control (WBC)**: Optimally coordinates all robot joints to achieve multiple tasks simultaneously (e.g., balance, reaching, obstacle avoidance).
3.  **Low-Level Control (Joint Control)**: Executes the desired joint trajectories by applying appropriate motor commands. This typically involves PID (Proportional-Integral-Derivative) controllers or more advanced methods.

## Key Control Strategies

*   **Position Control**: The most basic form, where each joint is commanded to a specific angle.
*   **Velocity Control**: Commands the speed of joint movement.
*   **Torque/Force Control**: Directly commands the forces or torques at the joints or end-effectors, crucial for compliant interaction and manipulation.
*   **Impedance Control**: A hybrid approach that regulates the relationship between force and displacement, allowing for controlled compliance during physical interactions.

## Balance and Locomotion

Maintaining balance is paramount for humanoid robots. Strategies include:

*   **Static Balance**: Maintaining the center of gravity within the support polygon (for standing or very slow movements).
*   **Dynamic Balance**: Utilizing momentum and active control to maintain balance during walking, running, or pushing.
*   **Model Predictive Control (MPC)**: Predicts future states of the robot and environment to optimize control inputs over a receding horizon, excellent for dynamic tasks.

## Sensor Fusion

Effective control relies on fusing data from various sensors (IMUs, force sensors, vision) to get an accurate estimate of the robot's state and environment. Kalman filters and Extended Kalman Filters are commonly used for this.