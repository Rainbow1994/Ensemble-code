from numpy import *
from pylab import *
class ensqr:
    def __init__(self, x, y, r):
        self.nx=size(x)
        self.x=array(x)
        self.x_mean=mean(self.x, axis=1)
        self.x=self.x[:,:]-self.x_mean[NewAxis,:]
        self.y=array(y)
        self.y_mean=mean(self.y)
        self.y=self.y-self.y_mean
        
        self.s=sum(self.y*self.y)
        self.yy=dot(transpose(self.y), self.y)
        self.r=r
        
    def get_k(self):
        k=dot(self.x, transpose(self.y))
        k=k/(self.r+self.s)
        return k
    def get_postprior(self,yobs):
        k=self.get_k
        x=self.x_mean+dot(k, yobs-self.ymean)
        return x
    
    def get_tma(self):
        k=self.get_k()
        alpha=1.0+sqrt(self.r/(self.r+self.s))
        alpha=alpha/self.s
        t=identity(self.nx, self.nx)-alpha*self.yy

    def set_y(self, y,r):
        self.y=array(y)
        self.y_mean=mean(self.y)
        self.y=self.y-self.y_mean
    def set_x(self,x):
        self.y=array(y)
        self.y_mean=mean(self.y)
        self.y=self.y-self.y_mean
        
        self.s=sum(self.y*self.y)
        self.yy=dot(transpose(self.y), self.y)
        self.r=r
        
    def get_k(self):
        k=dot(self.x, transpose(self.y))
        k=k/(self.r+self.s)
        return k
    def get_postprior(self,yobs):
        k=self.get_k
        x=self.x_mean+dot(k, yobs-self.ymean)
        return x
    
    def get_tma(self):
        k=self.get_k()
        alpha=1.0+sqrt(self.r/(self.r+self.s))
        alpha=alpha/self.s
        t=identity(self.nx, self.nx)-alpha*self.yy

    def set_y(self, y,r):
        self.y=array(y)
        self.y_mean=mean(self.y)
        self.y=self.y-self.y_mean
    def set_x(self,x):
        self.x=array(x)
        self.x_mean=mean(self.x, axis=1)
        self.x=self.x[:,:]-self.x_mean[NewAxis,:]

    
        
    
        
        
