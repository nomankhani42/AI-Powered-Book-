---
week: 1
sidebar_position: 2
---

# Chapter 1.2: Sensor Modalities for Robotics

## The Role of Sensors

Sensors are the "eyes" and "ears" of a robot, providing crucial information about its internal state and the external environment. The choice of sensors depends heavily on the robot's intended application and the environmental conditions it will operate in.

## Common Sensor Types

### Proprioceptive Sensors
These sensors measure the robot's internal state.
*   **Encoders**: Measure joint positions and velocities.
*   **IMUs (Inertial Measurement Units)**: Provide orientation, angular velocity, and linear acceleration.
*   **Force/Torque Sensors**: Measure forces and torques applied to the robot's links or end-effectors.

### Exteroceptive Sensors
These sensors gather information about the robot's environment.
*   **Cameras (Vision Systems)**:
    *   **Monocular Cameras**: Provide 2D images, used for object recognition, tracking, and visual servoing.
    *   **Stereo Cameras**: Mimic human binocular vision to provide depth perception.
    *   **RGB-D Cameras**: (e.g., Intel RealSense, Microsoft Azure Kinect) Provide color images along with per-pixel depth information.
*   **Lidar (Light Detection and Ranging)**:
    *   Measures distances by illuminating targets with laser light and analyzing the reflected light.
    *   Generates 2D or 3D point clouds, essential for mapping and navigation.
*   **Ultrasonic Sensors**:
    *   Use sound waves to measure distances to objects.
    *   Cost-effective for obstacle detection, but lower resolution than Lidar.
*   **Tactile Sensors**:
    *   Provide information about contact forces, pressure distribution, and texture.
    *   Crucial for dexterous manipulation and safe human-robot interaction.
*   **Microphones (Auditory Sensors)**:
    *   Detect sound for speech recognition, sound source localization, and environmental awareness.