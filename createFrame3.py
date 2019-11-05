#!/usr/bin/python
#-*-coding:	UTF-8-*-
from abaqus	import *
from abaqusConstants import	*
from caeModules import *
import regionToolset

def	createBeam(modelName,partName,length,width,height):
	s =	mdb.models[modelName].ConstrainedSketch(name='__profile__',	sheetSize=1.0)
	g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
	s.setPrimaryObject(option=STANDALONE)
	s.rectangle(point1=(0.0, 0.0), point2=(length, width))
	p =	mdb.models[modelName].Part(name=partName, dimensionality=THREE_D, type=DEFORMABLE_BODY)
	p =	mdb.models[modelName].parts[partName]
	p.BaseSolidExtrude(sketch=s, depth=height)
	s.unsetPrimaryObject()
	p =	mdb.models[modelName].parts[partName]
	del	mdb.models[modelName].sketches['__profile__']

def createFrame(modelName,partName,nX,nFloor,nZ,slabSet,slab2,column1,column2,column3,beamx1,beamx2,beamx3,beamz1,beamz2,beamz3,nc1,nc3,nbx2,nbxd,nbxu,nbzd,nbz2,nbzu,dsx,dsz):
	
	#参数定义
	c=0.028                                      #保护层厚度，可修改
	lc=column2-2*c
	lbx=beamx1
	lbz=beamz3

	# 计算受力筋长度及箍筋个数
	nc2m=(column2*10-1)/3.
	nc2m=int(round(nc2m))
	nbx1m=2*beamx2/0.1
	nbx1m=int(round(nbx1m))
	nbz3m=2*beamz2/0.1
	nbz3m=int(round(nbz3m))

	nc2s=nc2m/2.
	nc2s=int(round(nc2s))
	nbx1s=(lbx-column1-0.1-2*nbx1m*0.1)/0.2
	nbx1s=int(round(nbx1s))
	dc2=(column2-2*nc2m*0.1-0.1)/nc2s
	dbx1=(lbx-column1-0.1-2*nbx1m*0.1)/nbx1s
	nbz3s=(lbz-column3-0.1-2*nbz3m*0.1)/0.2
	nbz3s=int(round(nbz3s))
	dbz3=(lbz-column3-0.1-2*nbz3m*0.1)/nbz3s

	# 计算板筋个数及间距
	nsx=(beamz3-beamx3-0.4)/dsx
	nsx=int(round(nsx))
	nsz=(beamx1-beamz1-0.4)/dsz
	nsz=int(round(nsz))

	dsx=(beamz3-beamx3-0.4)/nsx
	dsz=(beamx1-beamz1-0.4)/nsz

	RebarC=[]
	RebarBx=[]
	RebarZx=[]
	RebarS=[]

	# 定义材料及截面
	m=mdb.Model(modelName)
	m.Material(name='test')
	m.materials['test'].Density(table=((1,0),))
	m.TrussSection(name='test1',material='test',area=1)
	m.TrussSection(name='test2',material='test',area=1)

	createBeam(modelName,partName='Beam-x',length=beamx1,width=beamx2, height=beamx3)
	createBeam(modelName,partName='Beam-y',length=beamz1,width=beamz2, height=beamz3)
	createBeam(modelName,partName='Column', length=column1,width=column2,height=column3)
	if(slabSet=='\xb4\xf8\xc2\xa5\xb0\xe5'):
		createBeam(modelName,'Slab',beamx1,slab2,beamz3)
	
	a=mdb.models[modelName].rootAssembly
	p = mdb.models[modelName].parts['Beam-x'] 
	a.Instance(name='Beam-x-1',	part=p,	dependent=ON)
	p= mdb.models[modelName].parts['Beam-y']
	a.Instance(name='Beam-y-1', part=p,dependent=ON)
	p= mdb.models[modelName].parts['Column']	
	a.Instance(name='Column-1',	part=p,	dependent=ON)
	#柱配筋模型 
	# *受力筋 
	s=m.ConstrainedSketch('sketch1',10.0) 
	s.Line(point1=(0.0, 0.0),point2=(lc,0.0)) 
	p=m.Part(name='Crebar', dimensionality=THREE_D, type=DEFORMABLE_BODY)	
	p=m.parts['Crebar']
	p.BaseWire(s)
	e=p.edges	
	region1=regionToolset.Region(edges=e[0:1]) 
	p.SectionAssignment(region=region1,	sectionName='test1') 
	a.Instance(name='Crebar',part=p,dependent=ON) 
	a.rotate(('Crebar',),(0,0,0),(0,0,1),90) 
	a.LinearInstancePattern(instanceList=('Crebar',),direction1=(1,0,0),direction2=(0,0,1),number1=nc1,number2=nc3,spacing1=(column1-2*c)/(nc1-1),spacing2=(column3-2*c)/(nc3-1)) 
	crebar=['Crebar']
	for i in range(1,nc1+1):
		for j in range(1,nc3+1):
			crebar.append('Crebar-lin-'+str(i)+'-'+str(j))

	crebar.remove('Crebar-lin-1-1')

	if nc1>2 and nc3>2:
		for	i in range(2,nc1):
			for	j in range(2,nc3):
				del	a.features['Crebar-lin-'+str(i)+'-'+str(j)]
				crebar.remove('Crebar-lin-'+str(i)+'-'+str(j))

	# *箍筋
	p=m.Part('Csteel',THREE_D,DEFORMABLE_BODY)
	s=m.ConstrainedSketch('sketch2',10.0)
	s.rectangle((0,0),(column1-2*c,column3-2*c))
	p.BaseWire(s)
	e=p.edges
	region2=regionToolset.Region(edges=e[0:4])
	p.SectionAssignment(region=region2,	sectionName='test2')
	a.Instance(name='Csteel',part=p,dependent=ON)
	a.rotate(instanceList=('Csteel',),axisPoint=(0,0,0),axisDirection=(1,0,0),angle=90)
	a.translate(instanceList=('Csteel',),vector=(0,0.05-c,0))
	a.LinearInstancePattern(instanceList=('Csteel',),direction1=(0,1,0),direction2=(0,1,0),number1=nc2m+1,number2=2,spacing1=0.1,spacing2=column2-nc2m*0.1-0.1)
	a.LinearInstancePattern(instanceList=('Csteel-lin-'+str(nc2m+1)+'-1',),direction1=(0,1,0),direction2=(0,1,0),number1=nc2s,number2=1,spacing1=dc2,spacing2=1)

	crebar.append('Csteel')
	for	i in range(1,nc2m+2):
		for	j in range(1,3):
			crebar.append('Csteel-lin-'+str(i)+'-'+str(j))
	 
	crebar.remove('Csteel-lin-1-1')

	for	i in range(2,nc2s+1):
		crebar.append('Csteel-lin-'+str(nc2m+1)+'-1-lin-'+str(i)+'-1')

	for	i in range(0,len(crebar)):
		RebarC.append(a.instances[crebar[i]])

	a.InstanceFromBooleanMerge(name='RebarC', instances=RebarC,	originalInstances=DELETE, domain=GEOMETRY)

	# x向梁配筋模型
	# *受力筋
	s=m.ConstrainedSketch('sketch3',10.0)
	s.Line(point1=(0.0,	0.0), point2=(lbx, 0.0))
	p=m.Part(name='Bxrebar', dimensionality=THREE_D, type=DEFORMABLE_BODY)
	p=m.parts['Bxrebar']
	p.BaseWire(s)
	e=p.edges
	region1=regionToolset.Region(edges=e[0:1])
	p.SectionAssignment(region=region1,	sectionName='test1')
	a=m.rootAssembly
	a.Instance(name='Bxrebar',part=p,dependent=ON)

	a.LinearInstancePattern(instanceList=('Bxrebar',),direction1=(0,0,1),direction2=(0,1,0),number1=1,number2=nbx2,spacing1=1,spacing2=(beamx2-2*c)/(nbx2-1))
	a.LinearInstancePattern(instanceList=('Bxrebar',),direction1=(0,0,1),direction2=(0,1,0),number1=nbxd,number2=1,spacing1=(beamx3-2*c)/(nbxd-1),spacing2=1)
	a.LinearInstancePattern(instanceList=('Bxrebar-lin-1-'+str(nbx2),),direction1=(0,0,1),direction2=(0,1,0),number1=nbxu,number2=1,spacing1=(beamx3-2*c)/(nbxu-1),spacing2=1)
	if nbx2>2:
		for i in range(2,nbx2):
			a.LinearInstancePattern(instanceList=('Bxrebar-lin-1-'+str(i),),direction1=(0,0,1),direction2=(0,1,0),number1=2,number2=1,spacing1=beamx3-2*c,spacing2=1)
	bxrebar=['Bxrebar']
	for	i in range(2,nbxd+1):
		bxrebar.append('Bxrebar-lin-'+str(i)+'-1')
	for i in range(2,nbxu+1):
		bxrebar.append('Bxrebar-lin-1-'+str(nbx2)+'-lin-'+str(i)+'-1')
	bxrebar.append('Bxrebar-lin-1-'+str(nbx2))
	if nbx2>2:
		for	i in range(2,nbx2):
			bxrebar.append('Bxrebar-lin-1-'+str(i))
			bxrebar.append('Bxrebar-lin-1-'+str(i)+'-lin-2-1')

	# *箍筋
	p=m.Part('Bxsteel',THREE_D,DEFORMABLE_BODY)
	s=m.ConstrainedSketch('sketch4',10.0)
	s.rectangle((0,0),(beamx3-2*c,beamx2-2*c))
	p.BaseWire(s)
	e=p.edges
	region2=regionToolset.Region(edges=e[0:4])
	p.SectionAssignment(region=region2,	sectionName='test2')
	a.Instance(name='Bxsteel',part=p,dependent=ON)
	a.rotate(instanceList=('Bxsteel',),axisPoint=(0,0,0),axisDirection=(0,1,0),angle=-90)
	a.translate(instanceList=('Bxsteel',),vector=(0.05+column1/2.,0,0))
	a.LinearInstancePattern(instanceList=('Bxsteel',),direction1=(1,0,0),direction2=(1,0,0),number1=nbx1m+1,number2=2,spacing1=0.1,spacing2=lbx-nbx1m*0.1-0.1-column1)
	a.LinearInstancePattern(instanceList=('Bxsteel-lin-'+str(nbx1m+1)+'-1',),direction1=(1,0,0),direction2=(0,1,0),number1=nbx1s,number2=1,spacing1=dbx1,spacing2=1)

	bxrebar.append('Bxsteel')
	for	i in range(1,nbx1m+2):
		for	j in range(1,3):
			bxrebar.append('Bxsteel-lin-'+str(i)+'-'+str(j))
	 
	bxrebar.remove('Bxsteel-lin-1-1')

	for	i in range(2,nbx1s+1):
		bxrebar.append('Bxsteel-lin-'+str(nbx1m+1)+'-1-lin-'+str(i)+'-1')

	for	i in range(0,len(bxrebar)):
		RebarBx.append(a.instances[bxrebar[i]])

	a.InstanceFromBooleanMerge(name='RebarBx', instances=RebarBx, originalInstances=DELETE,	domain=GEOMETRY)

	# z向梁配筋模型	
	# *受力筋
	s=m.ConstrainedSketch('sketch5',10.0)
	s.Line(point1=(0.0,	0.0), point2=(lbz, 0.0))
	p=m.Part(name='Bzrebar', dimensionality=THREE_D, type=DEFORMABLE_BODY)
	p=m.parts['Bzrebar']
	p.BaseWire(s)
	e=p.edges
	region1=regionToolset.Region(edges=e[0:1])
	p.SectionAssignment(region=region1,	sectionName='test1')
	a=m.rootAssembly
	a.Instance(name='Bzrebar',part=p,dependent=ON)
	a.rotate(instanceList=('Bzrebar',),axisPoint=(0,0,0),axisDirection=(0,1,0),angle=-90)
	a.LinearInstancePattern(instanceList=('Bzrebar',),direction1=(1,0,0),direction2=(0,1,0),number1=1,number2=nbz2,spacing1=1,spacing2=(beamz2-2*c)/(nbz2-1))
	a.LinearInstancePattern(instanceList=('Bzrebar',),direction1=(1,0,0),direction2=(0,1,0),number1=nbzd,number2=1,spacing1=(beamz1-2*c)/(nbzd-1),spacing2=1)
	a.LinearInstancePattern(instanceList=('Bzrebar-lin-1-'+str(nbz2),),direction1=(1,0,0),direction2=(0,1,0),number1=nbzu,number2=1,spacing1=(beamz1-2*c)/(nbzu-1),spacing2=1)
	if nbz2>2:
		for i in range(2,nbz2):
			a.LinearInstancePattern(instanceList=('Bzrebar-lin-1-'+str(i),),direction1=(1,0,0),direction2=(0,1,0),number1=2,number2=1,spacing1=beamz1-2*c,spacing2=1)
	bzrebar=['Bzrebar']
	for	i in range(2,nbzd+1):
		bzrebar.append('Bzrebar-lin-'+str(i)+'-1')
	for i in range(2,nbzu+1):
		bzrebar.append('Bzrebar-lin-1-'+str(nbz2)+'-lin-'+str(i)+'-1')
	bzrebar.append('Bzrebar-lin-1-'+str(nbz2))
	if nbz2>2:
		for	i in range(2,nbz2):
			bzrebar.append('Bzrebar-lin-1-'+str(i))
			bzrebar.append('Bzrebar-lin-1-'+str(i)+'-lin-2-1')

	# *箍筋
	p=m.Part('Bzsteel',THREE_D,DEFORMABLE_BODY)
	s=m.ConstrainedSketch('sketch6',10.0)
	s.rectangle((0,0),(beamz1-2*c,beamz2-2*c))
	p.BaseWire(s)
	e=p.edges
	region2=regionToolset.Region(edges=e[0:4])
	p.SectionAssignment(region=region2,	sectionName='test2')
	a.Instance(name='Bzsteel',part=p,dependent=ON)
	a.translate(instanceList=('Bzsteel',),vector=(0,0,0.05+column3/2.))
	a.LinearInstancePattern(instanceList=('Bzsteel',),direction1=(0,0,1),direction2=(0,0,1),number1=nbz3m+1,number2=2,spacing1=0.1,spacing2=lbz-nbz3m*0.1-0.1-column3)
	a.LinearInstancePattern(instanceList=('Bzsteel-lin-'+str(nbz3m+1)+'-1',),direction1=(0,0,1),direction2=(0,1,0),number1=nbz3s,number2=1,spacing1=dbz3,spacing2=1)

	bzrebar.append('Bzsteel')
	for	i in range(1,nbz3m+2):
		for	j in range(1,3):
			bzrebar.append('Bzsteel-lin-'+str(i)+'-'+str(j))
	 
	bzrebar.remove('Bzsteel-lin-1-1')

	for	i in range(2,nbz3s+1):
		bzrebar.append('Bzsteel-lin-'+str(nbz3m+1)+'-1-lin-'+str(i)+'-1')

	for	i in range(0,len(bzrebar)):
		RebarZx.append(a.instances[bzrebar[i]])

	a.InstanceFromBooleanMerge(name='RebarBz', instances=RebarZx, originalInstances=DELETE,	domain=GEOMETRY)

	if (slabSet=='\xb4\xf8\xc2\xa5\xb0\xe5'):
		p =	mdb.models[modelName].parts['Slab']
		a.Instance(name='Slab-1', part=p, dependent=ON)
		a.translate(instanceList=('Slab-1',	), vector=(column1/2.0,	column2-slab2, column3/2.0))
		# 板配筋

		sx=m.ConstrainedSketch('sketch7',10.0)
		sz=m.ConstrainedSketch('sketch8',10.0)
		sx.Line(point1=(0,0),point2=(beamx1,0.))
		sz.Line(point1=(0,0),point2=(beamz3,0.))
		px=m.Part('Slabx',THREE_D,DEFORMABLE_BODY)
		pz=m.Part('Slabz',THREE_D,DEFORMABLE_BODY)
		px.BaseWire(sx)
		pz.BaseWire(sz)
		ex=px.edges
		ez=pz.edges
		region1=regionToolset.Region(edges=ex[0:1])
		region2=regionToolset.Region(edges=ez[0:1])
		px.SectionAssignment(region=region1,sectionName='test2')
		pz.SectionAssignment(region=region2,sectionName='test2')
		a.Instance(name='Slabx',part=px,dependent=ON)
		a.translate(instanceList=('Slabx',),vector=(column1/2.,column2-0.7*slab2,(column3+beamx3)/2.+0.05))
		a.Instance(name='Slabz',part=pz,dependent=ON)
		a.rotate(instanceList=('Slabz',),axisPoint=(0,0,0),axisDirection=(0,1,0),angle=-90)
		a.translate(instanceList=('Slabz',),vector=((column1+beamz1)/2.+0.05,column2-0.7*slab2,column3/2.))
		a.LinearInstancePattern(instanceList=('Slabx',),direction1=(0,0,1),direction2=(0,0,1),number1=2,number2=2,spacing1=0.15,spacing2=beamz3-beamx3-0.25)
		a.LinearInstancePattern(instanceList=('Slabz',),direction1=(1,0,0),direction2=(1,0,0),number1=2,number2=2,spacing1=0.15,spacing2=beamx1-beamz1-0.25)
		srebar=['Slabx','Slabx-lin-2-1','Slabx-lin-1-2','Slabx-lin-2-2','Slabz','Slabz-lin-2-1','Slabz-lin-1-2','Slabz-lin-2-2']
		a.LinearInstancePattern(instanceList=('Slabx-lin-2-1',),direction1=(0,0,1),direction2=(0,0,1),number1=nsx,number2=1,spacing1=dsx,spacing2=1)
		a.LinearInstancePattern(instanceList=('Slabz-lin-2-1',),direction1=(1,0,0),direction2=(1,0,0),number1=nsz,number2=1,spacing1=dsz,spacing2=1)

		for	i in range(2,nsx+1):
			srebar.append('Slabx-lin-2-1-lin-'+str(i)+'-1')

		for	i in range(2,nsz+1):
			srebar.append('Slabz-lin-2-1-lin-'+str(i)+'-1')

		for	i in range(0,len(srebar)):
			RebarS.append(a.instances[srebar[i]])

		a.InstanceFromBooleanMerge(name='RebarS',instances=RebarS, originalInstances=DELETE,domain=GEOMETRY)

	a.translate(instanceList=('RebarC-1',),vector=(c,c,c))
	a.translate(instanceList=('RebarBx-1',),vector=(column1/2.,column2-beamx2+c,(column3-beamx3)/2.+c))
	a.translate(instanceList=('RebarBz-1',),vector=((column1-beamz1)/2.+c,column2-beamz2+c,column3/2.))
	a.translate(instanceList=('Beam-y-1', ), vector=((column1-beamz1)/2.0, column2-beamz2, column3/2.0))
	a.translate(instanceList=('Beam-x-1', ), vector=(column1/2.0, column2-beamx2, (column3-beamx3)/2.0))
	a.LinearInstancePattern(instanceList=('Column-1','RebarC-1', ),	direction1=(1.0, 0.0, 
		0.0), direction2=(0.0, 0.0,	1.0), number1=nX+1,	number2=nZ+1, spacing1=beamx1, spacing2=beamz3)
	a.LinearInstancePattern(instanceList=('Beam-y-1', 'RebarBz-1',), direction1=(1.0, 0.0, 
		0.0), direction2=(0.0, 0.0,	1.0), number1=nX+1,	number2=nZ,	spacing1=beamx1, spacing2=beamz3)
	a.LinearInstancePattern(instanceList=('Beam-x-1', 'RebarBx-1',), direction1=(1.0, 0.0, 
		0.0), direction2=(0.0, 0.0,	1.0), number1=nX, number2=nZ+1,	spacing1=beamx1, spacing2=beamz3)
	if (slabSet=='\xb4\xf8\xc2\xa5\xb0\xe5'):
		a.LinearInstancePattern(instanceList=('RebarS-1',),direction1=(0,1,0),direction2=(0,1,0),number1=2,number2=1,spacing1=0.4*slab2,spacing2=1)
		a.LinearInstancePattern(instanceList=('Slab-1',	'RebarS-1','RebarS-1-lin-2-1',), direction1=(1.0, 0.0, 
			0.0), direction2=(0.0, 0.0,	1.0), number1=nX, number2=nZ, spacing1=beamx1, spacing2=beamz3)
	if (slabSet=='\xb4\xf8\xc2\xa5\xb0\xe5'):
		allinstances=[a.instances['Beam-x-1'] for i	in range(0,(2*nX+1)*(2*nZ+1))]
	else:
		allinstances=[a.instances['Beam-x-1'] for i	in range(0,(nX+1)*(2*nZ+1)+nX*(nZ+1))]

	columnNames=['0' for i in range(0,(nX+1)*(nZ+1))]
	Rebar=['RebarC-1']
	for	i in range(0,nX+1):
		for	j in range(0,nZ+1):
			columnNames[j+i*(nZ+1)]='Column-1-lin-'+str(i+1)+'-'+str(j+1)
			if i is	not	0 or j is not 0:
				allinstances[j+i*(nZ+1)]=a.instances[columnNames[j+i*(nZ+1)]]
				Rebar.append('RebarC-1-lin-'+str(i+1)+'-'+str(j+1))

	beamxNames=['0'	for	i in range(0,nX*(nZ+1))]
	Rebar.append('RebarBx-1')
	for	i in range(0,nX):
		for	j in range(0,nZ+1):
			beamxNames[j+i*(nZ+1)]='Beam-x-1-lin-'+str(i+1)+'-'+str(j+1)
			if i is	not	0 or j is not 0:
				allinstances[j+i*(nZ+1)+(nX+1)*(nZ+1)]=a.instances[beamxNames[j+i*(nZ+1)]]
				Rebar.append('RebarBx-1-lin-'+str(i+1)+'-'+str(j+1))

	beamyNames=['0'	for	i in range(0,nZ*(nX+1))]
	Rebar.append('RebarBz-1')
	for	i in range(0,nX+1):
		for	j in range(0,nZ):
			beamyNames[j+i*nZ]='Beam-y-1-lin-'+str(i+1)+'-'+str(j+1)
			if i is	not	0 or j is not 0:
				allinstances[j+i*nZ+(2*nX+1)*(nZ+1)]=a.instances[beamyNames[j+i*nZ]]
				Rebar.append('RebarBz-1-lin-'+str(i+1)+'-'+str(j+1))
	
	if (slabSet=='\xb4\xf8\xc2\xa5\xb0\xe5'):
		slabNames=['0' for i in	range(0,nZ*nX)]
		Rebar.append('RebarS-1')
		Rebar.append('RebarS-1-lin-2-1')
		for	i in range(0,nX):
			for	j in range(0,nZ):
				slabNames[j+i*nZ]='Slab-1-lin-'+str(i+1)+'-'+str(j+1)
				if i is	not	0 or j is not 0:
					allinstances[j+i*nZ+(nX+1)*(2*nZ+1)+nX*(nZ+1)]=a.instances[slabNames[j+i*nZ]]
					Rebar.append('RebarS-1-lin-'+str(i+1)+'-'+str(j+1))
					Rebar.append('RebarS-1-lin-2-1-lin-'+str(i+1)+'-'+str(j+1))
		allinstances[(nX+1)*(2*nZ+1)+nX*(nZ+1)]=a.instances['Slab-1']

	allinstances[0]=a.instances['Beam-x-1']
	allinstances[(nX+1)*(nZ+1)]=a.instances['Column-1']
	allinstances[(2*nX+1)*(nZ+1)]=a.instances['Beam-y-1']
	a =	mdb.models[modelName].rootAssembly
	Frame1=partName+'1'
	a.InstanceFromBooleanMerge(name=Frame1,	instances=allinstances,	originalInstances=DELETE, domain=GEOMETRY)


	del	mdb.models[modelName].parts['Beam-x']
	del	mdb.models[modelName].parts['Beam-y']
	del	mdb.models[modelName].parts['Column']
	if (slabSet=='\xb4\xf8\xc2\xa5\xb0\xe5'):
		del	mdb.models[modelName].parts['Slab']
	a.LinearInstancePattern(instanceList=(Frame1+'-1', ), direction1=(1.0, 0.0,	0.0), direction2=(0.0, 1.0,	0.0), number1=1, number2=nFloor, spacing1=16.4,	spacing2=column2)
	allFrame1=[a.instances[Frame1+'-1']	for	i in range(0,nFloor)]
	for	i in range(1,nFloor):
		allFrame1[i]=a.instances[Frame1+'-1-lin-1-'+str(i+1)]
	if (nFloor>1):
		a.InstanceFromBooleanMerge(name=partName, instances=allFrame1, originalInstances=DELETE, domain=GEOMETRY)
		a.LinearInstancePattern(instanceList=Rebar,direction1=(0,1,0),direction2=(0,1,0),number1=nFloor,number2=1,spacing1=column2,spacing2=1)
	elif nFloor	is 1:
		 mdb.models[modelName].Part(name=partName, objectToCopy=mdb.models[modelName].parts[Frame1])
		 del a.instances[Frame1+'-1']
		 a.Instance(name=partName+'-1',part=mdb.models[modelName].parts[partName],dependent=ON)
	del	mdb.models[modelName].parts[Frame1]
	
	p=mdb.models[modelName].parts[partName]
	for i in range(0,nFloor):
		if (i!=0):
			p.DatumPlaneByPrincipalPlane(principalPlane=XZPLANE,offset=column2*i)
		if (beamx2==beamz2):
			p.DatumPlaneByPrincipalPlane(principalPlane=XZPLANE,offset=column2-beamx2+column2*i)
		elif (beamx2!=beamz2):
			p.DatumPlaneByPrincipalPlane(principalPlane=XZPLANE,offset=column2*(i+1)-beamx2)
			p.DatumPlaneByPrincipalPlane(principalPlane=XZPLANE,offset=column2*(i+1)-beamz2)
	for i in range(0,nX):
		p.DatumPlaneByPrincipalPlane(principalPlane=YZPLANE,offset=column1+i*beamx1)
		p.DatumPlaneByPrincipalPlane(principalPlane=YZPLANE,offset=beamx1*(i+1))
		if(column1!=beamz1):
			p.DatumPlaneByPrincipalPlane(principalPlane=YZPLANE,offset=(column1-beamz1)/2.+beamx1*(i+1))
			p.DatumPlaneByPrincipalPlane(principalPlane=YZPLANE,offset=(column1+beamz1)/2.+beamx1*i)
	for i in range(0,nZ):
		p.DatumPlaneByPrincipalPlane(principalPlane=XYPLANE,offset=beamz3*(i+1))
		p.DatumPlaneByPrincipalPlane(principalPlane=XYPLANE,offset=column3+beamz3*i)
		if (column3!=beamz3):
			p.DatumPlaneByPrincipalPlane(principalPlane=XYPLANE,offset=(column3-beamx3)/2.+beamz3*(i+1))
			p.DatumPlaneByPrincipalPlane(principalPlane=XYPLANE,offset=(column3+beamx3)/2.+beamz3*i)
	
	session.Viewport(name='Viewport:1',origin=(0,0),width=100,height=150)
	session.viewports['Viewport:1'].makeCurrent()
	session.viewports['Viewport:1'].maximize()
	session.viewports['Viewport:1'].setValues(displayedObject=p)