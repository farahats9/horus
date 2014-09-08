#!/usr/bin/python
# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------#
#                                                                       #
# This file is part of the Horus Project                                #
#                                                                       #
# Copyright (C) 2014 Mundo Reader S.L.                                  #
#                                                                       #
# Date: March & August 2014                                             #
# Author: Jesús Arroyo Torrens <jesus.arroyo@bq.com>                    #
#                                                                       #
# This program is free software: you can redistribute it and/or modify  #
# it under the terms of the GNU General Public License as published by  #
# the Free Software Foundation, either version 3 of the License, or     #
# (at your option) any later version.                                   #
#                                                                       #
# This program is distributed in the hope that it will be useful,       #
# but WITHOUT ANY WARRANTY; without even the implied warranty of        #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the          #
# GNU General Public License for more details.                          #
#                                                                       #
# You should have received a copy of the GNU General Public License     #
# along with this program. If not, see <http://www.gnu.org/licenses/>.  #
#                                                                       #
#-----------------------------------------------------------------------#

__author__ = "Jesús Arroyo Torrens <jesus.arroyo@bq.com>"
__license__ = "GNU General Public License v3 http://www.gnu.org/licenses/gpl.html"

import cv2
import math
import numpy as np

class Core:
	""" """
	def __init__(self):
		""" """
		self.points = None
		self.colors = None
		
		self.imgRaw  = None
		self.imgLas  = None
		self.imgDiff = None
		self.imgBin  = None
		self.imgLine = None

		self.points = None
		self.colors = None

	def initialize(self, imgType='raw',
						 openEnable=True,
						 openValue=2,
						 threholdEnable=True,
						 thresholdValue=30,
						 useCompact=True,
						 rhoMin=-100,
						 rhoMax=100,
						 hMin=0,
						 hMax=200,
						 zOffset=0,
						 degrees=0.45,
						 width=600,
						 height=800,
						 alpha=30.0,
						 calibrationMatrix=None,
						 laserCoordinates=None,
						 laserDepth=None,
						 rotationMatrix=None,
						 translationVector=None,
						 useLeftLaser=True):

		#-- Image type parameters
		self.imgType = imgType

		#-- Image Processing Parameters

		self.openEnable = openEnable
		self.openValue = openValue

		self.thresholdEnable = threholdEnable
		self.thresholdValue = thresholdValue

		#-- Point Cloud Parameters
		self.useCompact = useCompact

		self.rhoMin = rhoMin
		self.rhoMax = rhoMax
		self.hMin = hMin
		self.hMax = hMax

		self.zOffset = zOffset

		self.theta = 0

		self.degrees = degrees

		self.setResolution(width, height)

		self.W = np.ones((height,width))*np.linspace(0,width-1,width)

		#-- Constant Parameters initialization
		self.rad = math.pi / 180.0

		self.alpha = alpha
		
		alpha = self.alpha * self.rad

		#-- Calibration parameters
		if calibrationMatrix is not None:
			fx = calibrationMatrix[0][0]
			fy = calibrationMatrix[1][1]
			cx = calibrationMatrix[0][2]
			cy = calibrationMatrix[1][2]

		if laserCoordinates is not None:
			u11 = laserCoordinates[0][0]
			u12 = laserCoordinates[0][1]
			u21 = laserCoordinates[1][0]
			u22 = laserCoordinates[1][1]

		if laserDepth is not None:
			z = laserDepth

		#-- Determine point cloud X, Y, Z matrices in camera coordinates

		zl = z * (1 + (u11 - cx + ((u12-u11)/height) * np.linspace(0,height-1,height)) / (fx * math.tan(alpha)))

		a = (np.linspace(0,width-1,width) - cx) / fx
		b = (np.linspace(0,height-1,height) - cy) / fy

		Zc = ((np.ones((width,height)) * zl).T * (1. / (1 + a / math.tan(alpha)))).T
		Xc = (a * Zc.T).T
		Yc = b * Zc

		#-- Move point cloud matrices to world coordinates

		R = np.matrix(rotationMatrix)
		T = np.matrix(translationVector)

		Rt = R.T
		RT = R.T*T.T

		self.Xw = (Rt[0,0] * Xc + Rt[0,1] * Yc + Rt[0,2] * Zc - RT[0]).T
		self.Yw = (Rt[1,0] * Xc + Rt[1,1] * Yc + Rt[1,2] * Zc - RT[1]).T
		self.Zw = (Rt[2,0] * Xc + Rt[2,1] * Yc + Rt[2,2] * Zc - RT[2]).T

	def setResolution(self, width, height):
		self.width = width
		self.height = height

	def setOpen(self, enable, value):
		self.openEnable = enable
		self.openValue = value

	def setThreshold(self, enable, value):
		self.thresholdEnable = enable
		self.thresholdValue = value

	def setUseCompactAlgorithm(self, useCompact):
		self.useCompact = useCompact

	def setRangeFilter(self, rhoMin, rhoMax, hMin, hMax):
		self.rhoMin = rhoMin
		self.rhoMax = rhoMax
		self.hMin = hMin
		self.hMax = hMax

	def setZOffset(self, zOffset):
		self.zOffset = zOffset

	def setDegrees(self, degrees):
		self.degrees = degrees

	def getImage(self):
		""" """
		return { 'raw' : self.imgRaw,
				 'las' : self.imgLas,
				 'diff' : self.imgDiff,
				 'bin' : self.imgBin,
				 'line' : self.imgLine
				}[self.imgType]

	def setImageType(self, imgType):
		""" """
		self.imgType = imgType

	def getDiffImage(self, img1, img2):
		""" """
		r1 = cv2.split(img1)[0]
		r2 = cv2.split(img2)[0]

		return cv2.subtract(r1, r2)

	def imageProcessing(self, image):
		""" """
		#-- Image Processing

		if self.openEnable:
			kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(self.openValue,self.openValue))
			image = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)

		if self.thresholdEnable:
			image = cv2.threshold(image, self.thresholdValue, 255.0, cv2.THRESH_BINARY)[1]

		return image

	def pointCloudGeneration(self, imageRaw, imageBin):
		""" """
		#-- Line generation
		s = imageBin.sum(1)
		v = np.nonzero(s)[0]
		if self.useCompact:
			i = imageBin.argmax(1)
			l = ((i + (s/255.-1) / 2.)[v]).T.astype(int)
		else:
			w = (self.W * imageBin).sum(1)
			l = (w[v] / s[v].T).astype(int)

		self.imgLine = np.zeros_like(imageRaw)
		self.imgLine[v,l] = 255.0

		#-- Obtaining point cloud
		xw = self.Xw[v,l]
		yw = self.Yw[v,l]
		zw = self.Zw[v,l]
		thetaR = self.theta * self.rad
		x = np.array(xw * math.cos(thetaR) - yw * math.sin(thetaR))
		y = np.array(xw * math.sin(thetaR) + yw * math.cos(thetaR))
		z = np.array(zw + self.zOffset)
		if z.size > 0:
			points = np.concatenate((x,y,z)).reshape(3,z.size).T
			colors = np.copy(imageRaw[v,l])
			rho = np.sqrt(x*x + y*y)
			return points, colors, rho, z
		else:
			return None, None, None, None

	def pointCloudFilter(self, points, colors, rho, z):
		""" """
		#-- Point Cloud Filter
		idx = np.where((z >= self.hMin) &
					   (z <= self.hMax) &
					   (rho >= self.rhoMin) &
					   (rho <= self.rhoMax))[1]

		return points[idx], colors[idx]

	def getPointCloud(self, imageRaw, imageLas):
		""" """
 		#-- Update Raw, Laser and Diff images
		self.imgRaw = imageRaw
		self.imgLas = imageLas
		imgDiff = self.getDiffImage(imageLas, imageRaw)
		self.imgDiff = cv2.merge((imgDiff,imgDiff,imgDiff))

		imgBin = self.imageProcessing(imgDiff)

		self.imgBin = cv2.merge((imgBin,imgBin,imgBin))

		points, colors, rho, z = self.pointCloudGeneration(imageRaw, imgBin)

		if points != None and colors != None:
			points, colors = self.pointCloudFilter(points, colors, rho, z)

		if points != None and colors != None:
			if self.points == None and self.colors == None:
				self.points = points
				self.colors = colors
			else:
				self.points = np.concatenate((self.points, points))
				self.colors = np.concatenate((self.colors, colors))

 		self.theta += self.degrees

		return points, colors