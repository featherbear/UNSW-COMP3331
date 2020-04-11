set xlabel "time [s]"
set ylabel "throughput [pkts/s]"
set key bel

# In the plotting command, the argument ($i) denotes the ith column of the input data file
# plot "fairnessMon1.tr" u ($1):($3) t "flow: 2 - 3" w lp, "fairnessMon2.tr" u ($1):($3) t "flow: 4 - 5" w lp, "fairnessMon3.tr" u ($1):($3) t "flow: 6 - 7" w lp, "fairnessMon4.tr" u ($1):($3) t "flow: 8 - 9" w lp, "fairnessMon5.tr" u ($1):($3) t "flow: 10 - 11" w lp   
plot "fairnessMon1.tr" u ($1):($3) t "flow: 2 - 3" w lp, "fairnessMon2.tr" u ($1):($3) t "flow: 4 - 5" w lp, "fairnessMon3.tr" u ($1):($3) t "flow: 6 - 7" w lp, "fairnessMon4.tr" u ($1):($3) t "flow: 8 - 9" w lp, "fairnessMon5.tr" u ($1):($3) t "flow: 10 - 11" w lp,  "fairnessMon6.tr" u ($1):($3) t "flow: 12 - 13" w lp, "fairnessMon7.tr" u ($1):($3) t "flow: 14 - 15" w lp, "fairnessMon8.tr" u ($1):($3) t "flow: 16 - 17" w lp, "fairnessMon9.tr" u ($1):($3) t "flow: 18 - 19" w lp, "fairnessMon10.tr" u ($1):($3) t "flow: 20 - 21" w lp  

set term png
set output "fairness_pkt.png"
replot
pause -1
