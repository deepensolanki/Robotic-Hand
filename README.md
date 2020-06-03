# Robotic-Hand

This was a term-project for EECS452 Digital Signal Processing at UMich. This project, "Hand it Over", is a Robotic Hand based Real Time Human Hand Emulator. The following components are involved:

1) Raspberry Pi and Pi Camera
2) A (preferrably black) glove with distinctly colored fingertips
3) A 3D printed human hand (All parts were printed and assembled as per instructions from http://inmoov.fr/hand-and-forarm/)
4) Arduino Uno and Stepper Motors

The Raspberry Pi and Pi Camera are placed at about 60-80cm above the human hand such that the entire palm and wrist area is in view. The Pi processes this information and converts that into stepper coordinates. These coordinates are sent to an Arduino Uno via SPI. The servo motors are present on the 3D printed human hand model and actuate the fingers and wrist. 

NOTE - Use file "hand_pre.py" to calibrate and find the HSV ranges for each fingertip color. Feed those to the "hand_final_complete.py" in the DetectObject function for each finger.    
