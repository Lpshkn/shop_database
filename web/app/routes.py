import pymssql
from app import app
from app import forms
from app import mssql
from flask import render_template, flash, redirect, url_for, request
from flask.views import MethodView
from flask_login import login_user, logout_user, login_required
from app.models import User
from werkzeug.urls import url_parse


@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    logout_user()
    mssql.close_conn()
    form = forms.LoginForm()
    if form.validate_on_submit():
        try:
            user = User.query.filter_by(username=form.username.data).first()
            if not user:
                flash('Invalid user')
                return redirect(url_for('login'))
            mssql.set_conn(
                server=form.server.data,
                user=form.username.data,
                password=form.password.data,
                dbname=form.dbname.data)
            login_user(user)
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('workers_api')
            return redirect(next_page)
        except pymssql.OperationalError:
            flash('Invalid connection data')
            return redirect(url_for('login'))
        except pymssql.InterfaceError:
            flash('Connection to the database failed for an unknown reason')
            return redirect(url_for('login'))

    return render_template('login.html', title='Sign In | Shop database ', form=form)


class WorkerAPI(MethodView):
    decorators = [login_required]
    template = 'workers.html'
    url = '/workers/'
    context = {
        'title': 'Workers | Shop database',
        'table_name': 'Workers',
    }

    @staticmethod
    def get_workers() -> list:
        storage = mssql.WorkersStorage.get_connection(
            conn=mssql.get_conn())
        return storage.get_workers()

    def update(self, form):
        if form.validate_on_submit():
            try:
                storage = mssql.WorkersStorage.get_connection(
                    conn=mssql.get_conn())
                storage.update_worker(
                    fullname=form.fullname.data,
                    salary=form.salary.data,
                    job=form.job.data,
                    address=form.address.data,
                    passport_number=form.passport_number.data,
                    telephone=form.telephone.data,
                    email=form.email.data)
                self.context['message'] = f"Information about worker '{form.fullname.data}' was successfully updated."
                return render_template(self.template, **self.context)
            except (pymssql.OperationalError, pymssql.InterfaceError, pymssql.IntegrityError):
                flash("Error on inserting values into table.")
                return redirect(self.url)
        flash("Invalid form data.")
        return render_template(self.template, **self.context)

    def delete(self):
        self.context['message'] = ("Delete %s" % request.form['worker_id'])
        return render_template(self.template, **self.context)

    def add(self, form):
        if form.validate_on_submit():
            try:
                storage = mssql.WorkersStorage.get_connection(
                    conn=mssql.get_conn())
                storage.add_worker(
                    fullname=form.fullname.data,
                    salary=form.salary.data,
                    job=form.job.data,
                    address=form.address.data,
                    passport_number=form.passport_number.data,
                    telephone=form.telephone.data,
                    email=form.email.data)
                self.context['message'] = f"Worker '{form.fullname.data}' was successfully added to database."
                return render_template(self.template, **self.context)
            except (pymssql.OperationalError, pymssql.InterfaceError, pymssql.IntegrityError):
                flash("Error on inserting values into table.")
                return redirect(self.url)
        flash("Invalid form data.")
        return render_template(self.template, **self.context)

    def get(self):
        self.context['message'] = ''
        self.context['workers'] = WorkerAPI.get_workers()
        self.context['form'] = forms.WorkerForm()
        return render_template(self.template, **self.context)

    def post(self):
        self.context['customers'] = WorkerAPI.get_workers()
        form = forms.WorkerForm()
        self.context['form'] = form
        if request.form['submit'] == 'Add':
            return self.add(form)
        if request.form['submit'] == 'Update':
            return self.update(form)
        if request.form['submit'] == 'Delete':
            return self.delete()
        return render_template(self.template, **self.context)


app.add_url_rule('/workers/', view_func=WorkerAPI.as_view('workers_api'), methods=['POST', 'GET'])


@app.route('/suppliers/show', methods=['GET', 'POST'])
@login_required
def suppliers():
    storage = mssql.SuppliersStorage.get_connection(
        conn=mssql.get_conn())
    info = {
        'title': 'Suppliers | Shop database',
        'table_name': 'Suppliers',
        'link': 'suppliers',
        'suppliers': storage.get_suppliers()
    }
    return render_template('suppliers/show.html', **info)


@app.route('/suppliers/insert', methods=['GET', 'POST'])
@login_required
def insert_supplier():
    form = forms.SupplierForm()
    info = {
        'title': 'Add supplier | Shop database',
        'table_name': 'Suppliers',
        'link': 'suppliers',
        'form': form
    }
    if form.validate_on_submit():
        try:
            storage = mssql.SuppliersStorage.get_connection(
                conn=mssql.get_conn())
            storage.add_supplier(
                name=form.name.data,
                address=form.address.data,
                telephone=form.telephone.data,
                email=form.email.data)
            info['message'] = f"Supplier '{form.name.data}' was successfully added to database."
            render_template('suppliers/insert.html', **info)
        except (pymssql.OperationalError, pymssql.InterfaceError, pymssql.IntegrityError):
            flash("Error on inserting value into table.")
            return redirect(url_for('insert_supplier'))
    elif form.is_submitted():
        flash("Invalid form data.")

    return render_template('suppliers/insert.html', **info)


@app.route('/products/show', methods=['GET', 'POST'])
@login_required
def products():
    storage = mssql.ProductsStorage.get_connection(
        conn=mssql.get_conn())
    info = {
        'title': 'Products | Shop database',
        'table_name': 'Products',
        'link': 'products',
        'products': storage.get_products()
    }
    return render_template('products/show.html', **info)


@app.route('/products/insert', methods=['GET', 'POST'])
@login_required
def insert_product():
    form = forms.ProductForm()

    storage = mssql.ProducersStorage.get_connection(
        conn=mssql.get_conn())
    producers_choices = list(enumerate(storage.get_producers_names()))
    form.producer.choices = producers_choices

    storage = mssql.SuppliersStorage.get_connection(
        conn=mssql.get_conn())
    suppliers_choices = list(enumerate(storage.get_suppliers_names()))
    form.supplier.choices = suppliers_choices

    info = {
        'title': 'Add product | Shop database',
        'table_name': 'Products',
        'link': 'products',
        'form': form
    }
    if form.validate_on_submit():
        try:
            storage = mssql.ProductsStorage.get_connection(
                conn=mssql.get_conn())
            storage.add_product(
                name=form.name.data,
                quantity=form.quantity.data,
                price=form.price.data,
                promotion=form.promotion.data,
                supplier=suppliers_choices[form.supplier.data][1],
                producer=producers_choices[form.producer.data][1])
            info['message'] = f"Product '{form.name.data}' was successfully added to database."
            return render_template('products/insert.html', **info)
        except (pymssql.OperationalError, pymssql.InterfaceError, pymssql.IntegrityError):
            flash("Error on inserting value into table.")
            return redirect(url_for('insert_product'))
    elif form.is_submitted():
        flash("Invalid form data.")

    return render_template('products/insert.html', **info)


class CustomerAPI(MethodView):
    decorators = [login_required]
    template = 'customers.html'
    url = '/customers/'
    context = {
        'title': 'Customers | Shop database',
        'table_name': 'Customers'
    }

    @staticmethod
    def get_customers() -> list:
        storage = mssql.CustomersStorage().get_connection(
            conn=mssql.get_conn())
        return storage.get_customers()

    @staticmethod
    def get_form() -> forms.CustomerForm:
        cards_storage = mssql.DiscountCardsStorage().get_connection(
            conn=mssql.get_conn())
        choices = [(0, '-')] + [
            (i + 1, str(card_id))
            for i, card_id in enumerate(cards_storage.get_cards_ids())
        ]
        form = forms.CustomerForm()
        form.card_id.choices = choices
        return form

    def update(self, form):
        if form.validate_on_submit():
            try:
                choice = form.card_id.data
                card_id = self.choices[choice][1] if choice else "NULL"
                self.storage.update_customer(
                    fullname=form.fullname.data,
                    address=form.address.data,
                    telephone=form.telephone.data,
                    email=form.email.data,
                    card_id=card_id)
                message = f"Information about customer '{form.fullname.data}' was successfully updated."
                self.context['message'] = message
                return render_template(self.template, **self.context)
            except (pymssql.OperationalError, pymssql.InterfaceError, pymssql.IntegrityError):
                flash("Error on inserting value into table.")
                return redirect(self.url)
        flash("Invalid form data.")
        return render_template(self.template, **self.context)

    def delete(self):
        self.context['message'] = ("Delete %s" % request.form['customer_id'])
        return render_template(self.template, **self.context)

    def add(self, form):
        if form.validate_on_submit():
            try:
                choice = form.card_id.data
                card_id = self.choices[choice][1] if choice else "NULL"
                self.storage.add_customer(
                    fullname=form.fullname.data,
                    address=form.address.data,
                    telephone=form.telephone.data,
                    email=form.email.data,
                    card_id=card_id)
                self.context['message'] = f"Customer '{form.fullname.data}' was successfully added to database."
                return render_template(self.template, **self.context)
            except (pymssql.OperationalError, pymssql.InterfaceError, pymssql.IntegrityError):
                flash("Error on inserting value into table.")
                return redirect(self.url)
        flash("Invalid form data.")
        return render_template(self.template, **self.context)

    def get(self):
        self.context['message'] = ''
        self.context['customers'] = CustomerAPI.get_customers()
        self.context['form'] = CustomerAPI.get_form()
        return render_template(self.template, **self.context)

    def post(self):
        self.context['customers'] = CustomerAPI.get_customers()
        form = CustomerAPI.get_form()
        self.context['form'] = form
        if request.form['submit'] == 'Add':
            return self.add(form)
        if request.form['submit'] == 'Update':
            return self.update(form)
        if request.form['submit'] == 'Delete':
            return self.delete()
        return render_template(self.template, **self.context)


app.add_url_rule('/customers/', view_func=CustomerAPI.as_view('customer_api'), methods=['POST', 'GET'])


@app.route('/discount_cards/show', methods=['GET', 'POST'])
@login_required
def discount_cards():
    storage = mssql.DiscountCardsStorage.get_connection(
        conn=mssql.get_conn())
    info = {
        'title': 'Discount cards | Shop database',
        'table_name': 'Discount cards',
        'link': 'discount_cards',
        'cards': storage.get_cards()
    }
    return render_template('discount_cards/show.html', **info)


@app.route('/discount_cards/insert', methods=['GET', 'POST'])
@login_required
def insert_card():
    form = forms.DiscountCardForm()
    info = {
        'title': 'Add discount card | Shop database',
        'table_name': 'Discount cards',
        'link': 'discount_cards',
        'form': form
    }
    if form.validate_on_submit():
        try:
            storage = mssql.DiscountCardsStorage.get_connection(
                conn=mssql.get_conn())
            storage.add_card(
                discount=form.discount.data,
                start_date=form.start_date.data,
                expiration=form.expiration.data)
            info['message'] = f"Discount card [{form.discount.data * 100}%] was successfully added to database."
            return render_template('discount_cards/insert.html', **info)
        except (pymssql.OperationalError, pymssql.InterfaceError, pymssql.IntegrityError):
            flash("Error on inserting value into table.")
            return redirect(url_for('insert_card'))
    elif form.is_submitted():
        flash("Invalid form data.")

    return render_template('discount_cards/insert.html', **info)


@app.route('/producers/show', methods=['GET', 'POST'])
@login_required
def producers():
    storage = mssql.ProducersStorage.get_connection(
        conn=mssql.get_conn())
    info = {
        'title': 'Producers | Shop database',
        'table_name': 'Producers',
        'link': 'producers',
        'producers': storage.get_producers()
    }
    return render_template('producers/show.html', **info)


@app.route('/producers/insert', methods=['GET', 'POST'])
@login_required
def insert_producer():
    form = forms.ProducerForm()
    info = {
        'title': 'Add producer | Shop database',
        'table_name': 'Producers',
        'link': 'producers',
        'form': form
    }
    if form.validate_on_submit():
        try:
            storage = mssql.ProducersStorage.get_connection(
                conn=mssql.get_conn())
            storage.add_producer(
                name=form.name.data,
                address=form.address.data,
                telephone=form.telephone.data,
                email=form.email.data)
            info['message'] = f"Producer '{form.name.data}' was successfully added to database."
            return render_template('producers/insert.html', **info)
        except (pymssql.OperationalError, pymssql.InterfaceError, pymssql.IntegrityError):
            flash("Error on inserting value into table.")
            return redirect(url_for('insert_producer'))
    elif form.is_submitted():
        flash("Invalid form data.")

    return render_template('producers/insert.html', **info)


@app.route('/purchases/show', methods=['GET', 'POST'])
@login_required
def purchases():
    storage = mssql.PurchasesStorage.get_connection(
        conn=mssql.get_conn())
    info = {
        'title': 'Purchases | Shop database',
        'table_name': 'Purchases',
        'link': 'purchases',
        'producers': storage.get_purchases()
    }
    return render_template('purchases/show.html', **info)


@app.route('/purchases/insert', methods=['GET', 'POST'])
@login_required
def insert_purchase():
    form = forms.PurchaseForm()

    storage = mssql.ProductsStorage.get_connection(
        conn=mssql.get_conn())
    products_choices = [(i, str(_id)) for i, _id in enumerate(storage.get_products_ids())]
    form.product_id.choices = products_choices

    storage = mssql.CustomersStorage.get_connection(
        conn=mssql.get_conn())
    customers_choices = [(i, str(_id)) for i, _id in enumerate(storage.get_customers_ids())]
    form.customer_id.choices = customers_choices

    storage = mssql.WorkersStorage.get_connection(
        conn=mssql.get_conn())
    workers_choices = [(0, '-')] + [(i+1, str(_id)) for i, _id in enumerate(storage.get_workers_ids())]
    form.worker_id.choices = workers_choices

    info = {
        'title': 'Add purchase | Shop database',
        'table_name': 'Purchases',
        'link': 'purchases',
        'form': form
    }
    if form.validate_on_submit():
        try:
            worker_num = form.worker_id.data
            worker_id = workers_choices[worker_num][1] if worker_num else "NULL"

            storage = mssql.PurchasesStorage.get_connection(
                conn=mssql.get_conn())
            storage.add_purchase(
                total_cost=form.total_cost.data,
                quantity=form.quantity.data,
                date=form.date.data,
                product_id=products_choices[form.product_id.data][1],
                customer_id=customers_choices[form.customer_id.data][1],
                worker_id=worker_id)
            info['message'] = f"Purchase on total cost {form.total_cost.data} was successfully added to database."
            return render_template('purchases/insert.html', **info)
        except (pymssql.OperationalError, pymssql.InterfaceError, pymssql.IntegrityError):
            flash("Error on inserting value into table.")
            return redirect(url_for('insert_purchase'))
    elif form.is_submitted():
        flash("Invalid form data.")

    return render_template('purchases/insert.html', **info)
