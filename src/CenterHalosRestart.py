import numpy as np, sys, os

def diff(a, b):
    b = set(b)
    return [aa for aa in a if aa not in b]
#rho0 = (2048.0/1000.0)**3 # For MDR1
rho0 = (2048.0/250)**3 # For Bolshoi
crit = 740.0

path = sys.argv[1]
filenames = os.listdir(path)
filenum = len(filenames)
target_id = []
for filename in filenames:
    file_id = int(filename.split('_')[1].split('.')[0]) # For Bolshoi 
    target_id.append(file_id)

done_id = []
output_filenames = os.listdir('./CenteredHalos')
for filename in output_filenames:
    file_id = int(filename.split('_')[1].split('.')[0]) # For Bolshoi 
    done_id.append(file_id)

to_do_id = diff(target_id, done_id)

print ("%d files to process"%(len(target_id)))
print ("%d files in results directory"%(len(done_id)))
print ("%d files remaining to process "%(len(to_do_id)))

sys.stdout.write('\rCompiling the code used to calculate the center of each halo... ')
sys.stdout.flush()
os.system('cc potential.c -lm -o potential.out')
sys.stdout.write('Done\n')
os.system('mkdir CenteredHalos')

to_do_id.sort()
for file_id in to_do_id:
    filename = 'halo_%06d.dat'%(file_id)
    print('Working with file %d' % (file_id))

    #data = np.loadtxt(path+'/'+filename, delimiter=",",skiprows=16,usecols=(2,3,4)) # For MDR1
    data = np.loadtxt(path+'/'+filename) # For Bolshoi
    x,y,z = np.transpose(data)
    n_points = len(x)
    
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
    r = np.sqrt(x*x+y*y+z*z)

    indices = np.argsort(r)
    x = x[indices]
    y = y[indices]
    z = z[indices]
    r = r[indices]

    mass   = np.arange(1,n_points)
    radius = r[1:]
    dens = mass/((4.0/3.0)*np.pi*(radius**3))
    
    diff = np.abs(dens-rho0*crit)
    vir_index = np.argmin(diff)+1

    if vir_index == 1:
        vir_index = -1
    
    odata = np.dstack((x,y,z))[0,:vir_index]
    
    np.savetxt('./CenteredHalos/'+filename,odata,fmt='%lf,%lf,%lf')
    os.system('rm '+positions_name+' '+potential_name)
