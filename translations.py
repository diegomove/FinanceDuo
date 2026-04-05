"""Internationalisation — UI strings in Catalan, Spanish and English."""

LANGUAGES: dict[str, str] = {
    "ca": "Català",
    "es": "Castellano",
    "en": "English",
}

DEFAULT_LANG = "ca"

MONTH_NAMES: dict[str, list[str]] = {
    "ca": ["", "Gener", "Febrer", "Març", "Abril", "Maig", "Juny",
           "Juliol", "Agost", "Setembre", "Octubre", "Novembre", "Desembre"],
    "es": ["", "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
           "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"],
    "en": ["", "January", "February", "March", "April", "May", "June",
           "July", "August", "September", "October", "November", "December"],
}

STRINGS: dict[str, dict[str, str]] = {
    # ── App-wide ──────────────────────────────────────────────
    "app_name":             {"ca": "Els Nostres Dobbers", "es": "Nuestras Finanzas", "en": "Our Finances"},

    # Navbar
    "nav_months":           {"ca": "Mesos", "es": "Meses", "en": "Months"},
    "nav_trends":           {"ca": "Tendències", "es": "Tendencias", "en": "Trends"},
    "nav_settings":         {"ca": "Configuració", "es": "Configuración", "en": "Settings"},
    "nav_theme":            {"ca": "Tema", "es": "Tema", "en": "Theme"},
    "nav_logout":           {"ca": "Sortir", "es": "Salir", "en": "Log out"},
    "nav_language":         {"ca": "Idioma", "es": "Idioma", "en": "Language"},

    # Theme names
    "theme_warm":           {"ca": "Càlid", "es": "Cálido", "en": "Warm"},
    "theme_dark":           {"ca": "Fosc", "es": "Oscuro", "en": "Dark"},
    "theme_rose":           {"ca": "Rosa", "es": "Rosa", "en": "Rose"},
    "theme_forest":         {"ca": "Bosc", "es": "Bosque", "en": "Forest"},
    "theme_ocean":          {"ca": "Oceà", "es": "Océano", "en": "Ocean"},

    # Common actions
    "cancel":               {"ca": "Cancel·lar", "es": "Cancelar", "en": "Cancel"},
    "save":                 {"ca": "Desar", "es": "Guardar", "en": "Save"},
    "add":                  {"ca": "Afegir", "es": "Añadir", "en": "Add"},
    "edit":                 {"ca": "Editar", "es": "Editar", "en": "Edit"},
    "delete":               {"ca": "Eliminar", "es": "Eliminar", "en": "Delete"},
    "create":               {"ca": "Crear", "es": "Crear", "en": "Create"},
    "update":               {"ca": "Actualitzar", "es": "Actualizar", "en": "Update"},
    "use":                  {"ca": "Usar", "es": "Usar", "en": "Use"},
    "register":             {"ca": "Registrar", "es": "Registrar", "en": "Register"},
    "clear":                {"ca": "Netejar", "es": "Limpiar", "en": "Clear"},
    "select":               {"ca": "Selecciona...", "es": "Selecciona...", "en": "Select..."},
    "optional":             {"ca": "Opcional", "es": "Opcional", "en": "Optional"},
    "confirm_delete":       {"ca": "Estàs segur?", "es": "¿Estás seguro?", "en": "Are you sure?"},
    "total":                {"ca": "Total", "es": "Total", "en": "Total"},

    # Common fields
    "amount":               {"ca": "Import", "es": "Importe", "en": "Amount"},
    "description":          {"ca": "Descripció", "es": "Descripción", "en": "Description"},
    "category":             {"ca": "Categoria", "es": "Categoría", "en": "Category"},
    "date":                 {"ca": "Data", "es": "Fecha", "en": "Date"},
    "name":                 {"ca": "Nom", "es": "Nombre", "en": "Name"},
    "type":                 {"ca": "Tipus", "es": "Tipo", "en": "Type"},
    "notes":                {"ca": "Notes", "es": "Notas", "en": "Notes"},
    "from":                 {"ca": "De", "es": "De", "en": "From"},
    "to":                   {"ca": "A", "es": "A", "en": "To"},

    # ── Login ─────────────────────────────────────────────────
    "login_subtitle":       {"ca": "Inicia sessió per continuar", "es": "Inicia sesión para continuar", "en": "Log in to continue"},
    "password":             {"ca": "Contrasenya", "es": "Contraseña", "en": "Password"},
    "password_placeholder": {"ca": "Introdueix la teva contrasenya", "es": "Introduce tu contraseña", "en": "Enter your password"},
    "enter":                {"ca": "Entrar", "es": "Entrar", "en": "Log in"},
    "wrong_credentials":    {"ca": "Nom o contrasenya incorrectes.", "es": "Nombre o contraseña incorrectos.", "en": "Wrong name or password."},
    "welcome":              {"ca": "Benvingut/da, {}!", "es": "¡Bienvenido/a, {}!", "en": "Welcome, {}!"},

    # ── Months ────────────────────────────────────────────────
    "months_title":         {"ca": "Mesos", "es": "Meses", "en": "Months"},
    "new_month":            {"ca": "Nou Mes", "es": "Nuevo Mes", "en": "New Month"},
    "month":                {"ca": "Mes", "es": "Mes", "en": "Month"},
    "year":                 {"ca": "Any", "es": "Año", "en": "Year"},
    "closed":               {"ca": "Tancat", "es": "Cerrado", "en": "Closed"},
    "open":                 {"ca": "Obert", "es": "Abierto", "en": "Open"},
    "spent":                {"ca": "Gastat", "es": "Gastado", "en": "Spent"},
    "of_budget":            {"ca": "del pressupost", "es": "del presupuesto", "en": "of budget"},
    "no_months_yet":        {"ca": "Encara no hi ha mesos. Crea el primer per començar a planificar!", "es": "Aún no hay meses. ¡Crea el primero para empezar a planificar!", "en": "No months yet. Create the first one to start planning!"},
    "initial_label":        {"ca": "Inici", "es": "Inicio", "en": "Initial"},
    "income_label":         {"ca": "Ingressos", "es": "Ingresos", "en": "Income"},
    "paid_label":           {"ca": "Pagat", "es": "Pagado", "en": "Paid"},

    # Flash — months
    "month_invalid":        {"ca": "Mes o any no vàlid.", "es": "Mes o año no válido.", "en": "Invalid month or year."},
    "month_exists":         {"ca": "Aquest mes ja existeix.", "es": "Este mes ya existe.", "en": "This month already exists."},
    "month_created":        {"ca": "Mes creat correctament.", "es": "Mes creado correctamente.", "en": "Month created successfully."},
    "month_not_found":      {"ca": "Mes no trobat.", "es": "Mes no encontrado.", "en": "Month not found."},
    "month_reopened":       {"ca": "Mes reobert.", "es": "Mes reabierto.", "en": "Month reopened."},
    "month_closed_action":  {"ca": "Mes tancat.", "es": "Mes cerrado.", "en": "Month closed."},
    "fixed_copied":         {"ca": "{} despesa/es fixa/es copiada/es del mes anterior.", "es": "{} gasto(s) fijo(s) copiado(s) del mes anterior.", "en": "{} fixed expense(s) copied from previous month."},

    # ── Month overview ────────────────────────────────────────
    "copy_fixed":           {"ca": "Copiar Fixes", "es": "Copiar Fijos", "en": "Copy Fixed"},
    "close_month":          {"ca": "Tancar", "es": "Cerrar", "en": "Close"},
    "reopen_month":         {"ca": "Reobrir", "es": "Reabrir", "en": "Reopen"},
    "month_closed_info":    {"ca": "Aquest mes està tancat. Reobre'l per fer canvis.", "es": "Este mes está cerrado. Reábrelo para hacer cambios.", "en": "This month is closed. Reopen it to make changes."},
    "budget":               {"ca": "Pressupost", "es": "Presupuesto", "en": "Budget"},
    "budget_desc":          {"ca": "Ingressos i despeses previstes", "es": "Ingresos y gastos previstos", "en": "Income and expected expenses"},
    "expenses":             {"ca": "Despeses", "es": "Gastos", "en": "Expenses"},
    "expenses_desc":        {"ca": "Registra la despesa real", "es": "Registra el gasto real", "en": "Log actual spending"},
    "balance":              {"ca": "Balanç", "es": "Balance", "en": "Balance"},
    "balance_desc":         {"ca": "Qui deu a qui", "es": "Quién debe a quién", "en": "Who owes whom"},
    "summary":              {"ca": "Resum", "es": "Resumen", "en": "Summary"},
    "summary_desc":         {"ca": "Previst vs real", "es": "Previsto vs real", "en": "Expected vs actual"},

    # ── Budget ────────────────────────────────────────────────
    "budget_title":         {"ca": "Pressupost", "es": "Presupuesto", "en": "Budget"},
    "manage_categories":    {"ca": "Gestionar Categories", "es": "Gestionar Categorías", "en": "Manage Categories"},
    "total_income":         {"ca": "Ingressos Totals", "es": "Ingresos Totales", "en": "Total Income"},
    "total_budgeted":       {"ca": "Total Pressupostat", "es": "Total Presupuestado", "en": "Total Budgeted"},
    "surplus":              {"ca": "Sobrant", "es": "Sobrante", "en": "Surplus"},
    "income_section":       {"ca": "Ingressos", "es": "Ingresos", "en": "Income"},
    "fixed_expenses":       {"ca": "Despeses Fixes", "es": "Gastos Fijos", "en": "Fixed Expenses"},
    "variable_expenses":    {"ca": "Despeses Variables", "es": "Gastos Variables", "en": "Variable Expenses"},
    "extras":               {"ca": "Extres", "es": "Extras", "en": "Extras"},
    "who_pays":             {"ca": "Qui paga", "es": "Quién paga", "en": "Who pays"},
    "shared":               {"ca": "Compartit", "es": "Compartido", "en": "Shared"},
    "personal":             {"ca": "Personal", "es": "Personal", "en": "Personal"},
    "save_budget":          {"ca": "Desar Pressupost", "es": "Guardar Presupuesto", "en": "Save Budget"},
    "no_categories_type":   {"ca": "Encara no hi ha categories {}.", "es": "Aún no hay categorías {}.", "en": "No {} categories yet."},
    "add_one":              {"ca": "Afegeix-ne una", "es": "Añade una", "en": "Add one"},

    # Flash — budget
    "budget_saved":         {"ca": "Pressupost desat!", "es": "¡Presupuesto guardado!", "en": "Budget saved!"},
    "cant_edit_closed":     {"ca": "No es pot editar un mes tancat.", "es": "No se puede editar un mes cerrado.", "en": "Cannot edit a closed month."},

    # ── Categories ────────────────────────────────────────────
    "categories_title":     {"ca": "Gestionar Categories", "es": "Gestionar Categorías", "en": "Manage Categories"},
    "add_category":         {"ca": "Afegir Categoria", "es": "Añadir Categoría", "en": "Add Category"},
    "edit_category":        {"ca": "Editar Categoria", "es": "Editar Categoría", "en": "Edit Category"},
    "fixed_type":           {"ca": "Fixa", "es": "Fijo", "en": "Fixed"},
    "variable_type":        {"ca": "Variable", "es": "Variable", "en": "Variable"},
    "extra_type":           {"ca": "Extra", "es": "Extra", "en": "Extra"},
    "fixed_plural":         {"ca": "Fixes", "es": "Fijos", "en": "Fixed"},
    "variable_plural":      {"ca": "Variables", "es": "Variables", "en": "Variable"},
    "extra_plural":         {"ca": "Extres", "es": "Extras", "en": "Extras"},
    "no_categories":        {"ca": "No hi ha categories {}.", "es": "No hay categorías {}.", "en": "No {} categories."},
    "confirm_delete_cat":   {"ca": "Eliminar {}? S'eliminarà de tots els pressupostos.", "es": "¿Eliminar {}? Se eliminará de todos los presupuestos.", "en": "Delete {}? It will be removed from all budgets."},
    "cat_placeholder":      {"ca": "p. ex. Gimnàs", "es": "p. ej. Gimnasio", "en": "e.g. Gym"},

    # Flash — categories
    "cat_name_required":    {"ca": "El nom de la categoria és obligatori.", "es": "El nombre de la categoría es obligatorio.", "en": "Category name is required."},
    "cat_type_invalid":     {"ca": "Tipus de categoria no vàlid.", "es": "Tipo de categoría no válido.", "en": "Invalid category type."},
    "cat_exists":           {"ca": "Ja existeix una categoria amb aquest nom.", "es": "Ya existe una categoría con ese nombre.", "en": "A category with that name already exists."},
    "cat_added":            {"ca": "Categoria '{}' afegida.", "es": "Categoría '{}' añadida.", "en": "Category '{}' added."},
    "cat_updated":          {"ca": "Categoria actualitzada.", "es": "Categoría actualizada.", "en": "Category updated."},
    "cat_in_use":           {"ca": "No es pot eliminar: la categoria s'utilitza en pressupostos o despeses.", "es": "No se puede eliminar: la categoría se usa en presupuestos o gastos.", "en": "Cannot delete: category is used in budgets or expenses."},
    "cat_deleted":          {"ca": "Categoria eliminada.", "es": "Categoría eliminada.", "en": "Category deleted."},

    # ── Expenses ──────────────────────────────────────────────
    "expenses_title":       {"ca": "Despeses", "es": "Gastos", "en": "Expenses"},
    "add_expense":          {"ca": "Afegir Despesa", "es": "Añadir Gasto", "en": "Add Expense"},
    "new_expense":          {"ca": "Nova Despesa", "es": "Nuevo Gasto", "en": "New Expense"},
    "edit_expense":         {"ca": "Editar Despesa", "es": "Editar Gasto", "en": "Edit Expense"},
    "update_expense":       {"ca": "Actualitzar Despesa", "es": "Actualizar Gasto", "en": "Update Expense"},
    "quick_add":            {"ca": "Afegir Ràpid", "es": "Añadir Rápido", "en": "Quick Add"},
    "total_spent":          {"ca": "Total Gastat", "es": "Total Gastado", "en": "Total Spent"},
    "paid_by":              {"ca": "Pagat per", "es": "Pagado por", "en": "Paid by"},
    "split_mode":           {"ca": "Repartiment", "es": "Reparto", "en": "Split"},
    "all_categories":       {"ca": "Totes les categories", "es": "Todas las categorías", "en": "All categories"},
    "everyone":             {"ca": "Tothom", "es": "Todos", "en": "Everyone"},
    "custom":               {"ca": "Personalitzat", "es": "Personalizado", "en": "Custom"},
    "only_person":          {"ca": "Només {}", "es": "Solo {}", "en": "Only {}"},
    "person_share_pct":     {"ca": "Part de {} (%)", "es": "Parte de {} (%)", "en": "{}'s share (%)"},
    "desc_placeholder":     {"ca": "p. ex. Compra setmanal al Lidl", "es": "p. ej. Compra semanal en el Lidl", "en": "e.g. Weekly grocery shopping"},
    "no_expenses_yet":      {"ca": "Encara no hi ha despeses registrades aquest mes.", "es": "Aún no hay gastos registrados este mes.", "en": "No expenses recorded this month yet."},
    "add_first_expense":    {"ca": "Afegeix la primera despesa", "es": "Añade el primer gasto", "en": "Add the first expense"},

    # Templates
    "templates_title":      {"ca": "Plantilles", "es": "Plantillas", "en": "Templates"},
    "template":             {"ca": "Plantilla", "es": "Plantilla", "en": "Template"},
    "save_as_template":     {"ca": "Desar com a plantilla", "es": "Guardar como plantilla", "en": "Save as template"},
    "confirm_delete_tmpl":  {"ca": "Eliminar aquesta plantilla?", "es": "¿Eliminar esta plantilla?", "en": "Delete this template?"},

    # Extra income
    "extra_income_title":   {"ca": "Ingressos Extra", "es": "Ingresos Extra", "en": "Extra Income"},
    "received_by":          {"ca": "Rebut per", "es": "Recibido por", "en": "Received by"},
    "no_extra_income":      {"ca": "No s'han registrat ingressos extra aquest mes.", "es": "No se han registrado ingresos extra este mes.", "en": "No extra income recorded this month."},
    "extra_desc_placeholder": {"ca": "p. ex. Bizum de la mare", "es": "p. ej. Bizum de mamá", "en": "e.g. Refund from friend"},

    # Flash — expenses
    "expense_added":        {"ca": "Despesa afegida!", "es": "¡Gasto añadido!", "en": "Expense added!"},
    "expense_updated":      {"ca": "Despesa actualitzada!", "es": "¡Gasto actualizado!", "en": "Expense updated!"},
    "expense_deleted":      {"ca": "Despesa eliminada.", "es": "Gasto eliminado.", "en": "Expense deleted."},
    "expense_not_found":    {"ca": "Despesa no trobada.", "es": "Gasto no encontrado.", "en": "Expense not found."},
    "fill_required":        {"ca": "Si us plau, omple tots els camps obligatoris.", "es": "Por favor, rellena todos los campos obligatorios.", "en": "Please fill in all required fields."},
    "cant_add_closed":      {"ca": "No es poden afegir despeses a un mes tancat.", "es": "No se pueden añadir gastos a un mes cerrado.", "en": "Cannot add expenses to a closed month."},
    "cant_edit_exp_closed": {"ca": "No es poden editar despeses d'un mes tancat.", "es": "No se pueden editar gastos de un mes cerrado.", "en": "Cannot edit expenses in a closed month."},
    "cant_delete_closed":   {"ca": "No es poden eliminar despeses d'un mes tancat.", "es": "No se pueden eliminar gastos de un mes cerrado.", "en": "Cannot delete expenses in a closed month."},
    "cant_add_income_closed": {"ca": "No es poden afegir ingressos a un mes tancat.", "es": "No se pueden añadir ingresos a un mes cerrado.", "en": "Cannot add income to a closed month."},
    "cant_delete_income_closed": {"ca": "No es poden eliminar ingressos d'un mes tancat.", "es": "No se pueden eliminar ingresos de un mes cerrado.", "en": "Cannot delete income in a closed month."},
    "fill_income_required": {"ca": "Si us plau, omple l'import i qui el rep.", "es": "Por favor, rellena el importe y quién lo recibe.", "en": "Please fill in the amount and recipient."},
    "extra_income_added":   {"ca": "Ingrés extra afegit!", "es": "¡Ingreso extra añadido!", "en": "Extra income added!"},
    "extra_income_deleted": {"ca": "Ingrés extra eliminat.", "es": "Ingreso extra eliminado.", "en": "Extra income deleted."},
    "template_saved":       {"ca": "Plantilla desada!", "es": "¡Plantilla guardada!", "en": "Template saved!"},
    "template_not_found":   {"ca": "Plantilla no trobada.", "es": "Plantilla no encontrada.", "en": "Template not found."},
    "template_deleted":     {"ca": "Plantilla eliminada.", "es": "Plantilla eliminada.", "en": "Template deleted."},
    "cant_add_this_month":  {"ca": "No es pot afegir a aquest mes.", "es": "No se puede añadir a este mes.", "en": "Cannot add to this month."},
    "expense_from_template": {"ca": "Despesa afegida des de la plantilla!", "es": "¡Gasto añadido desde la plantilla!", "en": "Expense added from template!"},
    "confirm_delete_exp":   {"ca": "Eliminar aquesta despesa?", "es": "¿Eliminar este gasto?", "en": "Delete this expense?"},
    "confirm_delete_income": {"ca": "Eliminar aquest ingrés?", "es": "¿Eliminar este ingreso?", "en": "Delete this income?"},

    # CSV export
    "csv_date":             {"ca": "Data", "es": "Fecha", "en": "Date"},
    "csv_description":      {"ca": "Descripció", "es": "Descripción", "en": "Description"},
    "csv_category":         {"ca": "Categoria", "es": "Categoría", "en": "Category"},
    "csv_type":             {"ca": "Tipus", "es": "Tipo", "en": "Type"},
    "csv_paid_by":          {"ca": "Pagat per", "es": "Pagado por", "en": "Paid by"},
    "csv_split":            {"ca": "Repartiment", "es": "Reparto", "en": "Split"},
    "csv_amount":           {"ca": "Import", "es": "Importe", "en": "Amount"},

    # ── Balance ───────────────────────────────────────────────
    "balance_title":        {"ca": "Balanç", "es": "Balance", "en": "Balance"},
    "all_square":           {"ca": "Tot quadrat!", "es": "¡Todo cuadrado!", "en": "All square!"},
    "no_debts":             {"ca": "No hi ha deutes entre vosaltres aquest mes.", "es": "No hay deudas entre vosotros este mes.", "en": "No debts between you this month."},
    "owes_to":              {"ca": "{} deu a {}", "es": "{} debe a {}", "en": "{} owes {}"},
    "settled":              {"ca": "Liquidat!", "es": "¡Liquidado!", "en": "Settled!"},
    "pending":              {"ca": "Pendent", "es": "Pendiente", "en": "Pending"},
    "shared_expenses":      {"ca": "Despeses Compartides", "es": "Gastos Compartidos", "en": "Shared Expenses"},
    "person_paid":          {"ca": "{} ha pagat", "es": "{} ha pagado", "en": "{} paid"},
    "person_share":         {"ca": "Part de {}", "es": "Parte de {}", "en": "{}'s share"},
    "total_shared":         {"ca": "Total Compartit", "es": "Total Compartido", "en": "Total Shared"},
    "personal_expenses":    {"ca": "Despeses Personals", "es": "Gastos Personales", "en": "Personal Expenses"},
    "personal_person":      {"ca": "Personal {}", "es": "Personal {}", "en": "Personal {}"},
    "total_all_expenses":   {"ca": "Total Totes les Despeses", "es": "Total Todos los Gastos", "en": "Total All Expenses"},
    "settlements_title":    {"ca": "Pagaments / Liquidacions", "es": "Pagos / Liquidaciones", "en": "Payments / Settlements"},
    "who_pays_settlement":  {"ca": "Qui paga", "es": "Quién paga", "en": "Who pays"},
    "to_whom":              {"ca": "A qui", "es": "A quién", "en": "To whom"},
    "no_settlements_needed": {"ca": "No calen pagaments — tot quadrat!", "es": "No hacen falta pagos — ¡todo cuadrado!", "en": "No payments needed — all square!"},

    # Flash — balance
    "settlement_invalid":   {"ca": "Dades del pagament no vàlides.", "es": "Datos del pago no válidos.", "en": "Invalid payment data."},
    "settlement_registered": {"ca": "Pagament registrat!", "es": "¡Pago registrado!", "en": "Payment registered!"},
    "settlement_deleted":   {"ca": "Pagament eliminat.", "es": "Pago eliminado.", "en": "Payment deleted."},
    "confirm_delete_settle": {"ca": "Eliminar aquest pagament?", "es": "¿Eliminar este pago?", "en": "Delete this payment?"},

    # ── Dashboard ─────────────────────────────────────────────
    "summary_title":        {"ca": "Resum", "es": "Resumen", "en": "Summary"},
    "initial_balance_card": {"ca": "Saldo Inicial", "es": "Saldo Inicial", "en": "Initial Balance"},
    "income_card":          {"ca": "Ingressos", "es": "Ingresos", "en": "Income"},
    "budgeted_card":        {"ca": "Pressupostat", "es": "Presupuestado", "en": "Budgeted"},
    "actual_spent":         {"ca": "Gastat Real", "es": "Gastado Real", "en": "Actual Spent"},
    "net_savings":          {"ca": "Estalvi Net", "es": "Ahorro Neto", "en": "Net Savings"},
    "current_balance":      {"ca": "Saldo Actual", "es": "Saldo Actual", "en": "Current Balance"},
    "budget_health":        {"ca": "Salut del Pressupost", "es": "Salud del Presupuesto", "en": "Budget Health"},
    "spent_pct":            {"ca": "gastat", "es": "gastado", "en": "spent"},
    "expected_vs_actual":   {"ca": "Previst vs Real", "es": "Previsto vs Real", "en": "Expected vs Actual"},
    "spending_distribution": {"ca": "Distribució de la Despesa", "es": "Distribución del Gasto", "en": "Spending Distribution"},
    "detail_by_category":   {"ca": "Detall per Categoria", "es": "Detalle por Categoría", "en": "Detail by Category"},
    "difference":           {"ca": "Diferència", "es": "Diferencia", "en": "Difference"},
    "no_dashboard_data":    {"ca": "Configura un pressupost i registra despeses per veure les comparacions aquí.", "es": "Configura un presupuesto y registra gastos para ver las comparaciones aquí.", "en": "Set up a budget and record expenses to see comparisons here."},

    # ── Trends ────────────────────────────────────────────────
    "trends_title":         {"ca": "Tendències", "es": "Tendencias", "en": "Trends"},
    "back_to_months":       {"ca": "Tornar als Mesos", "es": "Volver a Meses", "en": "Back to Months"},
    "need_2_months":        {"ca": "Cal almenys 2 mesos amb dades per veure tendències.", "es": "Se necesitan al menos 2 meses con datos para ver tendencias.", "en": "Need at least 2 months of data to show trends."},
    "monthly_spending":     {"ca": "Despesa Mensual", "es": "Gasto Mensual", "en": "Monthly Spending"},
    "monthly_savings":      {"ca": "Estalvi Mensual", "es": "Ahorro Mensual", "en": "Monthly Savings"},
    "summary_per_month":    {"ca": "Resum per Mes", "es": "Resumen por Mes", "en": "Summary by Month"},
    "savings":              {"ca": "Estalvi", "es": "Ahorro", "en": "Savings"},
    "no_months_data":       {"ca": "Encara no hi ha mesos.", "es": "Aún no hay meses.", "en": "No months yet."},

    # Chart labels (used in JS via data attributes)
    "chart_budgeted":       {"ca": "Pressupostat", "es": "Presupuestado", "en": "Budgeted"},
    "chart_actual":         {"ca": "Real", "es": "Real", "en": "Actual"},
    "chart_income":         {"ca": "Ingressos", "es": "Ingresos", "en": "Income"},
    "chart_spent":          {"ca": "Gastat", "es": "Gastado", "en": "Spent"},
    "chart_savings":        {"ca": "Estalvi", "es": "Ahorro", "en": "Savings"},

    # ── Settings ──────────────────────────────────────────────
    "settings_title":       {"ca": "Configuració", "es": "Configuración", "en": "Settings"},
    "initial_balance_title": {"ca": "Saldo Inicial", "es": "Saldo Inicial", "en": "Initial Balance"},
    "initial_balance_desc": {"ca": "Estableix quants diners tenia cada persona al banc quan vau començar a fer servir l'app. S'utilitza com a punt de partida per a tots els càlculs.", "es": "Establece cuánto dinero tenía cada persona en el banco cuando empezasteis a usar la app. Se usa como punto de partida para todos los cálculos.", "en": "Set how much money each person had in the bank when you started using the app. Used as the starting point for all calculations."},
    "change_password_title": {"ca": "Canviar Contrasenya", "es": "Cambiar Contraseña", "en": "Change Password"},
    "change_password_desc": {"ca": "Actualitza la teva contrasenya d'accés.", "es": "Actualiza tu contraseña de acceso.", "en": "Update your access password."},
    "current_password":     {"ca": "Contrasenya actual", "es": "Contraseña actual", "en": "Current password"},
    "new_password":         {"ca": "Nova contrasenya", "es": "Nueva contraseña", "en": "New password"},
    "confirm_password":     {"ca": "Confirmar nova contrasenya", "es": "Confirmar nueva contraseña", "en": "Confirm new password"},
    "change_password":      {"ca": "Canviar Contrasenya", "es": "Cambiar Contraseña", "en": "Change Password"},

    # Flash — settings
    "balances_saved":       {"ca": "Saldos inicials desats!", "es": "¡Saldos iniciales guardados!", "en": "Initial balances saved!"},
    "wrong_current_pw":     {"ca": "La contrasenya actual no és correcta.", "es": "La contraseña actual no es correcta.", "en": "Current password is incorrect."},
    "pw_min_length":        {"ca": "La nova contrasenya ha de tenir almenys 8 caràcters.", "es": "La nueva contraseña debe tener al menos 8 caracteres.", "en": "New password must be at least 8 characters."},
    "pw_dont_match":        {"ca": "Les noves contrasenyes no coincideixen.", "es": "Las nuevas contraseñas no coinciden.", "en": "New passwords don't match."},
    "pw_changed":           {"ca": "Contrasenya canviada!", "es": "¡Contraseña cambiada!", "en": "Password changed!"},
}


def get_translations(lang: str) -> dict[str, str]:
    """Return a flat dict of key→string for the given language."""
    if lang not in LANGUAGES:
        lang = DEFAULT_LANG
    return {key: vals.get(lang, vals[DEFAULT_LANG]) for key, vals in STRINGS.items()}


def t(key: str, lang: str) -> str:
    """Get a single translated string."""
    entry = STRINGS.get(key)
    if entry is None:
        return key
    return entry.get(lang, entry.get(DEFAULT_LANG, key))
