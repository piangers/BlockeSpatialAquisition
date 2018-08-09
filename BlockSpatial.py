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

        self.layer = self.iface.activeLayer()
        
        # Criação da action e da toolbar
        self.toolbar = self.iface.addToolBar("My_ToolBar")
        pai = self.iface.mainWindow()
        icon_path = ':/plugins/BlockSpatial/icon.png'
        self.action = QAction (QIcon (icon_path),u"SpatialBlock.", pai)
        self.action.setObjectName ("Restrição quanto a delimitação de aquisição.")
        self.action.setStatusTip(None)
        self.action.setWhatsThis(None)
        self.action.setCheckable(True)
        self.toolbar.addAction(self.action)
        self.isEditing = 0

        if self.layer:
            self.iface.activeLayer().featureAdded.connect(self.run) # Sinal que chama a função e retorna o 'id'.
        else:
            pass
  
    def disconnect(self):
        
        try:
            self.layer.featureAdded.disconnect(self.run)
        except:
            pass

    def unload(self):

        del self.toolbar
        try:
            self.layer.featureAdded.disconnect(self.run)
        except:
            pass
        pass

    def unChecked(self):

        self.action.setCheckable(False)
        self.action.setCheckable(True)
     

    def run(self,fid): # recebendo  id da funcao
        
        
    
        
        name = u'area_trabalho_poligono'
        srid = QgsExpressionContextUtils.layerScope(self.layer).variable(name)
        if not srid:
            return
        else: 
            wkt = srid.replace('SRID=31982;','')
            
            mapcanvas = self.iface.mapCanvas()
                    
            geom = QgsGeometry()
            geom = QgsGeometry.fromWkt(wkt)
            
            for feat in self.layer.getFeatures():
                if feat.id() == fid:
                    if geom.intersects(feat.geometry()) == False:
                        QMessageBox.information (self.iface.mainWindow() ,  u'ATENÇÃO!' ,  u"A aquisicão esta fora do limite de trabalho na camada " + self.layer.name())
                        self.layer.deleteFeature(feat.id())
                        return
                    else:
                        return
                        
            mapcanvas.refresh()



