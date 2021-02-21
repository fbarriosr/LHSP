import os
import subprocess
from myPrint import *
from stages import *
from filesFunc import *
from project import *

class Operaciones:
    def __init__(self):
	self.paso = 0
	# datos de usuario
	self.X = 0
	self.Y = 0
	self.density = ''
	self.theory = ''
	
	# nombre de archivos
	
	self.MainMep = 0
	self.PosMep  = 0
	self.NegMep  = 0
	self.FDAPos  = 0
	self.FDANeg  = 0
	
	self.FFP     = 0
	self.DDP     = 0
	
	# Indicadores Archivos log
	
	self.Energy = {
	    'E(N+2)':0.0,
	    'E(N+1)':0.0,
	    'E(N)'  :0.0,
	    'E(N-1)':0.0,
	    'E(N-2)':0.0
	    }
	
	self.Indicadores = {
	    'A2':0.0,
	    'A1':0.0,
	    'I2':0.0,
	    'I1':0.0,
	    'mu':0.0,
	    'gamma':0.0,
	    'S':0.0,
	    'eta':0.0
	    }
	
	self.tempFiles   = []
	self.deleteFiles = []
	
    def viewMep(self):
	printElementName('MEP','-',40)
	print self.MainMep
	print self.PosMep
	print self.NegMep
	
    def getX(self):
	if self.X == 0:
	    printElementName('Number Cores X', '-',40)
	    print('Recommended 16, but you choose 4,8 or 12')
	    while True:
		answer = checker('Insert Cores')
		if answer <1 or answer > 16:
		    print('Action not valid: ', answer)
		else:
		    self.X = answer
		    break
	return self.X
    
    def getY(self):
	if self.Y == 0:
	    printElementName('Resolution Y','-',40)
	    print('Recommended 3, but you can choose:')
	    print('Low   : 2')
	    print('Medium: 3')
	    print('High  : 4')
	    while True:
		answer = checker('Insert Resolution')
		if answer <2 or answer >4:
		    print('Action not valid: ', answer)
		else:
		    self.Y = answer
		    break
	return self.Y
		
    def getDensity(self):
	if self.density == '':
	    printElementName('Choose Density','-',40)
	    print(' 1: Density')
	    print(' \t Corresponding to that formed by the external electrons, excluding the electronic density given by internal electrons (also called core electrons)')
	    print(' 2: FDensity')
	    print(' \t Full density (considering core electrons and those that are external) ')
	    while True:
		answer = checker('Insert Density')
		if answer <1 or answer >2:
		    print('Action not valid: ', answer)
		else:
		    if answer == 1:
			self.density = 'density'
		    elif answer == 2:
			self.density = 'fdensity'
		    break
	return self.density
	      
    def getTheory(self, project):
	if self.theory == '':
	    self.theory = getTheoryFile(project.files[0])
	    if self.theory == 'None':
		print('Problem with theory in files fchk')
		print('Valid Theories: MP2, SCF, CC, CI')
		sys.exit(0)
	    else:
		print('Theory Detected:'+ self.theory)
	return self.theory
    
    def operacion1(self, project):
	printElementName('OP1','-',40)
	input1 = project.getNameMainFile()
	input2 = project.getNameDenCubFile()
	output = project.getName()+'_MEP_'+project.getN()+'.cub'
	
	#print('input2', input2)
	x = self.getX()
	y = -1
	
	theory = self.getTheory(project)
	op1_a = CubeGenPot(input1, input2, output, y , x , theory )
	#op1_a.view()
	
	op1_a.viewQuery()
	#print op1_a.cube()
	
	op1_a.cube()
	 
	self.MainMep = output
	#op1_a.view()
	
	if op1_a.getStatus():
	    input1 = project.getNamePosFile()
	    output = project.getName()+'_MEP_'+ project.getN()+'+'+ project.getP()+'.cub'
	    
	    op1_b = CubeGenPot(input1, input2, output, y, x, theory)
	    op1_b.viewQuery()
	    op1_b.cube()
	    
	    self.PosMep = output
	    
	    if op1_b.getStatus():
		input1 = project.getNameNegFile()
		output = project.getName()+'_MEP_'+ project.getN()+'-'+ project.getQ()+'.cub'
		op1_c = CubeGenPot(input1, input2, output, y, x, theory)
		
		op1_c.viewQuery()
		op1_c.cube()
		
		self.paso = 1
		self.NegMep = output
		
	    else:
		printElementName('Error','-',40)
		self.paso = 0
		sys.exit(0)
		
    
	else:
	    printElementName('Error','-',40)
	    self.paso = 0
	    sys.exit(0)
	    
    def operacion2(self, project):
	printElementName('OP2','-',40)
	input1  = project.getNamePosFile()
	output = project.getName() + '_'+ project.getN()+'+'+project.getP()+'_den.cub'
	
	x = self.getX()
	
	y = self.getY()
	
	density = self.getDensity()
	
	theory = self.getTheory(project)
	
	op2 = CubeGenDens(input1, output, y, x, density, theory)
	

	op2.viewQuery()
	
	op2.cube()
	
	project.statusDen = True
	
	project.filesCub.append(output)
	
	self.tempFiles.append(output)
	
	#op2.view()
	
    def operacion3(self,project):
	printElementName('OP3','-',40)
	input1 = project.getNamePosFile()
	output = project.getName() + '_MEP_' + project.getN()+'+'+ project.getP()+'.cub'
	
	x = self.getX()
	y = self.getY()
	
	theory = self.getTheory(project)
	
	op3_1 = CubenGenPotOneFile(input1, output, y , x, theory)
	op3_1.viewQuery()
	op3_1.cube()
	
	self.PosMep = output
	
	input1 = project.getNameMainFile()
	input2 = project.getName() + '_MEP_' + project.getN()+ '+' + project.getP()+'.cub'
	
	output = project.getName() + '_MEP_' + project.getN()+ '.cub'
	y = -1
	
	op3_2 = CubeGenPot(input1, input2, output, y, x , theory)
	op3_2.viewQuery()
	
	op3_2.cube()
	
	self.MainMep = output
	
	input1 = project.getNameNegFile()
	output = project.getName() + '_MEP_' + project.getN()+'-'+project.getQ()+'.cub'
	
	op3_3 = CubeGenPot(input1, input2, output, y, x, theory)
	op3_3.viewQuery()
	
	op3_3.cube()
	self.NegMep = output
	
    def operacion4(self,project):
	printElementName('OP4','-',40)
	input1 = project.getNameMainFile()
	output = project.getName() + '_MEP_' + project.getN()+'.cub'
	
	x = self.getX()
	y = self.getY()
	
	theory = self.getTheory(project)
	
	op4_1 = CubenGenPotOneFile(input1, output, y , x, theory)
	op4_1.viewQuery()
	op4_1.cube()
	
	self.MainMep= output
	
	input1 = project.getNamePosFile()
	input2 = project.getName() + '_MEP_' + project.getN()+ '.cub'
	
	output = project.getName() + '_MEP_' + project.getN()+ '+' + project.getP()+'.cub'
	y = -1
	
	op4_2 = CubeGenPot(input1, input2, output, y, x, theory)
	op4_2.viewQuery()
	
	op4_2.cube()
	
	self.PosMep = output
	
	input1 = project.getNameNegFile()
	output = project.getName() + '_MEP_' + project.getN()+'-'+project.getQ()+'.cub'
	
	op4_3 = CubeGenPot(input1, input2, output, y, x, theory)
	op4_3.viewQuery()
	
	op4_3.cube()
	self.NegMep = output
	
    def operacion5(self,project):
	printElementName('OP5','-',40)
	input1 = project.getNameNegFile()
	output = project.getName() + '_MEP_' + project.getN()+'-'+ project.getQ() +'.cub'
	
	x = self.getX()
	y = self.getY()
	
	theory = self.getTheory(project)
	
	op5_1 = CubenGenPotOneFile(input1, output, y , x, theory)
	op5_1.viewQuery()
	op5_1.cube()
	self.NegMep = output
	
	input1 = project.getNamePosFile()
	input2 = project.getName() + '_MEP_' + project.getN()+ '-'+ project.getQ()  +'.cub'
	
	output = project.getName() + '_MEP_' + project.getN()+ '+' + project.getP()+'.cub'
	y = -1
	
	op5_2 = CubeGenPot(input1, input2, output, y, x, theory)
	op5_2.viewQuery()
	
	op5_2.cube()
	self.PosMep = output
	
	input1 = project.getNameMainFile()
	output = project.getName() + '_MEP_' + project.getN()+'.cub'
	
	op5_3 = CubeGenPot(input1, input2, output, y, x, theory)
	op5_3.viewQuery()
	
	op5_3.cube()
	self.MainMep = output
    
    def getEnergy(self, filename):
	energy = 0.0
	with open(filename) as f:
	    lines = f.readlines()  
	    f.close()
	#print('filename',filename)    
	#print('theory:',self.theory)
	if self.theory == 'SCF':
	    for line in lines:
		if line.upper().find('SCF DONE')!= -1:
		    t = line.split()
		    energy = float(t[4])
		    break
	elif self.theory == 'MP2':
	    for line in lines:
		if line.upper().find('EUMP2')!= -1:
		    t = line.split()
		    number = t[5]
		    #print('len:', len(t))
		    #print('line:',t)
		    #print('Energy:',number)
		    energy = float(number.replace("D", "E"))
		    break
		    
	elif self.theory == 'CC':
	    for line in lines:
		if line.upper().find('E(CORR)=')!= -1:
		    t = line.split()
		    if line.upper().find('CONVERGED')!=-1:
			number = t[4]
		    else:
			number = t[3]
		    #print('line:',t)
		    #print('Energy:',number)
		    energy = float(number)
	
	elif self.theory == 'CI':
	    #print(filename)
	    for line in lines:
		if line.upper().find('E(CI)=')!= -1:
		    t = line.split()
		    if line.upper().find('CONVERGED')!=-1:
			number = t[4]
		    else:
			number = t[3]
		    #print('len:', len(t))
		    #print('line:',t)
		    #print('Energy:',number)		    
		    energy = float(number)

	#print('energy:',energy)
	return energy
	
    def subEnergy(self, value1, value2, aprox):
	return round(value1-value2,aprox)
    
    def addEnergy(self,value1, value2, aprox):
	return round(value1+value2,aprox)
	
    def factorEnergy(self,value,factor, aprox):
	return round(value*factor, aprox)
	
    def powEnergy(self, value, ex, aprox):
	return round( pow(value, ex), aprox)
    
    
    
    def paso1(self, project, name,step,maxStep):
	info = name +' '+step+'/'+maxStep
	printElementName(info,'-',40)
	
	if project.statusDenCub == False:
	    while True:
		printElementName('_N+p_den.cub File is missing!', '*',40)
		answer = str(raw_input('Do you want create it? y/n\n'))
		if answer == 'y':
		    self.operacion2(project)
		    #project.view()
		    self.operacion1(project)
		    break
		elif answer == 'n':
		    while True:
			printElementName('Options','-',40)
			print '3: From N+p.fchk File'
			print '4: From N.fchk File'
			print '5: From N-q.fchk File'
			
			answer = checker('Choose Option')
			
			if answer == 3:
			    self.operacion3(project)
			    self.paso = 1
			    break
			elif answer == 4:
			    self.operacion4(project)
			    self.paso = 1
			    break 
			elif answer == 5:
			    self.operacion5(project)
			    self.paso = 1
			    break
		    break
		else:
		    print('Action not valid',answer)
	else:
	    #print('OP1',project.statusDenCub)
	    self.operacion1(project)
	    
    def paso2(self,project,name,step,maxStep):
	info = name +'' + step + '/'+maxStep
	#self.viewMep()
    
	printElementName(info,'-',40)
	line = 'Molecular electrostatic potential( system with '+project.getN()+'+'+project.getP() +' electrons)'
	
	printElementName('Writing','*',40)
	print self.PosMep 
	
	editL1L2(self.PosMep,self.PosMep,line)
	
	line = 'Molecular electrostatic potential( system with '+project.getN()+ ' electrons)'
	editL1L2(self.MainMep,self.MainMep, line)
	
	print self.MainMep
	
	line = 'Molecular electrostatic potential( system with '+project.getN()+'-'+project.getQ() + ' electrons)'
    	editL1L2(self.NegMep,self.NegMep, line)
    	
    	print self.NegMep
    	
    	self.tempFiles.append(self.NegMep)
    	self.tempFiles.append(self.PosMep)
    	
    	self.paso= 2
    	
    	
    def paso3a(self, value, action,inputFile1, inputFile2,outputFile ):
    
	#print ('value:',value)
    
	if value == 1:

	    t= CubeManP3NoScale(inputFile1, inputFile2,outputFile, action)
	    t.viewQuery()
	    t.cube()
	
	elif value > 1:
	    outputFilePro = outputFile.replace('_F-FP_FDA.cub','_pro_F-FP_FDA.cub')
	    outputFilePro = outputFilePro.replace('_F+FP_FDA.cub','_pro_F+FP_FDA.cub')
	    
	    t1 = CubeManP3NoScale(inputFile1, inputFile2, outputFilePro, action)
	    t1.viewQuery()
	    t1.cube()
	    
	    aprox = 8
	    factor = round(1./value,aprox)
	    #print( value, factor)
	    
    	    t2 = CubeManP3Scale(outputFilePro, outputFile, factor)
    	    t2.viewQuery()
    	    t2.cube()
    	    
    	    self.deleteFiles.append(outputFilePro)
    	    
    	return outputFile

    def paso3(self,project, name, step, maxStep):
    
	info = name +' '+ step+'/'+maxStep
	printElementName(info,'-',40)
	
	
	self.FDAPos = self.paso3a(int(project.getP()), 'SU', self.MainMep , self.PosMep  ,  project.getName()+'_F+FP_FDA.cub')

	self.FDANeg = self.paso3a(int(project.getQ()), 'SU', self.NegMep  , self.MainMep ,  project.getName()+'_F-FP_FDA.cub') 
    
	self.paso = 3
	
    def paso4(self, project, name, step, maxStep):
	info = name+' '+ step+'/'+maxStep
	printElementName(info,'-',40)
	line = 'Nucleophilic Fukui function potential by means of the finite difference approximation'
	
	printElementName('Writing','*',40)
	print self.FDAPos
	
	editL1L2(self.FDAPos, self.FDAPos, line)
	
	print self.FDANeg
	line = line.replace('Nucleophilic','Electrophilic')
	editL1L2(self.FDANeg, self.FDANeg, line)
	
	self.paso = 4
	
    def paso5b(self, action, inputFile1, inputFile2, outputFile ):
    
	t = CubeManP3NoScale(inputFile1, inputFile2, outputFile, action)
	t.viewQuery()
	t.cube()
	return outputFile
	
    def paso5a(self, action, inputFile1, inputFile2, outputFile):
	outputFilePro = outputFile.replace('_FFP_FDA.cub','_pro_FFP_FDA.cub')
	
	t1= CubeManP3NoScale(inputFile1, inputFile2, outputFilePro, action)
	t1.viewQuery()
	t1.cube()
	
	scale = 0.5
	t2 = CubeManP3Scale(outputFilePro, outputFile, scale)
	t2.viewQuery()
	t2.cube()
	
	self.deleteFiles.append(outputFilePro)
	
	return outputFile
	
    def paso5(self,project, name, step, maxStep):
	info = name +' '+ step+'/'+maxStep
	printElementName(info, '-', 40)
	
	self.FFP = self.paso5a( 'A', self.FDAPos, self.FDANeg, project.getName()+'_FFP_FDA.cub' )
	self.DDP = self.paso5b('SU', self.FDAPos, self.FDANeg, project.getName()+'_DDP_FDA.cub' )
	
	
	self.paso = 5
	
    def paso6(self, name, step, maxStep):
	info = name+' '+step+'/'+maxStep
	printElementName(info,'-',40)
	
	line = 'Fukui function potential by means of finite difference approximation'
	
	printElementName('Writing','*',40)
	print self.FFP
	
	editL1L2(self.FFP, self.FFP, line)
	
	line = line.replace('Fukui function','Dual descriptor')
    
	print self.DDP
	
	editL1L2(self.DDP, self.DDP, line)
	
	self.paso = 6
	
    def paso7(self, name, step, maxStep):
	info = name +''+step+'/'+maxStep
	printElementName(info,'-',40)
	printElementName('Delete Files','*',40)
	for t in self.deleteFiles:
	    print t
	removeFiles(self.deleteFiles)
	
	self.deleteFiles = []  # vaciar la lista
	printElementName('Temporal Files','-',40)
	for t in self.tempFiles:
	    print t
	    while True:
		answer = str(raw_input('Do you want delete it? y/n\n'))
		if answer == 'y':
		    self.deleteFiles.append(t)
		    break
		elif answer == 'n':
		    break
		else:
		    print('Action not valid',answer)
	    
	printElementName('Delete Files','*',40)
	for t in self.deleteFiles:
	    print t
	removeFiles(self.deleteFiles)
	
	
	self.paso = 7
	
	return 0
    
    def paso8(self, name, step, maxStep, files):
    
	info = name +''+step+'/'+maxStep
	printElementName(info,'-',40)
	# find energies
	for f in files:
	    if 'N+2.log' in f:
		self.Energy['E(N+2)'] = self.getEnergy(f)
	    elif 'N+1.log' in f:
		self.Energy['E(N+1)'] = self.getEnergy(f)
	    elif 'N.log' in f:
		self.Energy['E(N)'] = self.getEnergy(f)
	    elif 'N-1.log' in f:
		self.Energy['E(N-1)'] = self.getEnergy(f)
	    elif 'N-2.log' in f:
		self.Energy['E(N-2)'] = self.getEnergy(f)
	aprox = 8
	
	if self.Energy['E(N)'] == 0.0 and self.Energy['E(N-1)'] == 0.0 and self.Energy['E(N-2)'] == 0.0 and self.Energy['E(N+1)'] == 0.0 and  self.Energy['E(N+2)'] == 0.0:
	    sys.exit('Problem with get Energies')
	
	printElementName('Extract - Energies','*',40)
	
	for key, value in self.Energy.items():
	    print(str(key) +'\t = '+ str(value))
	
	printElementName('Loading - Parameters','*',40)
	
	self.Indicadores['A2'] = self.subEnergy( self.Energy['E(N+1)'],self.Energy['E(N+2)'] , aprox)
	self.Indicadores['A1'] = self.subEnergy( self.Energy['E(N)']   ,self.Energy['E(N+1)'] , aprox)
	
	self.Indicadores['I1'] = self.subEnergy( self.Energy['E(N-1)']   ,self.Energy['E(N)'] , aprox)
	self.Indicadores['I2'] = self.subEnergy( self.Energy['E(N-2)']   ,self.Energy['E(N-1)'] , aprox)
	
		
	self.Indicadores['mu'] = self.factorEnergy( self.addEnergy(self.Indicadores['A1'] , self.Indicadores['I1'], aprox)  ,-0.5,aprox)
	
	self.Indicadores['eta']= self.subEnergy(self.Indicadores['I1'] ,self.Indicadores['A1'], aprox)
	
	self.Indicadores['S']  = self.powEnergy(self.Indicadores['eta'] , -1, aprox  )
	
	self.Indicadores['gamma']= self.factorEnergy(
			 self.subEnergy( 
			    self.subEnergy( self.addEnergy( self.Indicadores['I1'] , self.Indicadores['A1']  , aprox), 
					    self.Indicadores['I2'] ,
					    aprox),
			    self.Indicadores['A2'] ,
			    aprox),
			 0.5   ,
			  aprox)
			  
	#print('Energies:',self.Energy)
	#print('Indicadores:', self.Indicadores)
	
	
	for key, value in self.Indicadores.items():
	    print(str(key) +'\t = '+ str(value))
	
	
	self.paso = 8
	
	return 0


	
    def paso9(self,project,name, step, maxStep):
	info = name +step+'/'+maxStep
	printElementName(info,'-',40)
	
	aprox = 8
	
	inputFile  = self.DDP
	outputFile =  project.getName()+'_'+'LHSP1_FDA.cub'
	factor = round(pow(self.Indicadores['S'],2),aprox)
	#print(self.Indicadores['S'],factor)
	print('Factor (S^2)=\t'+str(factor) )
	t1 = CubeManP3Scale(inputFile,outputFile,factor)
	t1.viewQuery()
	t1.cube()
	
	
	self.paso = 9

	
	return 0     
	
    def paso10(self,project,name, step, maxStep):
	info = name +step+'/'+maxStep
	printElementName(info,'-',40)
	
	aprox = 8
	
	inputFile  = self.FFP
	outputFile =  project.getName()+'_'+'LHSP2_FDA.cub'
	factor = round(self.Indicadores['gamma']*pow(self.Indicadores['S'],3),aprox)
	#print(self.Indicadores['gamma'],self.Indicadores['S'] ,factor)
	print('Factor (gamma*S^3)=\t'+str(factor) )
	t1 = CubeManP3Scale(inputFile,outputFile,factor)
	t1.viewQuery()
	t1.cube()
	
	
	self.paso = 10

	
	return 0 
	
    def paso11(self,project,name, step, maxStep):
	info = name +step+'/'+maxStep
	printElementName(info,'-',40)
	
	aprox = 8
	
	inputFile1  = project.getName()+'_'+'LHSP1_FDA.cub'
	
	inputFile2 =  project.getName()+'_'+'LHSP2_FDA.cub'
	
	outputFile =  project.getName()+'_'+'LHSP_FDA.cub'
	
	action = 'Su'
	
	t1 = CubeManP3NoScale(inputFile1, inputFile2,outputFile, action)
	t1.viewQuery()
	t1.cube()
	
	
	self.paso = 11

	
	return 0 
	
    def paso12(self,project,name, step, maxStep):
	info = name +step+'/'+maxStep
	printElementName(info,'-',40)
	
	file_1 = project.getName()+'_'+'LHSP1_FDA.cub'
	info = name +step+'/'+maxStep
	

	line = 'First component of the local hypersoftness potential by means of the finite difference approximation.'
	    
	printElementName('Writing','*',40)
	print file_1

	editL1L2(file_1,file_1 , line)

	line = 'Second component of the local hypersoftness potential FDA by means of the finite difference approximation.'

	file_1 = project.getName()+'_'+'LHSP2_FDA.cub'
	print file_1


	editL1L2(file_1,file_1, line)
	
	line = 'Local hypersoftness potential by means of the finite difference approximation.'

	file_1 = project.getName()+'_'+'LHSP_FDA.cub'
	print file_1

	editL1L2(file_1, file_1, line)

	self.paso = 12

	   
    def paso13(self,name, step, maxStep, filename):
	info = name +step+'/'+maxStep
	printElementName(info,'-',40)
	
	msn = 'Export Energies and Parameters'
	printElementName(msn,'*',40)
	csv(filename,self.Energy,self.Indicadores)
	print(filename)

	
	self.paso = 13
	return 0

	
	
	
	

	


	
	
	
	
    