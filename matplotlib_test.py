import matplotlib
matplotlib.use('Agg')
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.pyplot import savefig
from itertools import izip_longest 
import os
from functools import wraps

filename = "/Users/ak7310/z/300to2500mono_superfine"
T0 = 300 # initial temperature in K
T_increment = 5 # temperature increment in K
chunk_size = 700 # number of lines per chunk
plt.figure(figsize=(9,9)) # plot size
plt.figure().add_axes([0.1, 0.1, 0.6, 0.8])

#plt.ioff() # turn off interactive mode. Don't waste time opening window

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
	lineNames = {0:'mew_e',1:'electrons',2:'holes',3:'VO{2}',4:'VO{1}',5:'VO{0}',6:'VM{-4}',7:'VM{-3}',8:'VM{-2}',9:'VM{-1}',10:'VM{0}',11:'Oi{-2}',12:'Oi{-1}',13:'Oi{0}',14:'Mi{4}',15:'Mi{3}',16:'Mi{2}',17:'Mi{1}',18:'Mi{0}',19:'Stoich',20:'zero'}
	#plotparams = []
	exes = list(column(batch,0))
	for i in range(1,len(batch[0])-1):
		plt.plot(exes, list(column(batch,i+1)), label = lineNames[i])
		#plotparams.append(exes) # puts the x values in
		#plotparams.append(list(column(batch,i))) # subsequent y value
	#plt.plot(*plotparams) # *plotparams takes each element
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

#group = grouper(line_yielder(filename), chunk_size)
# currentbatch = next(group)
# "/tmp/plot"+str(i)
#superplot(next(group),"Test")

#plt.show()



#print(currentbatch)

# x=list(column(currentbatch,0))
# y1=list(column(currentbatch,1))
# y2=list(column(currentbatch,2))

# print(currentbatch[0])
# print(x)
# print(y1)
# print(len(currentbatch[0]))
# print(os.getcwd())

#savefig("test1")

# fig1 = plt.figure()

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
