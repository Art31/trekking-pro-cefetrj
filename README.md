<div align="center">
  <img src="https://user-images.githubusercontent.com/34986200/50385772-207d1080-06c2-11e9-9d39-1e848a18d02a.jpg" width="50%" height="50%" ><br><br>
</div>

# Autonomous Robot for Traffic Cone Detection

English: This is an amateur autonomous robot project developed by the trekking robotics team at CEFET-RJ. It uses tensorflow and python to recognize traffic cones for a competition. The rules for the competition are available in portuguese.

Português: Esse repositório contém todo o desenvolvimento por trás do robo autonomo capaz de reconhecer cones. Ele foi desenvolvido pelos membros da equipe do ramo IEEE CEFET-RJ em 2018.1 para competir na modalidade trekking pro da winter challenge. O manual se encontra [aqui](other_files/robocore_regras_robo_trekking.pdf).

The [Mechanics](Mechanics) page contains a step by step description about the process of building the robot with photos.

The [Electronics](Electronics) folder holds information regarding the schematics of the robot and an explanation of how we conceived it.

The [Image_Processing](Image_Processing) page provides a step by step description regarding the process of training a CNN for object detection and optimizing average precision, with the source tutorials properly mentioned. Also we will explain in detail how we managed to build our own dataset and label it using LabelImg.

The [Sensoring_and_Reacting](Sensoring_and_Reacting) contains details about how we read sensors like Ultrasonic, GPS, Camera, encoder and Gyroscope. We wrote code for a range of sensors but we didnt use them all in our robot, those will be properly signalled during the description.

## Contribution guidelines

If you want to contribute or give us any suggestion, we will be happy to hear it.

## License

[Apache License 2.0](LICENSE)
