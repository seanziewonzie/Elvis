%function newton3
function [t1]=newton3(f1,guess1,accuracy)

t1_new =guess1;
t1_old = guess1+1;
df1d1 = diff(f1);
f1=
while(abs(t1_new-t1_old)>=accuracy
    t1_old =t1_new;
    d = [f1(t1_old) f2(t1_old)];
    a = [df1d1(t1_old) df1d2(t1_old)];
    b =inv(a);
    p=b*d;
    t1_new =t1_old-p(1);

end
t1=t1_new;
