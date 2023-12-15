# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'latestinterface.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import vtkmodules.all as vtk
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QAction, QVBoxLayout, QWidget, QPushButton, QDockWidget, QTextBrowser, QFrame,QColorDialog,QDialog,QLabel, QLineEdit, QHBoxLayout,QInputDialog
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
import os
import math
from collections import namedtuple
import numpy as np
from PyQt5.uic import loadUi

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout
#internal
try:
    import src.DicomCall as DCcall
    import src.sliceDcom as styleSlice
    import src.lineVtk as lineStyle
    import src.angleVtk as angleStyle
    import src.circleVtk as circleStyle
    import src.paintVtk as paintStyle
except:
    import DicomCall as DCcall
    import sliceDcom as styleSlice
    import lineVtk as lineStyle
    import angleVtk as angleStyle
    import circleVtk as circleStyle
    import paintVtk as paintStyle

class Ui_MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi('LooNYong\src\latestt.ui', self)

        self.actionExit.triggered.connect(self.closeEvent)
        self.actionSelect_Folder.triggered.connect(self.openFile)
        self.threeButton.toggled.connect(self.dimensionChanging)
        self.twoButton.toggled.connect(self.dimensionChanging)
        self.radioButton.toggled.connect(self.dimensionChanging)

        self.pushButton_2.setCheckable(True)
        self.pushButton_2.clicked.connect(self.on_button_clicked)

        self.pushButton_23.clicked.connect(self.resetCameraF)
        self.pushButton_25.clicked.connect(self.Capture)
        self.pushButton_26.clicked.connect(self.magnifier)
        self.pushButton_27.clicked.connect(self.magnifierout)
        self.pushButton_47.clicked.connect(self.resetcamera3d)
        self.pushButton_49.clicked.connect(self.save3d)

        self.pushButton_45.setCheckable(True)
        self.pushButton_45.clicked.connect(self.changetobone)
        self.pushButton_46.setCheckable(True)
        self.pushButton_46.clicked.connect(self.change_tissue)

        self.pushButton_3.clicked.connect(lambda:self.window_level(0))
        self.pushButton_4.clicked.connect(lambda:self.window_level(1))
        self.pushButton_5.clicked.connect(lambda:self.window_level(2))
        self.pushButton_11.clicked.connect(lambda:self.window_level(3))
        self.pushButton_18.clicked.connect(lambda:self.window_level(4))
        self.pushButton_24.clicked.connect(lambda:self.window_level(5))

        self.pushButton_30.clicked.connect(lambda:self.deleteWidget(0))
        self.pushButton_32.clicked.connect(lambda:self.deleteWidget(1))
        self.pushButton_34.clicked.connect(lambda:self.deleteWidget(2))

        self.radioButton.setCheckable(False)

        self.layoutVTK = QVBoxLayout(self.widget_9)
        self.actionAbout_Us.triggered.connect(lambda:self.getMessage("This project conducted by Loo and Yong, call us for more information.", "Introduction"))
        

        ### measurement
        self.layoutMesaure=QVBoxLayout(self.widget_16)
        self.widgetMeasure = QVTKRenderWindowInteractor(self.widget_16)
        self.layoutMesaure.addWidget(self.widgetMeasure)

        self.pushButton_51.setCheckable(True)
        self.pushButton_52.setCheckable(True)
        self.pushButton_53.setCheckable(True)
        self.pushButton_54.setCheckable(True)

        self.pushButton_51.clicked.connect(lambda:self.measurementVtk(0))
        self.pushButton_52.clicked.connect(lambda:self.measurementVtk(1))
        self.pushButton_53.clicked.connect(lambda:self.measurementVtk(2))
        self.pushButton_54.clicked.connect(lambda:self.measurementVtk(3))

        self.pushButton_38.clicked.connect(lambda:self.showImage(0))
        self.pushButton_39.clicked.connect(lambda:self.showImage(1))
        self.pushButton_40.clicked.connect(lambda:self.showImage(2))

        self.pushButton_50.clicked.connect(self.captureMeasure)


        self.vtk_widget2=None
        self.vtk_widget3=None
        self.vtk_widget4=None
        self.vtk_widget3D=None

        self.widgetc1 = QVTKRenderWindowInteractor(self.widget_9)
        self.layoutVTK.addWidget(self.widgetc1)
        self.layoutVTK = QVBoxLayout(self.widget_11)
        self.widgetc2 = QVTKRenderWindowInteractor(self.widget_11)
        self.layoutVTK.addWidget(self.widgetc2)
        self.layoutVTK = QVBoxLayout(self.widget_12)
        self.widgetc3 = QVTKRenderWindowInteractor(self.widget_12)
        self.layoutVTK.addWidget(self.widgetc3)

    #### measurement widget
    def measurementVtk(self, x=None):
        try:
            if x==0: 
                style=lineStyle.CustomInteractorStyle()
                self.pushButton_52.setChecked(False)
                self.pushButton_53.setChecked(False)
                self.pushButton_54.setChecked(False)
            elif x==1: 
                style=angleStyle.CustomInteractorStyle()
                self.pushButton_51.setChecked(False)
                self.pushButton_53.setChecked(False)
                self.pushButton_54.setChecked(False)

            elif x==2: 
                style=circleStyle.CustomInteractorStyle()
                self.pushButton_52.setChecked(False)
                self.pushButton_51.setChecked(False)
                self.pushButton_54.setChecked(False)
            elif x==3: 
                style=paintStyle.CustomInteractorStyle()
                self.pushButton_52.setChecked(False)
                self.pushButton_53.setChecked(False)
                self.pushButton_51.setChecked(False)    
            style.set_renderer(self.rendererMe, self.renderWindowMe1)
            self.widgetMeasure.SetInteractorStyle(style)
        except: pass

    #Show image viewer
    def showImage(self, x):
        try:

            self.rendererMe = self.widgetMeasure.GetRenderWindow().GetRenderers().GetFirstRenderer()

            if self.rendererMe is None:
                # If no renderer exists, create one
                self.rendererMe = vtk.vtkRenderer()
                self.renderWindowMe1= self.widgetMeasure.GetRenderWindow()
                self.renderWindowMe1.AddRenderer(self.rendererMe)

            self.rendererMe.RemoveAllViewProps()  # Clear existing props

            if x==0:
                actor=self.actora
            elif x==1:
                actor=self.actorb
            else:
                actor=self.actorc

            #.widgetMeasure.SetRenderWindow(renderWindow)
            self.rendererMe.AddActor(actor)
            style=vtk.vtkInteractorStyleImage()
            self.widgetMeasure.SetInteractorStyle(style)
            #self.widgetMeasure.Initialize()

            self.widgetMeasure.GetRenderWindow().Render()
            self.radioButton.setCheckable(True)
            self.radioButton.setChecked(True)
            self.stackedWidget_2.setCurrentIndex(2)
        except:
            pass

    #Capture for image viewer
    def captureMeasure(self):
        try:
            file_name, _ = QFileDialog.getSaveFileName(None, "Save Image", "", "PNG Files (*.png);;JPEG Files (*.jpg *.jpeg)")
            try:
                w1 = vtk.vtkWindowToImageFilter()
                w1.SetInput(self.widgetMeasure.GetRenderWindow())
                w1.Update()
                writer = vtk.vtkPNGWriter()
                writer.SetFileName(file_name)
                writer.SetInputConnection(w1.GetOutputPort())
                writer.Write()
            except: pass
        except:
            pass

    #Open the folder path
    def openFile(self):
        
        folder_path  = QFileDialog.getExistingDirectory()
        if folder_path:
            self.openFolderDcom(folder_path)

    #Open the selected dicom into 2d and 3d dicom model
    def openFolderDcom(self, folderName):
        if self.vtk_widget3D==None:
        ### main widget
            self.vtk_widget3D = QVTKRenderWindowInteractor(self.stackedWidget_2.widget(1))
            style =vtk.vtkInteractorStyleTrackballCamera()
            #change style for interactor 
            self.vtk_widget3D.SetInteractorStyle(style)
            self.horizontalLayout_2.addWidget(self.vtk_widget3D)

            self.renderer3D = vtk.vtkRenderer()
            self.renderWindow3D = self.vtk_widget3D.GetRenderWindow()

            self.renderer3D.ResetCamera()
            self.renderer3D.SetBackground(0.5,0.5,0.5)
            #add renderer to the main widget
            self.renderWindow3D.AddRenderer(self.renderer3D)
        try:
            self.renderer3D.RemoveActor(self.volume)

        except:
            pass


        #3D file
        self.reader ,self.volume= DCcall.DicomCall(folderName).dicom3DCall()
        self.renderer3D.AddVolume(self.volume)
        self.renderWindow3D.Render()


        ### slice 1
        if self.vtk_widget2 == None:
            self.vtk_widget2 = QVTKRenderWindowInteractor(self.stackedWidget_2.widget(0))
            self.axial_hBox_7.addWidget(self.vtk_widget2)

            self.renderer2 = vtk.vtkRenderer()
            self.renderWindow2 = self.vtk_widget2.GetRenderWindow()

            self.renderer2.ResetCamera()
            #add renderer to the main widget
            self.renderWindow2.AddRenderer(self.renderer2)


        #2D file
        self.reimage_viewerader2 ,self.image_viewer= DCcall.DicomCall(folderName).dicomFolderCall()
        #self.image_viewer.SetSliceOrientationToYZ()
        self.image_viewer.SetRenderWindow(self.renderWindow2)
        segg= styleSlice.MyVtkInteractorStyleImage()
        #segg2=styleSlice.StatusMessage()


        my_interactor_style = segg
        my_interactor_style.set_image_viewer(self.image_viewer)
        my_interactor_style.set_status_label(self.label_5)
        my_interactor_style.set_status_bar(self.sagittal_vSlider_4, self.coronal_vSlider_4)

        self.image_viewer.SetupInteractor(self.vtk_widget2)
        #self.renderer2.AddViewProp(self.image_viewer.GetImageActor())

        self.vtk_widget2.SetInteractorStyle(my_interactor_style)

        self.vtk_widget2.Initialize()
        #self.renderWindow2.Render()
        self.image_viewer.Render()


        ###slice 2
        if self.vtk_widget3==None:
            self.vtk_widget3 = QVTKRenderWindowInteractor(self.stackedWidget_2.widget(0))
            self.saggital_hBox_4.addWidget(self.vtk_widget3)

            self.renderer3 = vtk.vtkRenderer()
            self.renderWindow3 = self.vtk_widget3.GetRenderWindow()

            self.renderer3.ResetCamera()
            
            #add renderer to the main widget
            self.renderWindow3.AddRenderer(self.renderer3)

        self.reimage_viewerader3 ,self.image_viewer2= DCcall.DicomCall(folderName).dicomFolderCall()
        segg1= styleSlice.MyVtkInteractorStyleImage()
        #segg2=styleSlice.StatusMessage()
        self.image_viewer2.SetRenderWindow(self.renderWindow3)
        self.image_viewer2.SetSliceOrientationToXZ()
        

        my_interactor_style1 = segg1
        my_interactor_style1.set_image_viewer(self.image_viewer2)
        my_interactor_style1.set_status_label(self.label_6)
        my_interactor_style1.set_status_bar(self.axial_hSlider_7, self.coronal_hSlider_4)

        self.image_viewer2.SetupInteractor(self.vtk_widget3)
        

        self.vtk_widget3.SetInteractorStyle(my_interactor_style1)

        self.vtk_widget3.Initialize()
        self.renderWindow3.Render()

        ###slice 3
        if self.vtk_widget4==None:
            self.vtk_widget4 = QVTKRenderWindowInteractor(self.stackedWidget_2.widget(0))
            self.coronal_hBox_4.addWidget(self.vtk_widget4)

            self.renderer4 = vtk.vtkRenderer()
            self.renderWindow4 = self.vtk_widget4.GetRenderWindow()

            self.renderer4.ResetCamera()
            
            #add renderer to the main widget
            self.renderWindow4.AddRenderer(self.renderer4)

        self.reimage_viewerader4 ,self.image_viewer3= DCcall.DicomCall(folderName).dicomFolderCall()
        segg2= styleSlice.MyVtkInteractorStyleImage()
        #segg2=styleSlice.StatusMessage()
        self.image_viewer3.SetRenderWindow(self.renderWindow4)
        self.image_viewer3.SetSliceOrientationToYZ()
        my_interactor_style2 = segg2
        my_interactor_style2.set_image_viewer(self.image_viewer3)
        my_interactor_style2.set_status_label(self.label_7)
        my_interactor_style2.set_status_bar(self.axial_vSlider_7, self.sagittal_hSlider_4)

        self.image_viewer3.SetupInteractor(self.vtk_widget4)
        

        self.vtk_widget4.SetInteractorStyle(my_interactor_style2)

        self.vtk_widget4.Initialize()
        self.renderWindow4.Render()
        
    # to change the page between 2d,3d and image viewer
    def dimensionChanging(self):
        if self.threeButton.isChecked():
            self.stackedWidget_2.setCurrentIndex(1)
        elif self.twoButton.isChecked():
            self.stackedWidget_2.setCurrentIndex(0)
        else:
            self.stackedWidget_2.setCurrentIndex(2)

    #reset camera for 2d dicom
    def resetCameraF(self):
        try:
            self.image_viewer.GetRenderer().ResetCamera()
            self.image_viewer2.GetRenderer().ResetCamera()
            self.image_viewer3.GetRenderer().ResetCamera()
            self.image_viewer.Render()
            self.image_viewer2.Render()
            self.image_viewer3.Render()
        except:
            pass

    # to zoom in the 2d dicom
    def magnifier(self):
        try:
            self.image_viewer.GetRenderer().GetActiveCamera().Zoom(1.2)
            self.image_viewer2.GetRenderer().GetActiveCamera().Zoom(1.2)
            self.image_viewer3.GetRenderer().GetActiveCamera().Zoom(1.2)
            self.image_viewer.Render()
            self.image_viewer2.Render()
            self.image_viewer3.Render()
        except:
            pass

    # to zoom out the 2d dicom
    def magnifierout(self):
        try:
            self.image_viewer.GetRenderer().GetActiveCamera().Zoom(0.8)
            self.image_viewer2.GetRenderer().GetActiveCamera().Zoom(0.8)
            self.image_viewer3.GetRenderer().GetActiveCamera().Zoom(0.8)
            self.image_viewer.Render()
            self.image_viewer2.Render()
            self.image_viewer3.Render()
        except:
            pass

    # Capture the 2d dicom and put into the capture image
    def Capture(self):
        
        try:
            w2if = vtk.vtkWindowToImageFilter()
            w2if.SetInput(self.image_viewer.GetRenderWindow())
            w2if.Update()
            # Capture the image
            # Get the captured image data
            image_data = w2if.GetOutput()
            w2if2 = vtk.vtkWindowToImageFilter()
            w2if2.SetInput(self.image_viewer2.GetRenderWindow())
            w2if2.Update()
            # Capture the image
            # Get the captured image data
            image_data2 = w2if2.GetOutput()
            w2if3 = vtk.vtkWindowToImageFilter()
            w2if3.SetInput(self.image_viewer3.GetRenderWindow())
            w2if3.Update()
            
            # Capture the image
            # Get the captured image data
            image_data3 = w2if3.GetOutput()
            
            # Display the captured image in the second VTK widget
            self.renderera = self.widgetc1.GetRenderWindow().GetRenderers().GetFirstRenderer()

            if self.renderera is None:
                # If no renderer exists, create one
                self.renderera = vtk.vtkRenderer()
                self.widgetc1.GetRenderWindow().AddRenderer(self.renderera)

            self.renderera.RemoveAllViewProps()  # Clear existing props

            self.actora = vtk.vtkImageActor()
            self.actora.SetInputData(image_data)
            self.renderera.AddActor(self.actora)

            # Render the scene
            self.rendererb = self.widgetc2.GetRenderWindow().GetRenderers().GetFirstRenderer()

            if self.rendererb is None:
                # If no renderer exists, create one
                self.rendererb = vtk.vtkRenderer()
                self.widgetc2.GetRenderWindow().AddRenderer(self.rendererb)

            self.rendererb.RemoveAllViewProps()  # Clear existing props

            self.actorb = vtk.vtkImageActor()
            self.actorb.SetInputData(image_data2)
            self.rendererb.AddActor(self.actorb)

            # Render the scene
            self.rendererc = self.widgetc3.GetRenderWindow().GetRenderers().GetFirstRenderer()

            if self.rendererc is None:
                # If no renderer exists, create one
                self.rendererc = vtk.vtkRenderer()
                self.widgetc3.GetRenderWindow().AddRenderer(self.rendererc)

            self.rendererc.RemoveAllViewProps()  # Clear existing props

            self.actorc = vtk.vtkImageActor()
            self.actorc.SetInputData(image_data3)
            self.rendererc.AddActor(self.actorc)

            # Render the scene
            self.widgetc1.GetRenderWindow().Render()
            self.widgetc2.GetRenderWindow().Render()
            self.widgetc3.GetRenderWindow().Render()
        except:
            pass

    # change the window level of the 2d dicom
    def window_level(self,x):
        try:
            actorsss=[self.image_viewer, self.image_viewer2, self.image_viewer3]
            readerrr=[self.reimage_viewerader2, self.reimage_viewerader3, self.reimage_viewerader4]
            windowww=[self.renderWindow2, self.renderWindow3, self.renderWindow4]
            widgettt=[self.vtk_widget2, self.vtk_widget3, self.vtk_widget4]
            for image, reader, window, widget in zip(actorsss, readerrr, windowww, widgettt ):
                if x==0:
                    image_actor = image.GetImageActor()
                    window_level = vtk.vtkImageMapToWindowLevelColors()
                    window_level.SetInputConnection(reader.GetOutputPort())
                    window_level.SetWindow(400)  # Set the initial window width
                    window_level.SetLevel(40)   # Set the initial window level
                    # Set the output of the vtkImageMapToWindowLevelColors filter as the input to the image actor
                    image_actor.GetMapper().SetInputConnection(window_level.GetOutputPort())
                    # The rest of your existing code...
                    image.SetRenderWindow(window)
                    image.SetupInteractor(widget)
                    self.renderer2.AddViewProp(image_actor)
                    widget.Initialize()
                    window.Render()
                    image.Render()
                elif x==1:
                    image_actor = image.GetImageActor()
                    window_level = vtk.vtkImageMapToWindowLevelColors()
                    window_level.SetInputConnection(reader.GetOutputPort())
                    window_level.SetWindow(1500)  # Set the initial window width
                    window_level.SetLevel(-600)   # Set the initial window level
                    # Set the output of the vtkImageMapToWindowLevelColors filter as the input to the image actor
                    image_actor.GetMapper().SetInputConnection(window_level.GetOutputPort())
                    # The rest of your existing code...
                    image.SetRenderWindow(window)
                    image.SetupInteractor(widget)
                    self.renderer2.AddViewProp(image_actor)
                    widget.Initialize()
                    window.Render()
                    image.Render()
                elif x==2:
                    image_actor = image.GetImageActor()
                    window_level = vtk.vtkImageMapToWindowLevelColors()
                    window_level.SetInputConnection(reader.GetOutputPort())
                    window_level.SetWindow(150)  # Set the initial window width
                    window_level.SetLevel(-90)   # Set the initial window level
                    # Set the output of the vtkImageMapToWindowLevelColors filter as the input to the image actor
                    image_actor.GetMapper().SetInputConnection(window_level.GetOutputPort())
                    # The rest of your existing code...
                    image.SetRenderWindow(window)
                    image.SetupInteractor(widget)
                    self.renderer2.AddViewProp(image_actor)
                    widget.Initialize()
                    window.Render()
                    image.Render()
                elif x==3:
                    image_actor = image.GetImageActor()
                    window_level = vtk.vtkImageMapToWindowLevelColors()
                    window_level.SetInputConnection(reader.GetOutputPort())
                    window_level.SetWindow(2500)  # Set the initial window width
                    window_level.SetLevel(480)   # Set the initial window level
                    # Set the output of the vtkImageMapToWindowLevelColors filter as the input to the image actor
                    image_actor.GetMapper().SetInputConnection(window_level.GetOutputPort())
                    # The rest of your existing code...
                    image.SetRenderWindow(window)
                    image.SetupInteractor(widget)
                    self.renderer2.AddViewProp(image_actor)
                    widget.Initialize()
                    window.Render()
                    image.Render()
                elif x==4:
                    image_actor = image.GetImageActor()
                    window_level = vtk.vtkImageMapToWindowLevelColors()
                    window_level.SetInputConnection(reader.GetOutputPort())
                    window_level.SetWindow(80)  # Set the initial window width
                    window_level.SetLevel(40)   # Set the initial window level
                    # Set the output of the vtkImageMapToWindowLevelColors filter as the input to the image actor
                    image_actor.GetMapper().SetInputConnection(window_level.GetOutputPort())
                    # The rest of your existing code...
                    image.SetRenderWindow(window)
                    image.SetupInteractor(widget)
                    self.renderer2.AddViewProp(image_actor)
                    widget.Initialize()
                    window.Render()
                    image.Render()
                else:
                    image_actor = image.GetImageActor()
                    window_level = vtk.vtkImageMapToWindowLevelColors()
                    window_level.SetInputConnection(reader.GetOutputPort())
                    window_level.SetWindow(255)  # Set the initial window width
                    window_level.SetLevel(127.5)   # Set the initial window level
                    # Set the output of the vtkImageMapToWindowLevelColors filter as the input to the image actor
                    image_actor.GetMapper().SetInputConnection(window_level.GetOutputPort())
                    # The rest of your existing code...
                    image.SetRenderWindow(window)
                    image.SetupInteractor(widget)
                    self.renderer2.AddViewProp(image_actor)
                    widget.Initialize()
                    window.Render()
                    image.Render()
        except:
            pass
    
    # change the 3d dicom to only show it bone
    def changetobone(self):
        try:
 
            if self.pushButton_45.isChecked():
                self.pushButton_46.setChecked(False)
                thresh1 = 150
                thresh2 = 320
                thresh3 = 440

                scalarRange=self.reader.GetOutput().GetScalarRange()
                colorTransferFunction = vtk.vtkColorTransferFunction()
                colorTransferFunction.AddRGBPoint(scalarRange[0], 0.0, 0.0, 0.0)
                colorTransferFunction.AddRGBPoint(thresh1, 140/255, 64/255, 38/255)
                colorTransferFunction.AddRGBPoint(thresh2, 225/255, 154/255, 74/255)
                colorTransferFunction.AddRGBPoint(thresh3, 255/255, 239/255, 243/255)
                colorTransferFunction.AddRGBPoint(scalarRange[1], 211/255, 168/255, 255/255)

                funcOpacityScalar = vtk.vtkPiecewiseFunction()
                funcOpacityScalar.AddPoint(scalarRange[0],   0)
                funcOpacityScalar.AddPoint(thresh1,   0)
                funcOpacityScalar.AddPoint(thresh2,   0.45)
                funcOpacityScalar.AddPoint(thresh3,   0.63)
                funcOpacityScalar.AddPoint(scalarRange[1],   0.63)

                volumeProperty = vtk.vtkVolumeProperty()
                volumeProperty.ShadeOn()
                volumeProperty.SetScalarOpacity(funcOpacityScalar)
                volumeProperty.SetInterpolationTypeToLinear()
                volumeProperty.SetColor(colorTransferFunction)
                volumeProperty.SetAmbient(0.20)
                volumeProperty.SetDiffuse(1.00)
                volumeProperty.SetSpecular(0.00)
                volumeProperty.SetSpecularPower(0.00)

                self.volume.SetProperty(volumeProperty)# Define renderer for Volume

                self.renderWindow3D.Render()
            else:
                volumeProperty = vtk.vtkVolumeProperty() 
                gradientOpacity = vtk.vtkPiecewiseFunction() 
                scalarOpacity = vtk.vtkPiecewiseFunction() 
                color = vtk.vtkColorTransferFunction() 

                volumeProperty.ShadeOn() 
                volumeProperty.SetInterpolationTypeToLinear() 
                volumeProperty.SetAmbient(0.1) 
                volumeProperty.SetDiffuse(0.9) 
                volumeProperty.SetSpecular(0.2) 
                volumeProperty.SetSpecularPower(10.0) 
                gradientOpacity.AddPoint(0.0, 0.0) 
                gradientOpacity.AddPoint(2000.0, 1.0) 
                volumeProperty.SetGradientOpacity(gradientOpacity)  
                scalarOpacity.AddPoint(-800.0, 0.0) 
                scalarOpacity.AddPoint(-750.0, 1.0) 
                scalarOpacity.AddPoint(-350.0, 1.0) 
                scalarOpacity.AddPoint(-300.0, 0.0) 
                scalarOpacity.AddPoint(-200.0, 0.0) 
                scalarOpacity.AddPoint(-100.0, 1.0) 
                scalarOpacity.AddPoint(1000.0, 0.0) 
                scalarOpacity.AddPoint(2750.0, 0.0) 
                scalarOpacity.AddPoint(2976.0, 1.0) 
                scalarOpacity.AddPoint(3000.0, 0.0) 
                volumeProperty.SetScalarOpacity(scalarOpacity) 
                color.AddRGBPoint(-750.0, 0.08, 0.05, 0.03) 
                color.AddRGBPoint(-350.0, 0.39, 0.25, 0.16)  
                color.AddRGBPoint(-200.0, 0.80, 0.80, 0.80) 
                color.AddRGBPoint(2750.0, 0.70, 0.70, 0.70) 
                color.AddRGBPoint(3000.0, 0.35, 0.35, 0.35) 
                volumeProperty.SetColor(color)

                self.volume.SetProperty(volumeProperty)
            
                self.renderWindow3D.Render()
        except:
            pass

    #change the 3d dicom to only show it tissue
    def change_tissue(self):
        try:
            if self.pushButton_46.isChecked():
                self.pushButton_45.setChecked(False)
                thresh1 = 150
                thresh2 = 320
                thresh3 = 440
                scalarRange=self.reader.GetOutput().GetScalarRange()
                colorTransferFunction = vtk.vtkColorTransferFunction()
                colorTransferFunction.AddRGBPoint(scalarRange[0], 0.0, 0.0, 0.0)
                colorTransferFunction.AddRGBPoint(thresh1, 140/255, 64/255, 38/255)
                colorTransferFunction.AddRGBPoint(thresh2, 225/255, 154/255, 74/255)
                colorTransferFunction.AddRGBPoint(thresh3, 255/255, 239/255, 243/255)
                colorTransferFunction.AddRGBPoint(scalarRange[1], 211/255, 168/255, 255/255)

                funcOpacityScalar = vtk.vtkPiecewiseFunction()
                funcOpacityScalar.AddPoint(scalarRange[0],   0)
                funcOpacityScalar.AddPoint(thresh1,   0.1)
                funcOpacityScalar.AddPoint(thresh2,   0)
                funcOpacityScalar.AddPoint(thresh3,   0)
                funcOpacityScalar.AddPoint(scalarRange[1],   0)

                volumeProperty = vtk.vtkVolumeProperty()
                volumeProperty.ShadeOn()
                volumeProperty.SetScalarOpacity(funcOpacityScalar)
                volumeProperty.SetInterpolationTypeToLinear()
                volumeProperty.SetColor(colorTransferFunction)
                volumeProperty.SetAmbient(0.20)
                volumeProperty.SetDiffuse(1.00)
                volumeProperty.SetSpecular(0.00)
                volumeProperty.SetSpecularPower(0.00)

                self.volume.SetProperty(volumeProperty)# Define renderer for Volume

                self.renderWindow3D.Render()
            else:
                volumeProperty = vtk.vtkVolumeProperty() 
                gradientOpacity = vtk.vtkPiecewiseFunction() 
                scalarOpacity = vtk.vtkPiecewiseFunction() 
                color = vtk.vtkColorTransferFunction() 

                volumeProperty.ShadeOn() 
                volumeProperty.SetInterpolationTypeToLinear() 
                volumeProperty.SetAmbient(0.1) 
                volumeProperty.SetDiffuse(0.9) 
                volumeProperty.SetSpecular(0.2) 
                volumeProperty.SetSpecularPower(10.0) 
                gradientOpacity.AddPoint(0.0, 0.0) 
                gradientOpacity.AddPoint(2000.0, 1.0) 
                volumeProperty.SetGradientOpacity(gradientOpacity)  
                scalarOpacity.AddPoint(-800.0, 0.0) 
                scalarOpacity.AddPoint(-750.0, 1.0) 
                scalarOpacity.AddPoint(-350.0, 1.0) 
                scalarOpacity.AddPoint(-300.0, 0.0) 
                scalarOpacity.AddPoint(-200.0, 0.0) 
                scalarOpacity.AddPoint(-100.0, 1.0) 
                scalarOpacity.AddPoint(1000.0, 0.0) 
                scalarOpacity.AddPoint(2750.0, 0.0) 
                scalarOpacity.AddPoint(2976.0, 1.0) 
                scalarOpacity.AddPoint(3000.0, 0.0) 
                volumeProperty.SetScalarOpacity(scalarOpacity) 
                color.AddRGBPoint(-750.0, 0.08, 0.05, 0.03) 
                color.AddRGBPoint(-350.0, 0.39, 0.25, 0.16)  
                color.AddRGBPoint(-200.0, 0.80, 0.80, 0.80) 
                color.AddRGBPoint(2750.0, 0.70, 0.70, 0.70) 
                color.AddRGBPoint(3000.0, 0.35, 0.35, 0.35) 
                volumeProperty.SetColor(color)

                self.volume.SetProperty(volumeProperty)
            
                self.renderWindow3D.Render()
        except:
            pass

    # to allow delete the 2d capture image   
    def deleteWidget(self,dell):
        try:
            if dell==0:
                self.widgetc1.GetRenderWindow().GetRenderers().GetFirstRenderer().RemoveActor(self.actora)
                self.widgetc1.GetRenderWindow().Render()
                self.actora=None
                
            elif dell==1:
                self.widgetc2.GetRenderWindow().GetRenderers().GetFirstRenderer().RemoveActor(self.actorb)
                self.widgetc2.GetRenderWindow().Render()
                self.actorb=None
                
            elif dell==2:
                self.widgetc3.GetRenderWindow().GetRenderers().GetFirstRenderer().RemoveActor(self.actorc)
                self.widgetc3.GetRenderWindow().Render()
                self.actorc=None
        except:
            pass
            
    # make a boxWidget to make transformation for 3d diom
    def on_button_clicked(self):
        try:
            if self.pushButton_2.isChecked():
                colors=vtk.vtkNamedColors()
                self.boxWidget = vtk.vtkBoxWidget()
                self.boxWidget.SetInteractor(self.vtk_widget3D)
                self.boxWidget.SetPlaceFactor(1.25)
                self.boxWidget.GetOutlineProperty().SetColor(colors.GetColor3d('Gold'))
                self.boxWidget.SetProp3D(self.volume)
                self.boxWidget.PlaceWidget()
                callback = vtkMyCallback()
                self.boxWidget.AddObserver('InteractionEvent',callback)
                self.boxWidget.On()
                self.renderWindow3D.Render()
            else:
                
                self.boxWidget.Off()
                self.renderWindow3D.Render()
        except:
            pass
    
    #save 3d dicom into image form
    def save3d(self):
        try:
            file_name, _ = QFileDialog.getSaveFileName(None, "Save Image", "", "PNG Files (*.png);;JPEG Files (*.jpg *.jpeg)")

            if file_name:
                w2if = vtk.vtkWindowToImageFilter()
                w2if.SetInput(self.vtk_widget3D.GetRenderWindow())
                w2if.SetInputBufferTypeToRGBA()  # You can adjust this based on your requirements

                # Update()

                # Save the captured image to a file
                writer = vtk.vtkPNGWriter()
                writer.SetFileName(file_name)
                writer.SetInputConnection(w2if.GetOutputPort())
                writer.Write()
        except:
            pass

    # close the window
    def closeEvent(self, event):
        # Perform actions when the close button is clicked
        print("Closing the window...")
        sys.exit(1)

    #Make a about us message
    def getMessage(self, message, what):
        msg = QtWidgets.QMessageBox()
        msg.setText(what)
        msg.setInformativeText(message)
        msg.setWindowTitle("About Us")
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
        result = msg.exec_()
        return result

    # reset the 3d camera
    def resetcamera3d(self):
        try:
            self.renderer3D.ResetCamera()
            self.renderWindow3D.Render()
        except:
            pass

# the detial of transform for the boxWidget
class vtkMyCallback(object):
    def __call__(self,caller,ev):
        t=vtk.vtkTransform()
        widget=caller
        widget.GetTransform(t)
        widget.GetProp3D().SetUserTransform(t)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ex = Ui_MainWindow()
    ex.show()
    sys.exit(app.exec_())
