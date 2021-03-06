from PIL import Image
import numpy as np
import graphics
import math

def img_mat(path):
    with Image.open(path) as p:
        data = p.getdata()
        return np.uint8(data)

def refactors(x): # refactor in terms of a single last dimention

    if math.prod(x.shape) % 2 == 0:
        x1,x2 = x.shape
        x = x.reshape(x1*x2)
        x = x.reshape(int(x.shape[0]/2), 2, 1)
    else:
        raise ValueError #gotta fix this one
        x = x.reshape(int(x.shape[0]/2), 2)

    return np.uint8(x)

def get_reseter(x ):
    b = x.shape[0]
    w= int(np.ceil(np.sqrt(b)))  # result width
    h = int(b/w)
    t = []

    for i in range(w):
        for j in range(h):
            t.append(x[i*h + j])

    return np.array(t)

def factor_img(mat):
    x = refactors(mat)
    image = raster_2d(x)
    k = 0
    for i in range(image.shape[-1]):
        r = refactors(image[:,:,i])	
        x1,x2,x3 = r.shape
        d1, d2,d3 = image.shape
        k = (image[:, x2,x3]**2)/(k * image[:, x2,x3] + r[:d1, :,:])
    
    return k

def raster_2d(x):
   if len(x.shape) < 3:
       x = x.reshape(x.shape[0], x.shape[1], 1)
   
   np.repeat(x, 2, axis=2)

   n_batch = x.shape[0]

   width = int(np.ceil(np.sqrt(n_batch)))  # result width
   h = int(n_batch/width)
   d1,d2,d3 =int(h*x.shape[1]), int(width*x.shape[2]), 3
   z0 =  np.zeros((d1, d2, d3), dtype="uint8")
   for i in range(h):
	   for j in range(width):
		   z0[i * x.shape[1] : (i+1) * x.shape[2], j*x.shape[1]:(j+1)*x.shape[2]] = x[i*x.shape[1]+j*i, 0]
 
   assign = get_reseter(x)
   return z0
	

if __name__ == "__main__":
    def main():
        img = factor_img(img_mat("pepe.jpg"))
        img = np.uint8(img)
        graphics.save_image(img.T[:,:,:3], "p.jpg")    # gotta use the multiple saver


    main()
