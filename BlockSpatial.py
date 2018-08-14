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
        self.toolbar = self.iface.addToolBar("ToolBar")
        path = self.iface.mainWindow()
        icon_path = ':/plugins/BlockSpatial/icon.png'
        self.action = QAction (QIcon (icon_path),u"SpatialBlock.", path)
        self.action.setObjectName ("Restrição quanto a delimitação de aquisição.")
        self.action.setStatusTip(None)
        self.action.setWhatsThis(None)
        self.action.setCheckable(True)
        self.toolbar.addAction(self.action)
        self.mapcanvas = self.iface.mapCanvas()
        #associar botão a função run (toogle)
        
        self.action.toggled.connect(self.run)

    def run(self,b):
        #sinal de troca da layer
        if b:
            self.iface.layerTreeView().currentLayerChanged.connect(self.addSignal)
        else:
            self.disconnect()
    
    

    def addSignal(self):
            self.layer = self.mapcanvas.currentLayer()
            try:
                self.layer.featureAdded.connect(self.block) # Sinal que chama a função e retorna o 'id'
            except:
                pass


    def disconnect(self):
        #looping em todas as camadas disconectando o feature added
        #disconectar sinal de troca
        self.iface.layerTreeView().currentLayerChanged.disconnect(self.addSignal) 
        for i in self.iface.mapCanvas().layers():
           
            try:
                i.featureAdded.disconnect(self.run)
            except:
                pass   

    def unload(self):
        pass





    def block(self, fid): # recebendo  id da funcao
        if self.layer:
            name = u'area_trabalho_poligono'
            ewkt = QgsExpressionContextUtils.layerScope(self.layer).variable(name)
            if ewkt:
                wkt = ewkt.split(';')[1]

                geom = QgsGeometry()
                geom = QgsGeometry.fromWkt(wkt)
        
                request = QgsFeatureRequest().setFilterFid(fid)
                feat = next(self.layer.getFeatures(request))
                if not geom.intersects(feat.geometry()):
                    QMessageBox.information (self.iface.mainWindow() ,  u'ATENÇÃO!' ,  u"A aquisicão esta fora do limite de trabalho na camada " + self.layer.name())
                    self.layer.deleteFeature(fid)                 
                    self.mapcanvas.refresh()
   
   
   
   
   
   
   
   
    # def block(self, fid): # recebendo  id da funcao
    #     if self.layer:
    #         name = u'area_trabalho_poligono'
    #         ewkt = QgsExpressionContextUtils.layerScope(self.layer).variable(name)
    #         if ewkt:
    #             wkt = ewkt.split(';')[1]

    #             geom = QgsGeometry()
    #             geom = QgsGeometry.fromWkt(wkt)
        
            
    #         if not self.layer:
    #             pass
    #         else:
    #             name = u'area_trabalho_poligono'
    #             srid = QgsExpressionContextUtils.layerScope(self.layer).variable(name)
    #             if not srid:
    #                 pass
    #             else: 
    #                 wkt = srid.replace('SRID=31982;','')
                    

                            
    #                 geom = QgsGeometry()
    #                 geom = QgsGeometry.fromWkt(wkt)
                    
    #                 for feat in self.layer.getFeatures():
    #                     if feat.id() == fid:
    #                         if geom.intersects(feat.geometry()) == False:
    #                             QMessageBox.information (self.iface.mainWindow() ,  u'ATENÇÃO!' ,  u"A aquisicão esta fora do limite de trabalho na camada " + self.layer.name())
    #                             self.layer.deleteFeature(feat.id())                 
    #                             self.mapcanvas.refresh()
                                
  
            
    


