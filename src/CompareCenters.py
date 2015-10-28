import numpy as np
from os import system, listdir
from sys import argv

def get_inertia(x,y,z):
    r = np.dstack((x,y,z))[0]
    I = np.empty((3,3))

    for j in range(3):
        for k in range(3):
            I[j,k] = np.sum( (j == k)*np.sum(r*r,axis=1)-(r[:,j]*r[:,k]) )

    return np.linalg.eig(I)[0]
    
    
def get_centers(filename):
    
    file_id = filename.split('/')[-1].split('_')[1]
    print(file_id)
    x,y,z = np.loadtxt(filename,unpack=True,delimiter=",",skiprows=16,usecols=(2,3,4))
    n_points = len(x)

    get_inertia(x,y,z)

    positions_name =file_id+'_positions.dat'
    potential_name =file_id+'_potential.dat'

    np.savetxt(positions_name,np.dstack((x,y,z))[0],delimiter=',')
    system('./potential.out '+positions_name+' '+potential_name)

    potential = np.loadtxt(open(potential_name, 'r'))
    maximum = np.argmax(potential)
    system('rm '+positions_name+' '+potential_name)
    x_center,y_center,z_center = x[maximum],y[maximum],z[maximum]
    x_avg,y_avg,z_avg = np.mean(x),np.mean(y),np.mean(z)
    eigenvalues = get_inertia(x-x_center,y-y_center,z-z_center)

    data = np.concatenate(([int(file_id),x_center,y_center,z_center,x_avg,y_avg,z_avg],eigenvalues))
    return data

if __name__ == '__main__':
    path = argv[1]
    filenames = listdir(path)
    filenames.sort()
    results = ['halo_id,x_potential,y_potential,z_potential,x_mass,y_mass,z_mass,eig_1,eig_2,eig_3']
    outfile = open('output_centers.csv','w')
    try:
        for filename in filenames:
            data = get_centers(path+'/'+filename)
            data = [str(x) for x in data]
            data[0] = data[0].split('.')[0]
            results += [','.join(data)]
    finally:
        outfile.write('\n'.join(results))
        outfile.close()
