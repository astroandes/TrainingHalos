import numpy as np, sys, os

path = sys.argv[1]



filenames = os.listdir(path)
filenum = len(filenames)

sys.stdout.write('\rCompiling the code used to calculate the center of each halo... ')
sys.stdout.flush()
os.system('cc potential.c -lm -o potential.out')
sys.stdout.write('Done\n')
os.system('mkdir CenteredHalos')
for i in range(filenum):
    filename = filenames[i]
    print('Working with file %d of %d' % (i,filenum))

    data = np.loadtxt(path+'/'+filename, delimiter=",",skiprows=16,usecols=(2,3,4))
    x,y,z = np.transpose(data)
    n_points = len(x)
    
    file_id = int(filename.split('_')[1])
    positions_name ='positions_'+str(file_id)+'.dat'
    potential_name ='potential_'+str(file_id)+'.dat'

    np.savetxt(positions_name,np.dstack((x,y,z))[0],delimiter=',')
    os.system('./potential.out '+positions_name+' '+potential_name)

    potential = np.loadtxt(open(potential_name, 'r'))
    maximum = np.argmax(potential)
    x_center,y_center,z_center = x[maximum],y[maximum],z[maximum]
    x -= x_center
    y -= y_center
    z -= z_center
    odata = np.dstack((x,y,z))[0]
    odata = np.sort(odata)

    np.savetxt('./CenteredHalos/'+filename,odata,fmt='%lf,%lf,%lf')
    os.system('rm '+positions_name+' '+potential_name)
