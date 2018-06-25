function bif = srs_owen(r1,r2,x1,y1,x2,y2)

% Written by Emily Ribando-Gros
%
% TODO
% 
% 1. Only works for interface at y=0

%r1 = 1;             % speed of starting region
%r2 = 2;             % speed of other region
r3 = max([r1, r2]); % speed of interface

% starting position
%x1 = 1;
%y1 = 2;
p1 = [x1 y1];

% ending position
%x2 = 14;
%y2 = 3;
p2 = [x2 y2];

% x-distance between starting and ending position
z = abs(x2-x1);

% time to travel in straight line
T_S = @(y1, y2) sqrt(z^2+(y2-y1)^2)/w1;
% time to travel when using interface
T_SRS = @(y1, y2) z/w3+(y1+y2)/(w1*w3/sqrt(w1^2+w3^2));
%Total time to reach ball
T_tot = @(x1,y1,x2,y2,z,r1,r2) (1/r2)*(sqrt(y1^2+x1^2)+sqrt(y2^2+x2^2))+() %COME BACK TO THIS

% bifurcation
z_bif = @(y1, y2) (y1+y2+2*(r3/r1)*sqrt(y1*y2))/sqrt((r3/r1)^2-1);
z_bifval = z_bif(y1,y2);



figure(1)
axis([-1 15 -1 15]);
set(gca,'xtick',-1:15);
set(gca,'ytick',-1:15);
xlabel('x');
ylabel('y');
title('Least Time Path');

% Check to see which path is faster
if z < z_bifval       % stay in starting region
    plot([x1 x2],[y1 y2]);
elseif z > z_bifval   % use faster region
     
    d1 = y1/sqrt((r2/r1)^2-1);  % x-dist to faster region from slower region
    d2 = y2/sqrt((r2/r1)^2-1);  % x-dist back to slower region
    d3 = z-(d1+d2);             % dist travelled on faster region
    plot([x1 x1+d1],[y1 0],'b',[x1+d1 x1+d1+d3],[0 0],'r',[x1+d1+d3 x2],[0 y2],'b');
    
else                  % both paths take the same amount of time
    
end


bif=z_bifval;
