# Elvis

## Introduction

This project is based on the "Elvis the dog" problem, also known as the weighted region problem.

In Euclidean space, the shortest path between any two points is a straight line. However, this does not imply that the *quickest* path between two points is a straight line. For example, when driving, nobody goes in a straight line; they follow the road's curvature.
Wouldn't it be faster to drive from point A to point B without turning?

Obviously not, since there would be obstacles in your path, _slowing_ you down. Worse, you would probably get in a wreck.

"Slowing" is the keyword here. The concept of velocity is what explains this distinction between the shortest path and the quickest path. The shortest path in space and the quickest path in time are seldom equivalent in real-world applications, because velocity fields may not be uniform. It is quicker to run forward than to backpedal. It is quicker to sail with the wind than against it.

One common optimization problem that occurs on a daily basis is minimizing time consumption. Intuitively, one would think that minimizing movement in space would minimize time consumption in moving from point A to point B. However, as we just illustrated, the problem is rarely that simple.

## Elvis the dog

The formulation of the weighted region problem was inspired in part by the story of a dog named Elvis, who was on a beach and wanted to retrieve an object that was floating in the ocean, as illustrated below.

`insert pdf here`

One might expect Elvis to have taken the shortest path from his starting position to the object, i.e. going in a straight line. However, this is not what happened. Instead, Elvis adjusted his approach as shown below, thereby reducing the time spent in the ocean and increasing the time spent in the sand.

`insert pdf here`


Intuitively, this makes sense; dogs can run faster than they can swim, so it would be inefficient to cover more distance in the ocean. But how did Elvis have the foresight to know this? Biologists suspect that natural selection may have a role, since animals competing for resources need to be able to minimize the time it takes to reach them to increase their fitness for reproduction.

## The problem

The weighted region problem is stated as follows:

*to be continued*

## The theory

## Problem analysis

## Numerical approach to solving the problem

## Make sure to extract Elvis into your Documents folder, then run Setup.py
