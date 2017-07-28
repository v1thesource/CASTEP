# Sensitivity analysis tool for Brouwer diagrams! By Alexandros Kenich
# Example usage (to be improved with argument passing):
# python matplotlib_test.py 

import matplotlib
matplotlib.use('Agg')
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.pyplot import savefig
from itertools import izip_longest 
import os
from functools import wraps

#print(sys.argv[0]) # prints name of script
#print(sys.argv[1]) # prints argument1
#print(sys.argv[2]) # prints argument2 (uncomment if needed)

filename = "/Users/ak7310/z/300to2500mono_superfine"
T0 = 300 # initial temperature in K
T_increment = 5 # temperature increment in K
chunk_size = 700 # number of lines per chunk
plt.figure(figsize=(9,9)) # plot size
plt.figure().add_axes([0.1, 0.1, 0.6, 0.8])

def listify(func):
	@wraps(func)
	def new_func(*args, **kwargs):
		return list(func(*args, **kwargs))
	return new_func


def line_yielder(filename):
	with open(filename) as lines:
		for line in lines:
			line = line.strip()
			yield [float(v) for v in line.split()]


def grouper(iterable, n, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx
    args = [iter(iterable)] * n
    return izip_longest(fillvalue=fillvalue, *args)


def column(lines, yindex):
	for line in lines:
		yield line[yindex]


def superplot(batch):
	lineNames = {
		0: 'pO2',
		1: 'mew_e',
		2: 'electrons',
		3: 'holes',
		4: 'VO{2}',
		5: 'VO{1}',
		6: 'VO{0}',
		7: 'VM{-4}',
		8: 'VM{-3}',
		9: 'VM{-2}',
		10:'VM{-1}',
		11:'VM{0}',
		12:'Oi{-2}',
		13:'Oi{-1}',
		14:'Oi{0}',
		15:'Mi{4}',
		16:'Mi{3}',
		17:'Mi{2}',
		18:'Mi{1}',
		19:'Mi{0}',
		20:'Stoich',
	}
	exes = list(column(batch,0))
	plt.plot(exes, list(column(batch, 2), label = lineNames[2] ) # 'electrons'
	plt.plot(exes, list(column(batch, 3), label = lineNames[3] ) # 'holes'
	plt.plot(exes, list(column(batch, 4), label = lineNames[4] ) # 'VO{2}'
	plt.plot(exes, list(column(batch, 5), label = lineNames[5] ) # 'VO{1}'
	plt.plot(exes, list(column(batch, 6), label = lineNames[6] ) # 'VO{0}'
	plt.plot(exes, list(column(batch, 7), label = lineNames[7] ) # 'VM{-4}'
	plt.plot(exes, list(column(batch, 8), label = lineNames[8] ) # 'VM{-3}'
	plt.plot(exes, list(column(batch, 9), label = lineNames[9] ) # 'VM{-2}'
	plt.plot(exes, list(column(batch,10), label = lineNames[10]) # 'VM{-1}'
	plt.plot(exes, list(column(batch,11), label = lineNames[11]) # 'VM{0}'
	plt.plot(exes, list(column(batch,12), label = lineNames[12]) # 'Oi{-2}'
	plt.plot(exes, list(column(batch,13), label = lineNames[13]) # 'Oi{-1}'
	plt.plot(exes, list(column(batch,14), label = lineNames[14]) # 'Oi{0}'
	plt.plot(exes, list(column(batch,15), label = lineNames[15]) # 'Mi{4}'
	plt.plot(exes, list(column(batch,16), label = lineNames[16]) # 'Mi{3}'
	plt.plot(exes, list(column(batch,17), label = lineNames[17]) # 'Mi{2}'
	plt.plot(exes, list(column(batch,18), label = lineNames[18]) # 'Mi{1}'
	plt.plot(exes, list(column(batch,19), label = lineNames[19]) # 'Mi{0}'
	plt.plot(exes, list(column(batch,20), label = lineNames[20]) # 'Stoich'
	#for i in range(0,len(batch[0])-2): # len(batch[0]) == 2
	#	plt.plot(exes, list(column(batch,i+2)), label = lineNames[i+2])
	plt.ylim([-10,0])
	plt.xlim([-35,0])
	plt.xlabel("log10(pO2) (atm)")
	plt.ylabel("log10([D]) (per f.u.)")
	plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.) # Legend, allegedly
	#plt.show()


def plot_all(filename,startTemp,tempIncrement,plotname):
	initialTemp = startTemp
	for i, batch in enumerate(grouper(line_yielder(filename), chunk_size)):
		superplot(batch)
		temperature = initialTemp + (tempIncrement*(i))
		plt.title("T = " + str(temperature) + " K")
		plotFilename = plotname+str(300+(i*tempIncrement))
		savefig(plotFilename,bbox_inches='tight')
		plt.clf() # clear figure or you'll get 182392u394 lines


from multiprocessing import Pool

def plot_all2(filename):
	p = Pool(3)
	p.map(superplot2, ((batch, "/tmp/plot"+str(i)) for i, batch in enumerate(grouper(line_yielder(filename), chunk_size))))


def superplot2((batch,plotname)):
	return superplot(batch,plotname)


plot_all(filename,T0,T_increment,"/tmp/mono_brouwer_superfine")

# print(os.getcwd())

# data = np.random.rand(2, 25)
# l, = plt.plot([], [], 'r-')
# plt.xlim(0, 1)
# plt.ylim(0, 1)
# plt.xlabel('x')
# plt.title('test')
# line_ani = animation.FuncAnimation(fig1, update_line, 25, fargs=(data, l),
#                                    interval=50, blit=True)

# # To save the animation, use the command: line_ani.save('lines.mp4')

# savefig(fname, dpi=None, facecolor='w', edgecolor='w',
#        orientation='portrait', papertype=None, format=None,
#        transparent=False, bbox_inches=None, pad_inches=0.1,
#        frameon=None)

# x = np.arange(-9, 10)
# y = np.arange(-9, 10).reshape(-1, 1)
# base = np.hypot(x, y)
# ims = []
# for add in np.arange(15):
#     ims.append((plt.pcolor(x, y, base + add, norm=plt.Normalize(0, 30)),))

# im_ani = animation.ArtistAnimation(fig2, ims, interval=50, repeat_delay=3000,
#                                    blit=True)
# # To save this second animation with some metadata, use the following command:
# # im_ani.save('im.mp4', metadata={'artist':'Guido'})
