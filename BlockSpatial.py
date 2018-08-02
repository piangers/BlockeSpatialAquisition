# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import QColor, QInputDialog, QLineEdit, QAction, QIcon
from qgis.core import QGis, QgsMapLayerRegistry, QgsDistanceArea, QgsFeature, QgsPoint, QgsGeometry, QgsField, QgsVectorLayer, QgsExpressionContextUtils, QgsExpressionContextScope
from qgis.gui import QgsMapToolEmitPoint, QgsRubberBand, QgsMapTool
import resources_rc

class BlockSpatial():
    

    def __init__(self, iface):
        self.iface = iface
		
    def initGui(self): 
        self.layer = self.iface.activeLayer()
        # cria uma ação que iniciará a configuração do plugin
        
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
        self.layer.QgsVectorLayer.featureAdded.connect(self.run)
  
    def disconnect(self):
        try:
            self.layer.featureAdded.disconnect(self.run)
        except:
            pass
    def unload(self):
        pass

    def unChecked(self):
        self.action.setCheckable(False)
        self.action.setCheckable(True)
     

    def run(self,fId):
          
        varName = u'area_trabalho_poligono'
        varSRID = QgsExpressionContextUtils.layerScope(self.layer).variable(varName)
        
        if not(varSRID):
            print (u"Variavel não encontrada.")
        else:
            print varSRID
            for feat in self.layer.getFeatures():
                self.layer.setSelectedFeatures(fId) # Teoricamente recebe o id da nova 
                
                if varSRID.geometry().intersects(feat.geometry()): # teoricamente testa se existe interseção

                    print 'ok'
                else:
                    print 'não pertence'

        #APOIO#
  
# layer = qgis.utils.iface.activeLayer()

# # primeiro recurso da camada
# elem1 = layer.getFeatures().next()
# poly1 = elem1.geometry()
# # segunda característica da camada
# elem2 = layer.getFeatures().next()
# poly2 = elem2.geometry()

# poly1.intersects(poly2)

# # então a linha de interseção
# poly1.intersection(poly2)
# # calcule os anéis
# ring1= QgsGeometry.fromPolyline(poly1.asPolygon()[0])
# ring2= QgsGeometry.fromPolyline(poly2.asPolygon()[0])
# # predicate
# ring1.intersects(ring2)
# ring1.intersection(ring2)


		
	
