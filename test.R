library(emuR)

ae=load_emuDB("/home/guest/Desktop/AlignTests/ForcedAlignMulti/clarin/emu")

serve(ae)

# sl=query(ae, query="Phonetic==I|o:|u:|V|@")
sl=query(ae, query="Phoneme==a|e|i|o|u|I")

library(dplyr)
set.seed(54321)
rs=sample_n(sl,1000)

#td=get_trackdata(ae,sl,onTheFlyFunctionName = "forest", resultType = "emuRtrackdata")
td=get_trackdata(ae,rs,'FORMANTS',resultType = "emuRtrackdata")
td=td[which(td$T1>0 & td$T2>0),]

meds<-aggregate(. ~ sl_rowIdx , data=td[,c('sl_rowIdx','T1','T2')], FUN=median)
meds<-unique(merge(meds,td[,c('sl_rowIdx','labels')],by='sl_rowIdx'))

library(ggplot2)
 
ggplot(meds, aes(x=T2,y=T1,label=meds$labels))+
  geom_text(aes(colour=factor(labels)))+
  scale_y_reverse()+scale_x_reverse()+
  labs(x="F2",y="F1")+
  guides(colour=FALSE)

