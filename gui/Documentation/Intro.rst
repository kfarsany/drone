.. _top:

*************************
Drime Drone Documentation
*************************
The following documentation provides an overview of quadcopter
fundamentals and relevant applications in the Drimage Drone.

.. note:: Research has been pulled from multiple sources. References can be viewed here: :doc:`Documentation/references.rst`

.. note::  This documentation aims to conceptually explain the quadcopter without exhaustive mathematical models and derivations.

.. warning:: Citations are currently being added. More resources may be added. Click to scroll through the documentation.

########################
Quadcopter Fundamentals: 
########################

Introduction
************

Back to top_

A quadrotor helicopter (quadcopter) is a helicopter which has four equally spaced
rotors. In the case of the Drimage Drone, a variant the X-Frame was used [1]. 

.. image:: Documentation/images/quad_frame.jpg
    :width: 400px
    :align: left
    :height: 400px
    :alt: Quadcopter X Frame

*Drimages Drone Frame*

The following table lists the advantages and disadvantages of the two most
common frames.

+-------------------------+------------------------+
| **X Frame**             | **H Frame**            |
+=========================+========================+
| Ideal Center of Gravity | Long and Spaceous Body |
+-------------------------+------------------------+
| Lighter                 | Easier to build        |
+-------------------------+------------------------+
| More Agile              | ---                    |
+-------------------------+------------------------+

A quadcopter is controlled by varying the rotation speed of each motor. The front motor (Mf) and back motor (Mb) pair are in the CW direction, while the right motor (Mr) and the left motor (Ml) are in the CCW direction [2].

.. image:: Documentation/images/quad_concept.png
    :width: 400px
    :align: left
    :height: 250px
    :alt: Quadcopter Concept
*Quadcopter Concept* [2]
 
 
Quadcopter movement is represented by throttle (altitude), yaw, pitch and roll. The controls are further explained through below.  *Refer to the figure below for a visual representation.*

.. image:: Documentation/images/quad_dynamics.png
    :width: 400px
    :align: left
    :height: 250px
    :alt: Quadcopter Dynamics
*Quadcopter Dynamics* [2]

 
**Throttle (Altitude)** Controls vertical up/down motion of the drone (Up is +, Down is -)

.. note:: Controlled by: Simultaneously increasing/decreasing speed of **all four** motors

**Yaw** Controls the side left/right motion of the drone (Right is +, Left is -)

.. note:: Controlled by: Simultaneously increasing/decreasing the **CW and CCW paired** motors. Represented by rotation about the z axis [3].

**Pitch** Controls the forward/backward tilt of the drone (Forward is +, Backward is -)

.. note:: Controlled by: Simultaneously increasing/decreasing the **front and back** motors. Represented by rotation about the y axis [3].

**Roll** Controls the left/right tilt of the drone (Right is +, Left is -)

.. note:: Controlled by: Simultaneously increasing/decreasing the **left and right** motors. Represented by rotation about the x axis [3].

.. warning:: Add 2.4 Aerodynamic forces and torques. Short intro about instability and use of PID controller by MPU 6050 and MultiWii firmware

Application
************

Back to top_

Four independent rotors presents a challenging problem as the quadcopter
exhibits innate instability. As a result, a well founded control design methodology
is necessary to control a quadcopter's motion.