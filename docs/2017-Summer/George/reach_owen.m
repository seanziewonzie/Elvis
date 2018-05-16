function bif = srs_owen(r1,r2,y1,t)

x1=0;
t_shore=0;                 % Initialize time spent on shore variable

mvd = r1*t;                % Max verticle distance if you went straight out to sea
dist_after_shore = mvd-y1; % Distance left after the shore that you could reach if region 2 was also water

x_enter=0; % X coordinate where dog hits the shore
x_exit=0;  % Init x_exit

entry_angle = @(x_enter, y1) asin(x_enter/y1);
time_sea1   = @(x_enter, y1, r1) sqrt(x_enter^2+y1^2)/r1;
t_shore  = @(x_enter, x_exit, r2) (x_exit-x_enter)*(1/r2);


