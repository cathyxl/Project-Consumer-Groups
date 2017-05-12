rm(list=ls())
orient=read.csv("E:/Academy/BDCCL/data/DBAD/Python_DBAD/data1_2.csv",head=F)
ang=orient[,3]/180*pi
orient=cbind(orient[-3],ang)
library(movMF)

###extract data from different person
per <- function(x){
    orient[which(orient[,1]==x),]
}

##第i个人第n个窗口的角度
win <- function(i,n){
    angle=per(i)[,3]
    ind=per(i)[,2]
    l=which(ind>(1500*(n-1)))
    u=which(ind<(1500*n))
    win.ind=intersect(l,u)
    res=angle[win.ind]
    return(res)
}

##估计第i个人第n个窗口的分布的参数
para <- function(i,n){
angle=win(i,n)
pts<- cbind(cos(angle), sin(angle))
est <- movMF(pts,1)
theta=est$thet
#VM分布的均值
mu <- atan2(est$theta[,2], est$theta[,1])  #atan2(y, x) == atan(y/x)
#concentration parameter
kap <- sqrt(rowSums(est$theta^2))
#混合概率
alpha=est$alpha
return(list(pts=pts,theta=theta,mu=mu,kap=kap,alpha=alpha))
}




###cal DJ
#f1 <- function(i,n){
    theta=para(i,n)$theta
    kap=para(i,n)$kap
    alpha=para(i,n)$alpha
    mu=para(i,n)$mu
    x=para(i,n)$pts
   # return(x)
    dmovMF(x,theta,alpha)
}

DJ <- function(i,n,j,m){
    th1=para(i,n)$theta
    
    alpha1=para(i,n)$alpha
    
    f1<-function(x){
        xx<- cbind(cos(x), sin(x))
        dmovMF(xx,th1,alpha1)
    }
    
    th2=para(j,m)$theta
    
    alpha2=para(j,m)$alpha
    
    
    f2<-function(x){
        xx<- cbind(cos(x), sin(x))
        dmovMF(xx,th2,alpha2)
    }
    
    f <- function(x){
        (f1(x)-f2(x))*log(f1(x)/f2(x))
    }
    
    
    X=runif(10000,0,2*pi)
    D=2*pi*mean(f(X))
    
    return(D)
}


div=0
for (i in 1:10){
    d=DJ(1,i,2,i)
    div=c(div,d)
}




###拟合优度
###分成8组 分别计算pi
fp <- function(kap,theta,n=8){
        th=c(kap)*theta
        sam=rmovMF(10000,th,alpha)  ##得到的数据和Pts一样的格式
        temp=matrix(sam,nrow=10000,ncol=2)
        rang=atan2(temp[,2],temp[,1])
        tabang=table(cut(rang,breaks=8))
        res=as.matrix(tabang)/10000
        return(res)
}

compare <- function(x,kap,theta){
    fp=fp(kap,theta,n=8)
    tabx=table(cut(x,breaks=8))  #x为原始数据转化为rad之后的角度 即win()的输出
    tabx=c(tabx[c(5:8)],tabx[c(1:4)])
    x2=0
    for (i in 1:8){
        temp=(length(x)*as.numeric(fp[i,]))^2/as.numeric(tabx[i])
        #期望值
        p=length(x)*as.numeric(fp[i,])
        #实际值
        phat=as.numeric(tabx[i])
        temp=(p-phat)^2/p
        x2=x2+temp
    }
    res=x2
    return(res)
}

theta=para(1,1)$theta
kap=para(1,1)$kap
alpha=para(1,1)$alpha
mu=para(1,1)$mu
compare(win(1,1),kap,theta)
