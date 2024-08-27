{
    "name": "Clinical Pathology",
    "version": "1.0",
    "author": "Orientech",
    "category": "Tools",
    "description": """Orientech Clinical Pathology Management""",
    "depends": ["base", "mail", "study", "animal_room"],
    "data": [
        'security/ir.model.access.csv',
        'views/cp_views.xml',
        'views/sample_order_views.xml',
        'views/subject_selection_dialog.xml',
    ],
    "license": "LGPL-3",
}
