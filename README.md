# Elvis

## Introduction

This project is based on the "Elvis the dog" problem, also known as the weighted region problem.

In Euclidean space, the shortest path between any two points is a straight line. However, this does not imply that the *quickest* path between two points is a straight line. For example, when driving, nobody goes in a straight line; they follow the road's curvature.
Wouldn't it be faster to drive from point A to point B without turning?

Obviously not, since there would be obstacles in your path, _slowing_ you down. Worse, you would probably get in a wreck.

"Slowing" is the keyword here. The concept of velocity is what explains this distinction between the shortest path and the quickest path. The shortest path in space and the quickest path in time are seldom equivalent in real-world applications, because velocity fields may not be uniform. It is quicker to run forward than to backpedal. It is quicker to sail with the wind than against it.

One common optimization problem that occurs on a daily basis is minimizing time consumption. Intuitively, one would think that minimizing movement in space would minimize time consumption in moving from point A to point B. However, as we just illustrated, the problem is rarely that simple.

## The project

This project allows you to construct polyhedra and velocity sets associated with them in order to numerically solve quickest-path problems in n dimensions.

First, download and extract the zip file. Then, in your command line interface, change into the 'Elvis/src' directory, then type

`sage Elvis.py`

to setup and run the program.
