mydata <- read.csv("/Users/kojin/psets/cs181/cs181-practical3/merged_df.csv")
install.packages("FactoMineR")
install.packages("missMDA")
library(FactoMineR)
require(missMDA)
# R.Version()
mydata <- imputePCA(mydata)
MFA(mydata,group=c(1,1,1,1,1,1,1,1,1,1,1,1,1,1,47,41,42,50,4))
install.packages(ade4)
library(ade4)
scatter.dudi(dudi.mix(iris,scannf=FALSE))

names(mydata)

