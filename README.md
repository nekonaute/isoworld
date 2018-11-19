World of Isotiles
=================

**Wofi** is a light-weight (non-optimised) implementation for creating isometric worlds. It features multi-level terrains with altitude, objects and agents. The code is primarily developed as a teaching material for the coding project on artificial life "2i013, projet: Vie Artificielle", part of the bachelor in computer science at Sorbonne Université (SU). This code is provided as an entry point to develop more complex projects including dynamic environments (e.g. forest fires, ecological changes) and species interactions (e.g. predator-prey dynamics, dynamic path planning), though you can probably develop simple games with it too.

* Author: *nicolas.bredeche(at)sorbonne-universite.fr*
* Started: *2018-11-17*
* Licence: CC-BY-SA -- *feel free to do whatever you want, but cite source.*

Installation and Running
========================

* **Dependencies**: Python3, Pygame
* **Running**: *python3 isoworld.py*

Snapshot
========

![Wofi screenshot](https://github.com/nekonaute/isoworld/blob/master/data/snapshot.png)

Credits for third party resources
=================================

**Assets**: https://www.kenney.nl/ (*great assets by Kenney Vleugels with public domain license*)

Benchmarking
============

Method:
* (1) in the console: **python3 demo_20181119_12h45.py**
* (2) wait for at least 3 FPS updates (see console), exit (press ESC in window), then record final line with fps count (line starts with "[Quit]")

Data:
* Macbook pro, Early 2015, 3.1ghz Intel Core i7, 16 GB RAM, Intel Iris Graphics 6100: 10.272582194960501 fps (2018-11-19)

*Hint: an efficient and quite easy way to optimise running speed is to redraw only cells that have changed inbetween updates, rather than the whole world (which is the current method).*
