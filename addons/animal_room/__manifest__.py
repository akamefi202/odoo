{
    "name": "Animal Room",
    "version": "1.0",
    "author": "Orientech",
    "category": "Tools",
    "description": """Orientech Animal Room Management""",
    "depends": ["base", "mail", "study"],
    "data": [
        'security/ir.model.access.csv',
        'report/ar_reports.xml',
        'report/ar_templates.xml',
        'views/ar_views.xml',
        'views/room_views.xml',
        'views/cage_views.xml',
        'views/protocol_views.xml',
    ],
    "assets": {
        "web.assets_backend": [
            'animal_room/static/src/scss/styles.scss',
        ],
    },
    "license": "LGPL-3",
}
