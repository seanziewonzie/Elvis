function [ x1, x2 ] = quad( a,b,c )
%UNTITLED2 Summary of this function goes here
%   Detailed explanation goes here
x1=((-b)+sqrt((b^2)-(4*a*c)))/(2*a)
x2=((-b)-sqrt((b^2)-(4*a*c)))/(2*a)
end

