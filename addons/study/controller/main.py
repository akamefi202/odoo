# -*- coding: utf-8 -*-

import random
import werkzeug

from odoo.http import Controller, request, route


class StudyController(Controller):

    # Generic display pages
    # --------------------------------------------------

    @route(['/study-list', '/study-list/page/<int:page>'], type='http', auth="public", website=True)
    def study_list(self, page=1, **post):
        plant_domain = []
        if post.get('category'):
            plant_domain += [('category_id.name', 'ilike', post['category'])]
        plants = request.env['nursery.plant'].search(plant_domain)

        values = {
            'company': request.env.user.company_id.sudo(),
            'plants': plants,
            'search': post,
            'error': post.get('error')
        }
        if post.get('order_id'):
            values['order'] = request.env['nursery.order'].browse(int(post['order_id']))

        return request.render("study_management.study_list", values)
