from nicegui import ui

# ---------- SIDEBAR ----------
with ui.left_drawer().classes('bg-gray-100 p-4'):
    ui.label('INSURANCE CATEGORIES').classes('text-gray-500 text-xs mb-4')

    ui.button('Business Auto', icon='directions_car').classes('w-full justify-start bg-blue-100')
    ui.button('General Liability', icon='gavel').classes('w-full justify-start')
    ui.button('Farm Auto', icon='agriculture').classes('w-full justify-start')
    ui.button('Property', icon='home').classes('w-full justify-start')

    ui.separator()
    ui.label('Support').classes('mt-10 text-gray-400')
    ui.label('Documentation').classes('text-gray-400')


# ---------- MAIN CONTENT ----------
with ui.column().classes('p-6 w-full'):

    # Header
    ui.label('Business Auto Ratebooks').classes('text-3xl font-bold')
    ui.label('Transforming uploaded ratebook data into standardized customer-facing rate pages.')\
        .classes('text-gray-500 mb-4')

    # ---------- GRID SECTION ----------
    with ui.row().classes('gap-4'):

        def upload_card(title):
            with ui.card().classes('w-64 h-40 flex items-center justify-center border-dashed border-2'):
                with ui.column().classes('items-center'):
                    ui.icon('cloud_upload', size='30px').classes('text-gray-400')
                    ui.label(title).classes('text-sm mt-2')
                    ui.upload().props('accept=.xlsx,.csv').classes('w-full')

        upload_card('Master Ratebook')
        upload_card('State Exceptions')
        upload_card('Territory Codes')

    with ui.row().classes('gap-4 mt-4'):
        upload_card('Class Factors')
        upload_card('Liability Rates')
        upload_card('Physical Damage')


    # ---------- OPTIONAL ----------
    ui.label('Optional Supplements').classes('mt-6 text-gray-500')

    with ui.row().classes('gap-4'):
        with ui.card().classes('w-80'):
            ui.label('Underwriting Guide')
            ui.label('PDF Documentation').classes('text-gray-400 text-sm')

        with ui.card().classes('w-80'):
            ui.label('Historical Delta')
            ui.label('Comparative Data').classes('text-gray-400 text-sm')


    # ---------- BUTTON ----------
    ui.button('🚀 Create Rate Pages').classes(
        'mt-6 w-full bg-blue-700 text-white text-lg py-3 rounded-xl'
    )


# ---------- RIGHT PANEL ----------
with ui.right_drawer().classes('bg-gray-50 p-4 w-80'):

    ui.label('⚙️ Ratebook Parameters').classes('text-lg font-bold')

    ui.label('Schedule Rating %').classes('mt-4')
    ui.number(value=0.0).classes('w-full')

    ui.slider(min=0, max=100, value=10).classes('w-full')

    ui.label('Save Location').classes('mt-4')
    ui.input(value='/outputs/rate-pages/').classes('w-full')

    ui.separator()

    ui.label('Process Status').classes('mt-4 text-gray-500')
    ui.label('Data Transformation 45%')

    ui.linear_progress(value=0.45).classes('w-full')

    ui.label('Step 2: Mapping Rows').classes('text-sm mt-2')


# ---------- RUN ----------
ui.run()