# particle_filter_lab
Particle filter visualization for Stepik course

To create a robot object use
```
myrobot = Robot.Robot(False)
```
or use
```
particle = Robot.Robot(True)
```
to create a particle object.

To change the navigation parameters of the robot (or a particle) you can set them directly with
```
myrobot.set(200, 200, 0.0)
```
Likewise you can set noise parameters:
```
myrobot.set_noise(0.5, 0.1, 15.0)
```

To perform a motion update use
```
myrobot = myrobot.move(angle, distance)
```
And to get measurements use
```
Z = myrobot.sense()
```
