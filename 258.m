x = zeros(2000,2000);
for i=2:2000
  x(i,i-1) = 1;
endfor
x(1,1999) = 1;
x(1,2000) = 1;
y = eye(2000);
function retval =matExp(k,base)
  retval = eye(2000);
  while (k>0)
    if k%2 != 0 
      base = (retval * base);
    end
    base = base*base;
    k = k/2;
  endwhile
endfunction
res = 0;
fn = matExp(1,x);
for i=1:2000
 res += fn(1,i);
endfor
res

