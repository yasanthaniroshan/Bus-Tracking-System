TweenMax.set("#bus-animation",
            {
  visibility: 'visible'
})
TweenMax.set(["#rotate-left","#rotate-right","#floor"],{
  transformOrigin:'50% 50%'
})

TweenMax.set(["#_1","#_2","#_3","#_4","#_5","#_6","#_7","#_8"],{
  drawSVG: '0%'
})

TweenMax.to(["#rotate-left","#rotate-right"],2,{
  rotation:460,
  repeat:-1,
  ease: Linear.easeNone
})

TweenMax.set("#bus",{
  transformOrigin:'50% 50%'
})

TweenMax.to("#bus",0.17,{
  y:-3,
  repeat:-1,
  ease: Linear.easeNone,
  yoyo: true
})

TweenMax.to(["#tire-left","#tire-right"],0.3,{
 y:-2.3,
 repeat:-1,
 ease: Linear.easeNone
})

TweenMax.to("#floor",0.4,{
  scaleX:0.98,
  repeat:-1
})

var tl = new TimelineMax({repeat:-1})
tl.to("#_2",0.5,{
  drawSVG:'40% 100%',
})
.to("#_2",0.3,{
  drawSVG: '100% '
 })

tl.to("#_3",0.5,{
  drawSVG:'40% 100%',
},'-=0.4')
.to("#_3",0.3,{
  drawSVG: '100% '
})

tl.to("#_7",0.5,{
  drawSVG:'40% 100%',
})
.to("#_7",0.3,{
  drawSVG: '100% '
})

.to("#_8",0.5,{
  drawSVG:'40% 100%',
},'-=0.5')
.to("#_8",0.3,{
  drawSVG: '100% '
})

.to("#_6",0.6,{
  drawSVG:'40% 100%',
},'-=0.5')
.to("#_6",0.3,{
  drawSVG: '100% '
})

.to("#_5",0.5,{
  drawSVG:'40% 100%',
},'-=0.5')
.to("#_5",0.3,{
  drawSVG: '100% '
})

.to("#_4",0.5,{
  drawSVG:'40% 100%',
},'-=0.5')
.to("#_4",0.3,{
  drawSVG: '100% '
})
