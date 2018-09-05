# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import QColor, QInputDialog, QLineEdit, QAction, QIcon, QMessageBox
from qgis.core import QGis, QgsMapLayerRegistry, QgsDistanceArea, QgsFeature, QgsPoint, QgsGeometry, QgsField, QgsVectorLayer, QgsExpressionContextUtils, QgsExpressionContextScope, QgsFeatureRequest
from qgis.gui import QgsMapToolEmitPoint, QgsRubberBand, QgsMapTool, QgsMessageBar
import resources_rc

class BlockSpatial():
    

    def __init__(self, iface):

        self.iface = iface
		
    def initGui(self): 
        # Criação da action e da toolbar
        self.toolbar = self.iface.addToolBar("Bloqueio espacial")
        path = self.iface.mainWindow()
        icon_path = ':/plugins/BlockSpatial/icon.png'
        self.action = QAction (QIcon (icon_path),u"SpatialBlock", path)
        self.action.setObjectName ("BlockSpatial")
        self.action.setStatusTip(None)
        self.action.setWhatsThis(None)
        self.action.setCheckable(True)
        self.toolbar.addAction(self.action)
        self.mapcanvas = self.iface.mapCanvas()

        self.geometryChange = False
        #associar botão a função run (toogle)
        
        self.action.toggled.connect(self.run)

    def run(self,b):
        #sinal de troca da layer
        if b:
            self.addSignal()
            self.iface.layerTreeView().currentLayerChanged.connect(self.addSignal)
           
        else:
            self.disconnect()
           
            
    def addSignal(self):
            self.layer = self.mapcanvas.currentLayer()
            try:
                self.ligado = True
                self.layer.featureAdded.connect(self.block) # Sinal que chama a função e retorna o 'id'
                self.layer.geometryChanged.connect(self.testChanged) # emitido quando edição de geometria são feitas na camada.
                self.layer.layerModified.connect(self.checkGeometryChanged) # emitido quando modificações são feitas na camada.
            except:
                return
    
    

    def disconnect(self):
        #looping em todas as camadas disconectando o feature added
        #disconectar sinal de troca
        
        self.iface.layerTreeView().currentLayerChanged.disconnect(self.addSignal)
        for i in self.iface.mapCanvas().layers():
              
            try: 
                i.featureAdded.disconnect(self.block)
                i.geometryChanged.disconnect(self.testChanged)
                i.layerModified.connect(self.checkGeometryChanged)
            except:
                pass
            

    def unload(self):
        pass
        
#################################     FUNÇÃO PROVISORIO    ##########################

    def block(self, fid): # recebendo  id da funcao
        
        if self.layer:
            name = u'area_trabalho_poligono'
            ewkt = QgsExpressionContextUtils().layerScope(self.layer).variable(name)
            if ewkt:
                wkt = ewkt.split(';')[1]

                geom = QgsGeometry()
                geom = QgsGeometry.fromWkt(wkt)

                    
                for feat in self.layer.getFeatures():
                    if feat.id() == fid:
                         if geom.intersects(feat.geometry()) == False:
                            QMessageBox.information (self.iface.mainWindow() ,  u'ATENÇÃO!' ,  u"A aquisicão esta fora do limite de trabalho na camada " + self.layer.name())
                            self.layer.deleteFeature(feat.id())                 
                            self.mapcanvas.refresh()
        
        
    def testChanged(self,fid,geom):
        
        if self.layer and self.ligado:
            name = u'geometria_editavel'
            var = QgsExpressionContextUtils().layerScope(self.layer).variable(name)
            
            
            if var == 'False' and self.geometryChange == False:
                QMessageBox.information (self.iface.mainWindow() ,  u'ATENÇÃO!' ,  u'A Geometria não pode ser alterada.')
                
                self.geometryChange = True

    def checkGeometryChanged(self):
        if self.geometryChange == True:
            self.ligado = False
            self.geometryChange = False
            self.layer.undoStack().undo() # Retorna para a           
            self.ligado = True


#################################    FUNÇÃO A SER IMPLEMENTADA     ##########################

    # def block(self, fid): # recebendo  id da funcao

    #     if self.layer:
    #         name = u'area_trabalho_poligono'
    #         ewkt = QgsExpressionContextUtils.layerScope(self.layer).variable(name)
    #         if ewkt:
    #             wkt = ewkt.split(';')[1]

    #             geom = QgsGeometry()
    #             geom = QgsGeometry.fromWkt(wkt)
        
    #             request = QgsFeatureRequest().setFilterFid(fid)
    #             feat = next(self.layer.getFeatures(request))
    #             if not geom.intersects(feat.geometry()):
    #                 QMessageBox.information (self.iface.mainWindow() ,  u'ATENÇÃO!' ,  u"A aquisicão esta fora do limite de trabalho na camada " + self.layer.name())
    #                 self.layer.deleteFeature(fid)                 
    #                 self.mapcanvas.refresh()
        
           
    
                
        


