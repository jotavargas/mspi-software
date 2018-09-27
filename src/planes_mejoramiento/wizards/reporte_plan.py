# -*- coding: utf-8 -*-

from openerp import models, fields, api, exceptions
from openerp.exceptions import Warning, ValidationError
from openerp.addons.base_idu.tools import reportes

TIPO_PLAN = [
    ('interno', 'Interno'),
    ('contraloria_bog', 'Contraloría de Bogotá'),
    ('contraloria_gral', 'Contraloría General'),
]

class plan_mejoramientos_wizard_reporte_plan(models.TransientModel):
    _name = 'plan_mejoramiento.wizard.reporte_plan'

    # -------------------
    # Fields
    # -------------------
    archivo = fields.Binary('Archivo',readonly=True,filters="xls")
    nombre_archivo = fields.Char('Nombre del Archivo', size=255)

    tipo = fields.Selection(
        TIPO_PLAN,
        string='Tipo',
        required=True,
        track_visibility='onchange',
        help='''Topo''',
    )
    plan_id = fields.Many2one(
        string='Plan de Mejoramiento',
        required=True,
        track_visibility='onchange',
        comodel_name='plan_mejoramiento.plan',
        ondelete='restrict',
        help='''Plan de Mejoramiento''',
        domain="[('tipo','=',tipo)]",
    )


    # -------------------
    # methods
    # -------------------

    @api.multi
    def crear_reporte_plan(self):
        print "AAAAAAAAAAAAA"
        proyecto = {}
        # construir diccionario
        #proyecto['nombre'] = self.proyecto_id.name or ''

        # crear reporte
        documento = reportes.crear_reporte(
            self,
            proyecto,
            'VISITAS',
            'pdf',
            'plantilla_visitas.odt',
            'urbamizadores_ruta_plantillas'
        )
        # eliminar imagenes
        reportes.limpiar_carpeta('/tmp/img_reporte')
        # nombre del reporte para campos de odoo
        self.archivo_encuesta = documento[0]
        self.nombre_archivo_encuesta = documento[1]
        # buscamos el wizar de descarga
        view_ids = self.env['ir.ui.view'].search([('model','=','plan_mejoramiento.wizard.reporte_plan'),
                                                  ('name','=','plan_mejoramiento_wizard_reporte_visitas_download')])
        ids = self.id
        return {
                'view_type':'form',
                'view_mode':'form',
                'res_model':'urbanizadores.wizard.reporte_visitas',
                'target':'new',
                'type':'ir.actions.act_window',
                'view_id':view_ids.id,
                'res_id': ids
        }