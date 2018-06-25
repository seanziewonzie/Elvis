function [output] = addition(x);
output=0;
n=length(x);
for i=1:n
    output=output+x(i);
end
end